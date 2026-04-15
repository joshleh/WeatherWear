from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path

from .agent import WeatherWearAgent
from .data import load_seattle_weather_csv, row_to_features
from .model import load_model, save_model, train_random_forest
from .types import WeatherFeatures


DEFAULT_MODEL_PATH = Path("artifacts/weatherwear_rf.joblib")


def _print_outcome(label: str, outfit: dict) -> None:
    print(f"Predicted weather: {label}")
    print("Outfit recommendation:")
    print(f"- Top: {outfit['top']}")
    print(f"- Bottom: {outfit['bottom']}")
    if outfit.get("outerwear"):
        print(f"- Outerwear: {outfit['outerwear']}")
    print(f"- Footwear: {outfit['footwear']}")
    accessories = outfit.get("accessories") or []
    if accessories:
        print(f"- Accessories: {', '.join(accessories)}")


def cmd_train(args: argparse.Namespace) -> int:
    ds = load_seattle_weather_csv(args.data)
    model, report = train_random_forest(ds.df, random_state=args.random_state)
    save_model(model, args.model_out)
    print("Trained model saved to:", args.model_out)
    print()
    print("Validation report:")
    print(report)
    return 0


def cmd_demo_from_date(args: argparse.Namespace) -> int:
    ds = load_seattle_weather_csv(args.data)
    df = ds.df
    date = args.date
    matches = df[df["date"].dt.strftime("%Y-%m-%d") == date]
    if matches.empty:
        raise SystemExit(f"No row found for date {date!r}. Try a date like 2012-01-01.")
    row = matches.iloc[0]
    features = row_to_features(row)

    model = load_model(args.model)
    agent = WeatherWearAgent(model=model)
    label, outfit = agent.decide(features)

    print(f"Inputs (from dataset): precipitation={features.precipitation_mm}mm, "
          f"temp_max={features.temp_max_c}C, temp_min={features.temp_min_c}C, wind={features.wind_m_s}m/s")
    _print_outcome(label, asdict(outfit))
    return 0


def cmd_demo_manual(args: argparse.Namespace) -> int:
    features = WeatherFeatures(
        precipitation_mm=float(args.precipitation),
        temp_max_c=float(args.temp_max),
        temp_min_c=float(args.temp_min),
        wind_m_s=float(args.wind),
    )
    model = load_model(args.model)
    agent = WeatherWearAgent(model=model)
    label, outfit = agent.decide(features)
    _print_outcome(label, asdict(outfit))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="weatherwear", description="WeatherWear AI agent demo.")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_train = sub.add_parser("train", help="Train model from seattle-weather.csv")
    p_train.add_argument("--data", default="seattle-weather.csv")
    p_train.add_argument("--model-out", default=str(DEFAULT_MODEL_PATH))
    p_train.add_argument("--random-state", type=int, default=42)
    p_train.set_defaults(func=cmd_train)

    p_demo = sub.add_parser("demo", help="Run a demo recommendation")
    demo_sub = p_demo.add_subparsers(dest="demo_cmd", required=True)

    p_date = demo_sub.add_parser("date", help="Use a row from the dataset by date")
    p_date.add_argument("--data", default="seattle-weather.csv")
    p_date.add_argument("--model", default=str(DEFAULT_MODEL_PATH))
    p_date.add_argument("--date", required=True, help="YYYY-MM-DD present in the dataset")
    p_date.set_defaults(func=cmd_demo_from_date)

    p_manual = demo_sub.add_parser("manual", help="Provide weather features manually")
    p_manual.add_argument("--model", default=str(DEFAULT_MODEL_PATH))
    p_manual.add_argument("--precipitation", type=float, required=True, help="mm")
    p_manual.add_argument("--temp-max", type=float, required=True, help="C")
    p_manual.add_argument("--temp-min", type=float, required=True, help="C")
    p_manual.add_argument("--wind", type=float, required=True, help="m/s")
    p_manual.set_defaults(func=cmd_demo_manual)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

