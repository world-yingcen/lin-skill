# 內頁麵包屑指定寫法｜breadcrumb001

使用者於 2026-10-05 指定內頁 breadcrumb 依照 [evo263525 優惠專案頁](https://evo263525_demo.miracle-g1.tw/zh-tw/post/category/post-qndptiib?via=26) 的 `breadcrumb001`。製作內頁麵包屑時沿用以下結構、class 與 data 契約，外觀配合本案首頁及內頁 Banner。

## 已核對來源

已讀取參考頁 HTML、[元件 CSS](https://evo263525_demo.miracle-g1.tw/page-resource/20/css) 與後載入的 [共用 CSS](https://evo263525_demo.miracle-g1.tw/css/evomni-root.css)。本紀錄為原始碼核對，尚未做瀏覽器操作或後台路徑生成驗證。

## HTML 結構

以下是可替換內容的結構示例；連結與層級須依本案真實網站架構填入。EVO 產生的 `data-instance-id` 與實例 class 由本案實例提供，不沿用參考站的 `5i11e`。

```html
<div data-template-id="breadcrumb001" class="tpl-model tpl-breadcrumb001 template-wrapper">
  <nav data-component="breadcrumb" data-template-variant="breadcrumb001" aria-label="麵包屑導覽" class="tpl-breadcrumb001-container tpl-container">
    <ol data-param="list" class="tpl-breadcrumb001-list">
      <li data-param="list-item" class="tpl-breadcrumb001-item">
        <a href="index.html" data-param="item-link" class="tpl-breadcrumb001-link">
          <span data-param="item-title">首頁</span>
        </a>
      </li>
      <li data-param="separator" aria-hidden="true" class="tpl-breadcrumb001-separator">•</li>
      <li data-param="list-item" class="tpl-breadcrumb001-item">
        <a href="news.html" data-param="item-link" class="tpl-breadcrumb001-link">
          <span data-param="item-title">最新消息</span>
        </a>
      </li>
      <li data-param="separator" aria-hidden="true" class="tpl-breadcrumb001-separator">•</li>
      <li data-param="current" aria-current="page" class="tpl-breadcrumb001-current">優惠專案</li>
    </ol>
  </nav>
</div>
```

- 上層項目使用真實連結；最後一項為目前頁文字，不另外包自我連結，保留 `aria-current="page"`。
- 分隔符為獨立 `.tpl-breadcrumb001-separator`，使用 `•` 與 `aria-hidden="true"`。不要改成斜線、箭頭或自製另一套結構。
- 層級依頁面實際歸屬，不固定三層、不直接複製參考站文案或 `via=26`。HTML 中保留完整頁名，即使視覺上省略也不截斷原始文字。

## 樣式與共用方式

元件基底使用 flex、flex-wrap，並使用 `--Space1`、`--FontSizeNavi`、`--TextColorSecondary`、`--TextColorPrimary`、`--ColorPrimary` 等共用變數。本案已有定義就沿用，不另造同義 token。

參考站放在 `.inner-banner-text` 裡、標題之後；共用 CSS 將清單置中、gap 設為 0，文字與分隔符設為白色、14px、字重 400，容器 padding-top 為 10px。目前頁採 `max-width: 8em`、單行及 ellipsis。這些是該站 Banner 的外觀值，依本案背景、可讀性與構圖調整；保留結構與狀態，不把白色硬套到淺色背景。

樣式放在本案內頁共用 SCSS，不逐頁複製。參考 CSS 的 hover 未包裝置條件；套用時依 T08 將 `&:hover` 收在元素內的 `@media (hover: hover) and (pointer: fine)`，`:active`／`:focus-visible` 放外面，保留可見鍵盤焦點。

## EVO 串接與驗收

正式 EVO 環境沿用平台提供的 breadcrumb 資料與渲染，保留上述 data-param；靜態切版先填真實路徑與文字，不用 JS 猜 URL 或自造後台邏輯。只有前台輸出可供觀察時，不能宣稱已驗證後台路徑生成。

交付前檢查首頁／上層連結、目前頁名稱、`aria-current`、分隔符、長標題省略、鍵盤焦點與代表內頁的一致性。驗收尺寸依本案授權，RWD 依案件範圍處理。
