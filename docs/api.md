# API and Route Reference

This project is a server-rendered Flask application. Most routes return HTML templates and use form submissions instead of JSON APIs.

## Authentication

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/` | Redirects to the login page. | Public |
| `GET` | `/login` | Renders the login form. | Public |
| `POST` | `/login` | Authenticates a user and redirects to the admin or video dashboard. | Public |
| `GET` | `/logout` | Clears the session and redirects to login. | User |

## Admin

Admin access is determined by usernames containing `admin`.

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/admin` | Shows the admin dashboard and user list. | Admin |
| `GET` | `/admin/register` | Renders the user creation form. | Admin |
| `POST` | `/admin/register` | Creates a user with a UUID primary key and hashed password. | Admin |
| `GET` | `/admin/edit/<user_id>` | Renders the user edit form. | Admin |
| `POST` | `/admin/edit/<user_id>` | Updates username, contact info, gender, and optionally password. | Admin |
| `GET` | `/admin/user/<user_id>` | Shows user details and recent videos. | Admin |
| `GET` | `/admin/delete/<user_id>` | Deletes a user and related graph data. | Admin |
| `POST` | `/admin/backup` | Creates a database backup with `mysqldump`. | Admin |
| `POST` | `/admin/restore` | Restores a backup file from `database/backup`. | Admin |

## Video

| Method | Path | Description | Auth |
| --- | --- | --- | --- |
| `GET` | `/videos` | Shows the current user's videos and hot videos. | User |
| `POST` | `/videos` | Searches hot videos by author ID. | User |
| `GET` | `/upload_video` | Renders the video upload form. | User |
| `POST` | `/upload_video` | Creates a video with a UUID primary key. | User |
| `POST` | `/update_video` | Updates a video title. The current user must be the author. | User |
| `POST` | `/delete_video` | Deletes a video. The current user must be the author. | User |
| `POST` | `/like_video` | Creates a like record and increments `videos.likes_count`. | User |
| `GET` | `/video/<video_id>` | Shows video details. | User |

## Route Layer Mapping

| File | Responsibility |
| --- | --- |
| `backend/routes/auth.py` | Login, logout, and home redirect |
| `backend/routes/admin.py` | Admin dashboard, user management, backup, restore |
| `backend/routes/video.py` | Video dashboard, upload, update, delete, like, detail |

## Service and DAO Mapping

| Layer | Files | Responsibility |
| --- | --- | --- |
| Service | `backend/services/user_service.py` | Authentication, password validation, password hashing, admin check |
| Service | `backend/services/video_service.py` | Video upload/update/delete business rules and author permission checks |
| DAO | `backend/dao/user_dao.py` | User SQL and user-related graph deletion |
| DAO | `backend/dao/video_dao.py` | Video SQL, stored procedure calls, likes, and video details |

## Benchmark Commands

The benchmark scripts are not HTTP APIs. They are command-line entry points for database performance experiments.

```bash
python experiments/insert/insert_worker.py --threads 8 --batch-size 500 --duration 300
python experiments/query/query_worker.py --threads 8 --duration 300 --field-id 3
python experiments/run_parallel.py --threads 8 --batch-size 500 --duration 300
```

Outputs include total operations, elapsed time, average latency, P95 latency, and QPS.

