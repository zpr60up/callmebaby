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
