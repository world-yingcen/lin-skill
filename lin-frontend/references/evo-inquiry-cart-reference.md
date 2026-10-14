# EVO 公版詢問車｜CSS 可調，HTML／JS 不改

使用者於 2026-10-14 指定依照 [evo265987 產品頁](http://192.168.168.99/php83/sites/evo265987/public/zh-tw/product/product-ug8q44d1?via=24)，並明確確認：**詢問車頁／抽屜的公版 CSS 可以依案件調整；公版 HTML、JS 不可修改。產品頁的排版 HTML 不在此限制內，可以新增 `.inquiry-group`。** 有詢問需求的案件沿用原生功能架構，不由 AI 重做；本規範不表示所有無產品／無詢問需求的網站都要啟用。

## 已核對來源與範圍

已讀取產品 HTML、Header 詢問清單、[詢問確認頁](http://192.168.168.99/php83/sites/evo265987/public/zh-tw/inquiry-cart)，以及 `vendor/page-builder/js/page-builder.js`、`vendor/form-inquiry/js/query_form.js`。瀏覽器已查看側欄開啟、確認頁導航及既有清單項目／數量控制／聯絡欄位；未操作加入、數量變更、移除、驗證碼或送出，不宣稱這些流程已實測通過。

## 固定功能流程

產品頁「加入詢問單」 → 全站 Header 的詢問清單入口／數量 badge → 側欄列商品與數量、提供移除與「確認詢問內容」 → 本案 inquiry-cart 確認頁 → 清單數量／移除及聯絡表單 → 系統檢核與送出結果。

正式版不得改成直接跳聯絡頁、付款／結帳、其他步驟或另外建立一套車；不把詢問車誤當購物車交易功能。同商品／規格如何合併、數量上下限與送出結果均依本案系統契約，不憑畫面猜規則。

## 必須保留的元件與資料契約

| 部位 | 已核對的系統識別／結構 |
|---|---|
| 產品加入按鈕 | 原生 product-detail 元件的 `data-pdbtn="ask"`、`data-param="inquiry-add"`、`data-product-id`、平台 i18n／轉譯標記與必要子元素。商品 ID 由本案平台提供，不複製參考站的 16。 |
| Header 詢問入口 | `data-template-id="header_query"`、`data-component="query"`、`.tpl-header_query.header-query-block`、`data-confirm-url`、`.js-query-count`；保留 toggle、panel、overlay、title、close、confirm 的 data-param。 |
| 側欄清單 | `.query-panel`、`.query-panel__drawer`、header／body／footer、`.query-list.js-query-list` 與系統填入的商品／數量／移除控制。保留 dialog 的 aria 與開關狀態，不另建自製彈窗取代。 |
| 確認頁 | 本案語系路由 `/{locale}/inquiry-cart`；`.query-form`、`.query-form__container`、header／grid、`.query-list`、`.query-contact` 及既有 h1／h2 結構。 |
| 商品項目與數量 | `.js-item-count`、`.query-list__items.js-items`、`.query-card[data-item-id]`、`.js-remove-item`、`.js-qty-decrease`／`.js-qty-increase`／`.js-qty-input`。清單項目 ID 與商品 ID 是不同識別，不互換；數量上下限由 `.query-form[data-min-qty][data-max-qty]` 的後端設定提供，不寫死範例值。 |
| 空清單 | `.query-list__empty` 與其系統空狀態；清單／筆數與聯絡表單行為保留原生邏輯，不自行補假商品或改送出規則。 |
| 聯絡表單 | `#inquiry-form[data-component="form"]`、系統 action／method／enctype、locale、CSRF、`.eforms-wrapper` 及欄位／驗證契約。參考有姓名、電話、Email、備註、驗證碼與送出；本案欄位及 form_data 識別由後台設定，不複製參考的欄位編號。 |
| 驗證碼 | 系統圖片端點、`.captcha-img[data-captcha-refresh]` 與欄位檢核，沿用平台生成與更新；不自造驗證碼或略過驗證。 |

上述 class 中的 header 是名稱，不使用 `<header>` 重建側欄或表單標題；保留原生容器。平台生成的實例 class、media／item ID、內網網址、session／CSRF 即時值均不得跨案複製。

## 系統接入責任，不另寫功能

- 詢問側欄與加入／移除由原生 page-builder handlers 與 Header 元件協作；確認頁使用系統 `query_form.js`、`query_form.css` 及既有表單管線。正式版沿用平台載入與初始化，不再綁同一按鈕、另寫 API 或自製 localStorage／JS 商品陣列車。使用者要求的獨立靜態 Demo 依下節處理。
- 已核對確認頁數量／移除會呼叫系統詢問車 API，送出由既有表單處理，query_form 監聽平台 `evo:form-submitted`／`evo:form-error`。這是來源紀錄，不授權 AI 重寫請求或偽造成功事件；本案仍須工程師核對版本及正式路由。
- 欄位、狀態保存、跨頁同步、規格必填、重複加入、成功／失敗／清單清空等依系統處理；不以本地畫面變更冒充伺服器成功。沒有本案正式契約時標待確認，不推定所有版本完全相同。
- 詢問車頁／抽屜的公版 HTML 與 JS 不改：不新增其內部 wrapper、搬移其內部按鈕、改 DOM／class／data／欄位識別、重寫事件、API 或驗證。案件可以用 CSS 調容器、字級、間距、顏色、按鈕外觀、RWD 與疊層；保留原生選擇器及操作可用性，案件 SCSS 編譯後在公版 CSS 後載入，不直接改 vendor 原始檔。CSS 做不到的需求列工程師待處理，不用 JS 搬 DOM 規避限制。
- 靜態切版展示保留公版結構與必要狀態；示範與正式系統接入分開記錄，缺公版素材／本案契約就列缺口。公版 HTML／JS 的不可修改界線也適用於 Demo，模擬程式另放。

## 靜態 Demo 與正式版

使用者要求 Demo 時，可以用獨立、僅供預覽的程式模擬加入、跨頁保存、數量、移除及表單操作；示範資料使用獨立命名，不冒充平台正式 ID，不呼叫正式詢問 API、不寄出詢問。模擬程式不得回寫公版 HTML／JS 原始檔，也不能和原生處理器同時綁定同一操作；缺少可隔離的預覽環境時先列缺口。

正式接入前停用並排除 Demo 程式與示範資料，回到平台原生功能；交接須明列模擬檔案、載入位置、停用方式及尚未正式驗證的功能。若專案有產頁腳本，每次修改同步腳本與唯一的 `工程師交接說明.md`，避免重產頁面後覆蓋修正。

## 案件外觀與工程師待處理項目

- Header 的「立即購買」按鈕依案件要求，可用頁面範圍內的 CSS 在產品內頁與詢問車頁隱藏，包含手機置底版本；分類／列表保留。確認 `.header-btn-link` 確實是該購買按鈕，避免誤隱藏詢問入口或其他導覽。
- 「加入詢問單」視覺上應與購買按鈕分組，位於商品資訊底部。切版端可以在產品頁新增獨立 `.inquiry-group` div，放在購買按鈕群下方、商品資訊區最下面，不必交工程師。保留按鈕的原生 class／data、平台資料與加入事件，不改詢問車頁或抽屜本體。
- 加入成功沿用原生 `EvomniAlert`，訊息「已加入詢問單」，已核對來源的加入成功提示為 4 秒自動關閉；不自製 toast，也不將所有提示時間一律改為 4 秒。
- 抽屜不得被 Cookie 提示或 Footer 遮住。優先檢查 CSS 的疊層與父層 stacking context，必要時利用既有開啟狀態做樣式調整；不重設 Cookie 同意狀態。若需求需要新增 JS 才能實現，列工程師待處理。
- 抽屜聚焦造成橫向捲動／抖動時，交接建議工程師評估 `focus({ preventScroll: true })`。這是系統 JS 待修建議，切版端不得自行修改，也不得標為已修正。
- 詢問頁容器與字級沿用案件既有設定，以既有根元素限定 CSS；不得為套樣式新增原生 HTML 的 class 或 wrapper。副標「請填寫以下資訊，我們將儘快為您服務。」、驗證碼 placeholder「請輸入驗證碼」、送出「送出」是此案指定文案，透過平台可編輯設定處理；無設定入口時交工程師，不硬改公版 HTML／JS。

以下是已確認案件的外觀範例，可由各案指定覆蓋，不能當作所有案件的固定值：`container-75` 的容器寬度、主標 `FontSizePrimary × 0.93`、區段標題 `FontSizeItemTitle × 1.15`、商品名稱 `FontSizeItemTitle`、說明／欄位／數量 `FontSizeBody`。未有原生 `container-75` class 時，用既有容器的 CSS 套用相同寬度。

```css
/* 此案外觀範例；.inquiry-page 須為既有頁面範圍，否則換成既有根選擇器。 */
.inquiry-page .query-form { margin-bottom: clamp(64px, 6.67vw, 128px); }
.inquiry-page .eforms-wrapper { background: #f4f4f4; padding: var(--Space3); }
.inquiry-page .eforms-wrapper .form-style { background-color: #fff; }
.inquiry-page .eforms-wrapper .form-col { width: 100%; }
```

## 校稿與工程師交接

本案啟用詢問車時，頁面清單須涵蓋產品加入入口、全站 Header 側欄與確認頁；依授權尺寸核對原生開關、badge／筆數、商品連結、數量／移除、空清單、必填／Email／驗證碼與錯誤提示，確認缺載入、重複初始化與被樣式遮住的控制項。核對本案實際系統行為，不只確認按鈕存在。

規範來源查核不代表已送出正式詢問。案件的正式流程測試依該案授權與測試環境執行；未測就列待驗。公版輸出與 LIN 的標題／語意或其他規則衝突時記錄具體問題並交工程師，不擅改不可編輯的系統輸出，也不將問題標成已修正。

`工程師交接說明.md` 必須記元件來源／版本、本案路由與 ID 對應來源、欄位設定、原生 JS／CSS 載入責任、案件 CSS 調整範圍、靜態與正式實測狀態及待驗事項。CSS 可調、HTML／JS 不改的界線須明列，避免工程師接手才發現設計需要重做功能。
