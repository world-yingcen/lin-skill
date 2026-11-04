# 隱私權政策公版｜innerpage-body

使用者於 2026-11-04 指定 [旅人驛站隱私權政策](https://www.traveler-inn.com/zh-tw/post/post-r6dxztlg) 為 Lin-EVO 隱私權政策公版。首次製作網站或補做政策頁時，正文統一放在 `.innerpage-body`，內容、章節與順序逐字沿用下列範本，**只替換公司完整名稱**；未經使用者明確指定，不增刪、改寫或另做一份政策文案。

## 頁面與樣式原則

- 頁面沿用本案 Header、Footer、內頁 Banner、breadcrumb001、`.innerpage-container.section-spacing.container-65` 與既有內頁載入方式；Cookie 的「隱私權政策」連到這個實際頁面。
- `.innerpage-body` 版型、標題間距、編號圓點及閱讀節奏沿用公版。字型、字級、文字色、標題色、背景色、區塊間距等本案已有 `:root` 變數者必須引用本案變數，不複製旅人驛站的品牌值，也不在政策頁重複宣告另一套 root。
- 公版正文只替換 `{{公司完整名稱}}`。不要替換成品牌簡稱，也不要把「網站」誤放進變數；輸出應為「公司完整名稱網站」。
- 內頁標題／Banner 仍須提供本頁唯一的 `<h1>隱私權政策</h1>`；正文各章沿用 `<h3>`，不為了改字級調整標題層級。
- 來源頁的 GrapesJS `id`、`data-instance-id` 與實例 class 不是公版內容，不複製到其他案件；正式 EVO 由本案平台產生實例識別。可保留本案既有 `tpl-list001` 結構，但不得因此改寫文字或視覺。

## 固定正文 HTML

```html
<div class="innerpage-container section-spacing container-65">
  <div class="innerpage-body">
    <div>
      非常歡迎您光臨「{{公司完整名稱}}網站」（以下簡稱本網站），為了讓您能夠安心的使用本網站的各項服務與資訊，特此向您說明本網站的隱私權保護政策，以保障您的權益，請您詳閱下列內容
      <br><br>
    </div>

    <h3>一、隱私權保護政策的適用範圍</h3>
    <div>隱私權保護政策內容，包括本網站如何處理在您使用網站服務時收集到的個人識別資料。隱私權保護政策不適用於本網站以外的相關連結網站，也不適用於非本網站所委託或參與管理的人員。</div>

    <h3>二、個人資料的蒐集、處理及利用方式</h3>
    <ol class="numbered-list">
      <li>當您造訪本網站或使用本網站所提供之功能服務時，我們將視該服務功能性質，請您提供必要的個人資料，並在該特定目的範圍內處理及利用您的個人資料；非經您書面同意，本網站不會將個人資料用於其他用途。</li>
      <li>本網站在您使用服務信箱、問卷調查等互動性功能時，會保留您所提供的姓名、電子郵件地址、聯絡方式及使用時間等。</li>
      <li>於一般瀏覽時，伺服器會自行記錄相關行徑，包括您使用連線設備的IP位址、使用時間、使用的瀏覽器、瀏覽及點選資料記錄等，做為我們增進網站服務的參考依據，此記錄為內部應用，決不對外公佈。</li>
      <li>為提供精確的服務，我們會將收集的問卷調查內容進行統計與分析，分析結果之統計數據或說明文字呈現，除供內部研究外，我們會視需要公佈統計數據及說明文字，但不涉及特定個人之資料。</li>
    </ol>

    <h3>三、資料之保護</h3>
    <ol class="numbered-list">
      <li>本網站主機均設有防火牆、防毒系統等相關的各項資訊安全設備及必要的安全防護措施，加以保護網站及您的個人資料採用嚴格的保護措施，只由經過授權的人員才能接觸您的個人資料，相關處理人員皆簽有保密合約，如有違反保密義務者，將會受到相關的法律處分。</li>
      <li>如因業務需要有必要委託其他單位提供服務時，本網站亦會嚴格要求其遵守保密義務，並且採取必要檢查程序以確定其將確實遵守。</li>
    </ol>

    <h3>四、網站對外的相關連結</h3>
    <div>本網站的網頁提供其他網站的網路連結，您也可經由本網站所提供的連結，點選進入其他網站。但該連結網站不適用本網站的隱私權保護政策，您必須參考該連結網站中的隱私權保護政策。</div>

    <h3>五、與第三人共用個人資料之政策</h3>
    <div>
      本網站絕不會提供、交換、出租或出售任何您的個人資料給其他個人、團體、私人企業或公務機關，但有法律依據或合約義務者，不在此限。
      <br>前項但書之情形包括不限於：
    </div>
    <ol class="numbered-list">
      <li>經由您書面同意。</li>
      <li>法律明文規定。</li>
      <li>為免除您生命、身體、自由或財產上之危險。</li>
      <li>與公務機關或學術研究機構合作，基於公共利益為統計或學術研究而有必要，且資料經過提供者處理或蒐集者依其揭露方式無從識別特定之當事人。</li>
      <li>當您在網站的行為，違反服務條款或可能損害或妨礙網站與其他使用者權益或導致任何人遭受損害時，經網站管理單位研析揭露您的個人資料是為了辨識、聯絡或採取法律行動所必要者。</li>
      <li>有利於您的權益。</li>
      <li>本網站委託廠商協助蒐集、處理或利用您的個人資料時，將對委外廠商或個人善盡監督管理之責。</li>
    </ol>

    <h3>六、Cookie之使用</h3>
    <div>為了提供您最佳的服務，本網站會在您的電腦中放置並取用我們的Cookie，若您不願接受Cookie的寫入，您可在您使用的瀏覽器功能項中設定隱私權等級為高，即可拒絕Cookie的寫入，但可能會導致網站某些功能無法正常執行。</div>

    <h3>七、隱私權保護政策之修正</h3>
    <div>本網站隱私權保護政策將因應需求隨時進行修正，修正後的條款將刊登於網站上。</div>
  </div>
</div>
```

## 公版 SCSS

樣式放進本案內頁共用 SCSS，沿用既有變數，不在這個元件內重複建立 `:root`。下列 fallback 只避免外部變數缺失時失去可讀性，不取代本案 root。

```scss
.innerpage-body {
  color: var(--TextColorPrimary, #212121);
  font-size: var(--FontSizeBody, 1rem);
  line-height: 1.7;

  h3 {
    margin: var(--Space3, 3rem) 0 var(--Space2, 1.5rem);
    color: var(--TextColorTitle, #212121);
    font-size: var(--FontSizeItemTitle, 1.25rem);
  }

  .numbered-list {
    margin: 0;
    padding: 0;
    list-style: none;
    counter-reset: privacy-list;

    > li {
      position: relative;
      margin-bottom: 0.5rem;
      padding-left: 2rem;
      color: var(--TextColorSecondary, #555);
      line-height: 1.6;
      counter-increment: privacy-list;

      &::before {
        position: absolute;
        top: 0;
        left: 0;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.5rem;
        height: 1.5rem;
        border-radius: 50%;
        color: var(--BgColor, #fff);
        background-color: var(--TextColorPrimary, #212121);
        font-weight: 700;
        content: counter(privacy-list);
      }
    }
  }
}
```

若本案已由 `tpl-list001` 輸出同一套編號圓點樣式，沿用既有樣式，不重複寫第二套 selector；只核對視覺與上述公版一致，並確認實際值來自本案 `:root`。容器寬度與上下留白由 `.container-65`、`.section-spacing` 及本案 RWD 共用規則處理，不另寫固定頁寬。

## 驗收

逐字比對七個章節與清單順序，確認只替換公司完整名稱；檢查政策頁唯一 h1、`.innerpage-body`、公版標題與編號樣式、root 變數實際生效、桌機／平板／手機閱讀寬度，以及 Cookie 連結可從不同目錄深度正常開啟。靜態頁通過不代表 EVO 後台已完成編輯、儲存與發布驗證，分開記錄。
