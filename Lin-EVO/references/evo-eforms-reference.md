# EVO 電子表單｜現行公版結構

2026-10-15 使用者指定 [evo266200 contact 電子表單](http://192.168.168.99/php83/sites/evo266200/public/zh-tw/formManager/contact) 為最新公版結構。這是獨立電子表單，不是詢問車；舊目錄的電子表單樣式 B 已移除，舊 A 示範不再作為現行工程依據。

## 來源與查核範圍

已透過瀏覽器實看頁面、讀取表單 DOM、欄位屬性及頁面載入的 CSS／JS URL。未讀取資源程式全文、未送出表單、未操作驗證錯誤、未驗收 RWD 或後台編輯／儲存／發布。不可把資源已載入當作所有功能驗證完成。

內網示範網址是查核來源，不是其他案件的正式路由；無法連內網時依本文件保留已確認結構，另列本案輸出與功能待核對，不猜測新契約。

## 公版 DOM

| 部位 | 已核對的結構／識別 |
|---|---|
| 表單根節點 | `form.eforms-wrapper`，來源有 `id="form-16"`、`data-data-id="16"`、`data-i18n`、`method="POST"`、`enctype="multipart/form-data"`、`novalidate`。來源 action 為本案 `/form/16/submit`。 |
| 每一欄 | `.form-row` → `.form-tag` 與 `.form-col`；標題內 `.main-red` 為必填星號。 |
| 輸入與提示 | `.form-col` 內為 `.form-item`（含控制項）及同層 `.form-require-alert`。 |
| 一般輸入／多行文字 | `input.form-style`、`textarea.form-style`；保留原生 `id`、`name`、`aria-label`、placeholder 等欄位設定。 |
| 下拉選單 | `select.form-style.form-select-style` 與後台產生的 options。 |
| 檢核標記 | 來源電話為 `input[type="text"][data-validate="phone"]`，信箱為 `input[type="text"][data-validate="email"]`；不要只依 input type 推定檢核。來源可見星號不等於已核對原生 required 或所有必填處理。 |
| 送出 | `.form-row > .form-col.btn-group > button.outline-btn.submit-btn[type="submit"]`。 |

以下為已核對的一欄結構示意；佔位值不是可直接提交的正式表單，不拿此片段取代平台輸出：

```html
<div class="form-row">
  <div class="form-tag">姓名<span class="main-red">*</span></div>
  <div class="form-col">
    <div class="form-item">
      <input class="form-style" type="text" id="本案欄位識別" name="本案欄位名稱" placeholder="" aria-label="姓名">
    </div>
    <div class="form-require-alert">必填</div>
  </div>
</div>
```

來源有姓名、公司／社區名稱、所在地區、聯繫電話、聯繫信箱、服務需求、資訊來源及備註。這些是示範站欄位，不是所有案件固定欄位；欄位名稱、順序、選項、必填與驗證依本案後台設定。

表單 ID、`data-data-id`、`field_1` 等 name、欄位 ID、action 及隱藏欄位均由本案平台提供，不跨案複製示範的 `16` 或欄位編號，不保存／複製 CSRF 或其他即時 token。`data-i18n` 保留本案平台輸出，不自行偽造送出結果。

## 樣式與功能資源

來源載入：

- `vendor/page-builder/css/eforms.css`
- `vendor/page-builder/js/page-builder.js`
- `vendor/page-builder/js/eforms-validate.js`
- 頁面專屬 `page-resource/19/css` 與 `page-resource/19/js`

以上是已觀察到的資源路徑，不表示已核對每支 JS 的內部責任或所有依賴。正式案沿用本案平台載入與初始化；`19` 為來源頁面識別，不跨案寫死。不要另綁送出處理器取代原生功能。

外觀以本案 SCSS 調整，編譯後在公版樣式後載入，不直接改 vendor。保留公版結構及欄位／驗證識別，依案件調整容器、欄寬、間距、字級、色彩、邊框、按鈕及 responsive；參考站品牌介紹、電話、社群與頁面構圖不強制成為所有表單的固定版型。不要新增舊樣式 B 作為現行公版選項。

evo266200 來源沒有展示 radio、checkbox、上傳、地址、驗證碼或同意條款的實際欄位。單選與多選另依下方禾雅來源補充；上傳、地址及同意條款尚未核對，驗證碼在禾雅頁面可見但本輪未查核其結構／行為。不能僅依 `data-i18n` 的文字推定元件契約。

## 單選／多選補充來源

2026-10-15 使用者補充 [禾雅電子表單 formseries](https://www.hoya-design.com/zh-tw/forms/formseries)，作為單選與多選的結構參考；主要電子表單來源仍為前述 evo266200，不重新加入舊樣式 B。已讀取此頁實際 DOM 與載入資源，未操作選取、驗證碼、送出或後台設定。

兩者沿用 `.form-row` → `.form-tag` 與 `.form-col`；`.form-col` 內有 `.form-item` 與同層 `.form-require-alert`。選項直接放在 `.form-item` 內，每個選項以 label 包住 input 及 `span.text`：

| 類型 | 已核對結構 | 分組／提交欄位 |
|---|---|---|
| 單選 | `label.form-radio > input[type="radio"] + span.text` | 同一題共用相同 `name`（來源如 `field_32`），每個選項的 `id` 唯一，`value` 對應該選項。 |
| 多選 | `label.form-checkbox > input[type="checkbox"] + span.text` | 同一題共用帶 `[]` 的 `name`（來源如 `field_41[]`），保留陣列命名，每個選項的 `id` 唯一。 |

以下僅示意已確認的選項結構，須放在原生 `.form-item` 內，欄位識別與選項值由本案平台產生，不把示意值當正式資料：

```html
<!-- 單選：同一題共用 name -->
<label class="form-radio"><input type="radio" id="example-radio-0" name="example_radio" value="選項一"><span class="text">選項一</span></label>
<label class="form-radio"><input type="radio" id="example-radio-1" name="example_radio" value="選項二"><span class="text">選項二</span></label>

<!-- 多選：同一題共用帶 [] 的 name -->
<label class="form-checkbox"><input type="checkbox" id="example-checkbox-0" name="example_checkbox[]" value="選項一"><span class="text">選項一</span></label>
<label class="form-checkbox"><input type="checkbox" id="example-checkbox-1" name="example_checkbox[]" value="選項二"><span class="text">選項二</span></label>
```

來源單選有「裝修類型」「建物坪數」，多選有「商空營業項目」「方便聯絡時間」「期望面談時間」「如何認識我們」。欄位、必填與選項依本案設定，不複製來源表單 `29`、欄位編號或業主文案；來源中沒有星號的選填題仍存在 `.form-require-alert`，不能僅憑提示節點存在就判定為必填。

樣式沿用 `.form-radio`、`.form-checkbox`、`.text` 及原生 input，以本案 SCSS 調整；保留 label 點選與鍵盤操作、焦點及選取狀態，不改成缺少原生欄位的自製按鈕，也不另寫互斥／多選事件取代原生行為。每題的 `name`、選項 `value` 及必填檢核契約依本案平台輸出核對。

此頁同樣載入 `vendor/page-builder/css/eforms.css`、`vendor/page-builder/js/page-builder.js`、`vendor/page-builder/js/eforms-validate.js`；僅確認資源 URL，未讀取其程式全文，不據此宣稱不同站台版本完全相同。

## 校稿與交接

記錄本案來源版本、表單／欄位識別、實際資源與樣式覆寫位置。依本案授權測試必填、電話／信箱格式、選單、文字區、送出中及成功／失敗狀態與 RWD；正式送出按案件測試授權執行。未測列待驗，靜態示範不得顯示假的寄送成功。功能接入與實測狀態寫入本案唯一的工程師交接說明。
