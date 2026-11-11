---
name: Lin-EVO
description: 依 Lin-EVO 切版規範實作、修改與校稿品牌及企業網站的 HTML、SCSS、JavaScript、Swiper 與共用頁面，適用 Figma／設計稿轉網頁及既有前端修正。依案件決定尺寸與 RWD 範圍；不啟動品牌提案、Eagle 整理或整體視覺方案確認流程。
---

# Lin-EVO 網頁切版與校稿

## 來源與本機安裝位置

本 Skill 由 Lin-EVO repo 維護；實際來源以目前工具 Skills 目錄內的 `.Lin-EVO-install.json` 為準，`source` 指向安裝器／來源管理 repo，`skill_path` 指向本 Skill。來源管理 repo 有 `skill-sources.json` 時依其設定解析，不照抄其他電腦的絕對路徑，也不假設安裝一定採連結模式。

Miffy-EVO 由獨立 repo 維護。安裝器可依 `skill-sources.json` 分別定位兩個來源；只在對應 Git 乾淨、位於 `main`、origin 正確且能 fast-forward 時更新指定 Skill。更新 Lin-EVO 不代表 Miffy-EVO 或其工程師套件已更新，反之亦然。

把使用者視為網頁設計師／前端實作者。以繁體中文與台灣用語溝通，先做出完整可用的授權成果，再討論細節；說明問題時直接給可執行的修正。

本 Skill 是 Lin-EVO 的工程規範獨立版。明確的使用者指示優先，其次為案件已確認規格及既有工程；本 Skill 補足未指定的切版慣例。局部修改不擴大為全站改名或重構。

## 每輪工作：偵測 Git、更新、重讀、再工作

Lin-EVO 共用工程規範來源為 https://github.com/world-yingcen/lin-skill 。Miffy-EVO 可由獨立 repo 維護，實際位置以各工具的安裝紀錄、`skill_path` 與來源管理資料夾的 `skill-sources.json`（若有）為準，不假設兩者在同一 repo。各方案可保留設計流程、動態上限與 RWD 順序，但不另存共用規範副本。Lin 的 Git 更新不代表 Miffy 或工程師 `evomni-html` 已更新；工程師套件仍由人工提供。維護來源或人工替換套件後有未提交修改時保留現況，按已確認來源做必要本機同步，不為更新而自行提交。

- 每輪工作前（含續作、修改與校稿）核對來源與安裝模式，偵測到 Git 來源就先安全更新，再重讀 SKILL.md 與本輪需要的 references；不要求使用者每次另說更新，同一 repo 每輪一次。維護此 repo 本身時先檢查 Git 狀態，保留工作中修改，不為更新覆蓋現況。
- 依當前執行工具的 Skills 目錄讀取 `.Lin-EVO-install.json`，使用其 source 定位獨立來源。Codex 預設 `~/.codex/skills`（有 CODEX_HOME 時遵守），Claude 預設 `~/.claude/skills`；不因同機有另一工具就更新錯位置。
- **連結模式（mode=link）**：核對 Skill 捷徑確實指向安裝紀錄的 `skill_path`；舊紀錄沒有此欄位時才使用 source 下的 Lin-EVO。每輪工作前偵測到 Git 就執行 `python3 <source>/install.py --update --skill Lin-EVO --target <本次實際 Skills 目錄>`，再重讀。直接使用更新後的來源，不需額外複製或改回副本；本機修改也直接反映在來源，但未提交修改時保留現況並回報更新未完成。
- **複製模式（mode=copy）**：核對 source 的 install.py 與 Git origin 確為此 repo，再執行 `python3 <source>/install.py --update --skill Lin-EVO --target <本次實際 Skills 目錄>`。工具只接受乾淨 main、指定 origin 及 fast-forward，不 reset、stash、強制合併或覆蓋修改過的副本。
- 成功後重新讀取實際安裝位置的 SKILL.md 全文及本輪需要的 references，沿用原案件確認與範圍。記錄來源 commit、更新成功與否；不能只因檔案存在就說是遠端最新；連結模式未查遠端時標示「直接讀本機 Git 來源」，不宣稱已拉取最新版。
- 網路／權限／分歧／本機修改導致失敗時，明說「尚未確認最新版」，讀現有規範後繼續不受影響工作；缺少必要契約的部分列待確認。沒有紀錄或来源不明時，先確認安裝方式，不自行猜來源、覆蓋或執行任意 repo 的腳本。
- 使用者已授權：本機缺少本輪需要的 Skill 時，從已確認來源直接安裝，不重複請示。Lin-EVO 從上述 repo 安裝完整 Lin-EVO，只有 Lin-EVO 需求時指定 `--skill Lin-EVO`；Miffy-EVO 使用其已確認的獨立來源或來源管理設定，不以 lin-skill 內的舊副本取代。核對當前工具位置與安裝紀錄，只安裝相關 Skill 及必要依賴，同名不同來源或本機修改不覆蓋。缺來源／帳號／權限時列具體缺口；沒有本機操作能力的網頁／App 不假裝已安裝，改用已啟用 Skill 或提供上傳方式。此授權不擴大為安裝應用程式、JS 套件、工程工具庫或改系統權限；EVO 套件仍依 vendor 契約。安裝後驗證檔案與來源並重讀規範，需重新載入時如實告知，不把安裝成功當成已驗收。
- 當高效或整體視覺呼叫 Lin-EVO 時只接工程工作，不重啟獨立方案流程：高效保留五角色、母版確認、簡單動態限制及原 RWD 順序；整體視覺保留方向／視覺／動態關卡及 2560×1280 桌機優先。使用者依操作手冊已指定桌機後接續 RWD 時直接依確認節點接續，否則另確認 RWD 範圍。

