"""
Caller Model — 來電者資料 CRUD
管理來電者的名稱、電話、大頭貼、語音檔等資訊。
"""

import sqlite3
import os

# 資料庫路徑
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')


def get_db_connection():
    """取得資料庫連線，啟用 Row 模式以便用欄位名稱取值。"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create(data):
    """
    新增一筆來電者記錄。

    Args:
        data (dict): 包含 name, phone, avatar, voice_file, call_style

    Returns:
        int: 新增記錄的 ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            '''INSERT INTO callers (name, phone, avatar, voice_file, call_style)
               VALUES (?, ?, ?, ?, ?)''',
            (
                data.get('name', '未知'),
                data.get('phone', '0000-000-000'),
                data.get('avatar', 'avatar_default.png'),
                data.get('voice_file', 'voice_family'),
                data.get('call_style', 'ios')
            )
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id
    except Exception as e:
        print(f"[Caller Model] create error: {e}")
        return None


def get_all():
    """
    取得所有來電者記錄。

    Returns:
        list[sqlite3.Row]: 所有來電者資料
    """
    try:
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM callers ORDER BY created_at DESC').fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[Caller Model] get_all error: {e}")
        return []


def get_by_id(caller_id):
    """
    取得單筆來電者記錄。

    Args:
        caller_id (int): 來電者 ID

    Returns:
        sqlite3.Row or None: 來電者資料
    """
    try:
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM callers WHERE id = ?', (caller_id,)).fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"[Caller Model] get_by_id error: {e}")
        return None


def update(caller_id, data):
    """
    更新來電者記錄。

    Args:
        caller_id (int): 來電者 ID
        data (dict): 要更新的欄位

    Returns:
        bool: 是否更新成功
    """
    try:
        conn = get_db_connection()
        conn.execute(
            '''UPDATE callers
               SET name = ?, phone = ?, avatar = ?, voice_file = ?, call_style = ?,
                   updated_at = datetime('now','localtime')
               WHERE id = ?''',
            (
                data.get('name'),
                data.get('phone'),
                data.get('avatar', 'avatar_default.png'),
                data.get('voice_file', 'voice_family'),
                data.get('call_style', 'ios'),
                caller_id
            )
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Caller Model] update error: {e}")
        return False


def delete(caller_id):
    """
    刪除來電者記錄。

    Args:
        caller_id (int): 來電者 ID

    Returns:
        bool: 是否刪除成功
    """
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM callers WHERE id = ?', (caller_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Caller Model] delete error: {e}")
        return False
