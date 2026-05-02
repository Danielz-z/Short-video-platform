USE short_video_platform;

DELIMITER //

DROP PROCEDURE IF EXISTS GetHotVideosByAuthor//
CREATE PROCEDURE GetHotVideosByAuthor(IN p_author_id CHAR(36))
BEGIN
    SELECT video_id, title, likes_count, author_id
    FROM videos
    WHERE author_id = p_author_id
    ORDER BY likes_count DESC, upload_time DESC
    LIMIT 10;
END//

DROP PROCEDURE IF EXISTS InsertNewVideo//
CREATE PROCEDURE InsertNewVideo(
    IN p_video_id CHAR(36),
    IN p_title VARCHAR(100),
    IN p_video_url VARCHAR(255),
    IN p_author_id CHAR(36),
    IN p_field_id INT,
    IN p_upload_time DATETIME
)
BEGIN
    INSERT INTO videos (video_id, title, video_url, author_id, field_id, upload_time)
    VALUES (p_video_id, p_title, p_video_url, p_author_id, p_field_id, p_upload_time);
END//

DROP PROCEDURE IF EXISTS UpdateVideoTitle//
CREATE PROCEDURE UpdateVideoTitle(IN p_video_id CHAR(36), IN p_title VARCHAR(100))
BEGIN
    UPDATE videos
    SET title = p_title
    WHERE video_id = p_video_id;
END//

DROP PROCEDURE IF EXISTS DeleteVideoById//
CREATE PROCEDURE DeleteVideoById(IN p_video_id CHAR(36))
BEGIN
    DELETE FROM video_tags WHERE video_id = p_video_id;
    DELETE FROM likes WHERE video_id = p_video_id;
    DELETE FROM comments WHERE video_id = p_video_id;
    DELETE FROM videos WHERE video_id = p_video_id;
END//

DELIMITER ;

