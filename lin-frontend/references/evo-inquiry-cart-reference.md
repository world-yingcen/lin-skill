# EVO 公版詢問車｜功能架構不可改

使用者於 2026-10-14 指定依照 [evo265987 產品頁](http://192.168.168.99/php83/sites/evo265987/public/zh-tw/product/product-ug8q44d1?via=24)，並明確確認：**詢問車是系統公版功能，改不了。** 有詢問需求的案件沿用原生功能架構，不由 AI 重做；本規範不表示所有無產品／無詢問需求的網站都要啟用。

## 已核對來源與範圍

已讀取產品 HTML、Header 詢問清單、[詢問確認頁](http://192.168.168.99/php83/sites/evo265987/public/zh-tw/inquiry-cart)，以及 `vendor/page-builder/js/page-builder.js`、`vendor/form-inquiry/js/query_form.js`。瀏覽器已查看側欄開啟、確認頁導航及既有清單項目／數量控制／聯絡欄位；未操作加入、數量變更、移除、驗證碼或送出，不宣稱這些流程已實測通過。

## 固定功能流程

產品頁「加入詢問單」 → 全站 Header 的詢問清單入口／數量 badge → 側欄列商品與數量、提供移除與「確認詢問內容」 → 本案 inquiry-cart 確認頁 → 清單數量／移除及聯絡表單 → 系統檢核與送出結果。

不得改成直接跳聯絡頁、付款／結帳、其他步驟或另外建立一套車；不把詢問車誤當購物車交易功能。同商品／規格如何合併、數量上下限與送出結果均依本案系統契約，不憑畫面猜規則。

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

- 詢問側欄與加入／移除由原生 page-builder handlers 與 Header 元件協作；確認頁使用系統 `query_form.js`、`query_form.css` 及既有表單管線。沿用平台載入與初始化，不再綁同一按鈕、另寫 API 或自製 localStorage／JS 商品陣列車。
- 已核對確認頁數量／移除會呼叫系統詢問車 API，送出由既有表單處理，query_form 監聽平台 `evo:form-submitted`／`evo:form-error`。這是來源紀錄，不授權 AI 重寫請求或偽造成功事件；本案仍須工程師核對版本及正式路由。
- 欄位、狀態保存、跨頁同步、規格必填、重複加入、成功／失敗／清單清空等依系統處理；不以本地畫面變更冒充伺服器成功。沒有本案正式契約時標待確認，不推定所有版本完全相同。
- 功能流程、DOM 層級、必要 class／data、欄位識別、API／驗證與系統 JS 不改。僅可使用平台確認可調的外觀變數／設定；未確認前不重新排版、隱藏操作、換元件或改 CSS selector，也不提出需要改公版功能才能實現的設計。
- 靜態切版展示沿用完整公版結構與必要狀態，示範與正式系統接入分開記錄；缺公版素材／本案契約就列缺口，不把示範資料改成另一套正式詢問車。

## 校稿與工程師交接

本案啟用詢問車時，頁面清單須涵蓋產品加入入口、全站 Header 側欄與確認頁；依授權尺寸核對原生開關、badge／筆數、商品連結、數量／移除、空清單、必填／Email／驗證碼與錯誤提示，確認缺載入、重複初始化與被樣式遮住的控制項。核對本案實際系統行為，不只確認按鈕存在。

本輪只修改規範不送出正式詢問、不代填個資或解驗證碼。案件的正式流程測試依該案授權與測試環境執行；未測就列待驗。公版輸出與 LIN 的標題／語意或其他規則衝突時記錄具體問題並交工程師，不擅改不可編輯的系統輸出，也不將問題標成已修正。

`工程師交接說明.md` 必須記元件來源／版本、本案路由與 ID 對應來源、欄位設定、原生 JS／CSS 載入責任、可調外觀的核准範圍、靜態與正式實測狀態及待驗事項。系統公版不可改的界線須明列，避免工程師接手才發現設計需要重做功能。
