# EVO 選單指定參考｜evo266200

使用者於 2026-10-05 指定：選單架構、`:root`、漢堡、按鈕與語系做法參照 [evo266200 示範站](https://system62.webtech.com.tw/demo/evo266200/index.html)。製作 EVO Header 時先讀本檔，沿用元件結構與狀態，再依本案首頁調整樣式。這是指定的工程參考，不把參考站品牌、文案或圖片當成新案素材，也不代表所有 EVO 版本都採相同契約。

## 已核對來源

本次已讀取下列公開 HTML、CSS 與 JavaScript；尚未執行瀏覽器互動驗收。實作前應重新核對來源與本案版本。

- [共用 Header](https://system62.webtech.com.tw/demo/evo266200/partials/header.html)：實際元件層級及 data 屬性。
- [共用樣式](https://system62.webtech.com.tw/demo/evo266200/scss/evomni-root.css)：全站與導覽變數、元件外觀及斷點；這是編譯 CSS，不能假稱已取得 SCSS 原始碼。
- [共用載入器](https://system62.webtech.com.tw/demo/evo266200/js/shared-layout.js)：載入 Header／Footer 後依序載入 page-builder.js、masada-page-resource.js。
- [互動程式](https://system62.webtech.com.tw/demo/evo266200/js/masada-page-resource.js)：nav003 與 lang001 初始化、事件與狀態。

## 結構與識別

```text
header.header
├─ .tpl-header-logo → a.logo-link → img
├─ .tpl-nav003 [data-template-id="nav003"] [data-rwdpointer]
│  ├─ nav.tpl-nav003-nav [data-component="web-menu"] [data-menu-key="main"]
│  │  └─ ul.nav-menu → li.nav-item → a.nav-link
│  │     └─ 有子選單：li.has-child → ul.sub-menu
│  └─ button.tpl-nav003-toggle-menu-btn → span.menu-bar × 3
├─ .tpl-header-btn-box.btn-group → .btn-item → a.header-btn-link.btn-link.main-btn
│  ├─ .btn-text
│  └─ .btn-icon-box → svg.btn-icon
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

沿用名稱及角色，在案件共用樣式集中設定本案值。參考站 `--NaviHeight` 初值 85px、`--NaviBtnHeight: calc(var(--NaviHeight) - 30px)`，屬該案尺寸，不是每案固定規定。Logo、漢堡垂直位置與按鈕尺寸依導覽高度形成關係，不各區另造一組相同用途的變數。

## 漢堡與導覽行為

- 參考站 `data-rwdpointer="1512"`，CSS 對應 `max-width: 1512px`。調整本案切換點時，HTML 設定與 CSS 必須一致；這是選單收合門檻，不等同通用手機尺寸。
- 漢堡使用三條 `.menu-bar`；按鈕加 `.is-open` 時第一、三條旋轉成叉號，中間條隱藏。保留 `type="button"` 與可辨識名稱。
- 點擊同步切換按鈕、`.tpl-nav003`、`.nav-menu`、`.tpl-nav003-nav` 的 `.is-open`，Header 同步 `.menu-open`。窄版面板從右側進出；子選單以 `.has-child`、`.sub-menu` 的 `.is-open` 控制。
- 寬版子選單以 hover 顯示；窄版父連結點擊會攔截導頁並切換子選單。若父層有實際內容頁，須保留可到達該頁的入口。
- Header 本身固定於頂端；原程式捲動超過 10px 加 `.scroll-fixed`，展開選單時暫移除，關閉後依捲動位置恢復。沿用狀態關係，門檻可依本案調整。
- 沿用初始化去重、resize 及 Header 高度量測機制，避免共用片段尚未載入就初始化。實作時確認開關名稱、`aria-expanded`、控制目標、鍵盤開關、Escape、關閉後焦點及跨斷點恢復；這些是待驗收項目，不表示來源已全部具備。

## 按鈕與語系

- 前往頁面的 CTA 沿用 `a.header-btn-link.btn-link`，文字與圖示分為 `.btn-text`、`.btn-icon-box`；`main-btn`／`sub-btn`／`outline-btn` 沿用共用樣式角色，Header 尺寸與色彩由 `--NaviBtn*` 調整。
- 參考站在 650px 以下把 Header CTA 固定到底部；只在本案有此需求且 RWD 在案件範圍內時採用，並處理內容底部留白。不能把購物車或會員按鈕一併搬到底部。
- 語系沿用 `.tpl-lang001` 與 `data-mode="dropdown-icon"`、`data-show-lang="true"`；地球圖示按鈕開啟 `.lang-dropdown`。原 JS 以 click 切換 `.is-open`、點擊外部關閉，CSS 另提供 hover 展開。
- 語系連結保留 `data-lang-code`、`data-lang-link`；目前語系以 `.is-active` 與 `aria-current` 表示。連結需使用本案實際語系路由。
- 來源只有繁中一項，且連結指向內網；未證實跨語系切換。不能複製內網路徑、虛構英文頁，或把選單可展開當成語系功能完成。
- 來源的 icon 模式未像 text 模式同步 `aria-expanded`，另有重複語系程式但以旗標防止重複綁定；沿用結構時補齊必要狀態並維持單一初始化。來源全域移除 outline 的寫法也不能取代本案可見的鍵盤焦點。

## 適用邊界

使用者指定保留的 EVO 漢堡、語系與圖示操作按鈕，可保留必要的 `span`／`svg` 子元素，作為 T04「自訂 button 純文字」規則的局部例外。不要為符合純文字限制而改壞範本結構。

本次只整理工程參考，不啟動客戶案件；尺寸與 RWD 依案件範圍。實作驗收須分別記錄結構沿用、外觀、實際操作與平台串接；未經瀏覽器驗證不可標記通過。
