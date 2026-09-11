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
- PA0313 的器官是完整的 `Intestine/colon`；斜線不表示此專案接受只填其中一個。
- PA0162 完整答案維持教材 `microabscces`，`accepted` 明確增列 `microabscess`，並在展開答案顯示註記。
- `Center:`、`Periphery:` 也塗黃，因此跟後方片語一起納入必答。
- PA0081 第 63 頁表格下方的急性胰臟炎補充存於 `notes`，顯示但不額外計分。
