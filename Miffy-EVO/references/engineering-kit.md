# 工程工具與打包規範

來源：`http://192.168.168.133/share-skills/evomni-page-composer.git`（唯讀工程發行庫）。2026-10-12 核對 HEAD `3c45c1ed8c9aac59e420593238d82e8f68c5e9c0` 的 README、工程 Skill、workflow、packaging、template-injection、frame-slots 與 convert／validate 原始碼。此 commit 是本次查核紀錄，不要求未來鎖死；執行時核對實際版本。

## 取得與維護

- 優先沿用案件已指定的工程包。沒有時可在已授權的轉換工作中將唯讀庫 clone 到案件工具位置；clone URL 不含密碼／Token，使用本機既有憑證管理。認證失敗明列缺口，不印出或索取聊天中的密碼。
- 發行庫是工程團隊單向同步成果；不得手改 knowledge、tools 或工程 Skill，也不回寫、推送、發版或發 issue。
- 每次開工核對更新：先確認 remote 來源、分支、工作樹及本地提交，乾淨且無分歧時只做 fast-forward。保留本機修改，不 reset／stash／強制合併。離線或無法更新時明說尚未確認最新版。
- 記錄工程 commit、`template-spec.json` 的 `source.commit` 與發布說明，對應目標站台是否同步更新；取得最新工具不等於目標站台也最新。
- package.json 依賴 `htmlparser2`、`postcss`，工具需要 Node.js。先檢查可用 runtime／依賴；缺少時依工程包 lockfile 在隔離工具位置安裝，不變更案件前端套件。
- 命令從工程庫根目錄執行；庫內成果只放其 `output/<案名>/` 或 scratchpad。可將驗證通過成果交付到案件的 `evo-export/`，不改動工程來源、不覆蓋既有交付。

### 每次開工的更新程序

1. 從案件紀錄定位實際工程庫；核對 Git 根目錄與 origin 是上述指定庫，不在案件上層 repo 執行更新。remote 以不含憑證的方式檢查及記錄，勿輸出含 Token 的設定。
2. 確認目前分支、工作樹與本地提交。沿用已確認的工程發行分支，未確認時查遠端預設分支，不硬猜 main。若有未提交修改、detached HEAD、來源不符或本地分歧，保留現況並說明原因，不 reset、stash 或強制切換。
3. 在可正常更新的 clone 執行 `git fetch origin`，再將目前發行分支以 `git merge --ff-only <對應的遠端追蹤分支>` 更新；不單凭本機檔案或舊 FETCH_HEAD 認定已最新。新 clone 也記錄本次取得的遠端 commit。
4. 比較更新前後 commit，讀 `knowledge/RELEASE-NOTES.md`，按變更重讀本輪需要的 workflow、packaging、template-injection、frame-slots、知識庫與工具參數。若 package／lockfile 改變，核對工具相依是否需同步安裝，再執行轉換。
5. 在案件既有紀錄留下本次查核時間、分支、工程 commit、spec source.commit、更新結果與影響。向設計師簡短說明有無更新及是否影響本次轉換，不要求設計師自行執行更新。

沒有 .git 的案件工具快照不能宣稱已查遠端。可在獨立工具位置取得新 clone，保留舊快照及原成果，核對差異後使用；不覆蓋使用者修改。連線／認證失敗時讀可用版本完成盤點，但缺必要新版契約的步驟列待確認。

發行庫更新後若與本 Skill 摘要不同，依已核對的工程契約執行並記錄差異，不擅自回寫共用 Skill 或修改發行庫；涉及已確認設計、來源斷點或目標站台不支援的變更，先提出影響與可執行方案，不因最新版工具就無聲改畫面。一次轉換與驗證使用同一版本，工作中不反覆更新工具；下一輪開工再檢查。

## 按階段閱讀

工程文件位於 `.claude/skills/page-composer/`。Miffy-EVO 只沿用轉換與接入契約，不啟動它的重新切版流程。

| 工作 | 必讀文件 |
|---|---|
| 轉換模式與驗證 | `workflow.md`、`tools/convert.mjs`／`tools/validate.mjs` 支援參數 |
| 框架／分類介紹／內容頁 | `frame-slots.md` |
| 注入平台範本 | `template-injection.md`、命中範本的 `knowledge/template-spec.json` |
| 打包 | `packaging.md` |
| 真實資料與翻譯 | `knowledge/binding-params.json`、`knowledge/trans-keys.json`、`knowledge/designer-markup-guide.md` |

指南提到的 `prep-page.mjs` 不在本次查核的發行庫 tools 內；它是另一端的前處理工具，不假裝此庫包含它，也不依賴它自動修好來源。

## 轉換模式

本次查核的 convert 只接受 `--mode home`／`--mode inner`，不帶 mode 是單頁。**不要傳 `--mode single` 給 convert**；single 是 validate 的模式。

```text
node tools/convert.mjs <準備稿.html> <輸出.project-data.json> <輸出.signals.json>
node tools/inject-templates.mjs <輸入.project-data.json> <注入後.project-data.json>
node tools/validate.mjs <最終.project-data.json> --mode single --role detail
```

