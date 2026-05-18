import argparse
import csv
import statistics
import sys
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path

import mysql.connector

sys.path.append(str(Path(__file__).resolve().parents[2] / "backend"))
from config import DB_CONFIG  # noqa: E402

DEFAULT_AUTHOR_ID = "33333333-3333-3333-3333-333333333333"


def connect_db():
    return mysql.connector.connect(**DB_CONFIG)


def insert_batch(batch_size, author_id, field_id):
    conn = connect_db()
    cursor = conn.cursor()
    start = time.perf_counter()
    inserted = 0
    try:
        rows = []
        for _ in range(batch_size):
            video_id = str(uuid.uuid4())
            rows.append(
                (
                    video_id,
                    f"https://example.com/videos/{video_id}",
                    "Benchmark video",
                    0,
                    0,
                    datetime.now(),
                    author_id,
                    field_id,
                )
            )
        cursor.executemany(
            """
            INSERT INTO videos
                (video_id, video_url, title, likes_count, comments_count, upload_time, author_id, field_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            rows,
        )
        conn.commit()
        inserted = len(rows)
    finally:
        cursor.close()
        conn.close()
    return time.perf_counter() - start, inserted


def worker(args, stop_at, latencies, lock):
    while time.time() < stop_at:
        duration, inserted = insert_batch(args.batch_size, args.author_id, args.field_id)
        with lock:
            latencies.append((duration, inserted))


def percentile(values, p):
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(len(ordered) * p / 100))
    return ordered[index]


def write_log(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not exists:
            writer.writerow(["time", "operation", "duration_seconds", "rows"])
        for duration, count in rows:
            writer.writerow([datetime.now().isoformat(timespec="seconds"), "insert", f"{duration:.6f}", count])


def main():
    parser = argparse.ArgumentParser(description="Concurrent insert benchmark for videos table.")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--author-id", default=DEFAULT_AUTHOR_ID)
    parser.add_argument("--field-id", type=int, default=3)
    parser.add_argument("--log", type=Path, default=Path("../logs/insert_log.csv"))
    args = parser.parse_args()

    latencies = []
    lock = threading.Lock()
    stop_at = time.time() + args.duration
    started = time.perf_counter()
    threads = [
        threading.Thread(target=worker, args=(args, stop_at, latencies, lock))
        for _ in range(args.threads)
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - started
    total_rows = sum(count for _, count in latencies)
    durations = [duration for duration, _ in latencies]
    write_log(args.log, latencies)

    print(f"threads={args.threads}")
    print(f"batch_size={args.batch_size}")
    print(f"total_rows={total_rows}")
    print(f"elapsed_seconds={elapsed:.3f}")
    print(f"avg_latency_seconds={statistics.mean(durations) if durations else 0:.6f}")
    print(f"p95_latency_seconds={percentile(durations, 95):.6f}")
    print(f"qps={total_rows / elapsed if elapsed else 0:.2f}")


if __name__ == "__main__":
    main()
