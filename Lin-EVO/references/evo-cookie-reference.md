# Cookie 提示指定樣式與文字｜evo263525

2026-10-08 使用者指定 Cookie 提示的樣式與文字依照 [evo263525 首頁](https://evo263525_demo.miracle-g1.tw/zh-tw)。兩份套件同步維護此規則。製作 Cookie 提示前必讀，不自行改寫文案、增加標題或另設一套樣式。

## 首次製作必須一起完成

每個網站首次製作時，Cookie 提示與隱私權政策頁面是同一批必要交付，不能只完成提示、保留假連結，或將政策頁延後到另一次內頁製作階段。

- 建立本案實際可開啟、有內容的隱私權政策頁面，沿用本案共用 Header／Footer、內頁樣式與 breadcrumb001；尺寸與 RWD 仍依案件範圍。
- Cookie 文案中的「隱私權政策」這幾個字本身就是連結，指向上述頁面；不能使用 `#`、空 href、不存在的路徑或只有標題的占位頁。
- 政策內容優先使用本案提供或已確認的文字，不直接複製參考站的公司資訊，也不捏造資料蒐集、第三方服務、保存期限等事實。缺少確認內容時先完成可閱讀的草稿頁，明列待確認項目與內容確認狀態，不將草稿宣稱為已核准政策。
- 首次交付前，從首頁及不同目錄深度的內頁點擊連結，確認政策頁可正常開啟、內容存在、共用元件載入正常；Cookie 提示與政策頁缺任一項，都不能將這組功能標示為完成。

## 固定文字與結構

文字逐字保留，包括小寫 cookies 與原始標點；只將隱私權政策連結換成本案的有效網址。以下 privacy.html 是示例路徑，交付前必須確認存在。

```html
<div class="cookie-notice" data-align="right" id="cookieNotice">
  <p class="cookie-notice-text">本網站使用cookies為您提供更好的用戶體驗。繼續使用本網站表示您同意我們的<a class="privacy-link" href="privacy.html">隱私權政策</a></p>
  <div class="btn-group">
    <button type="button" class="btn-outline cookie-notice-btn agree-btn" id="cookieAgree">同意</button>
  </div>
</div>
```

保留 class、ID 與 data-align，一頁只輸出一份。指定外觀只有「同意」按鈕，不自行增加關閉叉號、拒絕、設定或其他文案；本案另有明確功能要求時依該要求處理。

## 樣式依據

已讀取 [Cookie 基底 CSS](https://evo263525_demo.miracle-g1.tw/css/cookie-consent.css) 與後載入的 [網站共用 CSS](https://evo263525_demo.miracle-g1.tw/css/evomni-root.css)，以兩者合併結果為準，不只套用基底的 400px 寬度。

- 桌機：右下固定，right／bottom 各 50px，寬 580px，z-index 9999；背景使用來源 --ColorPrimary 的 #1e1b18，文字白色。
- 內距使用 --CardPadding（來源 max(3vw, 2rem)），圓角使用 --BorderRadius（來源 2em）；文字字級沿用 --FontSizeBody，行高 1.8。
- 按鈕置中，與文案距離使用 --Space2（來源 max(2vw, 1.5rem)）；透明底、白字、1px #a1a1a1 邊框、2px 圓角，桌機基準寬 250px、高 60px、字級 17px。來源 1440px 以下改為寬 220px、高 50px。
- hover 為白底黑字。移植 SCSS 時依 T08 將 hover 收在元素內的 `@media (hover: hover) and (pointer: fine)`，觸控／鍵盤回饋置於外面，保留可見焦點。
- 1024px 以下：底部滿寬、right 0、bottom 0、無圓角、文字置中；768px 以下左右均為 0。576px 以下按鈕滿寬。
- 基底透過 .is-visible／.is-closing 管理顯示與關閉，過場為 0.3 秒 opacity／translateY(20px)。這是 Cookie 元件狀態過場，不使用 AOS 接管顯示。
- 來源 HTML 隱私權連結只有 .privacy-link，沒有 .cookie-notice-link；不能只看到基底後者的 underline 就宣稱此頁連結必有底線。

保留指定外觀與共用變數管理方式；若本案同名變數值不同，應在 Cookie 元件範圍補必要樣式來維持參考外觀，不修改全站品牌值。未經使用者另行指定，不自行換成另一種配色、位置或版型。尺寸與 RWD 實作仍依案件授權範圍。

## 初始化與驗收

沿用本案 EVO Cookie 初始化及儲存機制；共用載入時確保節點已存在才初始化，避免抓不到元素或重複綁定。不得從靜態 HTML／CSS 猜測儲存鍵、同意期限或追蹤程式的啟停行為。

檢查文案逐字一致、隱私權連結有效、按鈕可操作、同意後關閉與重載狀態，以及是否遮擋底部 CTA／回頂部。減少動態仍可正常閱讀及操作。來源本次只完成 HTML／CSS 核對，尚未實測同意儲存、瀏覽器外觀與跨尺寸行為；不可據此宣稱已驗收。
