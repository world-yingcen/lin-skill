# Blog 公版｜evo260865

2026-11-10 使用者指定：[evo260865 部落格分類頁](http://192.168.168.99/php83/sites/evo260865/public/zh-tw/post/category/post-zmnhlorm?via=81)。Blog 是系統公版，遇到 Blog／部落格／專業知識「側欄＋文章列表」版型，優先沿用此公版元件組合、HTML 層級與必要 class／data，再依案件設計修改 CSS，不另造同外觀的選單、搜尋或文章卡片結構。

本次已讀取實際前台 HTML；未執行搜尋、排序、手機下拉與後台驗收。此指定適用 Blog 內容區，不取代 LIN 已確認的 Header、Footer 等共用規範。其他分類側選單仍依 [left_menu001](evo-left-menu-reference.md)。

## 公版組合

```text
Blog 內容區
├─ 側欄
│  ├─ left_menu001
│  │  ├─ aside.tpl-leftmenu001-container[data-component="left-menu"]
│  │  │  ├─ 手機下拉按鈕與標籤
│  │  │  ├─ h2.tpl-leftmenu001-title[data-param="menu-title"]
│  │  │  └─ ul.left-menu[data-param="list"] → 分類項目及連結
│  │  └─ div.tpl-leftmenu001-bloglinks（aside 外，同一選單元件內）
│  │     └─ a.tpl-leftmenu001-link.tpl-leftmenu001-bloglink × 最新／熱門
│  ├─ search001[data-component="search"]
│  └─ hotkeywords001[data-component="hot-keywords"]
└─ div[data-list-group-container="true"]
   └─ bloglist001[data-component="blog-list"][data-bloglist001="true"]
      └─ div.bloglist001__grid[data-page-size] → a.bloglist001__card
```

此圖表示功能層級，不要求複製來源的冗餘外框、隨機實例識別或客戶內容。實際工程仍須核對本案平台輸出與匯入契約。

## 側選單與最新／熱門入口

- 分類使用 left_menu001 的標準層級、data-param、狀態 class 與原生手機下拉；來源的 aside 設定為 `data-show-title="true"`、`data-show-l2="true"`、`data-collapsible="false"`，不要直接把其他產品範本的 collapsible=true 套過來。此屬性不代表可刪除手機下拉結構。
- 最新／熱門入口位於 `.tpl-leftmenu001-bloglinks`，在分類 aside 外、選單元件內；不能塞進分類清單偽裝成後台分類，也不另寫一套排序按鈕。
- 原站路由為 `/post/latest?via=81`、`/post/hot?via=81`；這是來源站的實例，正式案使用本案路由與參數，不照抄 via=81、不自行改成 `?sort=new`／`?sort=hot` 當作平台已支援。
- 「所有文章」如案件需要，依本案公版輸出及實際入口設定；不能憑截圖推定原站就有此節點。單層導覽也沿用系統結構。

## 搜尋與熱門關鍵字

- 搜尋使用 `.tpl-search001[data-template-id="search001"][data-component="search"]`，內含 `form.search001-form[role="search"][data-param="form"]`，保留 field／label、`input.search001-input[data-param="keyword"][name="keyword"]`、submit 與平台設定。原站是 GET、scope=global；不能因放在 Blog 側欄就宣稱只搜尋文章。
- 熱門關鍵字使用 hotkeywords001，保留 section、標題、清單、項目、連結與文字層級，以及 data-source、data-limit 等配置；原站關鍵字連到搜尋網址，不能擅自換成自訂 tag 篩選並宣稱串接完成。
- 搜尋與熱門關鍵字是 left_menu001 外的獨立元件，不塞入 `.left-menu`／`.left-submenu`。這是系統搜尋表單，依 search001 契約，不誤套聯絡表單的 contact-form 結構。

## 文章列表

保留 `.tpl-bloglist001`、`data-template-id="bloglist001"`、`data-component="blog-list"`、`data-bloglist001="true"` 與 `.bloglist001__grid[data-page-size]`。來源卡片層級：

```html
<a href="本案文章網址" class="bloglist001__card">
  <div class="bloglist001__img-wrap">
    <img class="bloglist001__img" src="本案圖片" alt="本案圖片說明" loading="lazy">
  </div>
  <div class="bloglist001__body">
    <span class="bloglist001__category">分類名稱</span>
    <h3 class="bloglist001__card-title">文章標題</h3>
    <p class="bloglist001__desc">文章摘要</p>
    <div class="bloglist001__keywords">
      <span class="bloglist001__keyword">關鍵字</span>
    </div>
  </div>
</a>
```

整張卡片是連結，內部分類與關鍵字為 span，不在 a 裡再塞 a／button。這是 Blog 公版卡片，不能誤套一般 CTA 的 btn-group 結構。頁面標題層級與公版有衝突時核對整頁結構，不為字級改標籤。每頁筆數、文章資料、圖片及網址依本案平台提供；無法從此頁確認的分頁輸出，取得本案公版後再接，不自行捏造範本名稱或資料標記。

來源主列表外框實際只有 `data-list-group-container="true"`，沒有 data-replace。若本案內容頁需要沿用列表外框，另依 [替換範圍規範](shared-page-rules.md#列表頁與內容頁的替換範圍) 與當次平台契約確認 `data-replace="detail-content"`，不能把來源未出現的屬性說成已查到。

## 樣式與驗收

沿用本案 Common 與品牌值，使用既有 Blog SCSS 集中調整欄寬、間距、字型、圖片比例、卡片與側欄外觀。系統樣式先載入，案件 CSS 後載入；不改 vendor、不以 !important 掩蓋問題、不另綁搜尋／排序／手機選單 JS。

核對桌機與手機結構、分類選取、最新／熱門入口、搜尋範圍、熱門關鍵字目標、文章卡片與分頁；發布前台及後台可編輯狀態分開驗證。缺契約時列明具體缺口，不用自造 DOM 或假資料功能宣稱完成。
