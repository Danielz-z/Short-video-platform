USE short_video_platform;

INSERT IGNORE INTO users (user_id, username, phone_email, password, fans_count, register_time, gender) VALUES
('11111111-1111-1111-1111-111111111111', 'admin_demo', 'admin@example.com', 'scrypt:32768:8:1$uZKcA2njWOcHckAu$ed3c6bc855d528fb1e61248a852a129f584f35c14092f6d230257e652efdde5099833d06ed5651302f46e13efa2afc85fb1059a29b6c9c2ca9e042bf8928634f', 0, NOW(), 'U'),
('22222222-2222-2222-2222-222222222222', 'food_creator', 'food@example.com', 'scrypt:32768:8:1$uZKcA2njWOcHckAu$ed3c6bc855d528fb1e61248a852a129f584f35c14092f6d230257e652efdde5099833d06ed5651302f46e13efa2afc85fb1059a29b6c9c2ca9e042bf8928634f', 1500, NOW(), 'U'),
('33333333-3333-3333-3333-333333333333', 'tech_creator', 'tech@example.com', 'scrypt:32768:8:1$uZKcA2njWOcHckAu$ed3c6bc855d528fb1e61248a852a129f584f35c14092f6d230257e652efdde5099833d06ed5651302f46e13efa2afc85fb1059a29b6c9c2ca9e042bf8928634f', 2600, NOW(), 'U');

INSERT IGNORE INTO videos (video_id, video_url, title, likes_count, comments_count, upload_time, author_id, field_id) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'https://example.com/videos/food-demo', 'Five-minute home cooking demo', 120, 8, NOW(), '22222222-2222-2222-2222-222222222222', 1),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'https://example.com/videos/ai-demo', 'AI workflow tips for creators', 260, 18, NOW(), '33333333-3333-3333-3333-333333333333', 3);

INSERT IGNORE INTO likes (user_id, video_id, like_time) VALUES
('33333333-3333-3333-3333-333333333333', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW()),
('22222222-2222-2222-2222-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', NOW());

INSERT IGNORE INTO comments (video_id, user_id, content, comment_time) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '33333333-3333-3333-3333-333333333333', 'Clear and useful demo.', NOW()),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '22222222-2222-2222-2222-222222222222', 'Great workflow notes.', NOW());
