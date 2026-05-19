# 路由與頁面設計 (API Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 (設定頁) | GET | `/` | `index.html` | 顯示所有可用的語音情境與介面風格選項 |
| 觸發假來電 | POST | `/call/trigger` | 無 (重新導向) | 接收首頁表單設定，並導向帶來電參數的來電畫面 |
| 來電中畫面 | GET | `/call/incoming` | `call/incoming.html` | 顯示手機響鈴中的畫面，根據參數切換 iOS/Android 風格 |
| 通話中畫面 | GET | `/call/active` | `call/active.html` | 顯示通話進行中的畫面，並播放對應語音 |

## 2. 每個路由的詳細說明

### `GET /` (首頁)
- **輸入**：無。
- **處理邏輯**：呼叫 `Scenario.get_all()` 取得所有內建的情境劇本。
- **輸出**：渲染 `index.html`，將 `scenarios` 傳入模板。
- **錯誤處理**：若資料庫查詢失敗，顯示預設錯誤訊息。

### `POST /call/trigger`
- **輸入**：表單參數 `os_style` (ios 或 android)、`scenario_id` (情境 ID)。
- **處理邏輯**：驗證輸入值是否合法。若合法，則將這些參數帶入 URL，重新導向到 `/call/incoming`。
- **輸出**：重新導向至 `/call/incoming?os_style=...&scenario_id=...`。
- **錯誤處理**：若參數缺少，導回 `/` 並顯示錯誤訊息。

### `GET /call/incoming`
- **輸入**：URL 參數 `os_style` 與 `scenario_id`。
- **處理邏輯**：呼叫 `Scenario.get_by_id(scenario_id)` 取得來電者名稱與語音檔名。
- **輸出**：渲染 `call/incoming.html`，根據 `os_style` 載入對應的 CSS，並顯示來電者名稱。
- **錯誤處理**：若找不到對應情境，導回 `/`。

### `GET /call/active`
- **輸入**：URL 參數 `os_style` 與 `scenario_id`。
- **處理邏輯**：同上，取得情境詳細資訊。
- **輸出**：渲染 `call/active.html`，自動播放音檔，啟動通話計時。

## 3. Jinja2 模板清單

1. **`base.html`**：共用的 HTML 骨架，包含基本的 meta tag、重置 CSS 等。
2. **`index.html`**：繼承 `base.html`，包含選擇 OS 風格與情境的表單，以及「觸發假來電」按鈕。
3. **`call/incoming.html`**：繼承 `base.html`，全螢幕顯示，提供「接聽」與「拒接」按鈕。
4. **`call/active.html`**：繼承 `base.html`，全螢幕顯示，提供通話時間與「掛斷」按鈕，並隱藏播放語音檔。

## 4. 路由骨架程式碼

請參考 `app/routes/main.py` 與 `app/routes/call.py` 檔案。
