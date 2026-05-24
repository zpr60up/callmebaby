# 系統架構說明 (Architecture)

## 1. 技術架構說明
- 後端：Python + Flask
- 模板引擎：Jinja2（負責 HTML 頁面渲染）
- 資料庫：SQLite（透過內建 sqlite3 模組）
- 視覺/互動：純 Vanilla CSS 與 JavaScript，著重於深色模式 (Dark Mode) 與毛玻璃 (Glassmorphism) 特效。

## 2. 專案資料夾結構
```
callmebaby/
├── app/
│   ├── models/         # 資料庫與邏輯模型 (Model)
│   ├── routes/         # 路由控制器 (Controller)
│   ├── templates/      # Jinja2 樣板 (View)
│   └── static/         # CSS/JS 與靜態資源
│       ├── css/
│       ├── js/
│       └── audio/      # 預錄語音檔
├── database/           # 資料庫建表語法 (schema.sql)
├── instance/           # SQLite 資料庫檔案存放處
├── docs/               # 專案文件
├── app.py              # Flask 入口點
└── requirements.txt    # 套件清單
```

## 3. 元件關係圖
```mermaid
flowchart LR
    Browser[瀏覽器] -->|GET /scenarios| FlaskRoute[Flask Route]
    FlaskRoute -->|get_all()| Model[Scenario Model]
    Model <-->|SQL| SQLite[(SQLite DB)]
    FlaskRoute -->|Render| Template[Jinja2 Template]
    Template --> Browser
```

## 4. 關鍵設計決策
1. **Model-View-Controller 分離**：將邏輯層拆分，提升後續 F-01 與 F-02 的開發與維護性。
2. **Session 狀態管理**：因應脫逃情境，使用者選定的「當前劇本」將存放在 Session，這比存入 DB 更輕量且即時。
3. **無框架前端設計**：採用 Vanilla CSS 減少載入負擔，利用 CSS 變數實作全域設計系統。
