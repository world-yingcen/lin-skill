# EVO 電子表單｜evo266125 contact-form 公版

使用者於 2026-11-04 指定 [evo266125 聯絡我們頁](http://192.168.168.99/php83/sites/evo266125/public/zh-tw/post/contact?via=8) 的 `.contact-form` 為所有電子表單公版。只要頁面出現表單，不限聯絡我們、詢問、報名或其他用途，都沿用本文件的 HTML 層級、標籤、class、data、驗證與送出結構；**只有 CSS／SCSS 外觀可以依案件修改**，不自造另一套表單 DOM 或 JavaScript。

## 來源與驗證範圍

2026-11-04 已唯讀取得指定頁面的前台 HTML，核對 `.contact-form`、`form.eforms-wrapper`、隱藏欄位、單選、文字輸入、多行文字、驗證碼及送出按鈕。頁面載入平台 `eforms.css`、`page-builder.js` 與 `eforms-validate.js`。本次未送出正式表單、未操作錯誤狀態，也未驗證後台編輯、儲存、發布及所有 RWD；不能把原始碼核對當成功送件驗收。

內網網址只用來確認公版，不是其他案件的正式路由。表單 ID、action、token、locale、來源識別、欄位編號、選項與驗證資料均由本案平台提供，不複製來源表單 `20` 或任何即時值。

## 固定結構

| 部位 | 必須保留 |
|---|---|
| 表單外層 | `div.contact-form[data-rendered-component="form"][data-data-id]` |
| 表單根節點 | `form.eforms-wrapper` 及平台輸出的 action、method、ID、`data-data-id`、`data-i18n`、`novalidate`、`enctype` |
| 系統資料 | 表單內由平台輸出的 `_form_token`、`data_id`、`locale`、`_source` 等 hidden input |
| 每一欄 | `.form-row` 直接包含 `.form-tag` 與 `.form-col` |
| 欄位內容 | `.form-col` 內為 `.form-item` 與同層 `.form-require-alert` |
| 必填標示 | `.form-tag` 文字後的 `.main-red`；必填判定仍以本案平台設定與驗證為準 |
| 一般控制項 | `input.form-style`、`textarea.form-style`，保留平台輸出的 id、name、aria-label、placeholder、長度及 `data-validate` |
| 單選 | `label.form-radio > input[type="radio"] + span.text`，同題共用 name、各選項 ID 唯一 |
| 驗證碼 | `.form-item.captcha-col` 內依序為 `input.form-style` 與 `img.captcha-img[data-captcha-refresh]` |
| 送出 | `.form-row > .form-col.btn-group > button.outline-btn.submit-btn[type="submit"]` |

- 不把 `.form-tag` 換成自訂標題容器，不移除 `.form-col`、`.form-item` 或 `.form-require-alert`，也不增加會改變平台直系層級的 wrapper。
- `.form-require-alert` 可能存在於選填欄位，不能只看這個節點判定必填；依 `.main-red`、平台設定與實際驗證結果核對。
- 電話與 Email 來源使用 `input[type="text"]` 搭配 `data-validate="phone"`／`data-validate="email"`，不自行改成另一套驗證或另綁 submit handler。
- 欄位名稱、順序、選項與必填狀態依本案需求由平台設定；可以改資料內容，不能改平台輸出的結構格式。

## 公版 HTML 形狀

以下以佔位值說明固定層級。正式案必須使用本案平台實際輸出，不直接複製示例 ID、token、action 或欄位編號。

```html
<div data-rendered-component="form" data-data-id="本案表單ID" class="contact-form">
  <form
    action="本案平台送出網址"
    method="POST"
    id="form-本案表單ID"
    class="eforms-wrapper"
    data-data-id="本案表單ID"
    data-i18n="本案平台輸出"
    novalidate="novalidate"
    enctype="multipart/form-data"
  >
    <!-- 以下 hidden input 均由本案平台輸出 -->
    <input type="hidden" name="_form_token" value="本案即時 token">
    <input type="hidden" name="data_id" value="本案表單ID">
    <input type="hidden" name="locale" value="本案語系">
    <input type="hidden" name="_source" value="本案來源識別">

    <div class="form-row">
      <div class="form-tag">單選題<span class="main-red">*</span></div>
      <div class="form-col">
        <div class="form-item">
          <label class="form-radio">
            <input type="radio" id="本案選項ID-0" name="本案欄位名稱" value="選項一">
            <span class="text">選項一</span>
          </label>
          <label class="form-radio">
            <input type="radio" id="本案選項ID-1" name="本案欄位名稱" value="選項二">
            <span class="text">選項二</span>
          </label>
        </div>
        <div class="form-require-alert">必填</div>
      </div>
    </div>

    <div class="form-row">
      <div class="form-tag">姓名<span class="main-red">*</span></div>
      <div class="form-col">
        <div class="form-item">
          <input class="form-style" type="text" id="本案欄位ID" name="本案欄位名稱" placeholder="" aria-label="姓名">
        </div>
        <div class="form-require-alert">必填</div>
      </div>
    </div>

    <div class="form-row">
      <div class="form-tag">電話</div>
      <div class="form-col">
        <div class="form-item">
          <input class="form-style" type="text" id="本案電話ID" name="本案電話欄位" placeholder="" aria-label="電話" data-validate="phone">
        </div>
        <div class="form-require-alert">必填</div>
      </div>
    </div>

    <div class="form-row">
      <div class="form-tag">Email<span class="main-red">*</span></div>
      <div class="form-col">
        <div class="form-item">
          <input class="form-style" type="text" id="本案信箱ID" name="本案信箱欄位" placeholder="" aria-label="Email" data-validate="email">
        </div>
        <div class="form-require-alert">必填</div>
      </div>
    </div>

    <div class="form-row">
      <div class="form-tag">內容<span class="main-red">*</span></div>
      <div class="form-col">
        <div class="form-item">
          <textarea class="form-style" id="本案內容ID" name="本案內容欄位" placeholder="" aria-label="內容" rows="5"></textarea>
        </div>
        <div class="form-require-alert">必填</div>
      </div>
    </div>

    <div class="form-row">
      <div class="form-tag">驗證碼<span class="main-red">*</span></div>
      <div class="form-col">
        <div class="form-item captcha-col">
          <input class="form-style" type="text" id="本案驗證碼ID" name="本案驗證碼欄位" placeholder="請輸入驗證碼" aria-label="驗證碼" autocomplete="off">
          <img src="本案驗證碼網址" alt="驗證碼" class="captcha-img" data-captcha-refresh title="點擊重新整理">
        </div>
        <div class="form-require-alert">必填</div>
      </div>
    </div>

    <div class="form-row">
      <div class="form-col btn-group">
        <button type="submit" class="outline-btn submit-btn">送出</button>
      </div>
    </div>
  </form>
</div>
```

## 其他欄位類型

公版來源已確認 radio；checkbox、select、upload、地址、同意條款及 reCAPTCHA 若本案有使用，必須沿用同一平台實際輸出的 eforms 結構與驗證標記，不能從 `data-i18n` 猜 DOM，也不能為了符合設計稿改成自製按鈕、假下拉或另一套上傳元件。取得本案輸出後再補樣式；缺少實際結構時列待工程師確認。

詢問車頁內的表單仍由詢問車契約管理，但其中電子表單欄位不得另造與 eforms 不同的層級；有衝突時對照 [系統公版詢問車](evo-inquiry-cart-reference.md) 列出差異，不自行改 vendor HTML／JS。

## 唯一可調整範圍：樣式

- 保留平台 `vendor/page-builder/css/eforms.css`、`page-builder.js` 與 `eforms-validate.js`；不直接修改 vendor，不另綁送出、驗證、驗證碼刷新或成功訊息流程。
- 案件 CSS／SCSS 在公版樣式後載入，只調整寬度、排列、間距、字型、字級、色彩、背景、邊框、圓角、按鈕與 responsive；優先使用本案 `:root` 變數，避免重複宣告品牌值。
- 樣式 selector 以 `.contact-form` 或本頁範圍收斂，避免影響詢問車、會員或其他系統表單；不得為了 CSS 方便修改 HTML 層級或新增無意義 wrapper。
- 保留 label 點選、鍵盤焦點、錯誤文字、送出中、成功／失敗、disabled、captcha 更新及長內容狀態。hover 只套可 hover 裝置，觸控與鍵盤狀態放在外面。

## 校稿與交接

逐層核對 `.contact-form > form.eforms-wrapper`、hidden input、每個 `.form-row`、欄位識別、驗證標記、captcha 與送出按鈕；確認只改樣式，沒有自訂 DOM 或第二套 JavaScript。依本案授權測試必填、電話／Email、選項、文字區、驗證碼、送出中、成功／失敗、鍵盤操作及 RWD。正式送出需有測試授權；未測項目、後台編輯／儲存／發布狀態分開記錄到工程師交接說明。
