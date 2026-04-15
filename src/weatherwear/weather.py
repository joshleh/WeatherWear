from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import requests

from .types import WeatherFeatures


def _get_with_retry(url: str, params: dict, timeout: int = 10, retries: int = 3) -> requests.Response:
    """GET with exponential backoff on 429 / 5xx errors."""
    for attempt in range(retries):
        resp = requests.get(url, params=params, timeout=timeout)
        if resp.status_code == 429 or resp.status_code >= 500:
            if attempt < retries - 1:
                time.sleep(1.5 ** attempt + 0.5)
                continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()
    return resp

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

_DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
_DAY_ABBREV = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_MONTHS = ["January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"]
_MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _current_week_range() -> tuple[date, date]:
    """Return (sunday, saturday) for the current week."""
    today = date.today()
    days_since_sunday = (today.weekday() + 1) % 7
    sunday = today - timedelta(days=days_since_sunday)
    saturday = sunday + timedelta(days=6)
    return sunday, saturday


@dataclass(frozen=True)
class DayWeather:
    date_str: str
    date_display: str   # "15 April 2026"
    date_short: str     # "Apr 15"
    day_name: str
    day_abbrev: str
    is_today: bool
    is_past: bool
    features: WeatherFeatures


def fetch_week_weather(lat: float, lon: float) -> list[DayWeather]:
    """Fetch Sun-Sat weather for the current week via Open-Meteo (free, no key)."""
    today = date.today()
    sunday, saturday = _current_week_range()

    resp = _get_with_retry(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min,wind_speed_10m_max",
            "start_date": sunday.isoformat(),
            "end_date": saturday.isoformat(),
            "timezone": "auto",
        },
    )
    daily = resp.json()["daily"]

    days: list[DayWeather] = []
    for i, d_str in enumerate(daily["time"]):
        d = date.fromisoformat(d_str)
        wd = d.weekday()
        days.append(
            DayWeather(
                date_str=d_str,
                date_display=f"{d.day} {_MONTHS[d.month - 1]} {d.year}",
                date_short=f"{_MONTHS_SHORT[d.month - 1]} {d.day}",
                day_name=_DAY_NAMES[wd],
                day_abbrev=_DAY_ABBREV[wd],
                is_today=(d == today),
                is_past=(d < today),
                features=WeatherFeatures(
                    precipitation_mm=float(daily["precipitation_sum"][i] or 0.0),
                    temp_max_c=float(daily["temperature_2m_max"][i] or 0.0),
                    temp_min_c=float(daily["temperature_2m_min"][i] or 0.0),
                    wind_m_s=float(daily["wind_speed_10m_max"][i] or 0.0),
                ),
            )
        )
    return days


def reverse_geocode(lat: float, lon: float) -> str | None:
    """Best-effort city name from coordinates (free Nominatim API)."""
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json", "zoom": 10},
            headers={"User-Agent": "WeatherWear/0.2 (student project)"},
            timeout=5,
        )
        resp.raise_for_status()
        addr = resp.json().get("address", {})
        city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or ""
        state = addr.get("state", "")
        country = addr.get("country", "")
        parts = [p for p in [city, state, country] if p]
        return ", ".join(parts) if parts else None
    except Exception:
        return None


def _load_country_cache() -> dict[str, list[dict[str, Any]]]:
    p = Path(__file__).parent / "country_cities.json"
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {}


_COUNTRY_CITY_CACHE: dict[str, list[dict[str, Any]]] = _load_country_cache()

_search_cache: dict[str, list[dict[str, Any]]] = {}


def search_cities(query: str, count: int = 8) -> list[dict[str, Any]]:
    """Search cities via Open-Meteo geocoding (free, no key).

    - Country-name queries return pre-cached major cities (instant).
    - City queries use the live API with in-memory caching.
    - Filters to populated places, sorts by population.
    """
    query_lower = query.strip().lower()

    cache_key = f"{query_lower}:{count}"
    if cache_key in _search_cache:
        return _search_cache[cache_key]

    resp = _get_with_retry(
        GEOCODING_URL,
        params={"name": query, "count": 50, "language": "en", "format": "json"},
    )
    raw = resp.json().get("results", [])

    for r in raw:
        fc = r.get("feature_code", "")
        if fc.startswith("PCL") and r.get("name", "").lower() == query_lower:
            cc = r.get("country_code", "")
            if cc in _COUNTRY_CITY_CACHE:
                results = _COUNTRY_CITY_CACHE[cc][:count]
                _search_cache[cache_key] = results
                return results
            break

    filtered: list[dict[str, Any]] = []
    for r in raw:
        if not r.get("feature_code", "").startswith("PPL"):
            continue
        searchable = " ".join(
            str(r.get(f, "")).lower()
            for f in ("name", "admin1", "admin2", "admin3", "admin4", "country")
        )
        if query_lower not in searchable:
            continue
        filtered.append(r)

    filtered.sort(key=lambda r: r.get("population", 0) or 0, reverse=True)

    seen: set[tuple[str, str, str]] = set()
    results: list[dict[str, Any]] = []
    for r in filtered:
        key = (r.get("name", ""), r.get("admin1", ""), r.get("country", ""))
        if key in seen:
            continue
        seen.add(key)
        results.append({
            "name": r["name"],
            "country": r.get("country", ""),
            "admin1": r.get("admin1", ""),
            "latitude": r["latitude"],
            "longitude": r["longitude"],
        })
        if len(results) >= count:
            break

    _search_cache[cache_key] = results
    return results
