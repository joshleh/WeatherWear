from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

WeatherLabel = Literal["drizzle", "rain", "sun", "snow", "fog"]


@dataclass(frozen=True)
class WeatherFeatures:
    precipitation_mm: float
    temp_max_c: float
    temp_min_c: float
    wind_m_s: float


@dataclass(frozen=True)
class OutfitRecommendation:
    top: str
    bottom: str
    outerwear: Optional[str]
    footwear: str
    accessories: list[str]

