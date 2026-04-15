from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .types import WeatherFeatures, WeatherLabel


EXPECTED_COLUMNS = ["date", "precipitation", "temp_max", "temp_min", "wind", "weather"]


@dataclass(frozen=True)
class Dataset:
    df: pd.DataFrame


def load_seattle_weather_csv(path: str | Path) -> Dataset:
    p = Path(path)
    df = pd.read_csv(p)

    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}. Found: {list(df.columns)}")

    # Ensure types are sane
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if df["date"].isna().any():
        raise ValueError("Some rows have invalid `date` values.")

    for c in ["precipitation", "temp_max", "temp_min", "wind"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        if df[c].isna().any():
            raise ValueError(f"Some rows have invalid numeric values in `{c}`.")

    df["weather"] = df["weather"].astype(str).str.lower()

    return Dataset(df=df)


def row_to_features(row: pd.Series) -> WeatherFeatures:
    return WeatherFeatures(
        precipitation_mm=float(row["precipitation"]),
        temp_max_c=float(row["temp_max"]),
        temp_min_c=float(row["temp_min"]),
        wind_m_s=float(row["wind"]),
    )


def row_to_label(row: pd.Series) -> WeatherLabel:
    label = str(row["weather"]).lower()
    if label not in {"drizzle", "rain", "sun", "snow", "fog"}:
        raise ValueError(f"Unexpected weather label: {label!r}")
    return label  # type: ignore[return-value]

