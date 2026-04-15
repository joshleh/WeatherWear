from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from .types import WeatherFeatures, WeatherLabel


def _features_df(df: pd.DataFrame) -> pd.DataFrame:
    return df[["precipitation", "temp_max", "temp_min", "wind"]].copy()


@dataclass
class TrainedModel:
    clf: RandomForestClassifier

    def predict_label(self, features: WeatherFeatures) -> WeatherLabel:
        X = pd.DataFrame(
            [
                {
                    "precipitation": float(features.precipitation_mm),
                    "temp_max": float(features.temp_max_c),
                    "temp_min": float(features.temp_min_c),
                    "wind": float(features.wind_m_s),
                }
            ]
        )
        y = self.clf.predict(X)[0]
        label = str(y).lower()
        if label not in {"drizzle", "rain", "sun", "snow", "fog"}:
            raise ValueError(f"Unexpected predicted label: {label!r}")
        return label  # type: ignore[return-value]

    def predict_proba(self, features: WeatherFeatures) -> dict[WeatherLabel, float]:
        X = pd.DataFrame(
            [
                {
                    "precipitation": float(features.precipitation_mm),
                    "temp_max": float(features.temp_max_c),
                    "temp_min": float(features.temp_min_c),
                    "wind": float(features.wind_m_s),
                }
            ]
        )
        probs = self.clf.predict_proba(X)[0]
        classes = [str(c).lower() for c in self.clf.classes_]
        out: dict[WeatherLabel, float] = {}
        for cls, p in zip(classes, probs):
            if cls in {"drizzle", "rain", "sun", "snow", "fog"}:
                out[cls] = float(p)  # type: ignore[literal-required]
        return out


def train_random_forest(
    df: pd.DataFrame,
    *,
    random_state: int = 42,
) -> tuple[TrainedModel, str]:
    X = _features_df(df)
    y = df["weather"].astype(str).str.lower()

    # Handle mild imbalance without complicated resampling for now.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=random_state,
        stratify=y,
    )

    clf = RandomForestClassifier(
        n_estimators=400,
        random_state=random_state,
        class_weight="balanced_subsample",
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred, digits=3)
    return TrainedModel(clf=clf), report


def save_model(model: TrainedModel, path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model.clf, p)


def load_model(path: str | Path) -> TrainedModel:
    clf = joblib.load(Path(path))
    if not isinstance(clf, RandomForestClassifier):
        raise TypeError(f"Model at {path} was not a RandomForestClassifier: {type(clf)}")
    return TrainedModel(clf=clf)

