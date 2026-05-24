# 流程圖設計 (Flowcharts)

## 1. 使用者流程圖 (User Flow)

此流程圖描述使用者從進入系統到完成「假來電脫逃」的完整操作路徑。

```mermaid
flowchart TD
    A([使用者開啟網頁]) --> B[首頁 - 設定假來電與觸發]
    B --> C{設定選項}
    C -->|選擇作業系統| D[切換 iOS / Android 風格]
    C -->|選擇情境| E[選擇「催回家」等不同劇本]
    
    D --> F[點擊「立即觸發假來電」]
    E --> F
    
    F --> G[進入「來電中」全螢幕畫面]
    G --> H{操作來電介面}
    
    H -->|點擊「接聽」| I[進入「通話中」畫面]
    I --> J[開始計時並播放情境語音]
    J --> K{操作通話介面}
    K -->|點擊「掛斷」| L[語音停止，返回首頁]
    
    H -->|點擊「拒接」| L
```

## 2. 系統順序圖 (Sequence Diagram)

此圖描述點擊「觸發假來電」到接聽播放語音的系統資料流。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (JS/HTML)
    participant Flask as Flask Server
    participant DB as SQLite
    
    User->>Browser: 調整設定並點擊「觸發假來電」
    Browser->>Flask: POST /call/trigger (傳送 OS 與情境 ID)
    Flask->>DB: 查詢情境語音資料
    DB-->>Flask: 回傳情境資訊 (如: 媽媽, mom_call.mp3)
    Flask-->>Browser: 回傳來電畫面 (incoming.html)
    
    Note over User, Browser: 瀏覽器顯示全螢幕來電介面
    User->>Browser: 點擊「接聽」
    
    Browser->>Flask: GET /call/active?scenario_id=1
    Flask-->>Browser: 回傳通話中畫面 (active.html)
    
    Note over Browser: JS 開始通話計時
    Note over Browser: JS 播放情境音檔 (audio.play())
    
    User->>Browser: 點擊「掛斷」
    Note over Browser: JS 停止音檔
    Browser->>Flask: GET / (返回首頁)
    Flask-->>Browser: 回傳首頁
```

## 3. 功能清單對照表

| 功能 | HTTP 方法 | URL 路徑 | 說明 |
| :--- | :--- | :--- | :--- |
| 首頁 (設定) | GET | `/` | 顯示表單讓使用者選擇介面風格與語音劇本 |
| 觸發假來電 | POST | `/call/trigger` | 接收表單設定，跳轉到來電中畫面 |
| 來電中畫面 | GET | `/call/incoming` | 顯示來電響鈴介面，提供接聽與拒接按鈕 |
| 通話中畫面 | GET | `/call/active` | 顯示通話中介面，開始計時並播放對應語音 |
