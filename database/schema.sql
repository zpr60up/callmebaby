CREATE TABLE IF NOT EXISTS scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    caller_name TEXT NOT NULL,
    caller_phone TEXT NOT NULL,
    avatar_path TEXT,
    audio_path TEXT,
    category TEXT
);

CREATE TABLE IF NOT EXISTS custom_callers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caller_name TEXT NOT NULL,
    caller_phone TEXT NOT NULL,
    avatar_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
    phone_number TEXT NOT NULL,
    voice_path TEXT,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 預設插入的劇本資料
INSERT INTO scenarios (title, caller_name, phone_number, voice_path, description)
SELECT '家庭急事', '媽媽', '0912345678', '/static/audio/family_emergency.mp3', '假裝家裡有急事需要馬上回去'
WHERE NOT EXISTS (SELECT 1 FROM scenarios WHERE title = '家庭急事');

INSERT INTO scenarios (title, caller_name, phone_number, voice_path, description)
SELECT '公司加班', '老闆', '0987654321', '/static/audio/boss_overtime.mp3', '假裝公司臨時有狀況需要回公司處理'
WHERE NOT EXISTS (SELECT 1 FROM scenarios WHERE title = '公司加班');

INSERT INTO scenarios (title, caller_name, phone_number, voice_path, description)
SELECT '快遞取件', '快遞員', '0900000000', '/static/audio/delivery.mp3', '假裝有重要包裹送到，必須親自簽收'
WHERE NOT EXISTS (SELECT 1 FROM scenarios WHERE title = '快遞取件');
