# 每案必備搜尋頁｜evo266200 指定參考

每個案件都要有搜尋結果頁，首次網站製作就納入必備頁面與校稿，不只做 Header 搜尋入口。使用者於 2026-10-13 指定依照 [evo266200 搜尋頁](http://192.168.168.99/php83/sites/evo266200/public/zh-TW/search?keyword=%E9%9B%BB%E6%A2%AF) 的結構；**搜尋結果區是 EVO 系統共用頁，公版 HTML／JS 不可修改；CSS 可以依案件確認需求調整。** 只替換本案搜尋資料、圖片、連結、keyword 與筆數；共用 Header／Footer 使用本案版本。未指定 CSS 調整時，系統搜尋區的布局、字級、對齊、間距、卡片外觀與斷點忠實沿用參考；有確認調整時記錄差異，RWD 驗收範圍依案件約定。

## 已核對來源

已讀取指定頁 HTML、`css/search.css`、`page-resource/shared/zh-TW/css` 與後載入的 `css/evomni-root.css`，並另查無匹配關鍵字的回應 HTML。固定樣式已收錄為 [系統搜尋 CSS](../assets/search/search.css)，包含原始 `search.css`、後載入的系統搜尋規則，以及限搜尋區的必要繼承值。已用瀏覽器檢查參考與本機搜尋頁最終樣式；尚未做後台整合驗證。參考頁另載入 `css/list-search.css`，其 `.evo-list-search` 是分類列表原地搜尋，不代替本文件的全站搜尋頁。

## 固定版型，不自行重新設計

- 直接沿用下列系統結果區 HTML，保留 `#search-result > .page-container.search-result`、關鍵字標題、筆數、結果清單、卡片與空狀態。標題保留 `"關鍵字" 的搜尋結果`，不得改成品牌標語或「搜尋你喜歡的設計」。
- 不加入參考沒有的站內搜尋小標、頁面內搜尋表單、Hero／Banner、頁籤或裝飾；搜尋輸入沿用共用 Header。不得新增 `.search-page`、`.section-spacing`、`.container-85` 等改變系統容器的 class，或使用通用品牌標題／卡片樣式取代系統樣式。
- 靜態示範／未串接狀態記在交付文件或回報，不把「靜態預覽」說明塞進正式搜尋結果區，改變參考版面。
- CSS 以本文件附帶的原始檔為來源基準；可另加案件已確認的 CSS 調整，保留來源檔與原生選擇器，不改公版 HTML／JS。不要只沿用 class 卻重新寫一套置中大標題、搜尋框、漸層背景、圓角陰影卡片或不同 gap 的 CSS。

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

## 更多按鈕指定樣式

使用者於 2026-10-13 指定以下框線按鈕樣式。重新核對發現它位於參考站後載入的 `evomni-root.css`，且後面另有 `font-weight: 500` 與 hover 規則；完整順序已合併到內附 CSS。不可只擷取以下單一規則，忽略後續覆寫。尺寸、圓角與框線顏色使用本案既有系統按鈕變數，不另填固定值。

```css
.search-result__card-more {
  font-size: var(--BtnFontSize);
  font-weight: 700;
  letter-spacing: .2em;
  color: var(--search-result-text);
  width: var(--BtnWidth);
  height: var(--BtnHeight);
  border: 1px solid var(--BtnOutlineTextColor);
  border-radius: var(--BtnBorderRadius);
  text-align: center;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
}
```

## 樣式與搜尋入口

- 將 [系統搜尋 CSS](../assets/search/search.css) 原樣複製至本案搜尋頁資源位置並實際載入，保留全部 selector、宣告、media query、系統 `--search-result-*` 預設值及後載入的系統搜尋覆寫；可在基準之後載入案件已確認的 CSS 調整，不直接修改來源檔或公版 HTML／JS；未指定調整時不得自行重新設計。需配合既有資源管線時，確認基準樣式保真、案件調整按預期生效。
- 參考容器為 `width: var(--ContainerDefaultWidth)`、`max-width: calc(95% - 30px)`，padding 為 `calc(var(--NaviHeight, 80px) * 2) 0 var(--SectionPadding, 80px)`；標題區靠左且有底線。清單三欄、1200px 以下兩欄、768px 以下一欄，gap 為 `3rem var(--search-result-gap)`，圖片 1:1，摘要最多三行。不得改成其他 Common 容器或品牌卡片比例。
- 原始 CSS 已使用的 `--ContainerDefaultWidth`、`--NaviHeight`、`--SectionPadding` 與按鈕等系統共用變數，沿用本案既有值；額外外觀覆寫須符合本案已確認需求並記錄來源。若全站 Common 的 h1、a、卡片或 section 規則污染搜尋區，修正載入順序或造成污染的 selector，使系統搜尋 CSS 生效，不以未經案件確認的另一套樣式掩蓋。
- Header 搜尋入口沿用本案 [Header 指定參考](evo-header-reference.md)。來源使用 `header_search_full`、`data-component="search"`、`data-scope="global"`、`data-search-url-base` 及既有 toggle／search-panel／search-input／submit／close 契約；搜尋目標改成本案路徑，保留 `keyword` 查詢參數與 URL 編碼。不能把內網 IP、evo266200 或參考站語系寫死到其他案。
- 靜態預覽提供可操作入口與明確標示的示範資料，可使用 `search.html?keyword=...`；正式 EVO 沿用平台的 `/{locale}/search?keyword=...` 及資料來源。使用既有初始化，不另寫重複搜尋處理器；顯示關鍵字時以文字方式輸出，不把使用者輸入當 HTML。
- 來源 CSS 有 tabs 相關樣式，但此次回應未輸出頁籤或分頁；不可只憑 CSS 自行加入功能或宣稱已核對其後台契約。追蹤碼與平台 API 也不因參考 HTML 出現就自動跨案新增。

## 完整 CSS cascade 與文字驗收

參考站載入順序是 `search.css → page-resource/shared/zh-TW/css → evomni-root.css`。`search.css` 不是最終樣式；內附 `assets/search/search.css` 已將後載入的搜尋專用規則合併在尾端，另保留 [系統覆寫原始片段](../assets/search/search-system-overrides.css) 供核對。不得將其他客戶完整的 evomni-root.css 搬到本案。

2026-10-13 於 2560px viewport 實查結果如下；px 為該站變數的計算值，不取代原始 var／clamp，也不把參考站品牌色或按鈕尺寸覆蓋本案 Common。

| 項目 | 最終來源／規則 | 參考站實際值 |
|---|---|---|
| 關鍵字主標題 | search.css 的 clamp、700、line-height 1.4 | 40px／700／56px |
| 「的搜尋結果」 | .75em、300；顏色由 root 的 TextColorSecondary 覆寫 | 30px／300／42px |
| 結果筆數 | .95rem、繼承系統 body 字重與行高 | 15.2px／300／25.84px |
| 文章及產品卡片標題 | FontSizeItemTitle、500、line-height 1.3 | 約 24px／500／31.2px |
| 摘要 | 系統 root 規則、繼承 16px／300、line-height 1.5、TextColorSecondary | 16px／300／24px |
| 更多按鈕 | BtnFontSize；後續規則字重 500，保留框線、尺寸、置中與 hover | 17px／500／28.9px |

- 參考 root 的摘要寫成 `font-size: var(--FontFamily)`；該變數為字體名稱，不是合法字級，瀏覽器因此繼承 16px。保留來源契約並記錄此行為，不誤用 search.css 的 .875rem 當最後字級，也不把字體變數改成數字。未經系統修正授權不自行「修正」共用來源。
- 搜尋區需要保留系統 body 的 16px、字重 300、字距 1px、行高 1.7；內附 CSS 限 `#search-result` 設定這些繼承值，避免本案 body 的 400／1.8 改變結果。字體依本案既有 `--FontFamily`，參考站為 Nunito Sans／Noto Sans TC；字體或 Common 變數不同造成的差異須明列，不能宣稱像素完全一致。
- 完成時查主標題、後綴、筆數、卡片標題、摘要與按鈕的 computed style，以及對應 selector、CSS 檔案與載入順序。只比較主標題、只驗 HTML class、只確認 CSS 請求成功都不足以通過；產品與文章卡片皆須核對。

## 交付檢查

完成前必須用相同 viewport 與同類資料狀態，對照指定參考與本案搜尋結果區：容器、標題位置與比例、底線、筆數、欄數與 gap、圖片比例、卡片邊框／陰影、更多連結及空狀態依系統基準核對；有已確認 CSS 調整的項目依案件確認值驗收並記錄差異。逐項查 DOM、CSS 載入與 computed style；只有結構相同或功能可用不算通過。不能因風格符合首頁就判定搜尋頁合格；未實際對照畫面則明列視覺待驗。

搜尋頁列入案件頁面清單與工程師交付對照表，記錄預覽入口、SCSS／CSS、必要 JS 與正式串接狀態。實測搜尋開關、Enter／送出、中文及特殊字元 keyword、結果筆數、文章／產品卡片、無圖、無結果、返回首頁與共用導覽；空白 keyword 依本案既有平台規則處理，不自造結果。檢查本案範圍內的 RWD 與鍵盤操作。缺正式資料或平台環境時明列「靜態示範／整合後待驗」，不把校稿通過當成正式全站搜尋已完成。

## CSS 來源紀錄

2026-10-13 重新核對指定站台 search.css、shared CSS 與 evomni-root.css；瀏覽器已對照 reference／local 的實際文字樣式。內附目前完整基準 SHA-256：`ee0407c7ab123b25738227efb7b3cb3796f3ad805e0a6ac278ddbb93b850e128`。後續依使用者確認的系統版本更新，不自行改版。此次修正補齊原先漏收的系統覆寫，不代表本機案件頁面已套用或通過視覺驗收。
