USE short_video_platform;

ALTER TABLE users
    ADD COLUMN role ENUM('user', 'admin') NOT NULL DEFAULT 'user' AFTER password;

UPDATE users
SET role = 'admin'
WHERE LOWER(username) LIKE '%admin%';
