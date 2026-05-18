import argparse
import csv
from datetime import datetime
from pathlib import Path


def percentile(values, p):
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(len(ordered) * p / 100))
    return ordered[index]


def parse_time(value):
    value = value.strip()
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")


def read_log(path):
    rows = []
    with path.open(newline="", encoding="utf-8") as file:
        sample = file.readline()
        file.seek(0)
        has_header = sample.lower().startswith("time,")
        reader = csv.DictReader(file) if has_header else csv.reader(file)

        for row in reader:
            if has_header:
                duration = float(row["duration_seconds"])
                timestamp = parse_time(row["time"])
                count = int(row.get("rows") or row.get("matched_rows") or 1)
            else:
                timestamp = parse_time(row[0])
                duration = float(row[2])
                count = 1
            rows.append((timestamp, duration, count))
    return rows


def summarize(path):
    rows = read_log(path)
    if not rows:
        return {
            "file": path.name,
            "operations": 0,
            "avg_latency": 0,
            "p95_latency": 0,
            "throughput": 0,
        }

    durations = [duration for _, duration, _ in rows]
    total_operations = sum(count for _, _, count in rows)
    elapsed = max((rows[-1][0] - rows[0][0]).total_seconds(), 0)
    return {
        "file": path.name,
        "operations": total_operations,
        "avg_latency": sum(durations) / len(durations),
        "p95_latency": percentile(durations, 95),
        "throughput": total_operations / elapsed if elapsed else 0,
    }


def main():
    parser = argparse.ArgumentParser(description="Summarize benchmark log files.")
    parser.add_argument("logs", nargs="+", type=Path)
    args = parser.parse_args()

    print("| Log | Operations | Avg latency (s) | P95 latency (s) | Throughput (ops/s) |")
    print("| --- | ---: | ---: | ---: | ---: |")
    for log in args.logs:
        result = summarize(log)
        print(
            f"| {result['file']} | {result['operations']} | "
            f"{result['avg_latency']:.6f} | {result['p95_latency']:.6f} | "
            f"{result['throughput']:.2f} |"
        )


if __name__ == "__main__":
    main()
