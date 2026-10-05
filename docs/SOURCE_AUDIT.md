# 本次教材擷取稽核

所有頁碼均為 PDF 的 1-based 實體頁碼。2026-09-11 逐頁檢視縮圖、答案頁及輸出圖片；以答案表而非病例清單或章節標題作為標準答案。

- 教材 1：`Microteaching_20260910_Cell Injury and adaptation (1) (2).pdf`，31 頁。
- 教材 2：`Microteaching_20260911_Cell Injury and adaptation (2)_0910renew (1).pdf`，65 頁。

| 病例 | 教材 | 取圖頁碼（輪播順序） | 答案頁 | 黃色必答片語（每項必須出現） |
| --- | --- | --- | --- | --- |
| PA0097 | 1 | 15, 16, 17, 19, 20 | 21 | coagulative necrosis；preserved cellular outlines |
| PA0313 | 1 | 26, 27, 28, 30 | 29 | Coagulative necrosis with hemorrhage |
| PA0335 | 2 | 9, 10, 11, 12, 13, 14 | 15 | fibrosis；Granulation tissue；vacuolization；Hypertrophic |
| PA0162 | 2 | 22, 24, 27, 29 | 31 | liquefactive necrosis；Loosening；microabscces |
| PA0198 | 2 | 40, 41, 42, 44, 46 | 48 | Center: Caseous necrosis；Periphery: Granulomatous inflammation |
| PA0081 | 2 | 54, 57, 58, 59, 61, 62 | 63 | Shadowy outlines；calcium |

## 圖片選擇

每題 4–6 張，保留低倍總覽與不同局部視野。直接取出 PDF 內嵌影像，避免將 PowerPoint 疊加的答案標籤、頁碼、引用與箭頭納入。原本烙在影像內的圈線和尺度保留，不修補組織，也不生成替代影像。

- 教材 1 第 24–25 頁為正常腸組織對照，排除；第 30 頁雖在答案後，仍位於該病例區段，收錄為高倍視野。
- 教材 1 第 2 頁的 PA0096 只出現在病例清單，沒有獨立完整答案表，不建立額外題目。
- 教材 2 第 7–8、21、36–38、51–52 頁是正常組織對照，排除。
- 教材 2 第 16–17 頁為 lipofuscin 延伸說明，不混入心肌梗塞辨識題。
- 教材 2 第 40 頁只取第一張實際切片，不取右側 granuloma 示意圖。
- 教材 2 第 46 頁只取第一張切片，不取右側示例圖及馬蹄照片。
- 教材 2 第 45 頁的彩色覆蓋示意、64 頁的皮膚 panniculitis 延伸例不收錄。
- 輸出採等比例 WebP，最長邊不超過 2000 px，quality 94。小圖不放大；不增加不存在的細節。

每張圖在 `data/cases.json` 記錄原始 PDF 頁碼、`imageIndex`、`xref`、頁面上的 `bbox`、輸出尺寸與來源影像 SHA-256。選擇過程由人工視覺核對；不能把「第一張影像」當作適用於新教材的通則。

## 答案與標記

這兩份 PDF 沒有 PDF highlight annotations；黄色是投影片內容的一部分。關鍵字由渲染答案頁後逐項確認，不以粗體或文字抽取結果猜測。完整敘述保留英文與中文註記，只將項目符號和換行轉成網頁易讀格式。

- PA0335 的答案是 `Myocardial infarction, healed`，不能被清單的 `remote` 覆蓋。
- PA0313 的器官答案表為 `Intestine/colon`；題庫設定 `acceptedOrgan: ["Intestine", "colon", "Intestine/colon"]`，作答 `Intestine` 或 `colon` 均判定正確。
- PA0162 完整答案維持教材 `microabscces`，`accepted` 明確增列 `microabscess`，並在展開答案顯示註記。
- `Center:`、`Periphery:` 也塗黃，因此跟後方片語一起納入必答。
- PA0081 第 63 頁表格下方的急性胰臟炎補充存於 `notes`，顯示但不額外計分。

