# EVO 選單指定參考｜evo266200

使用者於 2026-10-05 指定：選單架構、`:root`、漢堡、按鈕與語系做法參照 [evo266200 示範站](https://system62.webtech.com.tw/demo/evo266200/index.html)。製作 EVO Header 時先讀本檔，沿用元件結構與狀態，再依本案首頁調整樣式。這是指定的工程參考，不把參考站品牌、文案或圖片當成新案素材，也不代表所有 EVO 版本都採相同契約。

## 已核對來源

本次已讀取下列公開 HTML、CSS 與 JavaScript；尚未執行瀏覽器互動驗收。實作前應重新核對來源與本案版本。

- [共用 Header](https://system62.webtech.com.tw/demo/evo266200/partials/header.html)：實際元件層級及 data 屬性。
- [共用樣式](https://system62.webtech.com.tw/demo/evo266200/scss/evomni-root.css)：全站與導覽變數、元件外觀及斷點；這是編譯 CSS，不能假稱已取得 SCSS 原始碼。
- [共用載入器](https://system62.webtech.com.tw/demo/evo266200/js/shared-layout.js)：載入 Header／Footer 後依序載入 page-builder.js、masada-page-resource.js。
- [互動程式](https://system62.webtech.com.tw/demo/evo266200/js/masada-page-resource.js)：nav003 與 lang001 初始化、事件與狀態。

## 現行 Header 樣式參考（2026-11-04）

使用者補充指定[目前 EVO 前台](http://192.168.168.99/php83/sites/evo266200/public/zh-tw) 作為整體 Header 樣式寫法參考。本輪實際讀取 HTML、[系統元件 CSS](http://192.168.168.99/php83/sites/evo266200/public/page-resource/7/css?v=26425233ca814bc3d77f8837d5ccc61a) 與[案件共用 CSS](http://192.168.168.99/php83/sites/evo266200/public/css/evomni-root.css?v=1793774870)；取得的是編譯後 CSS，未取得原始 SCSS，也尚未做瀏覽器操作驗收。上方舊示範站 JS 行為屬先前查核，不代表本輪已重新驗證目前前台的 JS。

**整體 Header 的排列與狀態參考 evo266200；跟隨按鈕仍採下方已確認的 evo266125 完整基底與 LIN 補齊規則。** 不因這次新增整體 Header 參考，退回 evo266200 不同的按鈕 padding、固定 height 或圖示尺寸。

### 樣式來源與編寫順序

- 先確認本案系統元件 CSS，再由既有 `_header.scss` 集中寫案件外觀；參考站先載入 page-resource CSS，後載入 evomni-root.css。不要把編譯 CSS 全檔貼進專案、重複帶入 nav003 或語系元件。
- 沿用 `.header`、`.tpl-header-logo`、`.tpl-nav003`、`.tpl-nav003-nav`、`.tpl-nav003-toggle-menu-btn`、`.tpl-lang001` 的用途與狀態 class。只新增必要案件覆寫，依「共用變數 → 外框與 Logo → 導覽／功能區 → 捲動／展開狀態 → RWD」集中排列。
- `:root` 使用現有 Navi 變數；每個 var() 都要有合理 fallback。不得複製來源的 `!important`、重複規則、隨機 instance class 或後台畫布專用 `.header-section-block` 樣式來完成前台。
- 案件顏色、Logo、間距、底線、陰影及斷點可依已確認設計調整；品牌值不是所有網站的固定規格。

### 外框、Logo 與導覽配置

參考站 `.header` 固定在視窗頂端，寬度 100%、z-index 100、flex 垂直置中，以 `--NaviHeight` 控制最小高度；桌機左右 padding 為 3%，1280px 以下改為 2%。Logo 高度依 NaviHeight 減 20px、寬度 auto；導覽以 margin-left:auto 靠右，桌機寬度 70%、justify-content:flex-end。這些比例以案件設計調整，不能為照抄 70% 擠壓功能按鈕。

以下是整理後的 SCSS 寫法示例（非整份 Header，需搭配系統元件與本檔其餘規則）。保留單一有效樣式來源；不把此片段另貼到每頁 CSS：

```scss
.header {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  width: 100%;
  min-height: var(--NaviHeight, 85px);
  padding: 0 3%;
  transition: background-color .3s, box-shadow .3s;
}

.tpl-header-logo {
  margin-right: 2%;

  .logo-link .img-responsive {
    width: auto;
    height: calc(var(--NaviHeight, 85px) - 20px);
  }
}

.tpl-nav003 {
  margin-left: auto;
  margin-right: 0;
  width: 70%;
  justify-content: flex-end;
}

@media (max-width: 1512px) {
  .header {
    height: auto;
    padding-right: calc(3% + 30px + 1rem);
  }

  .tpl-nav003-toggle-menu-btn {
    right: 3%;
    top: calc((var(--NaviHeight, 85px) - 30px) / 2);
  }

  .tpl-nav003 {
    width: 100%;
  }

  .tpl-nav003-nav.is-open {
    background: var(--ColorSecondary, #525252);
    padding-inline: 2rem;
  }
}
```

Logo 原站使用 !important，本規範不沿用。若本案仍有其他高優先級規則，先查 computed style 並回到有效來源整理，不用 !important 壓過去。固定 Header 下的內容與錨點需依案件配置預留空間；首屏刻意疊在主視覺上的設計依設計保留。

### 捲動、選單展開與功能區

- 區分 `.header` 頁首、`.header.scroll-fixed` 捲動後與 `.header.menu-open` 展開狀態。狀態由本案既有程式管理；CSS 不另建立一套同義 class 或重複捲動監聽。
- 原站另以 `.header::before` 作背景層：absolute、top/left 0、width 100%、初始 height 0、z-index -1，背景為 `--NaviUpBgColor`，scroll-fixed 時 height 100%；以 height .3s ease 過渡，並加陰影。這是參考手法，採用時檢查層級與捲動效能。
- **不能只貼偽元素就認為捲動背景完成**：原站系統 CSS 還對 scroll-fixed 直接設定半透明白底；案件需明確統一容器背景與偽元素的責任，核對最後生效值。menu-open 的透明背景／取消陰影也需連同偽元素檢查，避免仍有底色殘留。
- 頁首功能圖示採 `--NaviTextColor`，捲動後依 `--NaviUpTextColor`；互動用相對應 Hover 變數。原站搜尋、語系控制為 50px 正方形，1280px 以下寬度 45px，語系下拉寬 120px、z-index 200；實際尺寸與配色依案件。保留清楚的鍵盤焦點及觸控操作，不只處理 hover。
- 不將原站搜尋頁／產品頁對 Header 的額外背景色套成全站規則；首內頁有不同背景需求時在案件既有頁型 class 管理並驗收。

### RWD 契約與驗收

- 實際 HTML 的 `data-rwdpointer="1512"` 與 CSS 的 `max-width:1512px` 必須一起調整。小於等於門檻時，系統提供全視窗遮罩、右側滑入面板與漢堡；面板 max-width 400px，漢堡 30px、z-index 250。不要只改案件 CSS 斷點而漏掉系統生成規則與 JS 門檻。
- 窄版遮罩平時 pointer-events:none，展開時才可接收事件；面板以 translate(100%)／translate(0) 配合 `.is-open` 切換。保留關閉後不擋畫面的行為，確認長選單可捲動、手機瀏覽器高度變動與跨斷點狀態恢復。
- 650px 以下跟隨按鈕行為依 LIN 已確認按鈕基底處理；Logo、漢堡、搜尋／語系不得被底部 CTA 的規則一併搬動。
- 實作後至少檢查：頁首、捲動後、選單開／關、斷點兩側、長選單／長文案、首內頁、鍵盤焦點及手機底部遮擋。沒有實際操作或畫面結果時，標示「樣式已實作，互動／視覺待驗」。

## 結構與識別

```text
header.header
├─ .tpl-header-logo → a.logo-link → img
├─ .tpl-nav003 [data-template-id="nav003"] [data-rwdpointer]
│  ├─ nav.tpl-nav003-nav [data-component="web-menu"] [data-menu-key="main"]
│  │  └─ ul.nav-menu → li.nav-item → a.nav-link
│  │     └─ 有子選單：li.has-child → ul.sub-menu
│  └─ button.tpl-nav003-toggle-menu-btn → span.menu-bar × 3
├─ .tpl-model.tpl-header-btn-box.btn-group → .btn-item → a.header-btn-link.btn-link.main-btn
│  ├─ div.btn-text [data-trans]
│  └─ span.btn-icon-box → svg.btn-icon → path
├─ .tpl-header_search_full（本案需要搜尋時才採用）
└─ .tpl-lang001 [data-template-id="lang001"] [data-component="web-lang"]
   └─ .tpl-lang001-container
      ├─ button.tpl-lang001-lang-btn → .lang-icon → svg
      └─ ul.lang-dropdown → li → a.lang-link
```

保留上述用途明確的 class 與必要 data 契約。來源內的隨機 instance class、media ID、內網網址與客戶路徑需由本案資料替換，不複製成通用識別。Header 只有一份共用來源；靜態預覽可沿用先載入再初始化的順序，框架或 EVO 正式環境則沿用既有生命週期，不額外疊加另一套載入器。

## root 與樣式

這裡的 `:root` 是網站共用 CSS 變數，與 Swiper 自帶的 `--swiper-*` 變數分開管理。

| 用途 | 參考站實際變數 |
| --- | --- |
| 全站基礎 | `--ColorPrimary`、`--ColorSecondary`、`--FontFamily`、`--Space2`、`--TransitionDefault` |
| 導覽尺寸 | `--NaviHeight`、`--NaviStickyOffset`、`--FontSizeNavi` |
| 頁首文字與互動 | `--NaviTextColor`、`--NaviHoverTextColor` |
| 捲動後狀態 | `--NaviUpTextColor`、`--NaviUpHoverTextColor`、`--NaviUpBgColor` |
| 按鈕共用 | `--BtnBorderRadius`、`--BtnWidth`、`--BtnHeight`、`--BtnFontSize`，以及 `--BtnPrimary*`、`--BtnSecondary*`、`--BtnOutline*` 色彩變數 |
| Header 按鈕 | `--NaviBtnWidth`、`--NaviBtnHeight`，以及 `--NaviBtnPrimary*`、`--NaviBtnSecondary*` 色彩變數 |

沿用名稱及角色，在案件共用樣式集中設定本案值。參考站 `--NaviHeight` 初值 85px、`--NaviBtnHeight: calc(var(--NaviHeight, 85px) - 30px)`，屬該案尺寸，不是每案固定規定。Logo、漢堡垂直位置與按鈕尺寸依導覽高度形成關係，不各區另造一組相同用途的變數。

## 漢堡與導覽行為

- 參考站 `data-rwdpointer="1512"`，CSS 對應 `max-width: 1512px`。調整本案切換點時，HTML 設定與 CSS 必須一致；這是選單收合門檻，不等同通用手機尺寸。
- 漢堡使用三條 `.menu-bar`；按鈕加 `.is-open` 時第一、三條旋轉成叉號，中間條隱藏。保留 `type="button"` 與可辨識名稱。
- 點擊同步切換按鈕、`.tpl-nav003`、`.nav-menu`、`.tpl-nav003-nav` 的 `.is-open`，Header 同步 `.menu-open`。窄版面板從右側進出；子選單以 `.has-child`、`.sub-menu` 的 `.is-open` 控制。
- 寬版子選單以 hover 顯示；窄版父連結點擊會攔截導頁並切換子選單。若父層有實際內容頁，須保留可到達該頁的入口。
- Header 本身固定於頂端；原程式捲動超過 10px 加 `.scroll-fixed`，展開選單時暫移除，關閉後依捲動位置恢復。沿用狀態關係，門檻可依本案調整。
- 沿用初始化去重、resize 及 Header 高度量測機制，避免共用片段尚未載入就初始化。實作時確認開關名稱、`aria-expanded`、控制目標、鍵盤開關、Escape、關閉後焦點及跨斷點恢復；這些是待驗收項目，不表示來源已全部具備。

## 按鈕與語系

2026-11-04 使用者確認：Header 跟隨按鈕使用下列系統結構，優先於一般 `btn-group > a` 純文字規則；不能刪除 btn-item、文字容器或圖示容器。

```html
<div class="tpl-model tpl-header-btn-box btn-group">
  <div class="btn-item">
    <a href="本案實際目標網址" target="_self" class="header-btn-link btn-link main-btn">
      <div data-trans="evo-ecommerce::storefront_product_detail.cta.buy_now" class="btn-text">立即購買</div>
      <span class="btn-icon-box">
        <svg viewBox="0 -960 960 960" fill="currentColor" aria-hidden="true" class="btn-icon">
          <path d="M530-481 332-679l43-43 241 241-241 241-43-43 198-198Z"></path>
        </svg>
      </span>
    </a>
  </div>
</div>
```

- 保留上述 HTML 層級、標籤與必要 class；CSS 須先符合下方指定基準，再依案件調整品牌外觀。按設計擇一使用 main-btn（主色）、sub-btn（輔色）、outline-btn（外框），保留 header-btn-link 與 btn-link，Header 尺寸沿用 `--NaviBtn*`；主色款使用 `--NaviBtnPrimary*` 配色。LIN 基底已補上 sub-btn 的一般、hover、active／focus-visible 對應，使用 `--NaviBtnSecondary*`；outline-btn 沿用 Common 的 `--BtnOutline*`，不另造 Header 外框色彩變數。
- 範例為「立即購買」，其 data-trans 對應此用途；其他 CTA 使用本案已確認的翻譯鍵，不把購買翻譯鍵套到不同文案。網址改用本案目標，不複製他案站號或選單參數。
- 使用者提供的輸出另有 `__p="undefined"`；目前未確認它是必要平台契約，範例不主動補造，既有後台輸出也不因本規範擅自清除。
- 漢堡、語系與其他系統操作按鈕維持各自契約；一般內文連結型按鈕仍依 [統一按鈕結構](html-css-rules.md#連結型按鈕統一結構)。

- 手機 Header CTA 預設沿用 LIN 基底，在 650px 以下固定到底部，並處理內容底部留白；案件已確認不同設計時再調整。實作與驗收仍依案件約定的 RWD 範圍，不因本條擴大工作範圍。不能把購物車或會員按鈕一併搬到底部。
- 語系沿用 `.tpl-lang001` 與 `data-mode="dropdown-icon"`、`data-show-lang="true"`；地球圖示按鈕開啟 `.lang-dropdown`。原 JS 以 click 切換 `.is-open`、點擊外部關閉，CSS 另提供 hover 展開。
- 語系連結保留 `data-lang-code`、`data-lang-link`；目前語系以 `.is-active` 與 `aria-current` 表示。連結需使用本案實際語系路由。
- 來源只有繁中一項，且連結指向內網；未證實跨語系切換。不能複製內網路徑、虛構英文頁，或把選單可展開當成語系功能完成。
- 來源的 icon 模式未像 text 模式同步 `aria-expanded`，另有重複語系程式但以旗標防止重複綁定；沿用結構時補齊必要狀態並維持單一初始化。來源全域移除 outline 的寫法也不能取代本案可見的鍵盤焦點。

## Header 跟隨按鈕 CSS 基準

2026-11-04 使用者指定：Header 跟隨按鈕必須沿用以下 CSS，不只保留 HTML。寫入案件既有 Header 樣式來源，沿用編譯流程，不在各頁重複追加覆寫。

```css
.tpl-header-btn-box .header-btn-link {
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    gap: var(--Space1, 1rem);
    width: var(--NaviBtnWidth, 200px);
    min-height: var(--NaviBtnHeight, calc(85px - 30px));
    margin-top: 0;
    padding: 0 5px 0 var(--Space2, max(2vw, 1.5rem));
    font-size: var(--FontSizeNavi, clamp(0.9375rem, 0.7768rem + 0.1786vw, 1.0625rem));
    line-height: 1;
    min-width: unset;
}
```

- 保留上述選擇器、屬性、數值與變數對應；品牌色與 main-btn／sub-btn／outline-btn 外觀依案件 Common 調整，尺寸優先調整已存在的 NaviBtn 變數，不另造同義變數或用一般按鈕尺寸覆蓋這段。
- 確認 Common 已定義 `--Space1`、`--Space2`、`--NaviBtnWidth`、`--NaviBtnHeight`、`--FontSizeNavi` 且值有效。依使用者後續要求，包含 Header 在內的每個 var() 都補上合理 fallback；備用值取自內附基底預設值，案件調整時一併核對用途與數值。
- 這段依賴既有按鈕基礎樣式的 flex 排版；檢查 `.header-btn-link` 最終 computed display 是否為 flex／inline-flex，確保文字與圖示兩端對齊。若基礎樣式未載入，先修正依賴，不宣稱只貼這段就已完成。
- 校稿核對實際生效的寬度、最小高度、間距、padding、字級、line-height、margin-top 與 min-width，確認未被其他按鈕規則蓋掉；在本案範圍內檢查長文字與 RWD，不因尺寸限制裁掉文字。

## 適用邊界

使用者指定保留的 EVO 漢堡、語系與圖示操作按鈕，可保留必要的 `span`／`svg` 子元素，作為 T04「自訂 button 純文字」規則的局部例外。不要為符合純文字限制而改壞範本結構。

本次只整理工程參考，不啟動客戶案件；尺寸與 RWD 依案件範圍。實作驗收須分別記錄結構沿用、外觀、實際操作與平台串接；未經瀏覽器驗證不可標記通過。

### 完整 Header 跟隨按鈕基底

2026-11-04 已依[使用者指定前台](http://192.168.168.99/php83/sites/evo266125/public/zh-tw) 的實際共用 CSS 核對，完整規則收在[基底 _header.scss](../assets/evo-starter/06-切版/scss/_header.scss)。上方片段只說明按鈕本體，不是完整元件；切版必須連同以下規則使用，不得只複製該片段：

- `.tpl-header-btn-box` 的 flex 排列、gap、左右間距。
- `.header-btn-link` 的尺寸、內距與對齊，以及 `.btn-icon-box` 圓形底、`.btn-icon` 尺寸與顏色。
- `.main-btn` 一般、hover、active／focus-visible 配色；hover 保留精細指標裝置條件。
- 1200px 以下的外框間距與 NaviBtn 寬度；650px 以下的底部固定、全寬 btn-item、按鈕置中、取消圓角與隱藏圖示，以及 NaviBtn 尺寸覆寫。

基底依賴 Common 的 `.btn-group .btn-link` 共用樣式與變數，必須先載入 Common 再載入 Header。`.btn-text` 在參考站沒有獨立專用宣告，保留 HTML 並繼承按鈕文字設定，不虛構一份來源樣式。原站主色款之外的配色依上方說明處理。

桌機品牌色與尺寸可依案件調整，手機固定底部為此基底的預設行為；若案件已確認不同導覽行為則依案件調整。驗收時檢查桌機、1200px／650px 斷點兩側、手機底部是否遮住內容，以及 hover／鍵盤焦點；需要底部預留空間時於案件版面配置，不把固定按鈕直接蓋在最後一段內容上。此處完整規則為指定系統基底的一部分；保留結構與變數對應，依使用者要求補上 fallback。
