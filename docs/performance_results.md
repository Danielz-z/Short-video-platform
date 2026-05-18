# Performance Result Recording

This project includes benchmark scripts for insert-heavy, query-heavy, and mixed workloads. The recommended workflow is to run the same workload twice:

1. Initialize the schema without `database/indexes.sql`.
2. Run the benchmark and save logs with a `no_index` suffix.
3. Apply `database/indexes.sql`.
4. Re-run the same benchmark and save logs with a `with_index` suffix.
5. Summarize both logs with `experiments/analysis/summarize_logs.py`.

## Commands

```bash
python experiments/insert/insert_worker.py --threads 8 --batch-size 500 --duration 300 --log experiments/logs/insert_no_index.csv
python experiments/query/query_worker.py --threads 8 --duration 300 --field-id 3 --log experiments/logs/query_no_index.csv

mysql -u root -p < database/indexes.sql

python experiments/insert/insert_worker.py --threads 8 --batch-size 500 --duration 300 --log experiments/logs/insert_with_index.csv
python experiments/query/query_worker.py --threads 8 --duration 300 --field-id 3 --log experiments/logs/query_with_index.csv

python experiments/analysis/summarize_logs.py experiments/logs/query_no_index.csv experiments/logs/query_with_index.csv
```

## Metrics

| Metric | Meaning |
| --- | --- |
| Operations | Inserted rows or completed queries |
| Avg latency | Mean duration per batch or query |
| P95 latency | Tail latency for the slowest 5% of operations |
| Throughput | Operations per second over the log time range |

## Result Table Template

| Workload | Index state | Operations | Avg latency (s) | P95 latency (s) | Throughput |
| --- | --- | ---: | ---: | ---: | ---: |
| Query by `field_id` | No secondary index | TBD | TBD | TBD | TBD |
| Query by `field_id` | With `idx_videos_field_id` | TBD | TBD | TBD | TBD |
| Batch insert | No secondary indexes | TBD | TBD | TBD | TBD |
| Batch insert | With secondary indexes | TBD | TBD | TBD | TBD |

Use this table only after running a clean before/after experiment on the same machine, same data scale, and same thread count.