## 教材 3（2026-09-14 匯入）

來源：`pdf/Microteaching_20260914 Cell Injury and adaptation (3).pdf`，49 頁。逐頁渲染核對，並列出每頁內嵌圖片尺寸、bbox（PDF 點座標）及 xref；四個病例的完整答案均採答案表。

**第 12、22、32、48 頁答案表沒有黄色標記。使用者明確授權由 AI 仿照螢光筆邏輯選定必答字，並要求標明來源。** 下表是 AI 選定的片語，不是原教材黃色範圍；每題 `notes` 都有可見說明，`source.keywordBasis` 記錄此例外。保留完整答案，不另加同義詞。括號內 Adipocytic metaplasia 保留在答案，未選為必答。

| 病例 | 病例頁區間 | 取圖頁碼（imageIndex 從 0 起） | 答案頁 | AI 選定必答片語 |
| --- | --- | --- | --- | --- |
| PA0220 | 2–12 | 8:0, 9:0, 10:0, 11:0 | 12 | cystically dilated；hyperplastic glands |
| PA0074 | 13–22 | 19:0, 20:0, 21:0 | 22 | Lipid droplets；hepatocytes |
| PA0017 | 23–32 | 26:0, 27:0, 29:0, 31:0 | 32 | Dark black pigments；macrophages/histiocytes |
| PA0144 | 34–48 | 42:0, 43:2, 44:1, 45:0, 45:1, 47:0 | 48 | proliferative melanocytes；melanin pigmentation |

共新增 4 題、17 張原始內嵌切片，所有原始影像 SHA-256 均不同。輸出沿用等比例 WebP、quality 94、長邊最多 2000 px，不放大。逐圖與原頁對照，無診斷文字及正常對照混入；未重寫教材或修補組織。

### 排除與取圖判斷

- 1、2、13、23、34、49 頁為清單、標題或總結；3–5、14–15、24–25、35–37 頁為機轉、gross、教學示意及外部例圖，不作本病例取圖來源。
- 6–7、16–18、38–40 頁為正常組織對照，排除。
- 21 頁僅取 index 0 主切片，右側兩個液滴小圖排除。
- 28 與 26 頁共用 xref 103，只收錄一次；30 頁有重疊放大圖，採 31 頁獨立高倍視野。
- 33 頁為既有 PA0198 複習，無新增完整答案表，不重複建題，也不改既有病例。
- 41 頁混合正常表皮與 nevus 對照；採 42–45 頁互補视野。43 頁 index 0 是示意圖，取 index 2；44 頁取 index 1。兩頁共用的窄長低倍定位圖只作導覽，不重複收錄。
- 45 頁左右兩張都是實際切片，分別取 index 0、1。46 頁為混合正常皮下脂肪比較及低倍定位圖，排除；47 頁保留病例的脂肪化生視野。

沒有未釐清的病例對應。Description 無塗黃的判分問題已依使用者授權處理。可重現匯入腳本為 `scripts/import_lesson3.py`，片語存於 `data/imports/lesson3-keywords.json`，不執行舊重建程式。

## 教材 4（2026-09-14 匯入）

來源：`pdf/病理學 Micro｜0911 Cell Injury and adaptation (4).pdf`，51 頁。逐頁渲染核對，並列出每頁內嵌圖片尺寸、bbox（PDF 點座標）及 xref；四個病例的完整答案均採答案表。

**第 18、29、41、48 頁答案表具有明確的黃色填色矩形（draw fill = (1.0, 1.0, 0.0)）與底線標記。** 直接採用原教材黃色關鍵字，無需自行推測或授權設定必答片語。

