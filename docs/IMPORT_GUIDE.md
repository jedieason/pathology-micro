# 給語言模型：新增病理 Micro 教材

你的工作是把提供的 PPT/PPTX/PDF 整理成可追溯的病例題庫，接入本專案現有網站。先讀 `README.md`、`docs/SOURCE_AUDIT.md`、`data/cases.json` 及 `assets/grading.js`。維持極簡作答介面，擷取過程與教學說明放在文件，勿堆到主頁。

## 1. 先建立病例索引，還不要取圖

1. 列出所有教材的檔名、頁數。保留原檔，不重寫。
2. 按頁抽取文字並產生附頁碼的 contact sheet。PDF 同時列出每頁內嵌圖片的數量、尺寸、位置；PPTX 列出 slide 上的圖片、文字框與群組。
3. 以 PA 編號或教材的病例識別碼建立病例區間，記錄章節起始、答案頁、正常對照、病理影像、延伸例。病例清單只作導覽。
4. 找出包含 Organ、Diagnosis、Description 的完整答案表。病例跨頁時，追蹤至下一病例開始；答案表之後也可能有該病例的補充照片。
5. 沒有完整答案或病例對應不明時，列入待確認清單，不自行生成標準答案，也不要只憑切片顏色配病名。

輸出暫存索引：`caseId / source / pageRange / answerPage / candidateImages / exclusions / uncertainties`。先逐頁視覺檢查再進入下一步。

## 2. 系統性取出真正的病理切片

每個病例通常挑 3–6 張互補視野：低倍全貌、中倍病變分布、高倍細胞細節。若素材不足，保留實際張數，不複製湊數。

### PDF

優先使用 PyMuPDF：

```python
import fitz
pdf = fitz.open('source.pdf')
page = pdf[page_number - 1]
for index, info in enumerate(page.get_image_info(xrefs=True)):
    print(index, info['xref'], info['bbox'], info['width'], info['height'])
    if info['xref']:
        original_bytes = pdf.extract_image(info['xref'])['image']
```

`get_image_info` 按顯示實例列圖，圖片可能被重複利用。`xref` 是檔案內部編號，不跨 PDF 穩定。**絕對不要直接抽每頁第一張圖就當完成**；本次程式只對已核對的頁面採第一張。

若圖片為 inline、掃描頁、複合區塊或帶遮罩，無法安全抽出原圖，就用 `page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect)` 擷取指定區域。裁切 rect 使用 PDF 點座標，原點左上；記錄 bbox 和縮放倍率。若圖片只有一部分在 slide 上顯示，將原始圖與整頁渲染比對，只取教材可見且屬該病例的部分。

### PPT / PPTX

- `.ppt` 先用 PowerPoint 或 LibreOffice 轉 `.pptx` 或 PDF，保留原檔及 slide 編號對照。
- `.pptx` 可用 `python-pptx` 取得 picture shape 的 `image.blob`；群組需遞迴走訪。
- 讀取 `crop_left/right/top/bottom`、旋轉、遮罩、群組座標與版面比例。匯出原始 blob 可能包含投影片裁掉的圖片或其他診斷，不能無條件直接使用。
- 同時檢查文字框、表格、speaker notes；完整答案優先採可見答案表，notes 只能補充來源明確的資訊。
- 必須渲染投影片供肉眼核對；無法可靠重建裁切、疊圖、旋轉時，先輸出 PDF 再按可見切片範圍取圖。

### 必須排除

正常組織對照、gross 標本、示意圖、表格、流程圖、教材標題、答案表、其他病例或器官的延伸例。不要把同頁右側的教學示意圖當另一張切片。

直接抽取內嵌圖通常能去除 slide 上的答案文字與箭頭。若關鍵字已烙進原始圖片，選另一張未標記視野或做不傷組織的邊界裁切；若無法去掉而不破壞組織，標記為僅供答案補充，不用來盲測。不使用 AI 補圖、去字修補或色彩美化，不杜撰倍率。

用雜湊辨識完全重複圖片；同一張只加不同箭頭不算新視野。保留必要的原圖定位圈線和比例尺。等比例存為 WebP（本次 quality 94、長邊最多 2000），不放大小圖，不拉伸、不切掉病變。

## 3. 完整轉錄答案與黄色標記