上例為內容頁，需要範本時才執行 inject。實際輸入與輸出使用獨立路徑，角色不可照抄。

- **單頁內頁**：依內頁指南先取 main 內容，整理成轉換準備稿；convert 預設會讀 body 或根內容，不會自動保證「只取 main」。無平台 Header／Footer 的忠實內容使用不帶 mode 的 convert。
- **首頁**：準備稿以 `page_style="headermain"`／`page_style="footermain"` 標示平台段落，convert 使用 `--mode home`，validate 使用 `--mode home`。不能缺 marker 卻當作首頁分段成功。工具可能把導覽／Logo 等換成候選 slot，必須檢查 signals 與後續平台 Block 對應，不能當作完整互動已保留。
- **整頁取內文**：帶上述平台段落時 `--mode inner` 剔除它們；核對內容範圍及必要共用資源，與單頁 main 摘取流程分開。
- home 輸出同時有 merged `pages` 與 split `header`／`body`／`footer`；注入須涵蓋兩路，同一邏輯範本的 instance ID 一致。只改 pages 會造成畫布正常、發布消失。
- `--css` 是畫布用外部 stylesheet 注入，不代表發布有樣式；`--bake-css` 是把外部 CSS 解析進 project styles，會做 scope／狀態處理。先讀本版實作及相依資源，核對 media／cascade／原視覺是否改變；不得以開旗標代替驗收。
- 本版 validate 未提供 `--no-css`，不從其他 Skill 的歷史規範複製此旗標。CSS 可由準備稿 style 或已核對的工具路徑進 project data；原始 SCSS 仍保留，不在原網站手工插入 style。

## 框架與內容角色

| 角色 | 內容與替換洞 | 後台入口 |
|---|---|---|
| `frame` | 列表框架；list-group shell 產生 `detail-content`，分類介紹需要時在其中包 `category-content`，列表／分頁留在介紹洞外 | 第一層選單節點的頁面設計 |
| `category` | 分類自身介紹，不放 `data-replace`；一般不重複側欄、卡片列表或分頁 | 第 2 層以上節點的分類頁面設計 |
| `detail` | 產品／文章內容頁版型，不放 `data-replace` | 版面設定（進階）→ 內容頁版型 → 自訂 → 頁面設計 |

- 根據案件目標判角色，不對首頁或一般靜態頁硬套 frame／category／detail。無法判斷且會改變匯入入口時才問。
- 不重複手寫 shell 自帶的 `detail-content`；`category-content` 在它裡面，不能包住列表／分頁。查 validate R 系列，分類替換不應讓列表消失。
- 分類沒自訂介紹時沿用上層，皆無時移除介紹洞；分類採換整塊的特殊模式另依原文核對，不按一般介紹輸出。

## 範本、綁定與翻譯

- 真實資料綁定、專屬設定 Dialog、逐筆編輯是三種能力。自製區塊可用 `binding-params.json` 中的正式 `data-param`，不必為綁值重做範本；核對 `context` 與 `requires`，錯位會無聲不換值。
- 查不到翻譯或綁定詞時可依工程規範留下 `data-suggest-trans`／`data-suggest-param`，交付列缺口；不得編造正式鍵或因此自行發 issue。
- 使用 inject 工具生成範本節點與實例 ID，不手寫整棵 JSON。真動態 container fresh-add 路徑不得帶 components 蓋掉 defaults；plain list-group 則有自身 components。依 spec 判斷，不一律刪所有子內容。
- 需 Dialog 的資料設定不憑空 baked；交付說明到後台選分類等必要操作。畫布替換成真實資料後，不直接改資料庫來源值，回產品／文章管理修改。

## ZIP 契約與必要驗證

```text
<案名>.import.zip（所有項目 STORE，method 0）
├── project-data.json
└── assets/<素材檔名>
```

- `project-data.json` 頂層有 `importAssets`；每筆含 `url`、`name`、`mime`、`zipPath`，本地圖的 url 使用 `https://import.local/<檔名>`，zipPath 是 `assets/<檔名>`，mime 須為 `image/*`。
- 占位 URL 與內容引用逐字相同，副檔名與實檔一致。不同來源同檔名先排除衝突；圖片包含在 ZIP，不留依賴外站的圖片交付。
- `pack-import.mjs <pd.json>` 可抓遠端圖片打包；本地圖片依 packaging.md 的 importAssets 與 ZIP_STORED 流程。執行前核對下載來源與輸出副作用。
- 指南表示單圖 >20MB 失敗，>1.9MB 可能縮檔重試；必要壓縮另輸出版本並核對畫質，不覆蓋原素材。
- validate exit 0 **及** ZIP 自檢通過才可交付。逐項確認壓縮 method 0、manifest 的 zipPath 存在、URL 實際被內容引用，不只存在 manifest 裡。
- 最後說明正確後台入口、匯入 JSON／ZIP、選「上傳到媒體庫」、必要 Dialog 設定與 JS 接入；發布後確認沒有 import.local、真實內容與操作正確。
- 這些是已讀工程契約，未對客戶案件實際轉檔／匯入測試；交付與後台驗證仍分開記錄。
