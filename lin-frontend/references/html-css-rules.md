# LIN｜HTML、樣式與 RWD

本檔整理原套件保留的 LIN 工程條文與範例。尺寸與 RWD 依案件範圍；局部修改不自動授權全站改名或重構。既有框架命名沿用，新自製版型採 designer-tpl-*，平台元件保留契約原名。

## T04｜HTML、命名與語意

- 設計師自製版型使用 `designer-tpl-{語意名稱}` 作根 class，例如 `designer-tpl-about`；不附加平台專用的 `tpl-model`，也不自行編造範本實例識別。使用者已轉達工程師確認此命名可用。EVO 已有適用元件時，保留其原本必要 class、data 與結構（例如 `tpl-model tpl-faq001`），依 [T13](shared-page-rules.md) 調整樣式，不改成 designer-tpl 前綴；同用途不同自製版型有需要才加可辨識版本編號。此規則用於新製作與本輪已授權調整的區塊，不自動批次改名既有案件。
- 自製版型 class 使用 kebab-case，不用 BEM 的 `__`／`--`。子元素使用 `text-block`、`image-block`、`card-box` 等短語意名稱，版心沿用 Common container，不要求每個子元素重複整段區塊名稱。`tpl-container` 等平台 class 僅在沿用對應元件契約時保留，不作新自製區塊的預設命名。
- 上述自訂命名規則不覆蓋 Swiper 原生 class 或 EVO 範本必要的 class、ID、data 屬性；先查樣式、初始化及平台依賴，不為統一命名而任意改掉。
- 不用 left、right、top、bottom、upper、lower 或組合作為版面位置命名；同樣適用 JS 變數與 data 屬性。方向本身是功能時，previous／next 可用；圖示資源如 `arrow-left-icon` 可用。
- 文字角色使用 `main-title`、`sub-title`、`en-title`、`description` 或明確用途名稱；不要用結構位置充當文字語意。避免無意義 wrapper、無理由增添框架與重複元件。
- 前往其他頁面或網址使用 `<a>`；展開選單、切換內容及送出表單使用 `<button>`。button 內容依下方純文字規則及指定 EVO 元件例外處理。一般操作按鈕明列 `type="button"`，送出表單才使用 `type="submit"`。
- 標題階層須符合 SEO 的內容組織原則：頁面主標題清楚表達本頁主題，主要段落與子段落依邏輯安排 h1–h6，避免無理由跳級、空標題或關鍵字堆砌。標籤由內容層級決定，外觀由 SCSS 控制，不為字級大小選標籤。尚無頁面上下文的可重用區塊可先用文字 class，合併頁面後 實作端 必須逐頁核對完整標題階層。製作與校稿頁面的 noindex 仍須保留。
- 段落切分依已確認文案的原始分段，不自行加切。同一段文案不因為版面看起來較透氣就拆成多個 `<p>`；短句獨立成段，只在文案原本就分段、或該句確實是轉折與收束時才成立。分段密度須對照原文與實際閱讀畫面；驗收見 [實作與校稿](implementation-review.md)。
- 連結／按鈕文字需能辨識目的，例如「查看服務內容」，不要只有「更多」「點這裡」。連結說明需簡短且與目標相關，沒有明確理由不用裸網址作說明。以已確認文案為依據，不自行增加未證實的行銷宣稱。
- 自訂 `<button>` 內只能放純文字，不嵌入 `span`、`img`、`svg`、圖示或其他子標籤；使用者指定的 [EVO Header 元件](evo-header-reference.md) 為局部例外，漢堡、語系及圖示操作按鈕保留範本必要的子元素與可存取名稱，不為符合此條而改壞既有結構。
- `::before`、`::after` 可用於線條、色塊等裝飾；實際文案與客戶會替換的圖片仍放 HTML，不放偽元素。
- 裝飾不能遮住文字、連結或按鈕，也不能阻擋操作；不需互動的覆蓋層可使用 `pointer-events: none`。
- 圖層優先以清楚的定位與 `z-index` 管理；必要時可用負值，須實際確認元素不會掉到父層背景後方、消失或影響操作。
- HTML 原始檔的一般外觀寫在 SCSS，不手寫 inline style；執行時需要即時計算的樣式依 T10 處理。不使用 inline on* 事件或 javascript: 連結；既有來源遇到不相容寫法，限縮修正範圍並檢查影響。
- 平台產生的 wrapper、模組 ID 與雜湊識別不能憑空編造；後台相關事項見 [平台整合邊界](shared-page-rules.md#平台整合邊界)。

### EVO 內頁的頁面識別與匯入邊界

將轉 EVO 的內頁，依工程師 [HTML 匯入指南 §1](http://192.168.168.94/evomni_vue/docs/html-zip-import-cases/DESIGNER-GUIDE.md)，把自訂頁面 class 放在 `main` 內第一層 wrapper，供匯入後的 CSS／JS 識別：

```html
<main id="main-content" class="main-content">
  <div class="inner-page about-page">
    <!-- 本頁完整內容 -->
  </div>
</main>
```

- 靜態交付仍是可預覽的完整 HTML，保留 head、共用 Header／Footer 與必要資源；指南的內頁匯入範圍為 main 內容區，靜態 body 與 head 不隨之帶入。不可只把本頁必要 class 掛在 body，或依賴匯入範圍外的自訂祖先才能套到樣式。main 由正式平台 layout 提供，轉檔時由工程師對應內容，不額外嵌套第二個 main。
- 本頁內容選擇器依實際結構撰寫，例如 `.about-page .main-title`；不要寫 `.about-page .main-content`，因為 main-content 是外層而非子元素。在靜態 DOM 核對命中節點，不靠轉檔自動改寫補救。
- 本頁 overflow、間距與布局需求放在 wrapper 或對應區塊，檢查 sticky／釘選動畫所需條件；不要為單頁效果無差別修改全站 main-content。頁面作用域不涵蓋外面的 Header／Footer。
- 平台前台自動產生的 body 頁型 class 與上述自訂 wrapper 是不同來源；若要控制某類頁面的共用 Header，先核對正式輸出，不從 URL 猜 class，也不認為後台畫布必定有同樣標記。首頁、框架及分類介紹依各自正式契約，不直接套用本內頁示例。

## T05｜版面配置與 RWD

- 依已確認構圖與案件內容決定結構：水平／垂直排列用 flex row／column；明確網格用 grid。只有真實疊層或脫離文件流的元素才 absolute。
- absolute 必須確認定位父層、overflow、層級及 pointer-events，不能只抄 x/y。一般對齊、欄位排列與留白不得大量使用 absolute。
- 填滿容器、隨內容伸展、固定／自然高度需配合本案實際內容。客戶字數變多時合理調整，不能裁掉文字或用固定高度掩蓋溢出以假裝符合已確認構圖。
- 保留資訊層級與圖片主體；檢查長標題、多行文案、不同圖片比例、清單數量、手機導覽、表單與必要操作。修正橫向溢出、遮擋與錯位，不任意刪除內容或既有 RWD。
- 內頁側欄／分類選單在小螢幕**統一改為下拉形式**（EVO 系統既有行為，2026-09-11 使用者指定）；使用 EVO 此功能的案件採此行為，不自創抽屜、彈窗；其他平台依本案契約。
- 電商（購物車）與會員 icon 小螢幕**留在 header**，不移去別處（EVO 系統既有行為，2026-09-11 使用者指定）；只有 header 跟隨的行動按鈕（如訂位、預約類 CTA）才在小螢幕置底固定於畫面下方。
- 本案實際驗證尺寸要記錄；公司尚未定案的尺寸、容差與細則不自行補成正式規定。

## T06｜Common、root 與共用樣式

- 實作前讀本案 `_common.scss`。既有 reset、container、spacing、title、button、image、RWD utility 符合用途就直接使用，不在頁面 SCSS 重寫。
- 全站品牌、文字、背景、字級與間距優先對應已存在且語意符合的 Common token；依已確認品牌更新案件值，保留既有名稱，不逐區重複硬寫同一全站品牌值。
- 完全符合的 Common class 直接使用；用途相同但部分屬性不同時，加短別名並在區塊根下覆寫差異；核心用途不同或需大量反向覆寫時不用。
- 沒有合適 token／class 時，先寫有依據的區塊值，記共用候選，不為每個數值中斷切版。
- 不自行新增自訂 root token，不在單頁或區塊輸出另一份 `:root`。全站變數依案件 Common 管理，沿用案件既有定義位置；Swiper 優先沿用套件預設值，需要全站調整時才依 T11 在此集中覆寫原生 CSS 變數，不重複宣告預設值或另造同義變數。
- 字級需配合版面調整時，優先由案件 Common 已有且用途相符的字級變數搭配 `calc()` 計算，讓全站基準調整時維持字級比例，避免各區塊任意寫固定數值。主標題使用適合標題的變數，提示文字使用適合提示的變數；不要只因數值接近，就拿提示文字變數控制主標題。確認 `--FontSizeHint` 存在且用途相符時，可使用 `font-size: calc(var(--FontSizeHint, 16px) * 2);`；範例備用值與倍率依案件設定，不是全站固定規格。手機版依字數、換行與版面調整倍率，不強迫所有尺寸使用同一比例。沒有合適變數或計算方式無法合理呈現時，才使用有依據的明確數值，不為計算另建 root 變數。
- 每個 `var()` 都要有合理 fallback。變數名稱及用途以案件 Common 為準。
- 一般內容區優先使用現有 `.section-spacing`、`.section-spacing-top`、`.section-spacing-bottom`，同用途不要再疊加固定 padding。滿版圖片／影片、固定比例或輪播舞台可依構圖例外，需有明確理由。
- 區塊容器**依資料量與內容型態選級距**（2026-09-11 使用者修訂），`container-85` 是無特別理由時的預設，不是每區固定答案。選法以已確認構圖與官方參考站的用法為依據：文章列表、窄欄文字收窄（如 70／75）提高可讀性；一般內容區 85；資料飽滿或圖區放寬（90／95／fluid）。選 85 以外的級距在該區塊註記依據（資料量、已確認構圖對應或參考站做法）即可，不需提案；不因已確認構圖「看起來」較窄就縮，要有內容理由。
- 版心一律**直接在 HTML 掛 Common 既有的 `container-95`～`container-60`／`container-fluid` class**，不另造功能相同的自訂 class（如自定義 `tpl-container` 再寫一次寬度）也不在區塊 SCSS 重定義版心寬。系統版型與後台整合認的是這組官方 class；自造同義 class 在交接時會對不上（2026-09-11 年年3／大自然2 實測發現兩案都繞過了這組）。
- gap 處理 flex／grid 子項間距；子項需要完整可選取留白時使用自身 padding。gap 不取代區塊本身必要內距。

## T07｜SCSS 結構與寫法

### 檔案分工

依下列職責拆檔，SCSS 放在本案既有工程的 scss/；不為符合資料夾名稱擅自搬移案件。既有框架編譯入口不同時記錄對應，不建立第二套入口：

| 檔案 | 用途 |
|---|---|
| `_common.scss` | 全站共用變數與樣式 |
| `_header.scss`、`_footer.scss` | 共用 Header、Footer 樣式 |
| `_index.scss` | 首頁專用樣式 |
| `_innerpage-default.scss` | 多個內頁共同使用的基礎樣式 |
| `_about.scss`、`_careers.scss`、`_contact.scss` 等 | 依案件頁面用途命名的專用樣式 |
| `evomni-root.scss` | 靜態切版的共用樣式入口，只匯入約定共用檔 |
| `evomni-root.css` | 共用編譯輸出，由各頁 HTML 引用，不直接手改 |
| 本頁編譯入口與 CSS（如 `about.scss` → `about.css`） | 只輸出本頁樣式，由對應 HTML 引用；名稱與路徑沿用既有工程 |

- 使用者範例另有 `_downloads.scss`、`_knowledge.scss`、`_maintenance.scss`、`_news.scss`、`_team.scss`；依實際案件頁面建立，不將範例清單當成每案必備檔案。
- 切版時就分好共用與單頁來源。全站變數、字體、容器與元件放 Common／共用檔；跨內頁 Hero、CTA、麵包屑等放 `_innerpage-default.scss` 或既有共用元件檔，不藏在某一頁的專屬 SCSS。各頁檔只寫本頁樣式及必要差異。
- 每頁 HTML 只引用約定共用 CSS、本頁 CSS 與實際需要的套件 CSS；例如 `about.html` 載入 `evomni-root.css` 與 `about.css`，不載入其他頁面 CSS。首頁樣式同樣由首頁單獨引用。共用與單頁分開編譯，不能把所有頁面重新包進共用 CSS 掩蓋依賴。
- 沿用既有編譯工具與匯入語法，記錄「SCSS 來源 → 編譯 CSS → 引用 HTML」。底線 partial 可透過本頁薄入口輸出；已有多入口或框架按頁輸出就沿用，不強制新增 `pages/`、另一套建置工具或第二份相同樣式。單頁需要 Sass 變數／mixin 時使用既有編譯依賴，避免再次輸出整份 Common CSS。
- 單頁選擇器限縮在本頁／區塊作用域，不能無意間修改其他頁共用選擇器。保留合理的共用基礎與單頁覆寫，不因 selector 重複就刪除；檢查實際載入順序、選擇器權重及 computed style，不能只認為後載入就一定覆蓋。
- 上述是靜態製作與校稿的資源分工；EVO 正式站的全站／單頁輸出由工程師按本案轉檔方式對應同一份來源。使用者回報 evo266200 正式 root 仍須保留 common、index、innerpage-default、header、footer，其他內頁已有各自 CSS；這是該案現況，不能據此要求所有新案把 index 放進全站 root，也不能在既有站未核對前移除 index。

### 區塊寫法

- 同一自製區塊的一般樣式集中在自己的 `.designer-tpl-{語意名稱}` 根內巢狀撰寫；平台元件則以契約原有根 class 限縮樣式，不另加或改成 designer-tpl；子元素、偽元素與互動狀態收在所屬父層。修改時回原位置整理，不零散追加覆寫。跨頁共用樣式仍放共用檔，各頁只保留自身差異。
- RWD 依斷點集中：同一份 SCSS 中，相同條件的斷點集中成一個最外層 `@media`，其內再按區塊巢狀整理；不將 RWD 的 `@media` 放進個別元素或區塊根內。不跨檔把不同頁面的樣式混在一起。
- 集中整理與將 RWD 移到檔尾僅適用於不改變原始覆寫結果的情況；不得跨越會影響 cascade 的規則強行合併或搬移。既有已確認樣式的斷點保真優先於排版慣例：無法確認等效時，保留原本分散的查詢及相對順序，說明原因，不為滿足「集中成一個」改變生效結果。整理後依本案範圍檢查受影響斷點與重疊區間。
- RWD 區集中放在該檔的一般樣式之後，沿用案件斷點與覆寫順序；同時命中的條件須確認最終樣式正確。這是依斷點整理，不是允許任意追加重複覆寫。尺寸依案件內容決定，本規則不新增固定斷點。
- 斷點保真（切版 → 編譯 → EVO 轉檔／匯入）：以設計師已確認的 SCSS 及其編譯 CSS 為唯一樣式基準，保留 `@media` 的條件、數值、單位、比較運算子、規則相對順序與生效範圍。不得為適應工具排序而自行新增 `.001px`／epsilon 邊界、將 `max-width` 改成另一組 range 條件、拆成互斥 band 或搬遷屬性。來源原本有意重疊的查詢仍依原 cascade 保留，不一律改成互斥；來源本身有缺陷時回原 SCSS 修正並記錄，不以轉檔補償偷偷改設計。
- 若編輯器／轉檔工具無法保留上述基準，列出來源與輸出的 media／順序差異、受影響頁面及重現尺寸，停止該成果的匯入／交付／發布，回報工程師處理；不默默接受工具改寫、不要求設計師遷就奇怪斷點，也不直接關閉排序補償而忽略既有覆寫順序問題。其他不受影響的工作可繼續；修工具、匯入與發布仍依本次授權。

```scss
.designer-tpl-about {
  .main-title {
    // 一般標題樣式
  }
}

.designer-tpl-service {
  .card-box {
    // 一般卡片樣式
  }
}

// 以下 48rem 僅示意組織方式，實際斷點依案件設定。
@media (max-width: 48rem) {
  .designer-tpl-about {
    .main-title {
      // 此斷點的標題調整
    }
  }

  .designer-tpl-service {
    .card-box {
      // 同一斷點的卡片調整
    }
  }
}
```

- 一般巢狀二至三層，必要最多四層。偽元素、狀態與 media 不視為新增 HTML 結構層；`:is()`／`:where()` 可整理相關條件，但不能用來掩蓋過長 selector。
- 不使用 `!important`；整理時保留 cascade、權重與來源順序，不因合併 selector 改壞原本覆寫。刪除前先查 HTML 與 JS 動態產生的 class，確認無使用才移除空規則或失效規則。
- CSS 優先使用簡潔的簡寫形式，例如 `padding: 24px`、`border`、`border-radius`；含 `var()` 也適用，不因使用變數就拆成四邊或四角。
- 只有個別方向需要分開設定，或新版系統已確認有解析限制時，才拆寫必要屬性。限制須有本案實測或新版規格依據，不沿用舊系統假設。修改簡寫時確認不會重設原本需要保留的其他屬性。
- 範例變數先確認本案 Common 已有且用途相符；備用值與數值依案件設定，不是統一設計值。
- 不自行替圖片加上 `filter`、`mix-blend-mode` 等效果。已確認且不隨互動改變的調色、明暗、模糊或合成效果，能在圖片本身處理就優先輸出處理後素材，保留原檔，記錄素材來源與處理版本。確實需要隨互動或背景變化的效果才使用 CSS，限縮作用範圍並在實際畫面檢查捲動及動畫效能；不以大面積濾鏡補救素材問題。

```scss
.designer-tpl-about {
  .card-box {
    padding: 24px;
    border: 1px solid var(--BorderColorPrimary, #333);
    border-radius: var(--BtnBorderRadius, 0);
  }
}
```

## T08｜滑鼠、觸控與鍵盤狀態

- 互動元件 hover 必須放在 `(hover: hover) and (pointer: fine)` 內；不是只依畫面寬度判斷是否有滑鼠。
- 相同回饋以 `:is(:active, :focus-visible)` 放在 media 外，保留觸控按下及鍵盤操作。不得移除可見焦點而沒有等效提示。
- `hover`、`:active`、`:focus-visible` 狀態樣式收在所屬元素內，不另散落重複 selector。滑鼠能力判斷的 `@media (hover: hover) and (pointer: fine)` 隨元素狀態撰寫；RWD 尺寸斷點則依 T07 集中於檔案外層，兩者分開處理。實際確認 Tab 操作、焦點可見與手機點按，不能只看 hover 截圖。

```scss
.designer-tpl-about {
  .action-link {
    @media (hover: hover) and (pointer: fine) {
      &:hover {
        text-decoration: underline;
      }
    }

    &:is(:active, :focus-visible) {
      text-decoration: underline;
    }

    &:focus-visible {
      outline: 2px solid currentColor;
      outline-offset: 3px;
    }
  }
}
```

## Common 適用補充

新案尚無 Common 時，依已確認視覺系統集中建立一次；不可在各區各造 root。官方 container class 規則用於有此基底的案件，缺基底先核對，不假裝 class 已存在。沉浸式滿版、疊層與釘選舞台可依已確認構圖例外，記錄理由；不能為容器級距簡化確認過的設計。
