---
name: Lin-EVO
description: 依 Lin-EVO 切版規範實作、修改與校稿品牌及企業網站的 HTML、SCSS、JavaScript、Swiper 與共用頁面，適用 Figma／設計稿轉網頁及既有前端修正。依案件決定尺寸與 RWD 範圍；不啟動品牌提案、Eagle 整理或整體視覺方案確認流程。
---

# Lin-EVO 網頁切版與校稿

把使用者視為網頁設計師／前端實作者。以繁體中文與台灣用語溝通，先做出完整可用的授權成果，再討論細節；說明問題時直接給可執行的修正。

本 Skill 是 Lin-EVO 的工程規範獨立版。明確的使用者指示優先，其次為案件已確認規格及既有工程；本 Skill 補足未指定的切版慣例。局部修改不擴大為全站改名或重構。

## 每輪工作：偵測 Git、更新、重讀、再工作

共用工程規範唯一來源為 https://github.com/world-yingcen/lin-skill 。各方案可保留設計流程、動態上限與 RWD 順序，但不另存共用規範副本。

- 每輪工作前（含續作、修改與校稿）核對來源與安裝模式，偵測到 Git 來源就先安全更新，再重讀 SKILL.md 與本輪需要的 references；不要求使用者每次另說更新，同一 repo 每輪一次。維護此 repo 本身時先檢查 Git 狀態，保留工作中修改，不為更新覆蓋現況。
- 依當前執行工具的 Skills 目錄讀取 `.Lin-EVO-install.json`，使用其 source 定位獨立來源。Codex 預設 `~/.codex/skills`（有 CODEX_HOME 時遵守），Claude 預設 `~/.claude/skills`；不因同機有另一工具就更新錯位置。
- **連結模式（mode=link）**：核對 Skill 捷徑確實指向 source 下的 Lin-EVO；每輪工作前偵測到 Git 就執行 `python3 <source>/install.py --update --skill Lin-EVO --target <本次實際 Skills 目錄>`，再重讀。直接使用更新後的來源，不需額外複製或改回副本；本機修改也直接反映在來源，但未提交修改時保留現況並回報更新未完成。
- **複製模式（mode=copy）**：核對 source 的 install.py 與 Git origin 確為此 repo，再執行 `python3 <source>/install.py --update --skill Lin-EVO --target <本次實際 Skills 目錄>`。工具只接受乾淨 main、指定 origin 及 fast-forward，不 reset、stash、強制合併或覆蓋修改過的副本。
- 成功後重新讀取實際安裝位置的 SKILL.md 全文及本輪需要的 references，沿用原案件確認與範圍。記錄來源 commit、更新成功與否；不能只因檔案存在就說是遠端最新；連結模式未查遠端時標示「直接讀本機 Git 來源」，不宣稱已拉取最新版。
- 網路／權限／分歧／本機修改導致失敗時，明說「尚未確認最新版」，讀現有規範後繼續不受影響工作；缺少必要契約的部分列待確認。沒有紀錄或来源不明時，先確認安裝方式，不自行猜來源、覆蓋或執行任意 repo 的腳本。
- 使用者已授權：本機缺少本輪需要的 Skill 時，從已確認來源直接安裝，不重複請示。Lin-EVO 從上述 repo 安裝完整 Lin-EVO，只有 Lin-EVO 需求時指定 --skill Lin-EVO；其他 Skill 使用本案已指定來源或可信安裝器。核對當前工具位置與安裝紀錄，只安裝相關 Skill 及必要依賴，同名不同來源或本機修改不覆蓋。缺來源／帳號／權限時列具體缺口；沒有本機操作能力的網頁／App 不假裝已安裝，改用已啟用 Skill 或提供上傳方式。此授權不擴大為安裝應用程式、JS 套件、工程工具庫或改系統權限；EVO 套件仍依 vendor 契約。安裝後驗證檔案與來源並重讀規範，需重新載入時如實告知，不把安裝成功當成已驗收。
- 當高效或整體視覺呼叫 Lin-EVO 時只接工程工作，不重啟獨立方案流程：高效保留五角色、母版確認、簡單動態限制及原 RWD 順序；整體視覺保留方向／視覺／動態關卡及 2560×1280 桌機優先，RWD 仍須另行授權。

## 開始工作

