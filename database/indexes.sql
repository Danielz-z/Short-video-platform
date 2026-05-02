USE short_video_platform;

CREATE INDEX idx_videos_author_id ON videos(author_id);
CREATE INDEX idx_videos_field_id ON videos(field_id);
CREATE INDEX idx_videos_upload_time ON videos(upload_time);

CREATE INDEX idx_videos_hot_author ON videos(author_id, likes_count DESC, upload_time DESC);
CREATE INDEX idx_videos_popularity ON videos(likes_count DESC, comments_count DESC);
CREATE INDEX idx_likes_video_time ON likes(video_id, like_time);
CREATE INDEX idx_likes_user_time ON likes(user_id, like_time);
CREATE INDEX idx_comments_video_time ON comments(video_id, comment_time);
CREATE INDEX idx_comments_user_time ON comments(user_id, comment_time);
CREATE INDEX idx_follows_followed ON follows(followed_id);
CREATE INDEX idx_messages_sender_time ON messages(sender_id, send_time);
CREATE INDEX idx_messages_receiver_time ON messages(receiver_id, send_time);

