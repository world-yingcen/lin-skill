# Miffy-EVO｜既有 JSON 流程

工程師已提供唯讀發行庫：`http://192.168.168.133/share-skills/evomni-page-composer.git`。開始轉換時必讀 [工程工具與打包規範](engineering-kit.md)，使用案件既有工具或取得此庫，不再把工具來源當成未提供。認證沿用本機憑證管理；不得將密碼／Token 寫進 Skill、remote URL、報告或交付檔。

**每次採舊 JSON 流程進行轉換或轉換校稿，先更新工程庫，再讀規範、執行工具。** 續作也適用；同一輪不重複更新。依 engineering-kit.md 的更新程序自動核對，不因曾安裝、先前成功或摘要有日期便沿用舊版本。工程庫即時文件是轉換契約的依據，本 Skill 的摘要與查核 commit 僅協助定位，不是鎖版要求。更新成功後重新讀本輪需要的文件與工具參數；更新失敗須明說「尚未確認工程規範最新版」，不得宣稱最新。

開始轉換前讀 [轉換與驗收檢查](conversion-checklist.md)。內頁轉換另必讀 [工程師內頁匯入規範](designer-guide-rules.md)，並取得使用者指定的 [DESIGNER-GUIDE.md](http://192.168.168.94/evomni_vue/docs/html-zip-import-cases/DESIGNER-GUIDE.md) 最新內容。此指南的正本是工程師 repo 的 `docs/template-spec/designer-markup-guide.md`，指南補充內頁實測與前台 vendor 路徑；本案工程包負責實際轉換指令與打包格式。

內網無法讀取時，明列「尚未重新核對指南」，可依已記錄規則盤點與準備來源；缺必要工具或目標契約時不產生可匯入宣稱。指南未定義的首頁、ZIP 格式、CLI 參數不自行推定。與案件版本或既有已確認設計衝突時，列出具體差異並查工程師規格，不無聲刪除功能或重做設計。

- 優先找案件指定的工程包或既有 `_page-composer-kit/`。記錄實際路徑、版本／commit、指南與使用的命令；先讀說明及工具參數，再執行，不猜 CLI、檔名或資料格式。
- 按需查 `knowledge/template-spec.summary.md`、`knowledge/template-spec.json`、`knowledge/designer-markup-guide.md`、`binding-params.json`、`trans-keys.json`，以及轉換、驗證、打包文件與工程師 HTML 匯入指南。這些是查找線索，缺檔時依實際文件定位，不假裝每版都有同一路徑。
- 已安裝 Lin-EVO 時，涉及來源修正再讀其相關工程規範；不複製另一份 Lin-EVO 共用規範。不因讀工程包而啟動其他 Skill 的 Figma、固定尺寸、逐 Frame 確認或重新切版流程。
- 缺工程包、目標格式或必要契約時，仍完成來源盤點、資源清單及不受影響的檢查；將缺口列清楚，不自行產生假 `project-data.json` 或宣稱已可匯入。取得工具的 clone／安裝依本次授權處理，不執行來源不明的腳本。


## 舊 JSON 轉換專用事項

- 依已核對指南處理 main 擷取與平台 layout，FAQ、逐筆編輯及資料綁定使用本案舊契約；不要混入整站 HTML 的標記。
- 正式 page-resource、vendor 宣告及畫布生命週期依目標站台契約，CSS／JS 是否攜帶及另外接入位置分別記錄。
- 依工程工具完成必要的 convert／inject／validate／packaging；`project-data.json`、`assets/`、ZIP 方法與占位資源依 [工程工具與打包規範](engineering-kit.md)。
- CSS 可依工程工具轉入 project data，不一律要求外接，也不使用不存在的旗標。核對轉換前後 media、樣式順序與視覺差異；不靠改設計掩蓋工具改寫。
