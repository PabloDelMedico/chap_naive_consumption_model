import json
import sys

import numpy as np
import pandas as pd

N_SAMPLES = 100


def predict(model_filename: str, historic_data_filename: str, future_data_filename: str, output_filename: str):
    with open(model_filename) as f:
        model = json.load(f)

    historic_df = pd.read_csv(historic_data_filename).dropna(subset=["consumption"])
    # Recompute the recent mean from historic data so each forecast uses the latest observations
    recent_mean = historic_df.groupby("location")["consumption"].agg(lambda s: s.tail(model["window"]).mean())
    future_df = pd.read_csv(future_data_filename)

    rows = []
    for _, row in future_df.iterrows():
        loc = row["location"]
        mean = recent_mean.get(loc, model["mean"].get(loc, 0.0))
        samples = np.random.poisson(max(mean, 0.0), N_SAMPLES)
        row_data = {"time_period": row["time_period"], "location": loc}
        row_data.update({f"sample_{i}": s for i, s in enumerate(samples)})
        rows.append(row_data)

    pd.DataFrame(rows).to_csv(output_filename, index=False)


if __name__ == "__main__":
    predict(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
