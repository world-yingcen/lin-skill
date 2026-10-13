# 每案必備搜尋頁｜evo266200 指定參考

每個案件都要有搜尋結果頁，首次網站製作就納入必備頁面與校稿，不只做 Header 搜尋入口。使用者於 2026-10-13 指定依照 [evo266200 搜尋頁](http://192.168.168.99/php83/sites/evo266200/public/zh-TW/search?keyword=%E9%9B%BB%E6%A2%AF) 的結構；保留下列 DOM 層級與 class，字型、色彩、間距及卡片外觀配合本案首頁。尺寸與 RWD 依案件範圍。

## 已核對來源

已讀取指定頁 HTML、`css/search.css`，並另查無匹配關鍵字的回應 HTML。這是原始碼核對，未做瀏覽器操作或後台整合驗證。參考頁另載入 `css/list-search.css`，其 `.evo-list-search` 是分類列表原地搜尋，不代替本文件的全站搜尋頁。

## 結果頁結構

以下為可替換內容的靜態示例；實際文案、圖片、連結、keyword 與筆數使用本案內容，不複製參考站產品或測試網址。頁面共用 Header／Footer 沿用本案既有方式。

```html
<main id="main-content" class="main-content" role="main">
  <div id="search-result">
    <div class="page-container search-result">
      <div class="search-result__header">
        <h1 class="search-result__title">
          "<span class="js-keyword">本案關鍵字</span>"
          <span class="search-result__title-suffix">的搜尋結果</span>
        </h1>
        <p class="search-result__count">共找到 <span class="js-count">1</span> 筆相關資料</p>
      </div>
      <div class="search-result__list">
        <div class="search-result__card search-result__card--article" data-type="article">
          <a href="本案文章連結" class="search-result__card-link" aria-label="本案文章標題">
            <div class="search-result__card-img">
              <img src="本案圖片.webp" alt="本案圖片描述" loading="lazy">
            </div>
            <div class="search-result__card-body">
              <h2 class="search-result__card-title">本案文章標題</h2>
              <p class="search-result__card-desc">本案文章摘要</p>
              <div class="search-result__card-foot">
                <span class="search-result__card-more">閱讀全文</span>
              </div>
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>
</main>
```

- 產品項目使用 `search-result__card--product` 與 `data-type="product"`，更多文字為「查看詳情」；文章使用 `--article` 與 `data-type="article"`。結果可混排，順序與總筆數依平台資料，不寫死參考站的 10 筆。
- 卡片整張為單一連結，不在其中巢狀另放連結。圖片與摘要為有資料才輸出的區塊；參考頁已有無圖／無摘要文章，不補假圖或留下空圖片框。
- 無結果時，保留頁首關鍵字與 0 筆，以下方空狀態取代結果清單：

```html
<div class="search-result__empty">
  <h2 class="search-result__empty-title">找不到相關結果</h2>
  <p class="search-result__empty-desc">我們找不到符合「本案關鍵字」的產品或內容。<br>建議您嘗試其他關鍵字。</p>
  <a href="本案首頁連結" class="search-result__empty-back">返回首頁瀏覽</a>
</div>
```

## 樣式與搜尋入口

- 參考 CSS 使用 `--ContainerDefaultWidth`、`--NaviHeight`、`--SectionPadding` 與 `--search-result-*`；沿用本案已存在的 Common 變數。搜尋頁樣式集中管理，不逐頁重複。
- 參考清單為三欄，1200px 以下兩欄、768px 以下一欄，圖片為 1:1、`object-fit: cover`，摘要最多三行。這些是參考基底；依本案尺寸、RWD 範圍與品牌設計調整，保留上述結構與可讀性，不將參考色碼寫成每案固定值。
- Header 搜尋入口沿用本案 [Header 指定參考](evo-header-reference.md)。來源使用 `header_search_full`、`data-component="search"`、`data-scope="global"`、`data-search-url-base` 及既有 toggle／search-panel／search-input／submit／close 契約；搜尋目標改成本案路徑，保留 `keyword` 查詢參數與 URL 編碼。不能把內網 IP、evo266200 或參考站語系寫死到其他案。
- 靜態預覽提供可操作入口與明確標示的示範資料，可使用 `search.html?keyword=...`；正式 EVO 沿用平台的 `/{locale}/search?keyword=...` 及資料來源。使用既有初始化，不另寫重複搜尋處理器；顯示關鍵字時以文字方式輸出，不把使用者輸入當 HTML。
- 來源 CSS 有 tabs 相關樣式，但此次回應未輸出頁籤或分頁；不可只憑 CSS 自行加入功能或宣稱已核對其後台契約。追蹤碼與平台 API 也不因參考 HTML 出現就自動跨案新增。

## 交付檢查

搜尋頁列入案件頁面清單與工程師交付對照表，記錄預覽入口、SCSS／CSS、必要 JS 與正式串接狀態。實測搜尋開關、Enter／送出、中文及特殊字元 keyword、結果筆數、文章／產品卡片、無圖、無結果、返回首頁與共用導覽；空白 keyword 依本案既有平台規則處理，不自造結果。檢查本案範圍內的 RWD 與鍵盤操作。缺正式資料或平台環境時明列「靜態示範／整合後待驗」，不把校稿通過當成正式全站搜尋已完成。