| 病例 | 病例頁區間 | 取圖頁碼（imageIndex 從 0 起） | 答案頁 | 原教材黃色必答片語 |
| --- | --- | --- | --- | --- |
| PA0208 | 12–18 | 15:0, 16:0, 17:0 | 18 | ceroid-laden macrophages |
| PA0211 | 23–30 | 26:0, 27:0, 28:0 | 29 | hemosiderin |
| PA0214 | 31–41 | 35:0, 36:0, 37:0, 38:0, 39:0, 40:0 | 41 | Green-brown bile pigments；Portal edema；ductular reaction；neutrophil |
| PA0216 | 42–48 | 45:0, 46:0, 47:0 | 48 | Brown-black malaria pigments |

共新增 4 題、15 張原始內嵌切片，所有原始影像 SHA-256 均不同。輸出沿用等比例 WebP、quality 94、長邊最多 2000 px，不放大。逐圖與原頁對照，無診斷文字及正常對照混入；未重寫教材或修補組織。

### 排除與取圖判斷

- 1–8 頁為 Melanocytic nevus supplement、9 頁為 Prostate nodular hyperplasia supplement，均為補充範例且無答案表，排除。
- 10、11 頁為封面與 Intracellular accumulation 總覽清單。
- 14、25 頁為 gross 大體標本照片，排除。
- 19–22 頁為既有 PA0335 之複習（[Review]）與 Ceroid / Lipofuscin 比較表，無獨立答案表，不重複建題或修改既有題庫。
- 30 頁位於 PA0211 答案頁後，為無標籤之對照示例圖，排除。
- 33、34、43、44 頁為 Robbins 機轉圖、課本插圖示意，排除。
- 49–51 頁為 Take home message 與結尾總結。

可重現匯入腳本為 `scripts/import_lesson4.py`，不執行舊重建程式。

## 教材 5（2026-09-18 匯入）

來源：`pdf/Microteaching_20260918 Inflammation.pdf`，74 頁。逐頁渲染核對，並列出每頁內嵌圖片尺寸、bbox（PDF 點座標）及 xref；四個病例的完整答案均採答案表。

- **第 28 頁（PA0270）**：`Mucosal and mural neutrophil infiltration, involving muscularis propria` 跨兩行皆具有黃色填色與底線標記，依規定合併為單一必答片語。
- **第 45 頁（PA0044）**：答案表有明確的黃色填色矩形 `mixed` 與 `edema`。Organ 欄位原包含第二行引號附註，主答案設為 `Maxillary sinus`，附註移至 `notes` 提示。
- **第 57 頁（PA0143）**：答案表有明確的黃色填色矩形與底線 `Center: Suture` 與 `Periphery: Granulomatous inflammation`，依規定包含前綴全字必答。
- **第 73 頁（PA0202）**：答案表無黃色螢光標記。經使用者明確授權，由 AI 選定消化性潰瘍基底三層核心病理特徵（`fibrinous necrosis`、`Granulation tissue`、`Fibrosis/scar`）作為必答關鍵字，並於 `notes` 與 `source.keywordBasis` 標明來源。

| 病例 | 病例頁區間 | 取圖頁碼（imageIndex 從 0 起） | 答案頁 | 必答片語 |
| --- | --- | --- | --- | --- |
| PA0270 | 14–28 | 18:0, 19:0, 20:0, 23:2, 26:0, 27:0 | 28 | Mucosal and mural neutrophil infiltration, involving muscularis propria |
| PA0044 | 29–45 | 31:0, 32:0, 36:0, 37:0, 40:0, 43:0 | 45 | mixed；edema |
| PA0143 | 46–57 | 49:0, 50:0, 51:0, 52:0, 53:0, 56:0 | 57 | Center: Suture；Periphery: Granulomatous inflammation |
| PA0202 | 58–73 | 63:0, 64:0, 66:0, 67:0, 69:0, 71:0 | 73 | fibrinous necrosis；Granulation tissue；Fibrosis/scar |

