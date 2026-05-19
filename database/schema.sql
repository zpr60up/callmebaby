CREATE TABLE IF NOT EXISTS scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    caller_name TEXT NOT NULL,
    caller_number TEXT,
    audio_file TEXT,
    is_custom BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 插入一些預設情境資料
INSERT INTO scenarios (name, caller_name, caller_number, audio_file, is_custom)
VALUES 
('媽媽催回家', '媽媽', '0912-345-678', 'mom_call.mp3', 0),
('老闆要開會', '老闆', '0987-654-321', 'boss_call.mp3', 0),
('朋友有急事', '王大明', '0955-555-555', 'friend_call.mp3', 0);
