# MF IT Assets Management System

A web application for managing IT assets (laptops, desktops, printers, monitors). Built with FastAPI + SQLAlchemy (SQLite) backend and a modern dark-themed HTML frontend.

## Features

- **Asset List** — Searchable, filterable table of all IT assets with status badges
- **Asset Detail** — Click any row to see full device specs, financials, and assignment info
- **API Endpoints**:
  - `GET /` — Asset list page
  - `GET /detail?id=N` — Asset detail page
  - `GET /assets/` — JSON list (supports `?search=`, `?status=`, `?type=` filters)
  - `GET /assets/{id}` — Full asset detail JSON

## Quick Start

### 1. Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
python -m uvicorn app.main:app --reload
```

### 4. Open in browser
- **Asset List**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Project Structure

```
Asset-Management/
├── requirements.txt            # Python dependencies
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── api/assets.py           # API routes (list + detail)
│   ├── core/database.py        # SQLAlchemy engine & session
│   ├── models/asset.py         # MFITAsset ORM model
│   ├── data/asset_db.db        # SQLite database
│   └── static/
│       ├── index.html          # Asset list page
│       ├── detail.html         # Asset detail page
│       └── styles.css          # Dark theme styles
```

## Database

- **Table**: `MF_IT_Assets` (268 rows, 28 columns)
- **Engine**: SQLite at `app/data/asset_db.db`