共新增 4 題、24 張原始內嵌切片，所有原始影像 SHA-256 均不同。輸出沿用等比例 WebP、quality 94、長邊最多 2000 px，不放大。逐圖與原頁對照，無診斷文字及正常對照混入；未重寫教材或修補組織。

### 排除與取圖判斷

- 1–12 頁為 Cell injury 補充與既有病例（PA0211、PA0214、PA0216）複習，排除。
- 13 頁為單元封面標題；74 頁為 Caseating vs Fibrinous necrosis 比較表。
- 16、59、60 頁為 gross 大體標本照片，排除。
- 17 頁（闌尾）、41 頁下半（無基底膜增厚對照）、54 頁上半（正常真皮層）、61–62 頁（正常胃黏膜）為正常組織對照，排除。
- 18 頁圖 1（闌尾取材剖面圖）、24 頁（發炎細胞示意圖）、55 頁圖 2（纖維母細胞活化示意）為教材示意圖，排除。
- 34、39、42 頁為 PA0044 重複全景圖（xref 149），65、68、70 頁為 PA0202 重複全景圖（xref 237），排除。

可重現匯入腳本為 `scripts/import_lesson5.py`，不執行舊重建程式。

## 教材 6（2026-09-23 匯入）

來源：`pdf/病理學 Micro｜0923 Hemodynamic derangement.pdf`，64 頁。逐頁渲染核對，並列出每頁內嵌圖片尺寸、bbox（PDF 點座標）及 xref；五個病例的完整答案均採答案表。

**第 16、30、38、51、63 頁答案表無黃色螢光標記。經使用者授權，由 AI 仿照螢光筆邏輯依核心特徵選定必答關鍵字。** 關鍵字設定與投影片黃色標記（第 40 頁 `Centrilobular [zone 3] fibrosis`、第 53/55 頁 `coagulative necrosis`、第 64 頁 `Take Home Message` 各要點）具高度一致性。每題 `notes` 均標記說明，`source.keywordBasis` 記錄為 `ai-selected-user-authorized`。保留完整答案原文，不擴充無依據之同義詞。

| 病例 | 病例頁區間 | 取圖頁碼（imageIndex 從 0 起） | 答案頁 | 必答片語 |
| --- | --- | --- | --- | --- |
| PA0008 | 4–16 | 15:0, 10:0, 11:1, 12:0, 15:1 | 16 | Red pulp expansion；Red pulp congestion；Dilated sinusoids |
| PA0059 | 17–30 | 20:0, 21:0, 22:0, 25:0, 26:0, 28:0 | 30 | Dilated and congested submucosal vessels；Thrombosis；Organization & recanalization |
| PA0076 | 31–38 | 35:0, 36:0, 37:0 | 38 | Centrilobular [zone 3] congestion；Centrilobular [zone 3] hepatocyte necrosis |
| PA0215 | 39–51 | 41:0, 43:0, 44:0, 46:0, 47:0, 49:0 | 51 | Centrilobular congestion；Centrilobular hepatocyte fibrosis |
| PA0096 | 52–63 | 57:0, 58:0, 59:0, 60:0, 61:0, 62:0 | 63 | coagulative necrosis；acute tubular necrosis；Thrombosis |

共新增 5 題、26 張原始內嵌切片，所有原始影像 SHA-256 均不同。輸出沿用等比例 WebP、quality 94、長邊最多 2000 px，不放大。逐圖與原頁對照，無診斷文字及正常對照混入；未重寫教材或修補組織。

### 排除與取圖判斷

