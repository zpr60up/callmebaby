"""
Recording Model — 錄音檔案資料 CRUD
管理使用者錄製的自訂語音。
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


def create(filename, display_name):
    """
    新增一筆自訂錄音記錄。

    Args:
        filename (str): 音訊檔案的唯一名稱（含副檔名）
        display_name (str): 錄音的自訂顯示名稱

    Returns:
        int: 新增記錄的 ID
    """
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO recordings (filename, display_name) VALUES (?, ?)',
            (filename, display_name)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id
    except Exception as e:
        print(f"[Recording Model] create error: {e}")
        return None


def get_all():
    """
    取得所有自訂錄音記錄，以時間遞減排序。

    Returns:
        list[sqlite3.Row]: 所有錄音資料
    """
    try:
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM recordings ORDER BY created_at DESC').fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[Recording Model] get_all error: {e}")
        return []


def get_by_id(rec_id):
    """
    取得單筆錄音資料。

    Args:
        rec_id (int): 錄音 ID

    Returns:
        sqlite3.Row or None: 錄音資料
    """
    try:
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM recordings WHERE id = ?', (rec_id,)).fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"[Recording Model] get_by_id error: {e}")
        return None


def get_by_filename(filename):
    """
    依檔案名稱取得單筆錄音資料。

    Args:
        filename (str): 檔案名稱

    Returns:
        sqlite3.Row or None: 錄音資料
    """
    try:
        conn = get_db_connection()
        row = conn.execute('SELECT * FROM recordings WHERE filename = ?', (filename,)).fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"[Recording Model] get_by_filename error: {e}")
        return None


def delete(rec_id):
    """
    刪除一筆自訂錄音。

    Args:
        rec_id (int): 錄音 ID

    Returns:
        bool: 是否刪除成功
    """
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM recordings WHERE id = ?', (rec_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Recording Model] delete error: {e}")
        return False
