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

-- 預設來電者資料
INSERT INTO callers (name, phone, avatar, voice_file, call_style)
SELECT '爸爸', '0912-345-678', 'avatar_dad.png', 'voice_family', 'ios'
WHERE NOT EXISTS (SELECT 1 FROM callers WHERE name = '爸爸');

INSERT INTO callers (name, phone, avatar, voice_file, call_style)
SELECT '老闆', '02-2345-6789', 'avatar_boss.png', 'voice_boss', 'ios'
WHERE NOT EXISTS (SELECT 1 FROM callers WHERE name = '老闆');

INSERT INTO callers (name, phone, avatar, voice_file, call_style)
SELECT '好朋友', '0978-123-456', 'avatar_friend.png', 'voice_friend', 'ios'
WHERE NOT EXISTS (SELECT 1 FROM callers WHERE name = '好朋友');

-- 劇本資料表 (結合了所有版本欄位，避免舊有或新實作路由崩潰)
CREATE TABLE IF NOT EXISTS scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    name TEXT,
    caller_name TEXT NOT NULL,
    caller_phone TEXT,
    phone_number TEXT,
    caller_number TEXT,
    avatar_path TEXT,
    audio_path TEXT,
    voice_path TEXT,
    audio_file TEXT,
    category TEXT,
    description TEXT,
    is_custom INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 預設劇本資料
INSERT INTO scenarios (title, name, caller_name, caller_phone, phone_number, caller_number, avatar_path, voice_path, audio_path, audio_file, category, description)
SELECT '家庭急事', '家庭急事', '爸爸', '0912-345-678', '0912-345-678', '0912-345-678', '/static/images/avatar_dad.png', '/static/audio/family_emergency.mp3', '/static/audio/family_emergency.mp3', '/static/audio/family_emergency.mp3', 'emergency', '假裝家裡有急事需要馬上回去'
WHERE NOT EXISTS (SELECT 1 FROM scenarios WHERE title = '家庭急事');

INSERT INTO scenarios (title, name, caller_name, caller_phone, phone_number, caller_number, avatar_path, voice_path, audio_path, audio_file, category, description)
SELECT '老闆奪命連環call', '公司加班', '老闆', '0988-888-888', '0988-888-888', '0988-888-888', '/static/images/avatar_boss.png', '/static/audio/boss_overtime.mp3', '/static/audio/boss_overtime.mp3', '/static/audio/boss_overtime.mp3', 'work', '假裝公司臨時有狀況需要回公司處理'
WHERE NOT EXISTS (SELECT 1 FROM scenarios WHERE title = '老闆奪命連環call');

INSERT INTO scenarios (title, name, caller_name, caller_phone, phone_number, caller_number, avatar_path, voice_path, audio_path, audio_file, category, description)
SELECT '快遞取件', '快遞取件', '黑貓宅急便', '0933-222-111', '0933-222-111', '0933-222-111', '/static/images/avatar_delivery.png', '/static/audio/delivery.mp3', '/static/audio/delivery.mp3', '/static/audio/delivery.mp3', 'delivery', '假裝有重要包裹送到，必須親自簽收'
WHERE NOT EXISTS (SELECT 1 FROM scenarios WHERE title = '快遞取件');

-- 自訂來電者資料表
CREATE TABLE IF NOT EXISTS custom_callers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caller_name TEXT NOT NULL,
    caller_phone TEXT NOT NULL,
    avatar_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
