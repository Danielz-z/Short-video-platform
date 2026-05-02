from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"


def load_log(name):
    path = LOG_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing log file: {path}")
    df = pd.read_csv(path)
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df["duration_seconds"] = df["duration_seconds"].astype(float)
    return df


def draw_latency(log_name, title, output_name):
    df = load_log(log_name)
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["duration_seconds"])
    plt.xlabel("Time")
    plt.ylabel("Latency (s)")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    output = ROOT / "analysis" / output_name
    plt.savefig(output, dpi=160)
    print(f"saved {output}")


if __name__ == "__main__":
    draw_latency("insert_log.csv", "Insert Latency", "insert_latency.png")
    draw_latency("query_log.csv", "Query Latency", "query_latency.png")

