# EVO Header 唯一基底｜evo266200

2026-11-04 使用者最新指定：**Header 的 HTML 結構與全部預設樣式，直接使用 [evo266200 前台](http://192.168.168.99/php83/sites/evo266200/public/zh-tw) 作為基底，再依案件修改。包含 Header 跟隨按鈕，不再混用 evo266125 的 Header／按鈕預設。** 此指示取代先前保留 evo266125 按鈕尺寸、圖示與 padding 的規則；一般內文按鈕、FAQ 與側選單仍依各自規範。

## 內附來源與開始方式

- [Header 結構基底](../assets/header-evo266200/header.html)：以此結構建立案件 Header，保留 Logo、nav003、漢堡、跟隨按鈕、搜尋與語系的層級及必要 class／data。
- [系統元件 CSS](../assets/header-evo266200/system.css) 與[案件共用 CSS](../assets/header-evo266200/site.css)：原始查核快照，包含非 Header 內容，不整份載入客戶案件，也不在案件再次疊加兩套元件 CSS。
- [可編譯 Header 基底](../assets/evo-starter/06-切版/scss/_header.scss)：依來源的系統元件 → 案件覆寫順序整理 Header 相關樣式，保留狀態及 media 條件；完整 SCSS 收在單一 `.header` 巢狀作用域，以 `&`／`:where(&)` 保留原本選擇器權重。反整理自編譯 CSS 的 `text-decoration`、`white-space`、`transition` 使用標準 shorthand，不保留瀏覽器展開式 longhand。已移除 !important、補齊 var() 備用值，通用選擇器限於 Header，避免影響內文按鈕。全站品牌色、按鈕、文字、版心與間距變數只由 Common 管理；`.header` 只定義 Navi 專用變數，不再用同名區域變數蓋過 Common。
- [來源紀錄](../assets/header-evo266200/SOURCE.json)：來源日期與檔案雜湊。這些是實際前台 HTML 與編譯 CSS，不宣稱取得工程師原始 SCSS。

先讀內附 HTML 與 `_header.scss`，建立案件共用 Header，再替換本案 Logo、文字、分類、連結、語系及搜尋目標。HTML 基底已將 data-rwdpointer 改為 1199；原始 CSS 快照仍保留來源的 1512／1200 門檻，只供查核，不可直接載入而蓋回舊斷點。快照保留他案資料供核對，**不是可原封發布的案件成品**；不得帶入原站站號、via 值、media ID、隨機實例 class 或品牌素材。必要實例識別依本案系統生成，不隨意刪除既有有效識別。

基底包含 Header 系統樣式，靜態案可配合 Common 編譯使用；正式 EVO 已載入系統樣式時，先核對本案版本，避免重複載入或以舊快照覆蓋新版元件。此 CSS 快照不含互動程式；沿用本案工程師提供的 nav003、搜尋與語系初始化，不把 HTML／CSS 複製完成當成互動已完成。整站匯入契約有差異時列明並依工程師契約接入，不另造資料綁定。

## 結構與識別

```text
header.header
├─ .tpl-header-logo → a.logo-link → img.img-responsive
├─ .tpl-nav003 [data-template-id="nav003"] [data-rwdpointer="1199"]
│  ├─ nav.tpl-nav003-nav [data-component="web-menu"] [data-menu-key="main"]
│  │  └─ ul.nav-menu → li.nav-item → a.nav-link
│  │     └─ 有子分類：li.has-child → ul.sub-menu
│  └─ button.tpl-nav003-toggle-menu-btn → span.menu-bar × 3
├─ .tpl-model.tpl-header-btn-box.btn-group
│  └─ .btn-item → a.header-btn-link.btn-link.main-btn
│     ├─ div.tpl-header-btn-box001-btn-text.btn-text
│     └─ span.btn-icon-box → svg.btn-icon → polyline
├─ .tpl-header_search_full [data-component="search"]
└─ .tpl-lang001 [data-component="web-lang"]
```

完整結構以內附 HTML 為準。搜尋及語系需求依案件確認保留或設定，不用假的語系連結或無效搜尋入口假裝完成。保留按鈕 type、可辨識名稱、焦點樣式與狀態更新；這些系統元件允許必要 span／svg 子元素，不受一般純文字 CTA 限制。

## root 與樣式

保留 Navi 變數名稱及用途，包括 `--NaviHeight`、`--FontSizeNavi`、`--NaviTextColor`／`--NaviHoverTextColor`、`--NaviUpTextColor`／`--NaviUpHoverTextColor`／`--NaviUpBgColor`、`--NaviBtnWidth`／`--NaviBtnHeight`／`--NaviBtnBorderRadius` 與主／輔色按鈕變數。全站的 `--Color*`、`--Btn*`、`--TextColor*`、`--ContainerDefaultWidth`、`--Space*` 及 `--TransitionDefault` 從 Common 繼承，不在 `.header` 重複宣告。每個 var() 都有合理 fallback，仍需驗證變數與依賴載入正確。

從基底修改品牌色、字型、Logo、尺寸與間距，不重寫另一套 Header 或在每頁追加不同覆寫。預設 fixed 頂端、flex 垂直置中，Logo 高度依 NaviHeight，導覽靠右；具體宣告依 `_header.scss`。來源的品牌色及尺寸是可調預設，不是所有網站的固定視覺。

## 漢堡與導覽行為

使用者指定：**1199px 以下顯示漢堡選單，1200px 以上顯示桌機導覽。** `data-rwdpointer="1199"` 與系統／案件 CSS 的 `max-width: 1199px` 收合門檻必須一致；另有 1280px 及 650px 的外觀調整，保留各自用途，不混成單一門檻。若案件改收合尺寸，HTML、CSS、JS 與平台產生的規則一起核對。

保留 `.is-open` 控制遮罩、面板、漢堡與子選單的關係，面板由右側滑入；關閉後不可攔截背景點擊。字串連結與子層展開依系統功能處理，確認父分類仍有可到達的入口。檢查 Escape、焦點返回、aria-expanded、長選單捲動及跨斷點恢復，不另綁一套事件。

頁首、`.scroll-fixed` 與 `.menu-open` 分別檢查。來源同時有系統背景、案件偽元素與陰影覆寫，修改時核對最終 computed style，避免 menu-open 仍留下不預期背景。固定 Header 的內容與錨點留白依案件設計，首屏疊在主視覺上時保留已確認構圖。

## 按鈕與語系

Header 跟隨按鈕統一使用 evo266200 內附 HTML：保留 btn-item、btn-text、btn-icon-box、SVG polyline 與必要 class。原站是「聯絡我們」，本案文字與連結依任務替換；不再強加「立即購買」翻譯鍵或 evo266125 的 SVG path。

依設計選 main-btn、sub-btn 或 outline-btn，保留 header-btn-link 與 btn-link；以本基底實際提供的樣式為準，未提供的變體須在案件補齊並驗收，不能只改 class 就宣稱完整。語系保留 lang001 的結構、狀態與實際路由；來源有某語系標籤不代表該語系頁可用。

## Header 跟隨按鈕 CSS 基準

**直接採用內附 `_header.scss` 的 evo266200 完整按鈕規則**，包含容器、文字、圖示、配色、互動及 RWD。不再另貼先前 evo266125 的 min-height、14px 圖示扣除值或 padding 規則。案件修改時核對與 Common 的疊加結果，不以 !important 強壓。

### 完整 Header 跟隨按鈕基底

整體 Header 與按鈕為同一來源。手機底部跟隨行為預設沿用此基底；案件確認不同設計時再調整。處理底部內容留白，不搬動搜尋、語系或其他功能按鈕；實作與驗收依已確認 RWD 範圍。

## 適用邊界與驗收

本次已核對來源 HTML／CSS 並整理可編譯基底，尚未完成案件的瀏覽器互動與視覺驗收。檢查桌機、各斷點兩側、頁首／捲動／選單開關、Logo、按鈕圖示、長文案、搜尋、語系與首內頁。比較來源與本案差異時，分清楚已確認品牌調整和結構缺漏；不要把複製完成或編譯通過當成平台串接通過。