- 1 頁為前次 PA0202 複習與拼字提醒；2 頁為單元封面；3 頁為 Case List；64 頁為 Take Home Message 總結。
- 5 頁右側為 spleen 大體標本照片，排除。
- 7 頁（KMU 解剖脾臟圖）、8 頁（ExpertPath 正常脾臟）、9 頁圖 1（正常脾臟對照）、11 頁圖 0（正常脾臟對照）、33 頁（正常肝小葉 zone 示意背景圖）為正常組織或解剖示意，排除。
- 13 頁（VijayPatho 脾臟手繪示意圖）、18 頁（痔瘡解剖示意圖）、19 頁（ExpertPath 痔瘡組織示意）、29 頁（Fate of thrombus 流程圖）、32 頁（門脈分流手繪圖）、34 頁圖 0, 1（Robbins 11e 圖 4.3 豆蔻肝與肉豆蔻果實）、53 頁圖 0, 1（Robbins 梗塞楔形示意）、54 頁（手繪腎血管與梗塞示意）、56 頁（Toronto Notes ATN 流程圖）為教學插圖與流程圖，排除。
- 14 頁為文獻引用 Gamna-Gandy body 帶箭頭照片，非 NTU microteaching 切片，排除。
- 50 頁與 49 頁共用 xref 184，只收錄一次。
- PA0008 第 15 頁收錄 index 0（全景定位圖）與 index 1（Gamna-Gandy body 特寫），原頁之矩形定位框為 PowerPoint 向量形狀，抽取之原生圖檔完全無遮擋或圈線標記。
- PA0059 第 21 頁為肛門直腸交界移行上皮，對於器官辨識為關鍵視野，完整收錄。
- PA0215 第 41–49 頁投影片上的文字方塊及第 46 頁綠色劃線均為 PowerPoint 覆蓋向量物件，原生抽取影像乾淨清晰，無文字烙印。
- PA0096 診斷依答案表保留原文 `Infarct/Infarction`；題庫設定 `acceptedDiagnosis: ["Infarct", "Infarction", "Infract", "Infraction"]`，作答任一形式均判定正確。

可重現匯入腳本為 `scripts/import_lesson6.py`，不執行舊重建程式。

## 教材 7（2026-10-01 匯入）

來源：`pdf/病理學 Micro｜Infection (1).pdf`，59 頁。逐頁渲染核對，並列出每頁內嵌圖片尺寸、bbox（PDF 點座標）及 xref；四個病例的完整答案均採答案表。

- **第 21 頁（PA0255）**：答案表無黃色螢光標記。經使用者授權，由 AI 依答案表全部 5 項病理特徵（`Papillomatosis`、`Koilocytosis`、`Acanthosis`、`Hyperkeratosis`、`Parakeratosis`）選定為必答關鍵字，並於 `notes` 與 `source.keywordBasis` 標明來源。
- **第 33 頁（PA0271）**：答案表具有明確黃色填色矩形（`draw fill = (1.0, 1.0, 0.0)`）與底線覆蓋 `Molluscum bodies (Henderson-Patterson bodies)`，`accepted` 同時納入 `Molluscum bodies` 與 `Henderson-Patterson bodies`。
- **第 43 頁（PA0218）**：答案表無黃色螢光標記。經使用者授權，由 AI 依包含體病理核心特徵（`Large intranuclear basophilic inclusions` 與 `Small cytoplasmic basophilic inclusions`）選定為必答關鍵字，並於 `notes` 與 `source.keywordBasis` 標明來源。診斷欄位包含 `or` 多選一，`acceptedDiagnosis` 設定支援 CMV infection 或 CMV nephritis 各種全稱與簡稱。
- **第 57 頁（PA0306）**：第 4 頁目錄編號為 `PA0306 (4)`，第 44 頁標題與第 46–50 頁切片來源標記為 `PA0001 (4)`，經使用者確認採用病例編號 `PA0306`，附註記錄 PA0001 與玻片號 4。答案表僅 `Vegetation` 具有黃色填色矩形，依使用者授權嚴格採 `Vegetation` 為必答關鍵字（容許 `Vegetation:`）。器官依答案表附註設定 `acceptedOrgan: ["Heart valve", "Heart", "Mitral valve", "Aortic valve"]`。

