# Marquee 指定寫法｜tpl-marquee-block

使用者指定 marquee 參照 [evo263525 示範站](https://evo263525_demo.miracle-g1.tw/zh-tw) 的 `.tpl-marquee-block`。製作連續跑馬燈時必讀本檔，沿用 EVO `marquee001` 的結構與循環機制，依案件調整內容和樣式；不改用 Swiper 自動輪播或 GSAP 重做同一效果。一般分頁輪播仍用 Swiper，區塊淡入淡出仍用 AOS。

## 來源與查證範圍

2026-10-05 已讀取首頁 HTML、[元件 CSS](https://evo263525_demo.miracle-g1.tw/page-resource/3/css)、[共用 CSS](https://evo263525_demo.miracle-g1.tw/css/evomni-root.css) 與 [頁面 JS](https://evo263525_demo.miracle-g1.tw/page-resource/3/js)。這是公開輸出原始碼的核對，尚未進行瀏覽器循環、暫停或 resize 驗收；來源後續可能更新。共用 CSS 在元件 CSS 之後載入，須一起對照，不能只抄單一規則。

## 結構契約

```text
.tpl-marquee-block
└─ .container-fluid
   └─ .tpl-model.tpl-marquee001.marquee001-box.template-wrapper
      └─ .marquee001__viewport
         └─ .marquee001__content（同內容的循環組）
            └─ .marquee001__item
               ├─ img.marquee001__img
               └─ .marquee001__text
```

- 根元件保留 `data-marquee001="true"`、`data-component="marquee"`、`data-template-id="marquee001"` 與本案實例識別。
- 參考站設定為 `data-direction="left"`、`data-pause-on-hover="true"`、`data-mode="single"`、`data-seamless="false"`、`data-auto-width="true"`、`data-auto-height="true"`；viewport 同樣標明方向，item 使用 `data-marquee001-item`、`data-item-id`、`data-layout="image-top"`。
- `data-seamless="false"` 在此搭配項目間距；不能解讀成停止循環。是否連續移動需看實際動畫及內容補足程式。
- 保留 `marquee001__*` 的原始 class，這是 EVO 範本必要識別，自訂 class 才使用 kebab-case。來源 UID 不複製成全站共用值，實例選擇器須與本案識別一致。
- 圖片、文字寫在 HTML；只複製必要的循環組。替換為本案素材與文案，不搬用參考站客戶圖片、地名或 media ID。

## 外觀與動畫機制

- viewport 使用橫向 flex；參考值為寬度 140%、左側 margin -20%，外層裁切。content 為不收縮的 flex 組，CSS animation 以 linear、infinite 持續移動；方向由 data 屬性對應 keyframes。
- 參考實例週期為 25 秒；item 間距在元件 CSS 設 30px，後載入的共用 CSS 覆寫為 20px。實作時依最終 cascade 與本案規格設定，不保留互相矛盾的重複值。
- 圖片在上、文字在下；圖片比例 3:2、高度為 `clamp(12.5rem, .4464rem + 13.3929vw, 21.875rem)`，文字用 `--FontSizeItemTitle`。這些為參考數值，按本案構圖調整。
- `.tpl-marquee-block::before`／`::after` 建立兩側各 15vw 的背景色到透明漸層。沿用遮罩方式，色彩配合本案背景；裝飾層加 `pointer-events: none`，避免遮住 hover 或連結。
- `data-pause-on-hover="true"` 透過 `animation-play-state: paused` 暫停。AOS 若用於整區進場，應作用於外層，避免與移動中的 content 共用 transform。

## 內容補足與初始化

來源 JS 量測第一組 content 與 viewport 的寬度，所需組數為 `Math.max(2, Math.ceil(viewportWidth / contentWidth) + 1)`；不足就 clone，過多就移除多餘副本。不要固定堆很多組，也不把抓取 HTML 中已存在的三組誤當必填數量。垂直方向則量測高度。

圖片載入完成（或失敗）、字型就緒及容器 resize 後重新量測；合併排程後重啟 CSS 動畫。來源另處理 pageshow／分頁恢復顯示。圖片採 eager、async decoding，避免量測時尚無尺寸；保留可預期尺寸，並處理零尺寸或不可見容器，不能無限安排重試。

頁面資源包含多段重複 marquee 初始化，後段 `marquee001.js` 有 `__marquee001Bound` 防重複旗標。整合時保留一份有效初始化與補足邏輯，不整包複製重複監聽器；在 GrapesJS 畫布依本案範本規格保留靜態內容，沿用來源的畫布判斷。元件移除時清理自己註冊的 observer、事件與待執行排程。

## 實作後驗收

至少檢查一次完整循環的接縫、首次圖片載入、hover 暫停與繼續、resize 後補足組數，以及頁面是否橫向溢出。重複組避免重複 ID、重複讀屏與可聚焦連結；減少動態模式保留可讀內容並停止自動移動，有閱讀／操作需求時提供可操作的暫停方式。

依案件已授權尺寸驗收，不因本參考自動啟動 RWD。保留工程機制並套本案品牌，不把參考站的視覺或未驗證行為當作所有案件的固定結果。
