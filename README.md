# paper-database-to-notion

Automated research paper management system that builds a searchable, filterable database in Notion. Supports importing metadata and PDFs from arXiv, Semantic Scholar, and DOI. Ideal for researchers who want to stay organized without manual data entry.

---

## 🌟 Why This Exists

- Researchers often discover papers via arXiv.
- Managing PDFs, metadata, notes, and citations manually is slow and error-prone.
- This tool automates the entire process:
    - 🔄 Search by DOI, arXiv ID, or Semantic Scholar ID
    - 📂 Create a Notion page with metadata
    - 📁 Download and organize the PDF locally

---

## 🛠️ Setup: Preparing Your Notion Database

### Step 1: Duplicate the Template
Duplicate this [Notion template](https://thorn-nymphea-be8.notion.site/5949a9924cc546799804a42ca4917d81) into your own workspace.

### Step 2: Create a Notion Integration
- Go to: [Notion Integrations](https://www.notion.so/my-integrations)
- Create a new integration
- Copy the **Internal Integration Token**

### Step 3: [Connect Your Database](https://www.notion.com/help/add-and-manage-connections-with-the-api#add-connections-to-pages)
- In your duplicated database, go to the three dots (upper right corner) -> Connections -> Connect your created integration
- Copy the database ID from the URL (it's the part after the last `/`).

---

## 🗂️ Configuring `paper-database-to-notion`

First time setup inside the app: Go to `Configurations > Set API Keys` in the app and enter:

- Notion Token (from Step 2)
- Notion Database ID (from Step 3)
- Download Directory (Optional, where PDFs will be saved)

---

## 🚀 Using the App

1. Open the app (`paper-database-to-notion`)
2. Enter a **paper identifier** (DOI, arXiv ID, or Semantic Scholar ID)
3. Set an optional **subfolder** and **tags** (comma or semicolon separated)
4. Click **Search and Download**
5. PDF is saved locally + Notion page is created

---

## 📅 Example Inputs

| Type | Example |
|---|---|
| DOI | `10.48550/arXiv.2106.04566` |
| arXiv ID/Link | `arxiv:2106.04566` or `2106.04566` |
| Semantic Scholar Link | [Like this one](https://www.semanticscholar.org/paper/Impact-of-a-rigid-sphere-onto-an-elastic-membrane-Ag%C3%BCero-Alventosa/2e3e5215e75cedd8b1f49234cd9ffd33bbac6658) |

---

## 📝 Installation Options

### From Source (for Developers)
```bash
pip install -r requirements.txt
python QtUI.py
```

### Standalone App (for Users)
- Download from: [Releases Page](https://github.com/yourusername/paper-database-to-notion/releases)
- Double-click `paper-database-to-notion.app` (macOS) or `paper-database-to-notion.exe` (Windows)

---

## ⚠️ Important Notes

- Works best with Python 3.10+
- Requires a free Notion account
- You must prepare your Notion database first using the template provided.

---

## 📂 Config File Location

| OS | Path |
|---|---|
| macOS/Linux | `~/.paper-database-to-notion/config.json` |
| Windows | `%APPDATA%\paper-database-to-notion\config.json` |

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

