# Resume Packaging

## Project Title

Short Video Platform Database System

## One-Line Summary

Built a Flask + MySQL short video platform prototype with normalized relational modeling, role-based administration, connection pooling, stored procedures, indexing, concurrent database performance experiments, GitHub Actions CI, and Docker Compose local deployment.

## Resume Bullets

- Designed a MySQL schema for a short video platform with 9 business tables, foreign keys, unique constraints, CHECK constraints, and normalized relationships across users, videos, likes, comments, follows, messages, fields, and tags.
- Refactored the original single-file Flask course project into a layered `routes / services / dao` backend, separating HTTP handling, business rules, and SQL access for better maintainability.
- Implemented role-based admin access through a `users.role` field, hashed password storage with Werkzeug, and legacy plaintext-password migration after successful login.
- Added a MySQL connection pool for Flask request handlers to reuse database connections and reduce repeated connection setup overhead.
- Added stored procedures for hot-video lookup, video insertion, title update, and deletion, while keeping DAO-level fallback SQL for local development robustness.
- Optimized high-frequency queries with secondary and composite indexes on author, field/category, upload time, popularity, likes, comments, follows, and messages.
- Added `COUNT + LIMIT/OFFSET` pagination for admin user management and personal video lists to avoid full-result loading as data grows.
- Built concurrent insert/query benchmark scripts that report QPS, average latency, and P95 latency; in the local MySQL 8.0 benchmark, `idx_videos_upload_time` increased recent-video query throughput from 363.63 queries/s to 1,390.38 queries/s.
- Added service-layer unit tests for password policy, role authorization, user creation, and video ownership checks without requiring a live MySQL instance.
- Added Docker Compose orchestration for one-command Flask + MySQL startup with automatic schema, index, stored procedure, and seed-data initialization.
- Configured GitHub Actions CI to run unit tests and Python syntax checks on pushes and pull requests.

## Interview Talking Points

- The strongest database angle is the tradeoff between read optimization and write overhead: indexes improve author/category/timeline queries, but concurrent inserts must maintain additional secondary indexes.
- The strongest backend angle is the migration from a course-style monolithic Flask file to a maintainable layered architecture.
- The strongest security angle is replacing hard-coded database credentials and plaintext passwords with environment configuration and password hashing.
- The strongest reliability angle is using UUIDs and unique constraints to avoid ID collisions and duplicate likes under concurrent access.
- The strongest maintainability angle is making the project reproducible through Docker Compose and guarded by GitHub Actions tests.