## 開始工作

**每輪開始製作、續作、修改或校稿前，自動確認案件 Git 與遠端的差異，同一 repo 每輪一次，不等使用者提醒。** 這是案件版本檢查，與上方 Skill 規範更新分開處理；純說明或唯讀檢查不自動合併案件檔案。

先查案件階段；已成功轉 EVO 者依下方「已轉 EVO 案件與換電腦交接」改至後台，跳過已停用原 Git 的更新／推送流程。

- 以 `git rev-parse --show-toplevel` 定位案件 repo，檢查工作目錄（含未追蹤檔案）、目前分支與 upstream。針對已設定的 upstream 遠端執行 fetch，成功後才比對 HEAD 與 upstream 的 ahead／behind 數量；不猜遠端或分支。VSCode 左下角沒有數字、舊的遠端追蹤紀錄或本機檔案存在，都不能當成遠端最新的證明。
- 簡短回報「已同步、待拉取、尚未推送、雙方都有新提交（分歧）或無法確認」，另列有無未提交修改。只有 fetch 成功且 ahead／behind 都為 0 才稱提交已同步；ahead 大於 0 不代表需要自動 push。
- 已授權的製作工作中，只有工作目錄乾淨、有 upstream 且單純落後時，才對已取得的 upstream 執行 `git merge --ff-only @{upstream}` 安全更新，再核對狀態並讀取案件檔案。有未提交修改或分歧時保留現況，先詢問處理方式，不自動合併或開始受影響檔案的修改；使用者已明確要求保留現況繼續時依其範圍執行，不重複詢問。
- 缺 upstream、detached HEAD、無 Git 工具、網路／權限失敗時，回報「尚未確認遠端最新版」及原因；可先做不受影響的唯讀盤點，需要帶著操作時先詢問。不是 Git 的資料夾不自行初始化。不為通過檢查而 reset、stash、rebase、切換分支或自行 commit／push；提交與推送仍須另依使用者授權。

**切版開始與檔案檢查都必讀指定基底**：[LIN 切版基底](references/starter-baseline.md)。先讀內附 `assets/evo-starter/06-切版/` 的 Common、Header 與入口檔；新案以完整基底建立案件副本，既有案以它比對差異，不直接覆蓋。不得省略基底、自行建立替代 Common，或只檢查檔案分工。

先讀案件說明、既有修改、實際 HTML／SCSS／JS、Common、共用元件、套件版本、編譯與預覽入口。沿用現有框架、命名及初始化，不為套用規範重寫整份程式。

