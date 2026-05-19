# 使用者與系統流程圖 (Flowchart)

## 1. 使用者流程圖（User Flow）
```mermaid
flowchart LR
    A([開啟首頁]) --> B[顯示劇本列表 /scenarios]
    B --> C{選擇劇本操作？}
    C -->|點擊「套用此劇本」| D[將劇本資訊存入 Session]
    D --> E([顯示成功提示並停留在列表頁])
```

## 2. 系統序列圖（Sequence Diagram）
```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser
    participant Flask as Flask Route
    participant DB as SQLite

    User->>Browser: 點擊套用劇本 (POST /scenarios/<id>/apply)
    Browser->>Flask: 傳送請求
    Flask->>DB: 查詢劇本詳細資料 (get_by_id)
    DB-->>Flask: 回傳劇本資料
    Flask->>Flask: 將資料存入 Session
    Flask-->>Browser: 重導向至 /scenarios 並帶有 Flash Message
    Browser-->>User: 顯示「套用成功」
```

## 3. 功能清單對照表
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 顯示劇本列表 | GET | `/scenarios/` | `scenario/index.html` | 讀取所有預設劇本並展示 |
| 套用指定劇本 | POST | `/scenarios/<id>/apply` | — | 將選中的劇本資訊寫入 session |
