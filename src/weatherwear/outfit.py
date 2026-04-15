from __future__ import annotations

from .types import OutfitRecommendation, WeatherFeatures, WeatherLabel


def recommend_outfit(label: WeatherLabel, features: WeatherFeatures) -> OutfitRecommendation:
    # Simple, deterministic mapping intended for a demo.
    # Tuned for Seattle-like climate: mild temps + frequent rain.
    avg_temp = (features.temp_max_c + features.temp_min_c) / 2.0

    if avg_temp >= 22:
        top = "Short-Sleeve Shirt"
        bottom = "Shorts"
    elif avg_temp >= 14:
        top = "T-Shirt or Light Long-Sleeve"
        bottom = "Pants"
    elif avg_temp >= 6:
        top = "Long-Sleeve Shirt"
        bottom = "Pants"
    else:
        top = "Warm Base Layer + Long-Sleeve"
        bottom = "Warm Pants"

    outerwear: str | None = None
    accessories: list[str] = []

    if label in {"rain", "drizzle"} or features.precipitation_mm >= 1.0:
        outerwear = "Rain Jacket"
        accessories.append("Umbrella (Optional)")

    if label == "snow":
        outerwear = "Insulated Waterproof Jacket"
        accessories.append("Gloves")
        accessories.append("Beanie")

    if label == "fog":
        accessories.append("Reflective Layer (Low Visibility)")

    if features.wind_m_s >= 7.5 and outerwear is None:
        outerwear = "Windbreaker"

    if avg_temp <= 4:
        accessories.append("Scarf")

    if label in {"rain", "drizzle", "snow"}:
        footwear = "Water-Resistant Shoes"
    else:
        footwear = "Comfortable Sneakers"

    return OutfitRecommendation(
        top=top,
        bottom=bottom,
        outerwear=outerwear,
        footwear=footwear,
        accessories=accessories,
    )

