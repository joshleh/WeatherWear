from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def _get_with_retry(url: str, params: dict, timeout: int = 10, retries: int = 4) -> requests.Response:
    """GET with exponential backoff on 429 / 5xx errors."""
    for attempt in range(retries):
        resp = requests.get(url, params=params, timeout=timeout)
        if resp.status_code == 429 or resp.status_code >= 500:
            if attempt < retries - 1:
                time.sleep(2 ** attempt + 1)
                continue
        resp.raise_for_status()
        return resp
    resp.raise_for_status()
    return resp


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
