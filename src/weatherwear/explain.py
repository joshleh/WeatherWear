from __future__ import annotations

from .types import OutfitRecommendation, WeatherFeatures, WeatherLabel

WEATHER_EMOJI: dict[str, str] = {
    "sun": "☀️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "snow": "❄️",
    "fog": "🌁",
}

ITEM_EMOJI: dict[str, str] = {
    "Short-Sleeve Shirt": "👕",
    "T-Shirt or Light Long-Sleeve": "👕",
    "Long-Sleeve Shirt": "👕",
    "Warm Base Layer + Long-Sleeve": "👕",
    "Shorts": "🩳",
    "Pants": "👖",
    "Warm Pants": "👖",
    "Rain Jacket": "🧥",
    "Insulated Waterproof Jacket": "🧥",
    "Windbreaker": "🧥",
    "Water-Resistant Shoes": "👢",
    "Comfortable Sneakers": "👟",
    "Umbrella (Optional)": "☂️",
    "Gloves": "🧤",
    "Beanie": "🧢",
    "Reflective Layer (Low Visibility)": "🦺",
    "Scarf": "🧣",
}


def _ei(item: str) -> str:
    """Return the item prefixed with its emoji."""
    emoji = ITEM_EMOJI.get(item, "")
    return f"{emoji} {item}" if emoji else item


_CONDITION_OPENER: dict[str, str] = {
    "sun": "sunny skies ahead",
    "rain": "rain is in the forecast",
    "drizzle": "light drizzle expected",
    "snow": "snow is on the way",
    "fog": "foggy conditions expected",
}

_CONDITION_OPENER_PAST: dict[str, str] = {
    "sun": "it was a sunny day",
    "rain": "it was a rainy day",
    "drizzle": "there was light drizzle",
    "snow": "it was a snowy day",
    "fog": "it was foggy",
}


def _temp_feeling(avg: float, is_past: bool = False) -> str:
    if is_past:
        if avg >= 30:
            return "It was a hot one 🔥."
        if avg >= 22:
            return "Temperatures were warm and pleasant."
        if avg >= 14:
            return "It was mild — not too hot, not too cold."
        if avg >= 6:
            return "It was on the cool side."
        if avg >= 0:
            return "It was cold 🥶."
        return "It was below freezing 🥶."
    if avg >= 30:
        return "It's going to be hot out there 🔥."
    if avg >= 22:
        return "Temperatures are warm and pleasant."
    if avg >= 14:
        return "It'll be mild — not too hot, not too cold."
    if avg >= 6:
        return "It's on the cool side today."
    if avg >= 0:
        return "It's cold — bundle up 🥶."
    return "It's below freezing — stay warm 🥶."


def build_explanation(
    label: WeatherLabel,
    features: WeatherFeatures,
    outfit: OutfitRecommendation,
    *,
    is_past: bool = False,
) -> str:
    emoji = WEATHER_EMOJI.get(label, "🌤️")
    avg = (features.temp_max_c + features.temp_min_c) / 2

    parts: list[str] = []

    if is_past:
        opener = _CONDITION_OPENER_PAST.get(label, "mixed conditions")
        parts.append(
            f"{emoji} {opener.capitalize()} — "
            f"high of {features.temp_max_c:.0f}°C, low of {features.temp_min_c:.0f}°C."
        )
    else:
        opener = _CONDITION_OPENER.get(label, "mixed conditions")
        parts.append(
            f"{emoji} Looks like {opener} — "
            f"high of {features.temp_max_c:.0f}°C, low of {features.temp_min_c:.0f}°C."
        )

    temp_line = _temp_feeling(avg, is_past)
    extras: list[str] = []
    if features.precipitation_mm > 0.5:
        extras.append(f"💧 {features.precipitation_mm:.1f}mm precipitation")
    if features.wind_m_s >= 5:
        extras.append(f"💨 wind at {features.wind_m_s:.1f} m/s")
    if extras:
        temp_line += " " + ", ".join(extras) + "."
    parts.append(temp_line)

    if is_past:
        outfit_line = (
            f"The ideal outfit would have been {_ei(outfit.top)} "
            f"and {_ei(outfit.bottom)}"
        )
        if outfit.outerwear:
            outfit_line += f" with a {_ei(outfit.outerwear)}"
        outfit_line += "."
        parts.append(outfit_line)
        if outfit.accessories:
            parts.append(
                f"You would have also wanted: "
                f"{', '.join(_ei(a) for a in outfit.accessories)}."
            )
    else:
        outfit_line = f"I'd go with {_ei(outfit.top)} and {_ei(outfit.bottom)}"
        if outfit.outerwear:
            outfit_line += f" — and definitely grab a {_ei(outfit.outerwear)}"
        outfit_line += "."
        parts.append(outfit_line)
        if outfit.accessories:
            parts.append(
                f"Don't forget: "
                f"{', '.join(_ei(a) for a in outfit.accessories)}."
            )

    return " ".join(parts)


def brief_outfit(outfit: OutfitRecommendation) -> str:
    if outfit.outerwear:
        return f"{_ei(outfit.outerwear)} + {_ei(outfit.bottom)}"
    return f"{_ei(outfit.top)} + {_ei(outfit.bottom)}"
