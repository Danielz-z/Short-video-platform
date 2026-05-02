# Short Video Platform

An engineering-style Flask + MySQL short video platform. The project demonstrates backend layering, normalized database design, security cleanup, and a standalone database performance experiment system.

## Features

- User login and admin-managed user registration
- User profile viewing, editing, and deletion
- Video upload, listing, detail view, title update, and deletion
- Like records with duplicate-like protection
- Database backup and restore entry points
- MySQL schema, index, procedure, and seed scripts
- Concurrent insert/query benchmark scripts with QPS, average latency, and P95 latency output

## Architecture

![System architecture](docs/assets/architecture.png)

```text
backend/
  app.py              # Flask application entry point
  config.py           # Environment-based configuration
  routes/             # HTTP and template layer
  services/           # Business rules
  dao/                # SQL and stored procedure access
  utils/db.py         # MySQL connection helper
database/             # Schema, indexes, procedures, seed data, backups
experiments/          # Insert/query/concurrent performance experiments
docs/                 # Design and performance analysis documents
```

## Database Design

Core tables:

- `users`: user accounts with UUID primary keys and hashed passwords
- `videos`: video metadata linked to authors and content fields
- `likes`: like events with a unique `(user_id, video_id)` constraint
- `comments`: comment records linked to users and videos

Supporting tables include `fields`, `tags`, `video_tags`, `follows`, and `messages` to preserve the original platform features.

## Performance Optimization

The key indexes are defined in `database/indexes.sql`:

```sql
CREATE INDEX idx_videos_author_id ON videos(author_id);
CREATE INDEX idx_videos_field_id ON videos(field_id);
CREATE INDEX idx_videos_upload_time ON videos(upload_time);
```

These indexes optimize author pages, category filtering, timeline ordering, and hot-video queries. The experiment system is designed for before/after comparisons with and without secondary indexes.

## Experiment Output

![Database performance comparison](docs/assets/performance-results.png)

Benchmark scripts print:

- total operations
- elapsed time
- average latency
- P95 latency
- QPS

Logs are written to `experiments/logs`. Charts can be generated with `experiments/analysis/draw_pictures.py`. See `docs/performance_analysis.md` for the experiment plan.

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment variables. On Windows PowerShell:

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="short_video_platform"
$env:SECRET_KEY="change-me"
```

Initialize MySQL:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/indexes.sql
mysql -u root -p < database/procedures.sql
mysql -u root -p < database/seed.sql
```

The demo seed users use `DemoPass123` as the password. Change or remove these users before any real deployment.

Run the web app:

```bash
python backend/app.py
```

Run a mixed benchmark:

```bash
python experiments/run_parallel.py --threads 8 --batch-size 500 --duration 300
```

## Security Notes

- Do not commit `.env` files or real database backups.
- Set a strong `SECRET_KEY` before deployment.
- Store database credentials in environment variables only.
- Replace demo seed passwords before using seed accounts in a real environment.