| 病例 | 病例頁區間 | 取圖頁碼（imageIndex 從 0 起） | 答案頁 | 必答片語 |
| --- | --- | --- | --- | --- |
| PA0255 | 5–23 | 11:0, 13:0, 15:0, 19:0, 20:0 | 21 | Papillomatosis；Koilocytosis；Acanthosis；Hyperkeratosis；Parakeratosis |
| PA0271 | 24–33 | 27:0, 28:1, 29:0, 29:1, 32:0 | 33 | Molluscum bodies (Henderson-Patterson bodies) |
| PA0218 | 34–43 | 37:0, 40:0, 41:0, 42:0, 42:1 | 43 | Large intranuclear basophilic inclusions；Small cytoplasmic basophilic inclusions |
| PA0306 | 44–59 | 48:0, 49:0, 50:0, 52:0, 55:0, 56:0 | 57 | Vegetation |

共新增 4 題、21 張原始內嵌切片，所有原始影像 SHA-256 均不同。輸出沿用等比例 WebP、quality 94、長邊最多 2000 px，不放大。逐圖與原頁對照，無診斷文字及正常對照混入；未重寫教材或修補組織。

### 排除與取圖判斷

- 1–2 頁為前次 Suture granuloma 補充；3 頁為單元封面；4 頁為 Case List；58–59 頁為 Take Home Message 總結。
- 6–7 頁（正常皮膚）、38–39 頁（正常腎臟）、46 頁（正常房室瓣組織層構造）、47 頁（正常主動脈瓣）為正常組織對照，排除。
- 8 頁（尖型濕疣臨床肉眼照）、25 頁（傳染性軟疣臨床照）、45 頁圖 1（心內膜炎 gross 標本照）為大體或臨床肉眼照，排除。
- 10 頁（葡萄乾樣核示意圖）、26 頁圖 0, 1, 2, 3（教科書插圖與示意）、28 頁圖 0, 2（教科書插圖）、36 頁（Robbins CMV 示意）、41 頁圖 1（教科書插圖）、45 頁圖 0（心瓣膜示意）為教學插圖與示意，排除。
- 16 頁與 11 頁共用 xref 54，30 頁與 29 頁共用 xref 115, 116，排除重複。
- 20 頁圖 1 為微型 icon；21 頁為答案表下方標籤；22–23 頁為答案頁後之臨床延伸病例（48M 膀胱癌病史尿道腫瘤），非本題切片，排除。

可重現匯入腳本為 `scripts/import_lesson7.py`，不執行舊重建程式。

## 教材 8（2026-10-05 匯入）

來源：`pdf/病理學 Micro｜1002 Infection (2).pdf`，58 頁。逐頁渲染核對，並列出每頁內嵌圖片尺寸、bbox（PDF 點座標）及 xref；四個病例的完整答案均採答案表。

- **第 13 頁（PA0251）**：答案表具有明確黃色填色矩形（`draw fill = (1.0, 1.0, 0.0)`）與粗底線覆蓋 `Sulfur granules` 與 `Splendore-Hoeppli phenomenon`，採此兩項為必答關鍵字。第 3 項 `May granulomatous inflammation...` 原文為灰色字（`7E7E7E`），未設為必答。第 2 頁目錄標記器官為 `Ovary`，答案表附註「`此片被病灶佔滿，其實沒有可供辨認為卵巢之組織`」，完整答案保留原文並設定 `acceptedOrgan: ["Ovary", "Ovary (此片被病灶佔滿，其實沒有可供辨認為卵巢之組織)"]`。
- **第 30 頁（PA0022）**：答案表無黃色螢光標記，但第一項以粗底線明確標記 `Aseptate` 及 `wide-angle`，Take Home Message（第 58 頁）亦總結為 `Aseptate hyphae with wide-angle branching`。採 `Aseptate` 與 `wide-angle branching` 為必答關鍵字，並設定容許詞形與拼法。
- **第 43 頁（PA0015）**：答案表具有明確黃色填色矩形與粗底線完整覆蓋 `Fungal hyphae with septa and acute-angle branching`，直接採此片語為必答關鍵字，並相容 `septate hyphae with acute-angle branching` 等寫法。
- **第 56 頁（PA0201）**：答案表無黃色螢光標記。依 Take Home Message（第 58 頁）粗底線重點 `Yeasts & pseudohyphae` 及第 54 頁教學切片標記特徵，選定 `Fungal yeasts and pseudohyphae` 為必答關鍵字，並相容 `pseudohyphae` 等寫法。