- **Organ / Diagnosis：**完整保留答案表字串，含限定詞、逗號、斜線。章節標題和清單不能覆蓋答案表。
- **Description：**保留所有敘述、子項目、中英文括註與「本片無」。可以整理項目符號與換行，不可摘要、補寫或略去未塗黃句子。
- 表格外的附註存入 `notes`，展開完整答案時顯示。
- 檢查 PDF annotations；若沒有，黃色可能是內容串流的填色矩形、PPT 文字 highlight、圖層或 raster 像素。渲染答案頁確認每一段黃色覆蓋的精確字元。
- 不以「粗體」、一般醫學重要性或 OCR 猜測必答字；只用教材黃色範圍。分行但連續的同一片語合併，獨立標記則分開建項。
- 若黃色範圍包含 `Center:` 等前綴，前綴也必答。若只塗 `calcium`，不要擴成 `Basophilic calcium deposits`。
- 每個標記需附答案頁與可回看的範圍紀錄；在稽核文件列出實際關鍵字。
- 遇到拼字錯誤，顯示答案保留原文。只有核實後才能在該 keyword 的 `accepted` 明確增加更正拼法，並記錄理由與使用者可見註記。不要全域放寬拼字、詞幹或同義詞。
- 沒有黃色標記時不要建立空關鍵字可自動滿分的題目，先提出待確認項目。

## 4. 加入題庫，保留來源

一個病例就是一個 JSON case，多張照片放在 `images`，不是各自建題。以下只是 schema 示意，不能原樣當真實題目：

```json
{
  "id": "教材中的唯一病例編號",
  "lesson": 3,
  "organ": "答案表完整字串",
  "diagnosis": "答案表完整字串",
  "description": "完整敘述，包含黃色片語與其他內容",
  "notes": "表格外附註，沒有則空字串",
  "keywords": [{"text": "黃色片語", "accepted": ["黃色片語"]}],
  "source": {"file": "source.pdf", "answerPage": 12},
  "images": [{
    "src": "assets/images/唯一病例編號/01.webp",
    "page": 7,
    "imageIndex": 0,
    "xref": 42,
    "bbox": [20, 30, 700, 510],
    "width": 1200,
    "height": 850,
    "sourceImageSha256": "原始影像位元組的SHA256"
  }]
}
```

對 PPTX 可新增 `shapeId`、`crop` 與轉檔資訊；無意義的 PDF `xref` 可省略。裁切圖可新增 `extractionMethod` 及 `renderScale`。頁碼固定 1-based，bbox 固定 `[x0,y0,x1,y1]` 並記錄座標單位；图片路徑相對網站根目錄，不以 `/` 起頭。

保持 `id` 唯一與穩定，避免儲存紀錄對錯題；若教材版本改動標準答案，需評估資料版本及舊紀錄遷移。新教材加入 `index.html` 的教材選單（目前 lesson 1、2 為明列選項）。更新來源稽核與 README 數量。

本次 `scripts/extract_materials.py` 是兩份原教材的重建腳本，會覆寫題庫。新增教材應另寫可重現匯入腳本或安全合併到現有題庫，不可直接執行舊腳本抹掉新題。

## 5. 驗證後交付

1. 為輸出影像製作有病例、頁碼的 contact sheet，與原始 slide 對照所有圖片：病例一致、無答案文字、無誤收正常對照、無重複。
2. 對每題完整答案及所有黄色片語逐頁核對；記錄排除與不確定項目。
3. `npm test` 驗證 JSON、圖片存在、關鍵字可以在完整答案中被標出、大小寫與符號正規化、三欄獨立判分、每個關鍵字缺漏都失分。
4. 本機 HTTP 預覽並以桌面、窄螢幕檢查：同病例輪播、手勢、放大、輸入、獨立判分、答錯自動展開、答對手動展開、儲存與錯題篩選。
5. 確認所有網站路徑在 GitHub repository 子路徑下仍可工作。
6. 回報新增幾題幾圖、教材頁碼、任何待確認項目。沒有實際發布成功就不要聲稱已部署。

判分核心必須維持：Organ/Diagnosis 正規化後完整相等；Description 正規化後包含所有黃色片語，每組 accepted 擇一。單欄各 1 分，不能因其他欄答錯而一起判錯，也不能把「包含部分關鍵字」當 Description 正確。
