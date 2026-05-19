# 系統架構設計 (Architecture Design)

## 1. 技術架構說明

本專案「情境脫逃生產器」(Call Me Baby) 採用輕量級的 Python Flask 框架作為後端核心，並透過 Jinja2 模板引擎與 SQLite 資料庫組成傳統的 MVC（Model-View-Controller）架構。不採用前後端分離，以求快速開發與部署，適合 MVP 階段。

### 選用技術與原因
- **後端框架：Flask**
  - 原因：輕量、彈性高，適合中小型專案。能快速建立路由與處理 API 請求，且內建 Jinja2 模板引擎。
- **模板引擎：Jinja2**
  - 原因：與 Flask 無縫整合，負責伺服器端渲染 (SSR)。可利用版型繼承機制，重複利用共用的 HTML 結構。
- **資料庫：SQLite**
  - 原因：輕量且無須額外設定伺服器。所有資料儲存在單一檔案中，易於備份與轉移，完全滿足儲存使用者設定檔與情境劇本的需求。
- **前端技術：HTML5 / Vanilla CSS / JavaScript**
  - 原因：為了達到在手機上「不穿幫」的擬真效果，需要精準控制 UI。使用純 CSS（不依賴大型框架如 Bootstrap）有助於完美複製 iOS 與 Android 原生來電介面的樣式。純 JS 則用於處理倒數計時與語音播放。

### Flask MVC 模式說明
- **Model (模型)**：負責與資料庫溝通，處理資料的存取與邏輯（如：取得特定的假來電設定或劇本）。程式碼放在 `app/models/`。
- **View (視圖)**：負責呈現使用者介面，接收 Model 的資料並轉換成 HTML。由 `app/templates/` 內的 Jinja2 檔案負責。
- **Controller (控制器)**：負責接收使用者的 HTTP 請求（如點擊按鈕、提交表單），呼叫對應的 Model 處理資料，最後決定要渲染哪一個 View。在 Flask 中，Controller 就是定義在 `app/routes/` 中的路由函式。

---

## 2. 專案資料夾結構

本專案將採用以下資料夾結構，以確保程式碼模組化且易於維護：

```text
callmebaby/
├── app/                        # 應用程式主目錄
│   ├── __init__.py             # 初始化 Flask app，註冊路由與資料庫
│   ├── models/                 # Model 層：資料庫模型與存取邏輯
│   │   ├── __init__.py
│   │   ├── scenario.py         # 劇本設定模型
│   │   └── user_setting.py     # 使用者偏好設定模型
│   ├── routes/                 # Controller 層：路由處理
│   │   ├── __init__.py
│   │   ├── main.py             # 主頁面與設定路由
│   │   └── call.py             # 觸發與處理來電畫面的路由
│   ├── static/                 # 靜態資源 (CSS, JS, 圖片, 音檔)
│   │   ├── css/
│   │   │   ├── style.css       # 共用樣式
│   │   │   ├── ios.css         # iOS 擬真樣式
│   │   │   └── android.css     # Android 擬真樣式
│   │   ├── js/
│   │   │   └── call.js         # 處理計時器、接聽/掛斷動畫與語音播放
│   │   └── audio/              # 預錄情境音檔存放處
│   └── templates/              # View 層：Jinja2 模板
│       ├── base.html           # 共用基礎版型
│       ├── index.html          # 首頁 / 設定頁
│       └── call/
│           ├── incoming.html   # 來電中畫面
│           └── active.html     # 通話中畫面
├── database/                   # 資料庫相關檔案
│   ├── schema.sql              # 資料庫建表語法
│   └── callmebaby.db           # SQLite 資料庫檔案 (執行期產生)
├── docs/                       # 文件資料夾
│   ├── PRD.md                  # 產品需求文件
│   └── ARCHITECTURE.md         # 系統架構設計
├── app.py                      # 程式進入點
└── requirements.txt            # Python 套件相依清單
```

---

## 3. 元件關係圖

以下展示使用者從瀏覽器操作，到系統內部處理與回應的完整流程：

```mermaid
flowchart TD
    %% 定義節點
    Browser[瀏覽器 (Client)]
    Router[Flask 路由 (Controller)]
    Model[Model 層 (Python 類別)]
    DB[(SQLite 資料庫)]
    Template[Jinja2 模板 (View)]

    %% 使用者發出請求
    Browser -- "HTTP GET / POST\n(例如：請求來電畫面)" --> Router
    
    %% Controller 處理邏輯
    Router -- "讀取/寫入資料" --> Model
    Model -- "執行 SQL" --> DB
    DB -- "回傳資料" --> Model
    Model -- "回傳 Python 物件" --> Router
    
    %% Controller 渲染視圖
    Router -- "傳遞變數並要求渲染" --> Template
    Template -- "產生 HTML" --> Router
    
    %% 回應給使用者
    Router -- "回傳 HTML 頁面" --> Browser
```

---

## 4. 關鍵設計決策

1. **捨棄前端框架 (如 React/Vue) 改用 Flask SSR + Vanilla JS**：
   - 原因：本專案重點在於快速展現 MVP，且來電介面高度依賴 CSS 的視覺呈現，業務邏輯 (如觸發來電、播放音樂) 在前端可以用簡單的 Vanilla JS 解決。使用 SSR 能減少環境建置與編譯時間，加速團隊開發。
2. **樣式表 (CSS) 按作業系統拆分**：
   - 原因：為滿足 `[F-02]` 高度擬真，iOS 與 Android 的介面風格差異極大。將 `ios.css` 與 `android.css` 獨立分開，能避免樣式衝突，並透過 Flask 路由判斷動態載入，大幅降低切版的複雜度。
3. **音檔資源放於本機 (Static 資料夾)**：
   - 原因：目前專案在 MVP 階段，音檔數量不多。將預錄情境的音檔放在 `app/static/audio/` 中，可確保無網路延遲，使用者點擊「接聽」時能立刻播放，提升擬真度。
4. **採用 Factory Pattern 初始化 Flask (規劃在 `__init__.py`)**：
   - 原因：這是一種 Flask 最佳實踐，便於管理路由 (Blueprints) 以及未來擴充資料庫實例。
