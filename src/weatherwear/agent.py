from __future__ import annotations

from dataclasses import dataclass

from .model import TrainedModel
from .outfit import recommend_outfit
from .types import OutfitRecommendation, WeatherFeatures, WeatherLabel


@dataclass
class WeatherWearAgent:
    model: TrainedModel

    def decide(self, features: WeatherFeatures) -> tuple[WeatherLabel, OutfitRecommendation]:
        label = self.model.predict_label(features)
        outfit = recommend_outfit(label, features)
        return label, outfit

