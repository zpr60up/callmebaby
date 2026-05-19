-- Call Me Baby - 資料庫 Schema
-- 功能 F-02: 語音通話模擬與互動

CREATE TABLE IF NOT EXISTS callers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                              -- 來電者名稱（如：爸爸、老闆）
    phone TEXT NOT NULL,                             -- 電話號碼（顯示用）
    avatar TEXT DEFAULT 'avatar_default.png',        -- 大頭貼檔名
    voice_file TEXT DEFAULT 'voice_family.mp3',      -- 預錄語音檔名
    call_style TEXT DEFAULT 'ios',                   -- 來電風格：ios / android
    created_at TEXT DEFAULT (datetime('now','localtime')),
    updated_at TEXT DEFAULT (datetime('now','localtime'))
);

-- 預設資料
INSERT INTO callers (name, phone, avatar, voice_file, call_style) VALUES
    ('爸爸', '0912-345-678', 'avatar_dad.png', 'voice_family', 'ios'),
    ('老闆', '02-2345-6789', 'avatar_boss.png', 'voice_boss', 'ios'),
    ('好朋友', '0978-123-456', 'avatar_friend.png', 'voice_friend', 'ios');
