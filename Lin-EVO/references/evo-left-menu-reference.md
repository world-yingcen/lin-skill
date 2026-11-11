# EVO 分類與 Blog 側選單｜left_menu001

2026-11-04 使用者指定優先範本：[evo266125 刺繡吊飾分類頁](http://192.168.168.99/php83/sites/evo266125/public/zh-tw/product/category/charm?via=56)。**遇到分類側選單時，優先沿用此 `left_menu001` HTML 結構，再依案件設計修改 CSS；不先自造另一套側選單。** 適用產品、文章等具有相同分類導覽需求的頁面；不把一般側欄、篩選器或頁內目錄硬改為分類選單。

本輪已核對實際前台 HTML，尚未做瀏覽器互動驗收。此來源取代先前 evo265987 作為優先結構參考。手機版下拉操作沿用系統，不改寫或另綁一套事件；CSS 可依案件調整顏色、字級、間距、外框與選取狀態，保留原生下拉所需結構及識別。

## Blog／專業知識列表的側選單

Blog 的優先來源為使用者另指定的 [evo260865 Blog 公版](evo-blog-reference.md)，沿用 left_menu001、bloglinks、search001、hotkeywords001 與 bloglist001 組合；其中最新／熱門連結位於 aside 外的 `.tpl-leftmenu001-bloglinks`，不當成分類項目。Blog 設定與下方產品分類示例不同時，以 Blog 公版及本案工程契約為準。

2026-11-10 使用者指定：遇到「左側導覽＋右側文章列表」的 Blog、部落格、專業知識或文章列表版型，**側邊導覽必須沿用 left_menu001 結構，再依設計改 CSS**。即使畫面只有「所有文章／最熱門文章／最新文章」三個單層連結、沒有子分類或明顯外框，也不可另外寫一套自訂 ul／nav 取代範本，或只加同名 class 而省略必要層級、data 與手機下拉結構。

- 沿用下方完整範本的外層、aside、主列表、項目、連結、文字與手機下拉結構；沒有子層時依系統的無子分類狀態處理，不造空子選單。字級、顏色、間距、底線、外框與選取樣式用 CSS 配合本案。
- 「最熱門／最新」可能是排序入口，不必然是後台分類。保留本案已確認的連結及資料語意，正式動態網址、排序參數與選取狀態依工程師契約；不得因沿用結構就把排序偽裝成分類，或宣稱 left_menu001 自動提供熱門／最新排序功能。
- 文章搜尋、熱門關鍵字與其他側欄內容是獨立區塊，與 left_menu001 並列放在側欄中，不塞進 `.left-menu`／`.left-submenu` 或改掉系統選單的直系層級。各自功能仍依本案系統範本與資料契約。
- 校稿需同時檢查桌機側選單、手機下拉、目前項目與連結導向；搜尋／標籤另驗證，不把網址有 query 或外觀像範本當成實際篩選／排序完成。

以下為去除他案資料後的結構示例；實際分類、連結與實例識別由本案產生。SVG 及文字 span 是系統範本必要子元素，不受一般自訂純文字 button／CTA 規則限制。

```html
<div data-template-id="left_menu001" class="template-wrapper tpl-model tpl-left_menu001 tpl-leftmenu001">
  <aside data-component="left-menu" data-template-variant="left_menu001"
         data-show-title="true" data-show-l2="true" data-collapsible="true"
         class="tpl-leftmenu001-container tpl-container">
    <button type="button" aria-expanded="false" class="tpl-leftmenu001-dropdown-trigger">
      <span class="tpl-leftmenu001-dropdown-label">分類標題</span>
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </button>
    <h2 data-param="menu-title" class="tpl-leftmenu001-title">分類標題</h2>
    <ul data-param="list" class="left-menu">
      <li data-param="list-item" class="tpl-leftmenu001-item left-menu-item has-child">
        <a href="本案分類網址" data-param="item-link" class="tpl-leftmenu001-link">
          <span data-param="item-title">分類名稱</span>
        </a>
        <button type="button" aria-label="展開子選單" class="tpl-leftmenu001-toggle">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
        <ul data-param="submenu" class="left-submenu">
          <li data-param="submenu-item" class="tpl-leftmenu001-submenu-item left-submenu-item">
            <a href="本案子分類網址" data-param="submenu-link" class="tpl-leftmenu001-submenu-link">
              <span data-param="submenu-title">子分類名稱</span>
            </a>
          </li>
        </ul>
      </li>
    </ul>
  </aside>
</div>
```

不複製來源的 `data-instance-id="imp002"`、`left_menu001-imp002`／`left-menu001-imp002`、站號或 via 值；也不刪除本案系統已生成的實例識別。標記的用途依本案工程師契約核對。此使用者指定結構優先於舊流程的概括限制；若整站匯入契約不相容，記錄具體差異交工程師，不默默改造範本或宣稱已支援匯入。

## 原生結構與操作

已核對來源包含 `data-template-id="left_menu001"`、`data-component="left-menu"`、`.tpl-leftmenu001-container`、`.tpl-leftmenu001-dropdown-trigger`／`.tpl-leftmenu001-dropdown-label`、`.tpl-leftmenu001-title`、`.tpl-leftmenu001-item`／`.tpl-leftmenu001-link`／`.tpl-leftmenu001-toggle`、`.tpl-leftmenu001-submenu-item`／`.tpl-leftmenu001-submenu-link`；保留原生 data-param、狀態 class 與連結。實例 class、分類 ID 與路由由本案平台提供，不複製參考值。

分類文字負責導頁，箭頭獨立展開子分類；驗收時確認下拉標籤符合本案分類顯示需求，無子分類不出現可操作的展開箭頭。本次取得的 HTML 中 dropdown-label 仍是「列表頁標題」，且無子分類列仍有 toggle 標籤；不能僅憑 HTML 宣稱標籤同步或箭頭隱藏已正常，需核對系統 CSS／JS 與實際畫面。這些操作由原生系統負責，若本案版本不符，記錄差異交工程師，不改寫手機版下拉公版邏輯或另綁事件補做。

## 案件 CSS

公版原始樣式保留；案件桌機與手機版的 CSS 調整集中在既有 `_left-menu.scss`（或專案相同職責的檔案），編譯 CSS 在公版 CSS 後載入。桌機保留案件設計；下拉沿用公版結構與操作，外觀依案件調整，不用重造 HTML 達成設計。

此案確認為 1200px 以上桌機、1199px 以下下拉，桌機保留 sticky、圓角白底卡片、米色標題、原字級／間距與選取圓點。這些是案件設定，其他案件依指定公版或案件確認值覆蓋；核對 CSS 斷點與原生 JS 狀態一致，若需改原生 JS 才能使用新斷點，列工程師待處理。

```css
/* 此案指定值，其他案件依確認值調整。 */
@media (max-width: 1199px) {
  .tpl-leftmenu001-dropdown-trigger { padding: 10px 15px; }
  .tpl-leftmenu001-dropdown-trigger svg {
    flex: 0 0 auto;
    width: 18px;
    height: 18px;
  }
  .tpl-leftmenu001-submenu-link { padding: 2px 0; }
}
```

展開清單不得被 Footer 等區塊蓋住；檢查父層 overflow 與疊層關係，不只加大 z-index。桌機連結有上下 margin、箭頭絕對定位而第一列偏移時，先查 margin 合併；確認為此原因才在 `.tpl-leftmenu001-item` 加 `display: flow-root`，不只硬改第一列的 top。

修改後同步編譯 CSS、既有產頁腳本及唯一的 `工程師交接說明.md`；核對桌機與下拉外觀、目前分類標籤、導頁／展開及遮擋狀態，未實測原生行為須註明。
