# EVO 產品分類選單｜left_menu001

指定參考：[evo265987 產品分類頁](http://192.168.168.99/php83/sites/evo265987/public/zh-tw/product/category/product-uhh449fi?via=21)。沿用系統 `left_menu001` 的 HTML 與操作，**桌機外觀可依案件調整，手機版下拉的操作邏輯是公版，不可改寫或另綁一套事件**；保留原生下拉所需結構與識別。詢問車／搜尋頁的 HTML／JS 不可修改限制，不擴及整個產品頁或所有分類選單排版。不為恢復桌機外觀而換回舊結構或另寫選單 JS。

## 原生結構與操作

已核對來源包含 `data-template-id="left_menu001"`、`data-component="left-menu"`、`.tpl-leftmenu001-container`、`.tpl-leftmenu001-dropdown-trigger`／`.tpl-leftmenu001-dropdown-label`、`.tpl-leftmenu001-title`、`.tpl-leftmenu001-item`／`.tpl-leftmenu001-link`／`.tpl-leftmenu001-toggle`、`.tpl-leftmenu001-submenu-item`／`.tpl-leftmenu001-submenu-link`；保留原生 data-param、狀態 class 與連結。實例 class、分類 ID 與路由由本案平台提供，不複製參考值。

分類文字負責導頁，箭頭獨立展開子分類；下拉標籤顯示目前分類，無子分類不顯示箭頭。這些操作由原生系統負責，若本案版本不符，記錄差異交工程師，不改寫手機版下拉公版邏輯或另綁事件補做。

## 案件 CSS

公版原始樣式保留；案件桌機外觀與下拉微調集中在既有 `_left-menu.scss`（或專案相同職責的檔案），編譯 CSS 在公版 CSS 後載入。桌機保留案件設計；下拉沿用指定公版樣式，不擅自將桌機也換成公版外觀。

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