**樣式規範不能只檢查檔案分工。** 涉及切版、CSS／SCSS 修改或規範校稿時，先讀 [T06 Common／root](references/html-css-rules.md#t06commonroot-與共用樣式)，核對實際變數定義與使用，再處理本輪樣式；完成前依 [Common 與 root 檢核](references/implementation-review.md#common-與-root-檢核) 回報結果。`evomni-root.scss` 的檔案分工與 CSS `:root` 的變數契約是兩項不同檢查，前者通過不代表後者通過。

**開始切版或修改 SCSS 前，必須先檢查、補齊並驗證本案編譯流程**，依 [切版前的編譯設定與驗證](references/html-css-rules.md#切版前的編譯設定與驗證) 執行，不等使用者另外提醒。已有可用流程就沿用；缺少時在案件範圍準備 VSCode 設定，確認存檔編譯、共用／單頁輸出及 HTML 引用。需要安裝擴充功能或改用其他編譯方案時先取得授權；不能操作本機 VSCode 時提供設定檔與操作步驟，記錄待使用者執行及待驗項目，不把設定檔已建立當成編譯已通過。

建立或接續 Git 專案時，確認 repo 根目錄 `.gitignore` 包含 `.DS_Store`，忽略 macOS 在所有子目錄產生的資料夾資訊檔；保留既有規則。已追蹤檔案的處理與交付排除方式見 [實作與校稿](references/implementation-review.md#系統檔案與-git-追蹤)。

預計使用 EVO 後台的案件，切版前必讀 [EVO 範本查核](references/evo-preflight.md)。由 AI 查工程師套件，在切版時同步實作已核對的逐筆編輯結構與欄位標記，不只列成後續轉檔待辦；同一份來源仍提供完整靜態校稿與互動。設計師不用判斷技術標記；缺契約逐區列待確認。工程師後續處理匯入、必要接入及編輯／儲存／發布驗證，不自動啟動匯入或打包。

先依 [EVO 範本查核](references/evo-preflight.md) 判斷匯入方式。**採整站 HTML 匯入的案件**，切版前直接讀取本機 `evomni-html` 的版本與規範，在來源完成頁型、可編輯結構、欄位、共用區及資源安排，並於切版階段執行套件檢查；不等 Miffy-EVO 才重建。工程師套件由人工更新，Lin-EVO 不複製規格或鎖版。以下舊平台專用條文與 references 若涉及搜尋、詢問車、選單、FAQ、表單、資料標記、匯入邊界或套件載入，僅適用原流程；整站 HTML 案件以本次讀取的工程師契約為準，其餘視覺、程式品質、SEO 與 RWD 規範照常適用。

**分類側選單優先沿用系統範本**：遇到產品、文章等分類側選單，先讀 [evo266125 left_menu001](references/evo-left-menu-reference.md)，沿用已確認 HTML、class、data 與原生手機下拉操作，再依案件設計調整 CSS，不先自造側選單。Blog／專業知識等「側邊導覽＋文章列表」版型也必須使用此結構，包含只有所有／熱門／最新文章的單層導覽；搜尋與熱門關鍵字另列獨立區塊。這是使用者指定的優先結構，匯入契約衝突時列明差異，不默默換結構。

**Blog 統一公版**：Blog／部落格／專業知識側欄＋文章列表優先沿用 [evo260865 Blog 公版](references/evo-blog-reference.md)，使用 left_menu001（含最新／熱門 bloglinks）、search001、hotkeywords001、bloglist001，再依設計改 CSS；不只做外觀相似的自訂結構。搜尋屬系統 search001，不套 contact-form；文章卡片不套一般 CTA 結構。

**FAQ 統一使用系統範本 HTML**：依使用者 2026-11-04 指定，凡製作或修改 FAQ，必讀 [FAQ 統一系統結構](references/evo-faq-reference.md)，沿用 evo266125 的 `tpl-faq001` 層級、標籤、class 與 data 屬性；CSS／SCSS 外觀可改，HTML 結構不另造。此項明確指定優先於上述「FAQ 僅適用舊流程」的概括分流；匯入契約有衝突時列出待工程師確認，不自行改造範本。

**隱私權政策統一使用公版**：依使用者 2026-11-04 指定，凡首次製作網站或補做隱私權政策頁，必讀 [隱私權政策公版](references/evo-privacy-reference.md)。政策正文固定放在 `.innerpage-body`，逐字沿用公版內容與順序，只替換公司完整名稱；版型與指定樣式沿用公版，字型、字級、文字色、標題色、間距等已有本案 `:root` 變數者必須接本案變數，不複製參考站品牌值，讓政策頁與當下網站一致。

**所有電子表單統一使用 contact-form 公版 HTML**：依使用者 2026-11-04 指定，只要頁面出現電子表單，不限聯絡我們或其他用途，都必讀 [contact-form 公版結構](references/evo-eforms-reference.md)，沿用 evo266125 的 `.contact-form`、`form.eforms-wrapper`、欄位層級、class、data、驗證及送出結構；只允許用 CSS／SCSS 調整外觀，不改公版 HTML／JS、不自造另一套表單。表單 ID、action、token、欄位、選項及驗證值由本案平台輸出，不跨案複製。此項明確指定不受下方舊平台概括分流限制；若工程師套件有衝突，保留公版並列明差異確認。

**既有舊平台流程的案件**，每個案件都要有搜尋結果頁，首次網站製作時納入必備頁面，不能只做 Header 搜尋按鈕。製作前必讀 [搜尋頁指定參考](references/evo-search-reference.md)，公版 HTML／JS 不修改；CSS 以系統共用參考為基準，可依案件確認需求調整；既有案局部修正若尚未有搜尋頁，列為待補項目，不因局部修正擅自重做整站。

設計稿是主要視覺依據。核對容器、區塊高度、留白、字型與字重、行高、圖片比例與裁切、對齊及互動狀態；有 Figma 或參考圖時實看，不憑文字印象還原。字型需確認實際載入，缺檔或暫代素材如實標記。

尺寸、頁面、RWD、功能及交付方式依本案要求，不固定 2560×1280。完整網站任務須涵蓋 desktop、tablet、mobile；使用者明確限定桌機／區塊時依範圍執行。局部修改保留既有 responsive，檢查可能受影響的斷點，不藉此另設整套手機版。

HTML、CSS、JavaScript 與互動套件的寫法，以過去五年內發行且仍屬大眾使用範圍的 Chrome、Edge、Firefox、Safari 與 iOS Safari 可穩定支援為基準；案件既有 browser support／Browserslist 或平台契約更嚴格時，以較嚴格者為準。不把實驗性、需旗標開啟或支援仍不完整的功能當成唯一實作；確有需要時先查相容性，並提供不影響內容閱讀與主要操作的 fallback 或漸進增強。不得只因最新版瀏覽器可用就宣稱相容性完成，交付時記錄實際測試的瀏覽器與版本。

資訊足夠就直接做；小幅不確定先依現況判斷。只有選擇會改變已確認設計、重大架構或不可逆結果時才提出具體方案請使用者決定，已有授權不重問。

HTML 的 `<header>` 標籤只用於全站 Navi／主要導覽；其他區塊、內頁標題、卡片與搜尋結果標題區一律不用 `<header>`，改用保留原 class 的 `<div>` 等容器。詳見 [HTML／SCSS](references/html-css-rules.md#t04html命名與語意)，校稿時須檢查。

**公司內部規定：每個完整頁面必須有且只有一個 `<h1>`**，不是 Google 的排名硬性要求；`<h2>`～`<h6>` 依內容父子關係逐層安排，不往下跳級、不用標題標籤控制字級。校稿以共用元件及 JS 載入後的完整 DOM 核對，詳見 [HTML／SCSS](references/html-css-rules.md)。

**以下為舊平台流程規則；整站 HTML 匯入依工程師套件處理系統頁與連結。**

**詢問車頁／抽屜與搜尋頁的公版 CSS 可依案件調整，公版 HTML／JS 不可修改**，此限制不擴及產品頁；產品頁可以新增 `.inquiry-group` 分組並調整加入按鈕位置，保留原生加入功能的識別與綁定；詢問車依 [指定功能架構](references/evo-inquiry-cart-reference.md) 保留產品加入、Header 清單、確認頁與原生表單。使用者要求的靜態 Demo 可獨立模擬，正式接入前必須停用，不能同時綁兩套操作。產品分類選單依 [left_menu001](references/evo-left-menu-reference.md) 沿用原生結構與操作，桌機以 CSS 套案件外觀，手機版下拉邏輯是公版，不改寫或另綁一套事件。

**Header 統一基底**：整體 HTML 結構與預設 CSS（含跟隨按鈕）一律先使用 [evo266200 內附基底](references/evo-header-reference.md)，再依案件修改；不再混用 evo266125 Header 按鈕規則。

**連結型按鈕統一結構**：一般導頁 CTA 必須使用 `div.btn-group > a.btn-link`，文字直接放在 a 內；依設計擇一搭配 `main-btn`（主色）、`sub-btn`（輔色）、`outline-btn`（外框）。Header 跟隨按鈕是系統例外，保留 `btn-item`、`btn-text`、`btn-icon-box` 與 SVG，依 [Header 按鈕結構](references/evo-header-reference.md#按鈕與語系) 與 [指定 CSS 基準](references/evo-header-reference.md#header-跟隨按鈕-css-基準) 一起實作。一般按鈕詳見 [連結型按鈕規範](references/html-css-rules.md#連結型按鈕統一結構)。

**列表／內容頁替換容器必須完整輸出**：只要使用 `detail-content` 替換邊界，同一個 `<div>` 必須同時具有 `data-list-group-container="true"` 與 `data-replace="detail-content"`。兩個屬性不得省略其中一個、不得拆到父子層；只有 `<div data-replace="detail-content">` 視為不完整結構，校稿時必須修正。完整寫法與適用範圍依 [列表頁與內容頁的替換範圍](references/shared-page-rules.md#列表頁與內容頁的替換範圍)。

## 按需讀取規範

涉及下列項目時完整讀取對應文件；同輪未變的文件不用重讀。先完成匯入方式分流；表內舊平台指定元件與 vendor 契約不套入整站 HTML 流程，該流程直接查工程師套件，不為滿足舊條文而額外植入舊標記或系統頁。

| 任務 | 必讀 |
|---|---|
| HTML、SCSS、Common、命名、版面與互動狀態 | [HTML／SCSS](references/html-css-rules.md) |
| 每頁 title、描述、標題、圖片、連結與載入效能 | [切版端 SEO 責任](references/frontend-seo.md) |
| JavaScript、Swiper、AOS、GSAP 初始化與清理 | [JavaScript](references/javascript-rules.md) |
| 捲動動畫、GSAP pin／scrub、減少動態模式 | [雙模式動態規範](references/reduced-motion.md) |
| EVO 第三方套件載入、data-vendor、Lenis 開放狀態 | [系統套件載入契約](references/evo-vendor-libraries.md) |
| Header、Footer、Nav、內頁與平台功能 | [共用頁面](references/shared-page-rules.md) |
| EVO 多層分類、共用列表設計所屬層級 | [多層分類的共用列表頁設計](references/shared-page-rules.md#多層分類的共用列表頁設計) |
| EVO 列表頁／內容頁沿用外框、主列表替換邊界 | [列表頁與內容頁的替換範圍](references/shared-page-rules.md#列表頁與內容頁的替換範圍) |
| EVO Header 樣式、捲動狀態、RWD、選單、漢堡、按鈕、語系 | [Header 指定參考](references/evo-header-reference.md) |
| 連續 marquee | [marquee 指定參考](references/evo-marquee-reference.md) |
| 內頁 breadcrumb | [breadcrumb001 指定參考](references/evo-breadcrumb-reference.md) |
| 隱私權政策頁 | [隱私權政策公版](references/evo-privacy-reference.md) |
| Blog／部落格／專業知識公版 | [Blog 公版結構](references/evo-blog-reference.md) |
| FAQ | [FAQ 統一系統結構](references/evo-faq-reference.md) |
| 每案必備搜尋頁、Header 搜尋導向與結果狀態 | [搜尋頁指定參考](references/evo-search-reference.md) |
| 產品／文章分類、Blog／專業知識側選單與手機下拉 | [left_menu001 指定參考](references/evo-left-menu-reference.md) |
| 所有電子表單、contact-form 結構與欄位樣式 | [contact-form 公版結構](references/evo-eforms-reference.md) |
| 產品加入詢問車、Header 清單、詢問表單 | [系統公版詢問車](references/evo-inquiry-cart-reference.md) |
| 開始修改、共用影響檢查與交付校稿 | [實作與校稿](references/implementation-review.md) |
| 切版完成、功能修改後與交付工程師 | [工程師交接說明](references/engineer-handoff.md) |

規範是工程約定，不能代替品牌構圖或素材。EVO 的 container、系統選單與版權列規定依對應文件適用範圍執行；其他框架不捏造 EVO 元件或後台資料綁定。

## 實作與完成

### 已轉 EVO 案件與換電腦交接

- 開工先確認案件是否已成功匯入 EVO。**已轉 EVO 的案件，原靜態 Git 專案視同廢棄，只保留查閱；任何修改請至 EVO，不再修改或 push 原 Git。**「已產生 ZIP／預檢通過」不等於已成功匯入；首次匯入前的錯誤仍在本次有效來源修正。使用者只說「EVO 案件」但狀態不明時，先查交接紀錄，不憑名稱判定。
- 尚未轉 EVO、以 Git 管理的切版案件，下班換電腦固定採「整理交接紀錄與必要檔案 → commit 並 push 成功 → 另一台 Clone／更新同一版本 → Claude 先讀交接再繼續」。不以只 commit 或另傳未推送 ZIP 代替此流程；沒有 Git 的設計準備階段不因此自行初始化。
- 沿用唯一進度檔，記錄確認成果、本輪變更、待辦、已知問題、素材與預覽位置、repo／分支及交接版本。核對本次需提交的工程、素材與必要交接紀錄；排除帳密、token、含密鑰的 .env、客供私人文件與無關檔案，交接內容不得洩漏敏感資料。
- 執行前先確認本次 repo、分支與提交範圍，詢問是否需要 Claude 帶著操作；已有明確授權不重問。沒有 Git 工具就提供步驟並請使用者回傳結果。遇到衝突、認證或推送失敗，保留工作並標示交接未完成，不 force push、不覆蓋他人修改，也不宣稱另一台已能取得。
- 換電腦後，沒有專案才 Clone；已有專案直接開啟，依「工作前確認」檢查遠端並安全更新，不重複 Clone／初始化。確認交接版本已取得，先讀進度與必要檔案，再續作原範圍。只換對話或模型時更新進度即可，不因此要求 push。

### 修改與校稿

先判斷缺陷屬於結構、樣式、JavaScript、套件、資料或環境，再用 DOM、computed style、console、network 或小型驗證找根因。修正回原始位置，不一直追加 override 或用負 margin 掩蓋占位。

視覺與動畫必須幫助品牌、閱讀或操作。輪播統一用 Swiper，區塊淡入淡出統一用 AOS，連續 marquee 在舊平台流程沿用指定 EVO 元件，整站 HTML 流程依工程師套件與既有專案實作；複雜時間軸、視差與釘選沿用既有 GSAP／ScrollTrigger 及捲動系統。其他簡單效果用原生 CSS／JS。集中可調參數，處理 resize、去重、事件解除與 prefers-reduced-motion。未用到的工具或套件不安裝。

在可用環境編譯並開啟預覽，實際看畫面與操作；校稿依 references/implementation-review.md。無瀏覽器、缺素材或缺後台時，完成可執行部分並明列未驗證範圍，不把語法檢查當視覺通過。

切版完成後必檢查網站圖片的檔案大小與格式，依 [容量與圖片格式檢核](references/implementation-review.md#切版完成後的容量與圖片格式檢核) 列出非 WebP／SVG 圖片的路徑與大小，請使用者檢核專案容量並自行轉檔；Claude 不代為轉檔、壓縮或批次處理圖片。

切版與交付前必依 [切版端 SEO 責任](references/frontend-seo.md) 逐頁檢查 title、描述、標題層級、圖片、連結與載入效能，列明已完成及工程師待確認項目。

切版完成後必須建立或更新本案唯一的 `工程師交接說明.md`，依 [交接規範](references/engineer-handoff.md) 整理實際檔案、功能注意事項、後台可編輯需求、待串接及驗收狀態；功能或資源改動後同步更新，回報文件位置，不只留在聊天裡。

完成後簡短交付：改了什麼、修改檔案、預覽／啟動方式、實測範圍及需要使用者檢查的地方。安裝本 Skill 不等於安裝 Sass／Node／GSAP，也不授權 Git 推送或部署。
