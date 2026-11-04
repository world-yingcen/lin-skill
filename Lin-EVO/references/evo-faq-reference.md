# FAQ 統一系統結構｜tpl-faq001

使用者於 2026-11-04 指定 [evo266125 常見問題](http://192.168.168.99/php83/sites/evo266125/public/zh-tw/post/faqs?via=7) 為 FAQ 系統範本。凡 Lin-EVO 製作或修改 FAQ，統一沿用下列 HTML 層級、標籤、必要 class 與 data 屬性；CSS／SCSS 外觀可依案件自由調整，不另做自訂 accordion 結構。此規則取代舊禾雅參考作為目前的結構依據，不限於舊平台流程；不因此批次重寫本輪範圍外的既有頁面。

## 來源與驗證範圍

2026-11-04 已唯讀取得指定網址的前台 HTML：`tpl-faq001` 外層內是 `div[data-faq001="true"]`，其直接子層為逐題 `details`，沒有舊範例的空 `title-block`。每題包含 `summary > span` 及答案 `div`，第一題帶 `open`，並有平台輸出的 FAQPage JSON-LD。本次核對 HTML 結構，未執行瀏覽器互動或後台匯入驗收。

## HTML 結構範例

以下使用示例文案；實作時填入本案真實問答。平台實例 ID 與實例 class 由本案平台提供；保留本案既有值，不複製來源的 `data-instance-id="impfq1"`／`faq001-impfq1` 或客戶文案，也不自行編造實例識別。

```html
<div data-schema="FAQPage" data-schema-collection="mainEntity" data-template-id="faq001" class="tpl-model tpl-faq001 template-wrapper">
  <div data-faq001="true" class="tpl-container card-area">
    <details data-schema-item="Question" class="tpl-faq001-card-box card-box" open>
      <summary class="tpl-faq001-card-title card-title">
        <span data-schema-prop="name" class="tpl-faq001-card-title-text card-title-text">第一題問題</span>
      </summary>
      <div data-schema-prop="acceptedAnswer.text" data-schema-prop-type="Answer" class="tpl-faq001-card-description card-description">
        <p>第一題答案。</p>
      </div>
    </details>
    <details data-schema-item="Question" class="tpl-faq001-card-box card-box">
      <summary class="tpl-faq001-card-title card-title">
        <span data-schema-prop="name" class="tpl-faq001-card-title-text card-title-text">第二題問題</span>
      </summary>
      <div data-schema-prop="acceptedAnswer.text" data-schema-prop-type="Answer" class="tpl-faq001-card-description card-description">
        <p>第二題答案。</p>
      </div>
    </details>
  </div>
</div>
```

- 第一題預設 `open`，其餘收合；本案另有明確指定才改預設狀態。
- 使用 `summary` 作為操作入口、`details[open]` 作為狀態依據，不改成 div click 或自製按鈕收合，也不額外疊一套 open class。
- 來源 HTML 沒有共用 `name` 群組，不自行加入只能開一題的互斥行為。問題與答案保留在 HTML，不把問答搬到 JS 陣列。
- `summary` 裡的 span 是範本原有結構，不受自訂 button 純文字規則限制。保留必要 class／data 屬性，答案按已確認文案保留段落與連結。

## 結構固定、樣式可調

- 保留外層 `data-template-id="faq001"`、`data-schema="FAQPage"`、`data-schema-collection="mainEntity"` 與 `template-wrapper tpl-model tpl-faq001`。
- 保留 `data-faq001`、逐題 `Question`、問題 `name`、答案 `acceptedAnswer.text`／`Answer`，以及範例中各層 class。不改成自訂 `designer-tpl-*` FAQ 取代系統元件。
- 保持 `details > summary > span` 與答案 div 的層級及順序。問題文字填在既有 span，答案內容填在既有答案容器；可依本案增減題數、填入真實段落與連結，不為標題層級規則擅自把問題 span 換成 h2／h3，或插入新的收合按鈕與包覆層。
- 字型、字級、色彩、背景、邊框、圓角、留白、寬度、RWD 與展開指示圖示均可用 CSS／SCSS 調整。Q 標記不是固定視覺要求；需要裝飾或圖示時優先使用既有元素的偽元素，不改系統 HTML。
- 收合使用原生 `details[open]` 狀態，不以自訂 click／open class 另寫一套。保留鍵盤焦點、長答案完整顯示與減少動態模式；過場依案件瀏覽器支援設定，不支援時仍可正常展開閱讀。AOS 只處理區塊進場，不接管答案收合。
- 整站 HTML 匯入仍核對當次工程師套件的接入方式；若套件與本指定結構有實際衝突，保留範本，列出衝突交工程師確認，不靜默改成另一套 HTML，也不自行新增未支援的匯入標記。

## 結構化資料與驗收

正式 EVO 沿用平台產生的 FAQPage JSON-LD，避免重複輸出；靜態交付如需 JSON-LD，必須與可見問答一致，不能只靠 data 屬性宣稱已完成，也不複製來源站的問題與答案。

交付前核對 HTML 層級、class、data 屬性及本案實例識別，再實測滑鼠與 Enter／Space 收合、第一題初始狀態、多題展開、長答案、答案連結、焦點可見、減少動態及案件要求的 RWD。分別記錄靜態操作、後台編輯與發布後結果；未測部分標待驗。
