# 工程師內頁匯入規範

來源：[給設計師的切版共識（HTML zip → Evomni 內頁匯入）](http://192.168.168.94/evomni_vue/docs/html-zip-import-cases/DESIGNER-GUIDE.md)。2026-10-12 讀取；指南包含 2026-09-22 至 2026-09-30 案例更新。這是工作摘要，不另立工程規格；執行時重新核對原文與目標站台版本。

正本為工程師 repo 的 `docs/template-spec/designer-markup-guide.md`。本指南補充內頁匯入與 vendor 路徑，不涵蓋所有首頁模式、工具指令及 ZIP 格式。

## 內頁結構與樣式

靜態來源保留完整可操作預覽，匯入用內容僅取 main 範圍，head／body 不帶入站台。頁面識別放在 main 內第一層 wrapper：

```html
<main id="main-content" class="main-content">
  <div class="inner-page team-page">
    <!-- 本頁內容 -->
  </div>
</main>
```

- 平台 layout 提供 main，正式內容接入時不得再嵌套第二個 main。`#site-header`／`#site-footer` 在匯入準備稿留空殼，不把靜態載入的共用導覽塞進內頁內容；原始預覽保留。
- `.team-page .main-content` 命不中外層 main。單頁 overflow 放 wrapper 或區塊，不在 Common 的 `.main-content` 上設 `overflow: hidden` 破壞 sticky；全域裁切也須檢查捲動與釘選影響。
- 跨頁 Hero／CTA 放 `_innerpage-default.scss` 或本案有效共用檔，各頁 SCSS 只保留自身樣式。不要靠載入其他頁 CSS 補漏。
- 版面寬度、間距與基本可見性不能藏在 `.is-xxx-motion-ready` 等動效閘門下，初始化失敗仍要正常閱讀。
- 自製 class 不用平台保留的 `tpl-*`／`tpl-model`；本套件新自製區塊沿用 LIN 已確認的 `designer-tpl-*`，平台元件保留原名。既有衝突逐區查相依後修正，不全站盲目改名。
- main 內不放 script 或 inline `on*`，指南表示 `prep-page.mjs` 遇到會 exit 1。JS 另行接入。
- 圖片在匯入準備稿使用本案 `image/{頁面}/` 相對路徑，包內須有實檔；最終打包工具如要求其他路徑，依實際格式轉換並核對。
- 固定介面文字如麵包屑「首頁」、回上頁、表單欄位名，依正本翻譯契約與實際 `trans-keys` 掛 `data-trans`，不猜翻譯鍵。缺標記會觸發 validate O5。
- 站內連結不可寫死 `/php83/.../public` 子路徑。正式連結使用與目標 APP_URL 同前綴的絕對網址，存檔時由平台轉為 `{{APP_URL}}`；腳本使用已核對的平台占位符或路徑解析。靜態預覽與正式網址對應須列清楚，不能猜正式網域。

### 前台 body 識別

| 頁型 | 指南列出的 class |
|---|---|
| 首頁 | `index-page` |
| 列表 | `menu-{欄目名} page-list` |
| 分類列表 | `menu-{欄目名} page-list page-category` |
| 內頁 | `menu-{欄目名} page-detail` |
| 靜態頁 | `page-static static-{頁面代號}` |

欄目名不可從 URL 推測，查看前台實際 DOM。中文選單名不產生 `menu-*`。編輯器畫布沒有前台渲染才加的 body class；欄目 Header 差異等規則須到前台驗，不能用畫布無效果判定失敗。自訂 wrapper 與平台 body 標記是不同用途。

## 套件載入與初始化

指南列出的前台資源落地於 `{站台根}/admin/vendor/`，不走 CDN：

| 套件 | 指南版本 | 正式接入 |
|---|---|---|
| Swiper | 12.2.0 | 區塊根 `data-vendor="swiper"`；`swiper/swiper-bundle.min.js` 與 `.css` |
| GLightbox | 3.3.1 | 區塊根 `data-vendor="glightbox"`；`glightbox/glightbox.min.js` 與 `.css` |
| AOS | 2.3.1 | 後台「AOS 設定」全站開關；`aos/aos.js` 與 `.css` |
| GSAP／ScrollTrigger | 3.12.7 | 後台「GSAP 設定」全站開關；`gsap/gsap.min.js`、`gsap/ScrollTrigger.min.js` |

- `data-vendor` 可為 `swiper glightbox` 多值；AOS／GSAP 不走此屬性。
- 靜態 head 可載預覽資源，但 head 不匯入，不能靠原本 script 標籤宣稱正式套件已載入。比對目標版本；來源不同時檢查 API 與行為，不直接替換版本後當作通過。
- 指南未提供 Lenis、Lottie、Splide、Fancybox 等。既有頁面用到時列出接入缺口，提出納入站台資源需求；不自行塞套件，也不刪效果假裝轉換完成。
- `data-vendor` **只載入函式庫，不初始化**。自製輪播／燈箱的 JS 必須另接入。指南支援頁首 mini editor 的 JS 面板，為全站生效，需判 DOM、限制 root 與去重；目標另有 page-resource 機制時先核對。改平台範本或接受靜態會改變成果，須有相應授權。

## 逐筆編輯與畫布輪播

| 標記 | 用途 |
|---|---|
| `data-repeater="swiper"` | 根內 `.swiper-wrapper` 為項目容器 |
| `data-repeater="list"` | 根自己是項目容器 |
| `data-rp-field="key"` | 固定欄位 key；未設時依標籤與第一個 class 推導 |
| `data-rp-label="說明文字"` | 後台欄位顯示名稱 |
| `data-rp-type="text/image/link/lines"` | 表中斜線代表四種可選值，實際一次填一種 |
| `data-rp-skip` | 裝飾不進編輯表單 |
| `data-rp-swiper` | 合法 JSON，僅控制後台畫布預覽 |

- 第一筆為樣板，各筆結構一致；新增複製第一筆結構與預設內容。項目應包含完整內容單位，不只開放圖片卻綁死相關文字。
- img 推導選圖與獨立 alt 欄；a 推導網址、開新視窗及連結文字。後台支援新增、刪除、拖曳排序、改字、換圖與隱藏單筆。
- 純文字 li 組成的 ul／ol 自動作一個條列欄位。強制 `data-rp-type="lines"` 會在儲存時清掉 li 內標籤；含連結／圖片／strong 的清單不擅自強制。各 li 的 class／屬性沿用第一筆。
- 清單根以下在畫布鎖住，只透過逐筆編輯彈窗修改；整塊仍可選取、拖曳及刪除。不要解除鎖定來模擬完成。
- 不混用後端保留字 `data-loop`、`data-field`、`data-if`、`data-href`、`data-src`、`data-media-id` 作自製逐筆欄位。
- 指南表示 `prep-page.mjs` 對 `.swiper[data-vendor~=swiper]` 自動補 repeater；一般清單要自己掛。檢查實際輸出，不僅假定工具補好。
- `data-rp-swiper` 只允許 `slidesPerView`、`slidesPerGroup`、`spaceBetween`、`loop`、`breakpoints`、`centeredSlides`。例如 `'{"slidesPerView":3,"spaceBetween":30}'`；其餘忽略，無效 JSON 回預設 `{ slidesPerView: 1, spaceBetween: 16 }`。
- 畫布在清單根父層找 `.swiper-button-prev/next` 或 class 含 `-prev`／`-next` 的箭頭、含 `pagination` 的分頁。核對控制項不跨實例。
- 畫布輪播不代表前台已初始化。指南表示發布會剝除 Swiper 狀態 class 與 inline style，仍須在實際後台驗證；其他自製動畫不推定也會自動清理。

## FAQ 必須對應 faq001

指南要求使用以下必要結構，不沿用自製 button 手風琴當作可編輯 FAQ：

```html
<div class="tpl-model tpl-faq001" data-template-id="faq001">
  <div class="tpl-container card-area" data-faq001="true">
    <details class="tpl-faq001-card-box card-box" data-schema-item="Question" open>
      <summary class="tpl-faq001-card-title card-title">
        <span class="tpl-faq001-card-title-text card-title-text" data-schema-prop="name">本案問題</span>
      </summary>
      <div class="tpl-faq001-card-description card-description" data-schema-prop="acceptedAnswer.text" data-schema-prop-type="Answer">
        <p>本案答案。</p>
      </div>
    </details>
  </div>
</div>
```

- 必要 class 與 data 不少、不改名；題目在 summary 的 span，答案在 description 下的 p，可多段及含圖。區段標題可放容器外，`.title-block` 可省略。
- 原生 details 控制開合，不加自製 id／aria-controls／aria-expanded／hidden 或重複手風琴 JS。單題互斥只有原需求需要時才在本容器透過 toggle 管理。
- 自訂外觀限縮 `.tpl-faq001`，狀態用 `details[open]`。轉檔依指南提高特異度，不加 `!important`；若本案既有外觀不同，仍以原設計調整，不能換成預設外觀就交付。
- 檢查 Common 的 `.card-box` 是否造成圓角、背景或陰影污染，按本案設計明確局部覆寫。
- 畫布的 open 會帶入發布，核對預設展開題目；可多容器。匯入後測新增／排序題目與前台 FAQPage JSON-LD，不額外產重複 JSON-LD。

## 指南列出的轉檔行為與限制

- `prep-page.mjs` 可將 body 頁面 class 移到 wrapper、改寫錯置的 `.xxx-page .main-content`；檢查 report，優先修來源結構，不依賴自動修補掩蓋問題。
- 圖片缺檔會保留 URL 並列報告，不代表通過。`data-trans` 缺漏須查正式鍵再補。
- 內容頁上一篇／下一篇對應 `blogpostnav001` 與 `TPL_SKIN`；核對實際工具支援及正式前後篇，不保留寫死示例。
- 文章作者／發布日期／更新日期對應 `detail-author`、`detail-date`、`detail-update-date`；指南指出空作者隱藏、更新日不晚於發布日隱藏，須用目標真實資料測。
- 指南指出詳情頁不提供 `detail-category`，轉檔端會刪分類膠囊並記 report。若本案畫面需要分類，先提出保留需求與工程方案，不無聲刪掉；分類節點上的固定文字是指南提出的替代做法，不等於動態分類綁定。
- faq001 依 `data-template-id` 注入真範本並對應 schema；舊 button FAQ 不自動轉。指南的案例缺圖、政策入口及行高待確認事項只屬原案例，不變成本案待辦。
