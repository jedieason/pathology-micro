# 課外切片資源：取圖捷徑

課外單元只考 Organ（2 分）與 Diagnosis（5 分）。答案採資料庫圖說，附原教材對照；不把不同器官的專屬名稱硬當同義詞，不自行補寫黃色關鍵字。原教材維持原答案。

## NUS Pathweb

- 從 [公開 Slide Viewer 目錄](https://medicine.nus.edu.sg/pathweb/wp-content/uploads/slideViewer/) 找切片，以 `osd.html?slideId=m4` 之類的連結確認器官、診斷。公開目錄為 27 張；另一個完整切片入口需登入，不能宣稱已涵蓋全部館藏。
- 原圖是 Deep Zoom tiles：`slides/<slideId>_dz_files/<level>/<column>_<row>.jpeg`，不是一張可直接存下的全玻片 JPEG。全景與局部採不同 level；level 不等於實際顯微鏡倍率。
- 直接下載若只拿到 Incapsula HTML，改用瀏覽器正常載入切片，縮放／定位病灶後，以 `pageAssets.list()` 找已載入的 tiles，再用 `pageAssets.bundle()` 匯出。不要繼續反覆嘗試 curl 或用螢幕截圖代替原圖。
- 本次 tileSize = 254、overlap = 1；只組完整矩形，移除相鄰重疊像素。位置、URL、雜湊已存 `data/imports/pathweb.json`；快取結構為 `<cache>/<slideId>/<level>/<column>_<row>.jpeg`。用 `scripts/import_pathweb.py` 安全追加，補收病例可用 `--case-ids`。

## PEIR Digital Library（這次優先選擇）

- [PEIR](https://peir.path.uab.edu/library/) 的英文疾病標籤及器官圖說完整，適合找同病不同器官；例如 Candida、CMV、Aspergillus、Cryptococcus、Pneumocystis。PathoPic 也可作後備，但這次 PEIR 的匹配與直接下載較便利，並非宣稱它涵蓋所有疾病。
- **直接走公開 Piwigo API，毋須逐張點圖庫：**入口 `https://peir.path.uab.edu/library/ws.php?format=json`；`method=pwg.tags.getList` 取得疾病標籤，`method=pwg.tags.getImages&tag_id=2156&per_page=500&page=0` 取得圖片。依 `paging.total_count` 翻完各頁。2156 是 candidiasis，其他 tag ID 先查清單，不猜。
- `pwg.images.getInfo&image_id=9` 可讀作者和完整圖說；`element_url` 是原始 JPEG，`derivatives` 是縮圖，勿下載縮圖當原圖。每張保留 `page_url`、原圖 URL、photo ID、作者、完整圖說與 SHA-256。
- 只收來源明示為組織切片且器官／病變相符的圖片；排除 gross、放射影像、培養、血液／KOH／Tzanck 塗片、疑似病原、背景病史及器官被來源自己質疑的圖片。每張唯一原圖一題；位元組完全相同的圖只收一次。特殊染色保留原貌；肺外 Pneumocystis 不套用 pneumonia。
- 已選圖清單在 `data/imports/peir.json`，排除理由在 `data/imports/peir-exclusions.json`；`scripts/import_peir.py` 下載原圖、保留來源並安全追加。不要執行 `extract_materials.py`，它會覆寫題庫。

所有輸出為等比例 WebP，不放大小圖、不修補組織、不生成替代影像。來源版權與作者仍屬原資料庫；PathoPic 如日後使用，依其 [使用說明](https://pathorama.ch/help/1) 保留每圖可讀的 © PathoPic。本次依使用者指示，不再做網站／判分測試。
