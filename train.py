import json
import sys

import pandas as pd

WINDOW = 6


def recent_mean_consumption(df: pd.DataFrame, window: int) -> pd.Series:
    """Mean of the last `window` recorded consumption values per location.

    NaN means "not entered" and is skipped; 0 is a real observation. Months that ended with
    zero stock on hand are skipped, because consumption in a stock-out month understates demand.
    """
    recorded = df.dropna(subset=["consumption"])
    recorded = recorded[recorded["stock_on_hand"].fillna(1) > 0]
    return recorded.groupby("location")["consumption"].agg(lambda s: s.tail(window).mean())


def train(training_data_filename: str, model_path: str):
    df = pd.read_csv(training_data_filename)
    stats = recent_mean_consumption(df, WINDOW).to_dict()
    with open(model_path, "w") as f:
        json.dump({"window": WINDOW, "mean": stats}, f)


if __name__ == "__main__":
    train(sys.argv[1], sys.argv[2])
