"""
Call Me Baby - 啟動腳本
匯入 app.py 中的主應用程式並啟動。
"""

from app import app

if __name__ == '__main__':
    # 啟動應用程式，預設通訊埠為 5000
    app.run(debug=True, port=5000)
