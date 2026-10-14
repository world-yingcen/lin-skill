# FAQ 指定寫法｜tpl-faq001

使用者於 2026-10-05 指定 FAQ 參照 [禾雅服務相關問題](https://www.hoya-design.com/zh-tw/post/post-puqxkg2k?via=95) 的 `tpl-faq001`。製作 FAQ 時沿用原生 `details / summary`、既有 class、data 屬性與 Q 標記的做法，依本案調整內容與品牌樣式。

## 來源與驗證範圍

已核對參考頁 HTML、[頁面元件 CSS](https://www.hoya-design.com/page-resource/19/css?scope=own) 與後載入的 [共用 CSS](https://www.hoya-design.com/css/evomni-root.css)。頁面載入的 page-resource/117/js 與 page-resource/19/js 未查得 faq001 專用程式；基本收合由原生元素提供，不因此推定所有平台腳本均未介入。本次未進行瀏覽器操作驗收。

## HTML 結構範例

以下使用示例文案；實作時填入本案真實問答。平台實例 ID 與實例 class 由本案提供，不複製來源的 jtrnu、隨機 ID 或客戶內容。

```html
<div data-schema="FAQPage" data-schema-collection="mainEntity" data-template-id="faq001" class="tpl-model tpl-faq001 template-wrapper">
  <div data-faq001="true" class="tpl-container card-area">
    <div class="title-block"></div>
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

## 樣式與收合

每題有底部分隔線；標題以 padding 留出左側圓形 Q 標記的位置，`summary::marker` 隱藏原生符號。Q 與圓形背景由 `.card-title::before`／`::after` 呈現，並保留實際問題文字在 HTML。

後載入的共用樣式將問題字級設為 `--FontSizeItemTitle`、字重 500、文字色 `--TextColorPrimary`，分隔線採 `--BorderColorPrimary`；`details[open]` 的 Q 標記使用 `--ColorPrimary` 與白字。樣式集中在本案共用 FAQ／內頁 SCSS，沿用上述角色並依本案品牌調整。

來源 CSS 使用 `::details-content` 的 opacity／block-size 過場，搭配 `content-visibility`、`allow-discrete`；答案另有 padding／max-height 的 0.5 秒過場及展開 max-height 3000px。這些是來源實作，不是所有瀏覽器均已驗證的保證。使用時核對本案瀏覽器支援；不支援動畫時保留原生正常收合，長答案不得因固定高度被裁切。減少動態模式停用收合過場，資訊及操作仍完整。

FAQ 收合是元件狀態過場，沿用此原生機制；AOS 只負責 FAQ 整區進場時的淡入淡出，不控制答案收合。若新增 hover 樣式，依 T08 包在元素內的 `@media (hover: hover) and (pointer: fine)`；鍵盤焦點樣式放外面並保持可見。

## 結構化資料與驗收

來源保留 `FAQPage`、`Question`、`acceptedAnswer.text` 的 data-schema 契約，並輸出 FAQPage JSON-LD。正式 EVO 沿用平台輸出，避免另加重複資料；靜態交付如需 JSON-LD，必須與可見問答一致，不能只靠 data 屬性宣稱結構化資料已完成，也不複製他案答案或費用。

交付前實測滑鼠與 Enter／Space 開關、第一題初始狀態、多題展開、長答案、答案連結、焦點可見、減少動態及本案瀏覽器相容性。紀錄前端操作與平台／結構化資料驗證的實際範圍；本參考不自動啟動 RWD 或其他頁面製作。
