# 專案維護指示

- 使用繁體中文溝通。主頁維持極簡，以圖片與作答為主。
- 新增或更改教材先讀 `docs/IMPORT_GUIDE.md` 和 `docs/SOURCE_AUDIT.md`。
- 不依一般病理知識自行更改教材答案或黃色關鍵字。優先採可追溯的答案表。
- 不覆寫原始教材。不用生成式影像替代、修補病理組織。
- 網站為純靜態 GitHub Pages，所有資源路徑支援 repository 子路徑。
- `data/cases.json` 為網站的題庫。`scripts/extract_materials.py` 只用於原始兩份教材的重建，會覆寫題庫，新增資料後勿直接執行。
- 更改題庫或判分後執行 `npm test`；更改互動後在 HTTP 伺服器檢查桌面和手機。
