# Google Play Store 上架資料指南 (Play Store Listing Metadata)

本文件整理了將 **Micro — 病理切片練習** 上架至 Google Play Console 所需填寫的所有商店中繼資料、圖檔規格、隱私權政策與完整操作步驟。

---

## 一、商店商品詳情 (Store Listing)

### 0. 應用程式套件識別碼 (Package Name / Application ID)
- **套件名稱**：`com.jedieason.pathologymicro`

### 1. 應用程式名稱 (App Title)
- **繁體中文（台灣）**：`Micro — 病理切片練習`（15 字元 / 上限 30 字元）
- **English (US)**：`Micro: Pathology Practice`（24 characters / max 30）

### 2. 簡短說明 (Short Description - 上限 80 字元)
- **繁體中文**：`極簡流暢的病理組織切片練習工具：觀察鏡下切片、作答並核對關鍵字。`（34 字元）
- **English**：`Minimalist pathology slide practice: observe, answer, and check keywords.`（73 characters）

### 3. 完整說明 (Full Description - 上限 4000 字元)
#### 繁體中文版：
```text
Micro 是一款專為醫學生與病理學習者打造的極簡病理組織切片練習應用程式。

以圖片與即時作答為核心，幫助您在行動裝置上隨時隨地鍛鍊鏡下辨識能力與病理描述技巧。

【核心功能與特色】
• 鏡下切片高畫質檢視：完整支援各倍率切片輪播與全螢幕手勢縮放（Pinch to Zoom），細緻觀察病變組織細節。
• 三段式結構著作答：針對 Organ（器官）、Diagnosis（病理診斷）與 Description（組織病變描述）獨立作答與評分。
• 智慧關鍵字核對：嚴格比對描述重點，標示遺漏關鍵字，並以醒目黃色高亮標註標準解答重點。
• 教材與錯題分類：支援章節篩選（Cell Injury、Inflammation、Hemodynamics 等）與「只看錯題」專屬複習模式。
• 題庫即時同步：內建離線題庫，連網時自動與 GitHub 遠端儲存庫同步最新教材與修正，學習永遠保持最新。
• 純淨極簡無干擾：無廣告、無須註冊帳號、尊重隱私，所有作答歷程均保存在本機裝置。

【教材收錄範圍】
• Cell injury and adaptation (01 - 04)
• Inflammation (01)
• Hemodynamic disorders (01)
持續擴充更新中。
```

#### English Version:
```text
Micro is a minimalist pathology histology practice app designed for medical students and pathology learners.

Focused on slides observation and active recall, Micro helps you sharpen your microscopic diagnostic skills on the go.

[Key Features]
• High-Definition Slide Viewer: Browse multiple histological fields per case with fluid gestures and full-screen pinch-to-zoom.
• Structured Answering: Independent input and scoring for Organ, Diagnosis, and Histopathological Description.
• Keyword Verification Engine: Automatically grades your descriptions against essential medical keywords and highlights matched terms in context.
• Lesson & Missed-Case Filters: Practice by chapter (Cell Injury, Inflammation, Hemodynamics) or focus on missed questions.
• Seamless GitHub Sync: Built-in offline question bank that syncs with the latest updates from the pathology-micro repository.
• Distraction-Free & Privacy First: No ads, no account required, completely offline-capable with local storage.
```

---

## 二、圖像資源規格 (Graphic Assets)

| 素材項目 | 規格要求 | 檔案名稱（已備妥於本資料夾） |
| :--- | :--- | :--- |
| **應用程式圖示 (App Icon)** | 512 x 512 px, 32-bit PNG, 上限 1024 KB | `app-icon-512.png` |
| **宣傳主題圖片 (Feature Graphic)** | 1024 x 500 px, 24-bit PNG 或 JPEG, 無透明度 | `feature-graphic-1024x500.png` |
| **螢幕截圖 (Screenshots)** | 至少 2 張手機螢幕截圖（16:9 或 18:9，如 1080x1920 或 1080x2340） | 可安裝 `app-release.apk` 後擷取 2~4 張實機畫面 |

---

## 三、類別、分級與聯絡資訊

- **應用程式類型**：應用程式 (App)
- **類別**：醫學 (Medical) 或 教育 (Education)
- **標籤 (Tags)**：醫學 (Medical)、教育 (Education)、解剖與病理 (Pathology)
- **內容分級 (Content Rating)**：所有年齡層 (Everyone / PEGI 3) — 內容為醫學病理組織切片顯微照片，無不當內容。
- **目標客群 (Target Audience)**：18 歲以上（醫學生、醫事人員、大專院校學生）。

---

## 四、隱私權政策 (Privacy Policy)

Google Play 要求所有 App 提供公開的隱私權政策網址。您可直接使用 GitHub Pages 網址或在 GitHub 上建立 `PRIVACY.md`。

**政策範本（可放置於 https://jedieason.github.io/pathology-micro/privacy.html）：**
```markdown
# Privacy Policy for Micro (Pathology Micro)

Last updated: September 2026

Micro ("we", "our", or "the app") is committed to protecting your privacy.

1. Information Collection and Use:
Micro does not collect, transmit, sell, or share any personal identifying information (PII). All user inputs (answers, practice progress, missed questions) are stored exclusively in your local device storage.

2. Network Usage:
The app only accesses the internet to synchronize public pathology exercise data and load slide images from the official GitHub repository (https://github.com/jedieason/pathology-micro). No user diagnostics, analytics, or behavioral telemetry are gathered.

3. Third-Party Services:
The app does not incorporate third-party advertising SDKs, tracking libraries, or analytic frameworks.

4. Contact:
If you have questions regarding this Privacy Policy, please open an issue at:
https://github.com/jedieason/pathology-micro/issues
```

---

## 五、Google Play Console 上傳與發布步驟

1. **登入 Google Play 管理中心**：
   - 前往 [Google Play Console](https://play.google.com/console/)。
   - 點選「建立應用程式」，輸入應用程式名稱「Micro」、選擇預設語言「繁體中文（台灣）」、類型「應用程式」、免費。

2. **設定應用程式完整內容 (App Content)**：
   - **隱私權政策**：貼上您的隱私權政策網址。
   - **應用程式存取權**：選擇「所有功能均無須任何限制即可使用」。
   - **廣告**：選擇「否，我的應用程式不包含廣告」。
   - **內容分級**：完成簡短問卷，獲取 Everyone / PEGI 3 分級。
   - **目標客群**：勾選「18 歲以上」。
   - **資料安全性 (Data Safety)**：宣告「本應用程式不收集亦不分享任何使用者資料」。

3. **設定商店發布資訊 (Store Listing)**：
   - 填寫上述「名稱」、「簡短說明」與「完整說明」。
   - 上傳 `app-icon-512.png`（512x512 圖示）。
   - 上傳 `feature-graphic-1024x500.png`（1024x500 宣傳圖）。
   - 上傳手機截圖。

4. **上傳正式版套件 (Production or Testing Track)**：
   - 前往「發布」 >「正式版」（或先建立「內部測試」軌道進行驗證）。
   - 點選「建立新版本」。
   - 在「App 應用程式套件」區塊，直接拖曳上傳本資料夾中的 **`app-release.aab`**。
   - 版本名稱將自動代入 `1.0.0 (1)`。
   - 輸入版本資訊（Release Notes，如：`首次發布：支援鏡下病理切片觀察、三段式作答、智慧關鍵字核對與 GitHub 題庫即時同步。`）。
   - 點選「檢查發布版本」並確認送審！
