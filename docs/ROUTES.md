# 路由設計 (Routes Design)

## 1. 路由總覽表格
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 根目錄轉址 | GET | `/` | — | 重導向至 `/scenarios/` |
| 劇本列表 | GET | `/scenarios/` | `scenario/index.html` | 顯示所有可用的劇本 |
| 套用劇本 | POST | `/scenarios/<id>/apply` | — | 將劇本資料寫入 Session，並重導向回列表 |

## 2. 每個路由的詳細說明
- **GET `/scenarios/`**
  - 輸入：無
  - 處理邏輯：呼叫 `Scenario.get_all()` 取得資料。
  - 輸出：渲染 `scenario/index.html`，傳入劇本列表以及當前已套用的劇本 ID (從 Session 讀取)。
- **POST `/scenarios/<id>/apply`**
  - 輸入：URL 參數 `id`
  - 處理邏輯：呼叫 `Scenario.get_by_id(id)`，若存在則將 `caller_name`, `phone_number`, `voice_path` 存入 `session['active_scenario']`。
  - 輸出：Flash 提示「劇本套用成功」，重導向至 `/scenarios/`。

## 3. Jinja2 模板清單
- `base.html`: 網站共同版型，包含 `<head>`、CSS 與 Flash 訊息區塊。
- `scenario/index.html`: 繼承 `base.html`，以卡片形式顯示劇本列表。
