"""
Call Me Baby — Flask 應用程式入口
提供多樣化的假來電與訊息通知模板，幫助使用者安全脫身。
"""

import os
import sqlite3
from flask import Flask, redirect, url_for

# 初始化 Flask App
app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)
app.secret_key = os.environ.get('SECRET_KEY', 'callmebaby-secret-key-2024')

# 確保 instance 資料夾存在
os.makedirs('instance', exist_ok=True)


def init_db():
    """初始化資料庫：執行 schema.sql 建立資料表。"""
    db_path = os.path.join('instance', 'database.db')
    schema_path = os.path.join('database', 'schema.sql')

    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print('[Call Me Baby] 資料庫初始化完成！')


# 註冊 Blueprint
from app.routes.call import call_bp
app.register_blueprint(call_bp)


@app.route('/')
def index():
    """首頁重導向到來電設定頁面。"""
    return redirect(url_for('call.setup'))


# 啟動時自動初始化資料庫
with app.app_context():
    db_path = os.path.join('instance', 'database.db')
    if not os.path.exists(db_path):
        init_db()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
