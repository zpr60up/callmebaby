-- Call Me Baby - 資料庫 Schema

CREATE TABLE IF NOT EXISTS callers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                              -- 來電者名稱（如：爸爸、老闆）
    phone TEXT NOT NULL,                             -- 電話號碼（顯示用）
    avatar TEXT DEFAULT 'avatar_default.png',        -- 大頭貼檔名
    voice_file TEXT DEFAULT 'voice_family',          -- 預錄語音檔名
    call_style TEXT DEFAULT 'ios',                   -- 來電風格：ios / android
    created_at TEXT DEFAULT (datetime('now','localtime')),
    updated_at TEXT DEFAULT (datetime('now','localtime'))
);

-- 預設資料
INSERT INTO callers (name, phone, avatar, voice_file, call_style)
SELECT '爸爸', '0912-345-678', 'avatar_dad.png', 'voice_family', 'ios'
WHERE NOT EXISTS (SELECT 1 FROM callers WHERE name = '爸爸');

INSERT INTO callers (name, phone, avatar, voice_file, call_style)
SELECT '老闆', '02-2345-6789', 'avatar_boss.png', 'voice_boss', 'ios'
WHERE NOT EXISTS (SELECT 1 FROM callers WHERE name = '老闆');

INSERT INTO callers (name, phone, avatar, voice_file, call_style)
SELECT '好朋友', '0978-123-456', 'avatar_friend.png', 'voice_friend', 'ios'
WHERE NOT EXISTS (SELECT 1 FROM callers WHERE name = '好朋友');

CREATE TABLE IF NOT EXISTS recordings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    display_name TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    caller_name TEXT NOT NULL,
    caller_number TEXT NOT NULL,
    audio_file TEXT,
    is_custom INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS custom_callers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caller_name TEXT NOT NULL,
    caller_phone TEXT NOT NULL,
    avatar_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 預設插入的劇本資料
INSERT INTO scenarios (name, caller_name, caller_number, audio_file, is_custom)
SELECT '家庭急事', '媽媽', '0912345678', '/static/audio/family_emergency.mp3', 0
WHERE NOT EXISTS (SELECT 1 FROM scenarios WHERE name = '家庭急事');

INSERT INTO scenarios (name, caller_name, caller_number, audio_file, is_custom)
SELECT '公司加班', '老闆', '0987654321', '/static/audio/boss_overtime.mp3', 0
WHERE NOT EXISTS (SELECT 1 FROM scenarios WHERE name = '公司加班');

INSERT INTO scenarios (name, caller_name, caller_number, audio_file, is_custom)
SELECT '快遞取件', '快遞員', '0900000000', '/static/audio/delivery.mp3', 0
WHERE NOT EXISTS (SELECT 1 FROM scenarios WHERE name = '快遞取件');
