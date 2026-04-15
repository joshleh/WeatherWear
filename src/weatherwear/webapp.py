from __future__ import annotations

import os
from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .agent import WeatherWearAgent
from .data import load_seattle_weather_csv
from .explain import WEATHER_EMOJI, brief_outfit, build_explanation
from .model import load_model, save_model, train_random_forest
from .weather import fetch_week_weather, reverse_geocode, search_cities

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = Path(os.environ.get("WEATHERWEAR_DATA", str(ROOT / "seattle-weather.csv")))
MODEL_PATH = Path(os.environ.get("WEATHERWEAR_MODEL", str(ROOT / "artifacts" / "weatherwear_rf.joblib")))

TEMPLATES_DIR = ROOT / "web" / "templates"
STATIC_DIR = ROOT / "web" / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app = FastAPI(title="WeatherWear", version="0.2.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

_agent: WeatherWearAgent | None = None


def _get_agent() -> WeatherWearAgent:
    global _agent
    if _agent is not None:
        return _agent

    if MODEL_PATH.exists():
        model = load_model(MODEL_PATH)
    else:
        ds = load_seattle_weather_csv(DATA_PATH)
        model, _ = train_random_forest(ds.df)
        save_model(model, MODEL_PATH)

    _agent = WeatherWearAgent(model=model)
    return _agent


@app.on_event("startup")
def startup_event() -> None:
    _get_agent()


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> Any:
    return templates.TemplateResponse(request, "index.html", {})


@app.get("/api/cities")
def api_cities(q: str = "") -> JSONResponse:
    if len(q.strip()) < 2:
        return JSONResponse([])
    try:
        results = search_cities(q.strip())
    except Exception:
        results = []
    return JSONResponse(results)


@app.get("/api/reverse")
def api_reverse(lat: float, lon: float) -> JSONResponse:
    label = reverse_geocode(lat, lon)
    return JSONResponse({"label": label})


@app.get("/api/forecast")
def api_forecast(lat: float, lon: float, city: str = "Your Location") -> JSONResponse:
    agent = _get_agent()

    try:
        week = fetch_week_weather(lat, lon)
    except Exception as e:
        msg = "Weather service is temporarily unavailable. Please try again in a moment."
        if "429" in str(e):
            msg = "Weather API rate limit reached. Please wait a few seconds and try again."
        return JSONResponse({"error": msg}, status_code=502)

    days: list[dict[str, Any]] = []
    today_data: dict[str, Any] | None = None

    for day in week:
        label, outfit = agent.decide(day.features)
        is_past = day.is_past and not day.is_today
        explanation = build_explanation(label, day.features, outfit, is_past=is_past)
        emoji = WEATHER_EMOJI.get(label, "🌤️")

        day_data: dict[str, Any] = {
            "date": day.date_str,
            "date_display": day.date_display,
            "date_short": day.date_short,
            "day_name": day.day_name,
            "day_abbrev": day.day_abbrev,
            "is_today": day.is_today,
            "is_past": day.is_past,
            "features": asdict(day.features),
            "predicted_weather": label,
            "emoji": emoji,
            "outfit": asdict(outfit),
            "outfit_brief": brief_outfit(outfit),
            "explanation": explanation,
        }
        days.append(day_data)
        if day.is_today:
            today_data = day_data

    return JSONResponse({"city": city, "today": today_data, "week": days})