| 病例 | 病例頁區間 | 取圖頁碼（imageIndex 從 0 起） | 答案頁 | 必答片語 |
| --- | --- | --- | --- | --- |
| PA0251 | 3–13 | 7:0, 8:0, 9:0, 10:0 | 13 | Sulfur granules；Splendore-Hoeppli phenomenon |
| PA0022 | 14–30 | 18:0, 20:0, 22:0, 23:0, 25:0, 29:0 | 30 | Aseptate；wide-angle branching |
| PA0015 | 31–43 | 35:0, 36:0, 37:0, 38:0, 39:0, 40:0 | 43 | Fungal hyphae with septa and acute-angle branching |
| PA0201 | 45–56 | 50:0, 51:0, 52:0, 53:0, 54:0, 55:0 | 56 | Fungal yeasts and pseudohyphae |

共新增 4 題、22 張原始內嵌切片，所有原始影像 SHA-256 均不同。輸出沿用等比例 WebP、quality 94、長邊最多 2000 px，不放大。逐圖與原頁對照，無診斷文字及正常對照混入；未重寫教材或修補組織。

### 排除與取圖判斷

- 1 頁為封面；2 頁為 Case List；57–58 頁為 Take Home Message 總結。
- 4 頁（放線菌教科書介紹與臨床大體）、5 頁（Sulfur granule 示意圖）、6 頁（文獻手繪 Splendore-Hoeppli 機轉圖）、15 頁（真菌形態速查表手繪示意）、16 頁（毛黴菌臨床黑真菌肉眼照）、33 頁（Aspergillus 培養肉眼照）、34 頁（聖水器命名由來示意圖）、44 頁（答案頁後之毛黴菌對照圖）、46 頁（念珠菌教科書示意）、47 頁（假菌絲比較表）、48 頁（鵝口瘡與尿布疹臨床肉眼照）為教學插圖、示意與大體臨床照，排除。
- 49 頁（SIU 正常食道組織照）為正常組織對照，排除。
- 11 頁（ExpertPath HE 切片帶浮水印）、12 頁（ExpertPath GMS 及 Gram 特殊染色）為外部圖庫，排除；PA0251 採用 7–10 頁 NTU microteaching 之 4 張原生切片。
- 24 頁與 18 頁共用 xref 98；26 頁與 25 頁共用 xref 118；28 頁與 27 頁共用 xref 125，排除重複。26 頁圖 1（xref 122）為粉紅插畫手繪線條，排除。
- 40 頁圖 1（xref 165）為粉紅手繪示意，排除。41、42 頁為註明「壞掉的hyphae不適合用來判斷」之退化菌絲教學頁，排除。

可重現匯入腳本為 `scripts/import_lesson8.py`，不執行舊重建程式。

## 教材 9（2026-10-05 匯入）

來源：`pdf/病理學 Micro｜1005 Microteaching_20261005_Infection (3).pdf`，57 頁。逐頁渲染核對，並列出每頁內嵌圖片尺寸、bbox（PDF 點座標）及 xref；四個病例的完整答案均採答案表。

