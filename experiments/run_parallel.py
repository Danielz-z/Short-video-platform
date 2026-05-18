import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_AUTHOR_ID = "33333333-3333-3333-3333-333333333333"


def main():
    parser = argparse.ArgumentParser(description="Run insert and query benchmarks in parallel.")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--field-id", type=int, default=3)
    parser.add_argument("--author-id", default=DEFAULT_AUTHOR_ID)
    args = parser.parse_args()

    insert_log = ROOT / "logs" / "insert_log.csv"
    query_log = ROOT / "logs" / "query_log.csv"

    commands = [
        [
            sys.executable,
            str(ROOT / "insert" / "insert_worker.py"),
            "--threads",
            str(args.threads),
            "--batch-size",
            str(args.batch_size),
            "--duration",
            str(args.duration),
            "--field-id",
            str(args.field_id),
            "--author-id",
            args.author_id,
            "--log",
            str(insert_log),
        ],
        [
            sys.executable,
            str(ROOT / "query" / "query_worker.py"),
            "--threads",
            str(args.threads),
            "--duration",
            str(args.duration),
            "--field-id",
            str(args.field_id),
            "--log",
            str(query_log),
        ],
    ]

    processes = [subprocess.Popen(command) for command in commands]
    for process in processes:
        process.wait()

    failed = [process.returncode for process in processes if process.returncode != 0]
    if failed:
        raise SystemExit(f"Benchmark failed with return codes: {failed}")


if __name__ == "__main__":
    main()
