# arxiv-workflow

### Automatic pipeline to collect, store, and manage arXiv papers in **Notion** — with a user-friendly desktop app.

---

## 🌟 Why This Exists

- Researchers often discover papers via arXiv.
- Managing PDFs, metadata, notes, and citations manually is slow and error-prone.
- This tool automates the entire process:
    - 🔄 Search by DOI, arXiv ID, or Semantic Scholar ID
    - 📂 Create a Notion page with metadata
    - 📁 Download and organize the PDF locally

---

## 📊 The Core Idea

| Manual Process | After Using arxiv-workflow |
|---|---|
| Search on arXiv website | Search from the app |
| Manually create Notion page | Notion page auto-created |
| Download PDF manually | PDF auto-downloaded |
| Copy-paste BibTeX | BibTeX fetched for you |

---

## 🛠️ Setup: Preparing Your Notion Database

### Step 1: Duplicate the Template
Duplicate this [Notion template](https://thorn-nymphea-be8.notion.site/5949a9924cc546799804a42ca4917d81) into your own workspace.

### Step 2: Create a Notion Integration
- Go to: [Notion Integrations](https://www.notion.so/my-integrations)
- Create a new integration
- Copy the **Internal Integration Token**

### Step 3: Connect Your Database
- In your duplicated database, click "Share" and invite your integration.
- Copy the database ID from the URL (it's the part after the last `/`).

---

## 🗂️ Configuring `arxiv-workflow`

First time setup: Go to `Configurations > Set API Keys` in the app and enter:

- Notion Token (from Step 2)
- Notion Database ID (from Step 3)
- Download Directory (where PDFs will be saved)

---

## 🚀 Using the App

1. Open the app (`arxiv-workflow`)
2. Enter a **paper identifier** (DOI, arXiv ID, or Semantic Scholar ID)
3. Set an optional **subfolder** and **tags** (comma or semicolon separated)
4. Click **Search and Download**
5. PDF is saved locally + Notion page is created

---

## 📅 Example Inputs

| Type | Example |
|---|---|
| DOI | `10.48550/arXiv.2106.04566` |
| arXiv ID | `arxiv:2106.04566` or `2106.04566` |
| Semantic Scholar | `SS12345678` (future support) |

---

## 📝 Installation Options

### From Source (for Developers)
```bash
pip install -r requirements.txt
python QtUI.py
```

### Standalone App (for Users)
- Download from: [Releases Page](https://github.com/yourusername/arxiv-workflow/releases)
- Double-click `arxiv-workflow.app` (macOS) or `arxiv-workflow.exe` (Windows)

---

## ⚠️ Important Notes

- Works best with Python 3.10+
- Requires a free Notion account
- You must prepare your Notion database first using the template provided.

---

## 📂 Config File Location

| OS | Path |
|---|---|
| macOS/Linux | `~/.arxiv-workflow/config.json` |
| Windows | `%APPDATA%\arxiv-workflow\config.json` |

---

## 🔗 Useful Links

- Notion API Docs: [https://developers.notion.com/reference/post-database-query](https://developers.notion.com/reference/post-database-query)
- arXiv API Docs: [https://arxiv.org/help/api](https://arxiv.org/help/api)

---

## 📃 Contribute

- Found a bug? Open an issue!
- Want to improve it? Pull requests welcome.

---

## 💚 If you find this project helpful, give it a star on GitHub!

---

