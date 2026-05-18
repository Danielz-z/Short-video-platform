# Performance Result Recording

This project includes benchmark scripts for insert-heavy, query-heavy, and mixed workloads. The recommended workflow is to run the same workload twice:

1. Initialize the schema without `database/indexes.sql`.
2. Run the benchmark and save logs with a `no_index` suffix.
3. Apply `database/indexes.sql`.
4. Re-run the same benchmark and save logs with a `with_index` suffix.
5. Summarize both logs with `experiments/analysis/summarize_logs.py`.

## Commands

```bash
python experiments/insert/insert_worker.py --threads 8 --batch-size 500 --duration 300 --author-id 33333333-3333-3333-3333-333333333333 --log experiments/logs/insert_no_index.csv
python experiments/query/query_worker.py --threads 8 --duration 300 --query-type recent --limit 20 --log experiments/logs/query_no_index.csv

mysql -u root -p < database/indexes.sql

python experiments/insert/insert_worker.py --threads 8 --batch-size 500 --duration 300 --author-id 33333333-3333-3333-3333-333333333333 --log experiments/logs/insert_with_index.csv
python experiments/query/query_worker.py --threads 8 --duration 300 --query-type recent --limit 20 --log experiments/logs/query_with_index.csv

python experiments/analysis/summarize_logs.py experiments/logs/query_no_index.csv experiments/logs/query_with_index.csv
```

## Metrics

| Metric | Meaning |
| --- | --- |
| Operations | Inserted rows or completed queries |
| Avg latency | Mean duration per batch or query |
| P95 latency | Tail latency for the slowest 5% of operations |
| Throughput | Operations per second over the log time range |

## Local Benchmark Result

Environment:

- Date: 2026-05-18
- Database: MySQL 8.0 in Docker Desktop / WSL2
- Data scale: 124,602 rows in `videos` after the benchmark run
- Query workload: 8 threads, 30 seconds, `ORDER BY upload_time DESC LIMIT 20`
- Insert workload: 4 threads, 20 seconds, batch size 100

| Workload | Index state | Operations | Avg latency (s) | P95 latency (s) | Throughput |
| --- | --- | ---: | ---: | ---: | ---: |
| Recent-video query | Without `idx_videos_upload_time` | 10,915 queries | 0.020195 | 0.025821 | 363.63 queries/s |
| Recent-video query | With `idx_videos_upload_time` | 41,738 queries | 0.004746 | 0.006402 | 1,390.38 queries/s |
| Batch insert | Before secondary timeline index test | 11,900 rows | 0.019816 / batch | 0.030500 / batch | 577.28 rows/s |
| Batch insert | With secondary indexes enabled | 12,700 rows | 0.023985 / batch | 0.071130 / batch | 620.34 rows/s |

Summary:

- Adding `idx_videos_upload_time` improved recent-video query throughput by about 3.8x in this local benchmark.
- Average recent-query latency dropped from 20.2 ms to 4.7 ms.
- P95 recent-query latency dropped from 25.8 ms to 6.4 ms.
- Insert throughput stayed in the same range in this short run, while P95 batch latency increased after secondary indexes were enabled. This reflects the expected tradeoff that indexes speed up read paths but add write-maintenance work.

These values are machine-specific and intended as a reproducible local benchmark record rather than a universal performance claim.