- **第 16 頁（PA0316）**：答案表無黃色螢光標記。經使用者授權，由 AI 仿照 Take Home Message 與核心特徵選定必答關鍵字（`thick-walled fungal yeasts` 與 `Granulomatous inflammation`），並於 `notes` 與 `source.keywordBasis` 標明授權來源。答案表原文第一項拼寫為「`Numerus`」，完整答案保留原文並相容「`Numerous`」。
- **第 28 頁（PA0302）**：答案表具有明確黃色填色矩形（`draw fill = (1.0, 1.0, 0.0)`）與底線覆蓋 `Foamy, granular, eosinophilic exudate`。診斷支援全稱與簡稱（`PJP`、`Pneumocystis pneumonia`）。
- **第 40 頁（PA0206）**：答案表具有明確黃色填色矩形與底線覆蓋 `Ingested red blood cells`，答案表下方註記專科考試來源存於 `notes`。
- **第 55 頁（PA0354）**：第 2 頁目錄與第 41 頁標題特別註記「`更新 PA0354 (145)`」，採用病例編號 `PA0354`。答案表原僅塗黃底線 `herpes infection`，經使用者指示擴充 3M 病毒病效應（`Multinucleation`、`Margination of chromatin`、`Molding of nuclei`）為必答關鍵字。器官設定 `acceptedOrgan: ["Oral cavity (mouth floor)", "Oral cavity", "mouth floor", "Oral cavity, mouth floor"]`；診斷設定 `acceptedDiagnosis: ["Herpes virus infection", "Herpes simplex virus infection", "HSV infection", "Herpes infection"]`。

| 病例 | 病例頁區間 | 取圖頁碼（imageIndex 從 0 起） | 答案頁 | 必答片語 |
| --- | --- | --- | --- | --- |
| PA0316 | 3–16 | 7:0, 8:0, 9:0, 11:0, 12:0, 15:0 | 16 | thick-walled fungal yeasts；Granulomatous inflammation |
| PA0302 | 17–29 | 22:0, 23:0, 24:0, 25:0, 26:0, 27:0 | 28 | Foamy, granular, eosinophilic exudate |
| PA0206 | 30–40 | 35:0, 36:0, 36:1, 37:0, 39:0 | 40 | Ingested red blood cells |
| PA0354 | 41–55 | 46:0, 48:0, 51:0, 52:0, 54:0 | 55 | herpes infection；Multinucleation；Margination of chromatin；Molding of nuclei |

共新增 4 題、22 張原始內嵌切片，所有原始影像 SHA-256 均不同。輸出沿用等比例 WebP、quality 94、長邊最多 2000 px，不放大。逐圖與原頁對照，無診斷文字及正常對照混入；未重寫教材或修補組織。

### 排除與取圖判斷

- 1 頁為封面；2 頁為 Case List；56–57 頁為 Take Home Message 總結。
- 6 頁（免疫程度與菌量折線圖）、19–20 頁（Robbins PJP 示意圖）、31 頁（CDC 阿米巴生活史插圖）、33 頁（燒杯狀潰瘍插圖）、34 頁（阿米巴原蟲塗片帶箭頭圖）、37 頁右側（原蟲卡通示意）、42 頁（Pathodoodles HSV 手繪圖）、43–44 頁（外部文獻帶箭頭照片）、45 頁（皮膚水皰帶箭頭照片）均為教學示意與外部文獻圖，排除。
- 32 頁為阿米巴大體標本照片（gross），排除。
- 10 頁（Mucicarmine 特殊染色）為特殊染色，本題依互補性挑選 6 張代表性 HE 視野。
- 14 頁與 13 頁共用 xref 63；47 頁 index 0 與 46 頁共用 xref 222；53 頁與 50 頁共用 xref 234，排除重複。
- 21 頁為 ExpertPath 外部引用圖（含浮水印與箭頭），排除。
- 29 頁為形態比較表格，排除。
- 40 頁下方為 2025 專科考試題目截圖（xref 198），排除。

可重現匯入腳本為 `scripts/import_lesson9.py`，不執行舊重建程式。



