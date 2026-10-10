---
name: lin-frontend
description: 依 LIN 切版規範實作、修改與校稿品牌及企業網站的 HTML、SCSS、JavaScript、Swiper 與共用頁面，適用 Figma／設計稿轉網頁及既有前端修正。依案件決定尺寸與 RWD 範圍；不啟動品牌提案、Eagle 整理或整體視覺方案確認流程。
---

# LIN 網頁切版與校稿

把使用者視為網頁設計師／前端實作者。以繁體中文與台灣用語溝通，先做出完整可用的授權成果，再討論細節；說明問題時直接給可執行的修正。

本 Skill 是 LIN 的工程規範獨立版。明確的使用者指示優先，其次為案件已確認規格及既有工程；本 Skill 補足未指定的切版慣例。局部修改不擴大為全站改名或重構。

## 開始工作

先讀案件說明、既有修改、實際 HTML／SCSS／JS、Common、共用元件、套件版本、編譯與預覽入口。沿用現有框架、命名及初始化，不為套用規範重寫整份程式。

預計使用 EVO 後台的案件，切版前必讀 [EVO 範本查核](references/evo-preflight.md)。由 AI 查工程師套件，在切版時同步實作已核對的逐筆編輯結構與欄位標記，不只列成後續轉檔待辦；同一份來源仍提供完整靜態校稿與互動。設計師不用判斷技術標記；缺契約逐區列待確認。工程師後續處理匯入、必要接入及編輯／儲存／發布驗證，不自動啟動匯入或打包。

設計稿是主要視覺依據。核對容器、區塊高度、留白、字型與字重、行高、圖片比例與裁切、對齊及互動狀態；有 Figma 或參考圖時實看，不憑文字印象還原。字型需確認實際載入，缺檔或暫代素材如實標記。

尺寸、頁面、RWD、功能及交付方式依本案要求，不固定 2560×1280。完整網站任務須涵蓋 desktop、tablet、mobile；使用者明確限定桌機／區塊時依範圍執行。局部修改保留既有 responsive，檢查可能受影響的斷點，不藉此另設整套手機版。

資訊足夠就直接做；小幅不確定先依現況判斷。只有選擇會改變已確認設計、重大架構或不可逆結果時才提出具體方案請使用者決定，已有授權不重問。

## 按需讀取規範

涉及下列項目時完整讀取對應文件；同輪未變的文件不用重讀。

| 任務 | 必讀 |
|---|---|
| HTML、SCSS、Common、命名、版面與互動狀態 | [HTML／SCSS](references/html-css-rules.md) |
| JavaScript、Swiper、AOS、GSAP 初始化與清理 | [JavaScript](references/javascript-rules.md) |
| Header、Footer、Nav、內頁與平台功能 | [共用頁面](references/shared-page-rules.md) |
| EVO 選單、漢堡、按鈕、語系 | [Header 指定參考](references/evo-header-reference.md) |
| 連續 marquee | [marquee 指定參考](references/evo-marquee-reference.md) |
| 內頁 breadcrumb | [breadcrumb001 指定參考](references/evo-breadcrumb-reference.md) |
| FAQ | [tpl-faq001 指定參考](references/evo-faq-reference.md) |
| 開始修改、共用影響檢查與交付校稿 | [實作與校稿](references/implementation-review.md) |

規範是工程約定，不能代替品牌構圖或素材。EVO 的 container、系統選單與版權列規定依對應文件適用範圍執行；其他框架不捏造 EVO 元件或後台資料綁定。

## 實作與完成

先判斷缺陷屬於結構、樣式、JavaScript、套件、資料或環境，再用 DOM、computed style、console、network 或小型驗證找根因。修正回原始位置，不一直追加 override 或用負 margin 掩蓋占位。

視覺與動畫必須幫助品牌、閱讀或操作。輪播統一用 Swiper，區塊淡入淡出統一用 AOS，連續 marquee 沿用指定 EVO 元件；複雜時間軸、視差與釘選沿用既有 GSAP／ScrollTrigger 及捲動系統。其他簡單效果用原生 CSS／JS。集中可調參數，處理 resize、去重、事件解除與 prefers-reduced-motion。未用到的工具或套件不安裝。

在可用環境編譯並開啟預覽，實際看畫面與操作；校稿依 references/implementation-review.md。無瀏覽器、缺素材或缺後台時，完成可執行部分並明列未驗證範圍，不把語法檢查當視覺通過。

完成後簡短交付：改了什麼、修改檔案、預覽／啟動方式、實測範圍及需要使用者檢查的地方。安裝本 Skill 不等於安裝 Sass／Node／GSAP，也不授權 Git 推送或部署。
