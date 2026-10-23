import json
import sys

import pandas as pd

WINDOW = 6


def train(training_data_filename: str, model_path: str):
    df = pd.read_csv(training_data_filename)
    # NaN means "not entered" and is skipped; 0 is a real observation
    stats = (
        df.dropna(subset=["consumption"])
        .groupby("location")["consumption"]
        .agg(lambda s: s.tail(WINDOW).mean())
        .to_dict()
    )
    with open(model_path, "w") as f:
        json.dump({"window": WINDOW, "mean": stats}, f)


if __name__ == "__main__":
    train(sys.argv[1], sys.argv[2])
