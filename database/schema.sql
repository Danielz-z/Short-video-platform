CREATE DATABASE IF NOT EXISTS short_video_platform
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE short_video_platform;

CREATE TABLE IF NOT EXISTS users (
    user_id CHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    phone_email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
    fans_count INT NOT NULL DEFAULT 0,
    register_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    gender ENUM('M', 'F', 'O', 'U') NOT NULL DEFAULT 'U',
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_phone_email (phone_email),
    CHECK (fans_count >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS fields (
    field_id INT PRIMARY KEY AUTO_INCREMENT,
    field_name VARCHAR(50) NOT NULL,
    UNIQUE KEY uq_fields_name (field_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tags (
    tag_id INT PRIMARY KEY AUTO_INCREMENT,
    tag_name VARCHAR(50) NOT NULL,
    UNIQUE KEY uq_tags_name (tag_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS videos (
    video_id CHAR(36) PRIMARY KEY,
    video_url VARCHAR(255) NOT NULL,
    title VARCHAR(100) NOT NULL,
    likes_count INT NOT NULL DEFAULT 0,
    comments_count INT NOT NULL DEFAULT 0,
    upload_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id CHAR(36) NOT NULL,
    field_id INT,
    visibility ENUM('public', 'private', 'friends_only') NOT NULL DEFAULT 'public',
    UNIQUE KEY uq_videos_url (video_url),
    CONSTRAINT fk_videos_author FOREIGN KEY (author_id) REFERENCES users(user_id),
    CONSTRAINT fk_videos_field FOREIGN KEY (field_id) REFERENCES fields(field_id),
    CHECK (likes_count >= 0),
    CHECK (comments_count >= 0),
    CHECK (CHAR_LENGTH(title) BETWEEN 2 AND 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS likes (
    like_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id CHAR(36) NOT NULL,
    video_id CHAR(36) NOT NULL,
    like_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_likes_user_video (user_id, video_id),
    CONSTRAINT fk_likes_user FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_likes_video FOREIGN KEY (video_id) REFERENCES videos(video_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS comments (
    comment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    video_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    content TEXT NOT NULL,
    comment_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comments_video FOREIGN KEY (video_id) REFERENCES videos(video_id),
    CONSTRAINT fk_comments_user FOREIGN KEY (user_id) REFERENCES users(user_id),
    CHECK (CHAR_LENGTH(TRIM(content)) > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS follows (
    follow_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    follower_id CHAR(36) NOT NULL,
    followed_id CHAR(36) NOT NULL,
    follow_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_follows_pair (follower_id, followed_id),
    CONSTRAINT fk_follows_follower FOREIGN KEY (follower_id) REFERENCES users(user_id),
    CONSTRAINT fk_follows_followed FOREIGN KEY (followed_id) REFERENCES users(user_id),
    CHECK (follower_id <> followed_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS messages (
    message_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    sender_id CHAR(36) NOT NULL,
    receiver_id CHAR(36) NOT NULL,
    content TEXT NOT NULL,
    send_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_messages_sender FOREIGN KEY (sender_id) REFERENCES users(user_id),
    CONSTRAINT fk_messages_receiver FOREIGN KEY (receiver_id) REFERENCES users(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS video_tags (
    video_id CHAR(36) NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (video_id, tag_id),
    CONSTRAINT fk_video_tags_video FOREIGN KEY (video_id) REFERENCES videos(video_id),
    CONSTRAINT fk_video_tags_tag FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO fields (field_id, field_name) VALUES
    (1, 'Food'),
    (2, 'Travel'),
    (3, 'Technology'),
    (4, 'Music'),
    (5, 'Fitness');
