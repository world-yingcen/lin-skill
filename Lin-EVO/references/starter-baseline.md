# LIN 指定切版基底

使用者於 2026-11-04 指定：LIN 切版開始與檔案檢查都必須使用 EVO-common-css 的 `06-切版` 基底。為讓本機與 Claude 上傳包使用同一份資料，基底已完整內附於 [assets/evo-starter/06-切版](../assets/evo-starter/06-切版)，內附版含已記錄的 LIN 調整（移除 !important、整個 Header 改以 evo266200 HTML／CSS 為基底，包含按鈕、互動狀態與 RWD）；原始與目前逐檔雜湊及調整紀錄見 [SOURCE.json](../assets/evo-starter/SOURCE.json)。

維護來源為 `/Users/wd-t160/LINS/git/EVO-common-css/06-切版`；日常使用先讀 Skill 內附快照，不依賴該本機絕對路徑，也不宣稱快照自動跟隨來源更新。維護者更新時核對差異，保留必要空檔與資料夾，同步快照及來源紀錄後重新打包。不要在客戶案件工作中回寫來源庫或 Skill 基底。

## 新案開始

1. 完整讀內附 `scss/_common.scss`、`scss/_header.scss`、`scss/evomni-root.scss` 與檔案結構，先掌握既有變數、版心、間距、按鈕與共用 class，再動手切版。不可省略基底後自行發明一套 Common。
2. 將完整 `06-切版` 內容複製為案件普通檔案；不帶來源 Git、系統雜檔，不重複產生 `06-切版/06-切版`。沿用案件已確認的目錄位置，沒有時採 `06-切版/`。既有案件先依下節比對，不整包覆蓋。
3. 保留基底變數名稱與用途，再依設計調整案件值。Common 只維護一份有效來源，其他檔案沿用既有 class，不另建同義變數或樣式。
4. 基底的 index.html、main.js、Footer、首頁 SCSS 與 state 目前為空檔，是待製作位置，不代表網站已完成。依任務補齊，確認編譯出非空 CSS 並由 HTML 正確載入後才進行畫面驗證。
5. 基底目前的 evomni-root.scss 包含 index 匯入。新案初始化時依 LIN 現行共用／單頁分工調整：共用入口不輸出首頁專用樣式，首頁另編譯並引用；不修改 Skill 內的來源快照。這是明列的初始化差異，不將舊匯入方式誤判為現行交付規則。

## 檢查與既有案續作

- 每次檢查檔案，必須同時讀內附基底與案件實際檔案；不能只檢查案件自身是否前後一致。核對 Common／root 變數名稱、用途、定義與使用，container、spacing、button 等共用 class，以及 SCSS → CSS → HTML 的編譯載入關係。
- 分清楚「基底缺漏／結構偏離」與「案件已確認的品牌值、內容、RWD 或框架差異」。不要求顏色、字級、尺寸與基底逐字相同，也不覆蓋已完成頁面。缺漏在有效來源做最小修正，範圍外差異記錄，不任意重構。
- 基底是預設樣式與結構來源；使用者後續明確指定的 LIN 規則（例如按鈕、FAQ、Header 跟隨按鈕及資源分工）優先。遇到其他未確認衝突列明差異，不靜默選用舊版。
- 沿用案件唯一交接記錄，留下所用快照、比對範圍、必要差異、編譯與實測結果；不能只因已複製檔案就稱符合規範。
- 若內附基底缺失，先回報缺檔並取得完整 Skill／基底；網頁版不能假裝讀到維護者電腦，不用自造 Common 掩蓋缺件。

## 打包要求

LIN 獨立 ZIP 必須包含整個 `assets/evo-starter/`，保留必要空檔與 `image/.gitkeep`，排除 `.DS_Store`、`.git`、node_modules；核對 SOURCE.json 雜湊與相對參考。上傳包內附基底不需要另外啟用 Skill，仍只保留 LIN 一份入口 SKILL.md。

維護者固定使用來源管理 repo 的 `scripts/build_claude_upload.py --output <新ZIP路徑>`；不依賴臨時腳本或舊 ZIP 重建。基底變更後先核對並更新 SOURCE.json，不為通過檢查跳過雜湊驗證。

Header 的原始 HTML 與兩層來源 CSS 另附於 [header-evo266200](../assets/header-evo266200)，切版及檢查都依 [Header 唯一基底規範](evo-header-reference.md) 使用；原始快照的他案內容不得直接發布。
