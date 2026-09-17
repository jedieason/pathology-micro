# Micro · 病理切片刷題

極簡的靜態網頁，使用 Cell injury and adaptation 與 Inflammation 教材建立 **18 題、86 張切片**。不需後端或前端建置工具。

## 本機使用

```sh
npm start
```

開啟 http://localhost:8080 。請透過 HTTP 預覽，直接雙擊 HTML 的 `file://` 模式無法讀取 JSON 題庫。

## 使用方式

- 左右箭頭、觸控左右滑動、下方圓點：切換同一病例照片。
- 點切片放大；再點放大圖以原始尺寸查看，捲動檢視。Esc 關閉。影像區聚焦後可按鍵盤左右鍵。
- 三個欄位各得 1 分。答錯的欄位自動展開完整答案；答對也能展開。Description 以黃色標出必答片語。
- 切換教材、隨機排序、只看錯題。錯題練習開始時固定本輪題目，避免訂正時題目突然消失；重新切換「只看錯題」會刷新清單。
- 答案、完成狀態保存在目前瀏覽器的 localStorage。修改答案會清除該題舊判分，需重新檢查。不支援跨裝置同步。

## 判分規則

先做 Unicode NFKC 正規化、轉小寫、移除非字母與數字。Organ 與 Diagnosis 必須與答案表完整一致，不接受同義詞或只填一部分。

例如 `Intestine / COLON` 等同 `Intestine/colon`；只填 `colon` 不通過。`Myocardial infarction, healed` 依答案表為準，標題頁的 `remote` 不是可接受答案。

Description 必須含有每一段黃色片語；片語間可以自由排序、補充文字，但片語本身正規化後需連續出現。不做語意判讀、否定句理解或單複數推論。肺病例的 `Center:`、`Periphery:` 也屬原稿黃色範圍，因此必答。

教材第二份第 31 頁把 `microabscess` 寫成 `microabscces`。完整答案保留原文，這一個關鍵字明確接受兩種拼法，其餘不自行擴增別名。

## GitHub Pages

1. 建立 GitHub repository，將此資料夾的程式、`assets/`、`data/`、`docs/`、`scripts/`、`tests/`、`package.json` 與 `.github/` 推送至 `main`。
2. 在 repository 的 **Settings → Pages → Build and deployment → Source** 選 **GitHub Actions**。
3. 推送 `main` 或手動執行 **Actions → Deploy GitHub Pages → Run workflow**。
4. workflow 先跑測試，只將 `index.html`、`assets/`、`data/` 打包，完成後可在 Pages 設定或 workflow 中取得網址。

所有網站路徑都採相對路徑，可放在 `https://USERNAME.github.io/REPOSITORY/`。無外部字型、CDN、API key 或第三方追蹤。原始 PDF/PPT 已列入 `.gitignore`；網站執行不依賴它們。尚未替你建立遠端 repository 或發布網站。

部署設定依 [GitHub 官方自訂 Pages workflow 文件](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) 整理。

## 檔案結構

```text
.github/workflows/pages.yml  # 自動測試與 Pages 部署
index.html                  # 網頁
assets/
  app.js                    # 題目、輪播、互動與儲存
  grading.js                # 獨立判分與標記函式
  styles.css                # 桌面與手機版樣式
  favicon.svg
  images/paXXXX/*.webp       # 每病例獨立資料夾
data/cases.json            # 標準答案、關鍵字與圖片來源
docs/IMPORT_GUIDE.md       # 給其他語言模型的新增教材流程
docs/SOURCE_AUDIT.md       # 本次頁碼、取圖、關鍵字稽核
scripts/extract_materials.py # 由原始兩份 PDF 重建本次題庫
tests/grading.test.js      # 判分及題庫完整性測試
tests/browser.mjs         # 瀏覽器整合測試（需 Playwright）
```

## 新增教材與驗證

把 [docs/IMPORT_GUIDE.md](docs/IMPORT_GUIDE.md) 提供給下一個模型。題庫以 `data/cases.json` 為網站來源；擷取程式是本次兩份教材的可重現紀錄，**新增題目後不要直接執行它覆寫新題庫**。

```sh
npm test
```

重建本次 6 題需 Python 3、PyMuPDF、Pillow，並將原始兩份 PDF 放在根目錄：

```sh
python3 -m pip install PyMuPDF Pillow
python3 scripts/extract_materials.py
npm test
```

瀏覽器測試需另裝 Playwright（不屬網站依賴）：

```sh
npm install --no-save playwright
npx playwright install chromium
npm start
# 另一個 terminal
node tests/browser.mjs
```

可設 `PLAYWRIGHT_MODULE` 指向 Playwright 模組、`CHROME_EXECUTABLE` 指向本機 Chrome，或 `BASE_URL` 指定預覽網址。

影像與答案來自使用者提供的教學教材；原教材來源與逐圖追溯資料保存在題庫及稽核文件中。

### 教材 3 匯入

新增 4 題、17 張切片；原檔放在 `pdf/`。答案表未塗黃，經使用者授權由 AI 選定必答片語，完整答案有明確註記。原有教材的答案與黃色關鍵字不變。

```sh
python3 scripts/import_lesson3.py --keywords data/imports/lesson3-keywords.json
```

匯入程式只追加新病例；若病例 ID 已存在會停止，避免覆寫答案。不帶 `--keywords` 時只輸出待確認資料，不修改正式題庫。

### 教材 4 匯入

新增 4 題、15 張切片；原檔放在 `pdf/`。答案表包含原教材明確黃色填色矩形與底線標記，完全依教材標記建置必答關鍵字。原有教材的答案與關鍵字不變。

```sh
python3 scripts/import_lesson4.py
```