案件工作目錄也先偵測 Git；以 `git rev-parse --show-toplevel` 定位 repo，檢查狀態、目前分支與 upstream。乾淨且有 upstream 才執行 `git pull --ff-only`，再讀 README、進度與本輪工作檔。有未提交修改（含未追蹤檔案）、分歧、缺 upstream、detached HEAD 或連線失敗時保留現況，說明更新未完成並繼續不受影響的工作。不猜分支、不 reset、stash、提交或推送來完成更新；不是 Git 的資料夾不自行初始化。

先讀案件說明、既有修改、實際 HTML／SCSS／JS、Common、共用元件、套件版本、編譯與預覽入口。沿用現有框架、命名及初始化，不為套用規範重寫整份程式。

建立或接續 Git 專案時，確認 repo 根目錄 `.gitignore` 包含 `.DS_Store`，忽略 macOS 在所有子目錄產生的資料夾資訊檔；保留既有規則。已追蹤檔案的處理與交付排除方式見 [實作與校稿](references/implementation-review.md#系統檔案與-git-追蹤)。

預計使用 EVO 後台的案件，切版前必讀 [EVO 範本查核](references/evo-preflight.md)。由 AI 查工程師套件，在切版時同步實作已核對的逐筆編輯結構與欄位標記，不只列成後續轉檔待辦；同一份來源仍提供完整靜態校稿與互動。設計師不用判斷技術標記；缺契約逐區列待確認。工程師後續處理匯入、必要接入及編輯／儲存／發布驗證，不自動啟動匯入或打包。

每個案件都要有搜尋結果頁，首次網站製作時納入必備頁面，不能只做 Header 搜尋按鈕。製作前必讀 [搜尋頁指定參考](references/evo-search-reference.md)，公版 HTML／JS 不修改；CSS 以系統共用參考為基準，可依案件確認需求調整；既有案局部修正若尚未有搜尋頁，列為待補項目，不因局部修正擅自重做整站。

設計稿是主要視覺依據。核對容器、區塊高度、留白、字型與字重、行高、圖片比例與裁切、對齊及互動狀態；有 Figma 或參考圖時實看，不憑文字印象還原。字型需確認實際載入，缺檔或暫代素材如實標記。

尺寸、頁面、RWD、功能及交付方式依本案要求，不固定 2560×1280。完整網站任務須涵蓋 desktop、tablet、mobile；使用者明確限定桌機／區塊時依範圍執行。局部修改保留既有 responsive，檢查可能受影響的斷點，不藉此另設整套手機版。

HTML、CSS、JavaScript 與互動套件的寫法，以過去五年內發行且仍屬大眾使用範圍的 Chrome、Edge、Firefox、Safari 與 iOS Safari 可穩定支援為基準；案件既有 browser support／Browserslist 或平台契約更嚴格時，以較嚴格者為準。不把實驗性、需旗標開啟或支援仍不完整的功能當成唯一實作；確有需要時先查相容性，並提供不影響內容閱讀與主要操作的 fallback 或漸進增強。不得只因最新版瀏覽器可用就宣稱相容性完成，交付時記錄實際測試的瀏覽器與版本。

資訊足夠就直接做；小幅不確定先依現況判斷。只有選擇會改變已確認設計、重大架構或不可逆結果時才提出具體方案請使用者決定，已有授權不重問。

HTML 的 `<header>` 標籤只用於全站 Navi／主要導覽；其他區塊、內頁標題、卡片與搜尋結果標題區一律不用 `<header>`，改用保留原 class 的 `<div>` 等容器。詳見 [HTML／SCSS](references/html-css-rules.md#t04html命名與語意)，校稿時須檢查。

**公司內部規定：每個完整頁面必須有且只有一個 `<h1>`**，不是 Google 的排名硬性要求；`<h2>`～`<h6>` 依內容父子關係逐層安排，不往下跳級、不用標題標籤控制字級。校稿以共用元件及 JS 載入後的完整 DOM 核對，詳見 [HTML／SCSS](references/html-css-rules.md)。

**詢問車頁／抽屜與搜尋頁的公版 CSS 可依案件調整，公版 HTML／JS 不可修改**，此限制不擴及產品頁；產品頁可以新增 `.inquiry-group` 分組並調整加入按鈕位置，保留原生加入功能的識別與綁定；詢問車依 [指定功能架構](references/evo-inquiry-cart-reference.md) 保留產品加入、Header 清單、確認頁與原生表單。使用者要求的靜態 Demo 可獨立模擬，正式接入前必須停用，不能同時綁兩套操作。產品分類選單依 [left_menu001](references/evo-left-menu-reference.md) 沿用原生結構與操作，桌機以 CSS 套案件外觀，手機版下拉邏輯是公版，不改寫或另綁一套事件。

## 按需讀取規範

涉及下列項目時完整讀取對應文件；同輪未變的文件不用重讀。

| 任務 | 必讀 |
|---|---|
| HTML、SCSS、Common、命名、版面與互動狀態 | [HTML／SCSS](references/html-css-rules.md) |
| 每頁 title、描述、標題、圖片、連結與載入效能 | [切版端 SEO 責任](references/frontend-seo.md) |
| JavaScript、Swiper、AOS、GSAP 初始化與清理 | [JavaScript](references/javascript-rules.md) |
| 捲動動畫、GSAP pin／scrub、減少動態模式 | [雙模式動態規範](references/reduced-motion.md) |
| EVO 第三方套件載入、data-vendor、Lenis 開放狀態 | [系統套件載入契約](references/evo-vendor-libraries.md) |
| Header、Footer、Nav、內頁與平台功能 | [共用頁面](references/shared-page-rules.md) |
| EVO 選單、漢堡、按鈕、語系 | [Header 指定參考](references/evo-header-reference.md) |
| 連續 marquee | [marquee 指定參考](references/evo-marquee-reference.md) |
| 內頁 breadcrumb | [breadcrumb001 指定參考](references/evo-breadcrumb-reference.md) |
| FAQ | [tpl-faq001 指定參考](references/evo-faq-reference.md) |
| 每案必備搜尋頁、Header 搜尋導向與結果狀態 | [搜尋頁指定參考](references/evo-search-reference.md) |
| 產品分類選單、桌機側欄與下拉外觀 | [left_menu001 指定參考](references/evo-left-menu-reference.md) |
| 產品加入詢問車、Header 清單、詢問表單 | [系統公版詢問車](references/evo-inquiry-cart-reference.md) |
| 開始修改、共用影響檢查與交付校稿 | [實作與校稿](references/implementation-review.md) |
| 切版完成、功能修改後與交付工程師 | [工程師交接說明](references/engineer-handoff.md) |

規範是工程約定，不能代替品牌構圖或素材。EVO 的 container、系統選單與版權列規定依對應文件適用範圍執行；其他框架不捏造 EVO 元件或後台資料綁定。

## 實作與完成

先判斷缺陷屬於結構、樣式、JavaScript、套件、資料或環境，再用 DOM、computed style、console、network 或小型驗證找根因。修正回原始位置，不一直追加 override 或用負 margin 掩蓋占位。

視覺與動畫必須幫助品牌、閱讀或操作。輪播統一用 Swiper，區塊淡入淡出統一用 AOS，連續 marquee 沿用指定 EVO 元件；複雜時間軸、視差與釘選沿用既有 GSAP／ScrollTrigger 及捲動系統。其他簡單效果用原生 CSS／JS。集中可調參數，處理 resize、去重、事件解除與 prefers-reduced-motion。未用到的工具或套件不安裝。

在可用環境編譯並開啟預覽，實際看畫面與操作；校稿依 references/implementation-review.md。無瀏覽器、缺素材或缺後台時，完成可執行部分並明列未驗證範圍，不把語法檢查當視覺通過。

切版完成後必檢查網站圖片的檔案大小與格式，依 [容量與圖片格式檢核](references/implementation-review.md#切版完成後的容量與圖片格式檢核) 列出非 WebP／SVG 圖片的路徑與大小，請使用者檢核專案容量並自行轉檔；Claude 不代為轉檔、壓縮或批次處理圖片。

切版與交付前必依 [切版端 SEO 責任](references/frontend-seo.md) 逐頁檢查 title、描述、標題層級、圖片、連結與載入效能，列明已完成及工程師待確認項目。

切版完成後必須建立或更新本案唯一的 `工程師交接說明.md`，依 [交接規範](references/engineer-handoff.md) 整理實際檔案、功能注意事項、後台可編輯需求、待串接及驗收狀態；功能或資源改動後同步更新，回報文件位置，不只留在聊天裡。

完成後簡短交付：改了什麼、修改檔案、預覽／啟動方式、實測範圍及需要使用者檢查的地方。安裝本 Skill 不等於安裝 Sass／Node／GSAP，也不授權 Git 推送或部署。
