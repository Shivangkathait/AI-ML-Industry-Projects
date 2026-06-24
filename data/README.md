# 🛒 SmartCart — Customer Segmentation Deployment Guide

## Project Structure

```
ecommerce/
└── SmartCart/
    ├── app/
    │   ├── main.py              ← FastAPI backend (ML logic)
    │   └── streamlit_app.py     ← Streamlit frontend (dashboard)
    ├── data/                    ← Put your CSV here
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    └── .dockerignore
```

---

## Prerequisites

Install these before starting:

| Tool | Download |
|------|----------|
| Docker Desktop | https://www.docker.com/products/docker-desktop |
| VS Code | https://code.visualstudio.com |
| VS Code Docker Extension | Search "Docker" in VS Code Extensions |

---

## Step-by-Step Deployment

### Step 1 — Set Up Folder

Place your project inside your ecommerce folder:

```
ecommerce/
└── SmartCart/     ← all these files go here
```

Copy your CSV (`smartcart_customers.csv`) into the `data/` folder.

### Step 2 — Open in VS Code

```bash
code ecommerce/SmartCart
```

Or: File → Open Folder → select `SmartCart`

### Step 3 — Build Docker Images

Open the VS Code terminal (`Ctrl+\``) and run:

```bash
docker compose build
```

This installs all Python packages inside Docker. Takes ~2 minutes on first run.

### Step 4 — Start All Services

```bash
docker compose up
```

You'll see logs from both services. Wait until you see:
- `Application startup complete` (FastAPI)
- `You can now view your Streamlit app` (Streamlit)

### Step 5 — Open the Apps

| Service | URL |
|---------|-----|
| 🎨 Streamlit Dashboard | http://localhost:8501 |
| ⚡ FastAPI Docs (Swagger) | http://localhost:8000/docs |

### Step 6 — Use the Dashboard

1. Go to http://localhost:8501
2. Upload your `smartcart_customers.csv`
3. Click **"Find Optimal K"** to see elbow/silhouette analysis
4. Adjust sliders → click **"Run Segmentation"**
5. Explore the 3D PCA scatter, income vs spending chart, and cluster summary

---

## Stopping & Restarting

```bash
# Stop containers (keeps data)
docker compose down

# Stop and remove everything
docker compose down -v

# Restart after code changes
docker compose up --build
```

---

## API Endpoints (FastAPI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/segment` | POST | Run clustering on CSV |
| `/optimal-k` | POST | Elbow + silhouette analysis |

### Example API call (curl):

```bash
curl -X POST "http://localhost:8000/segment?n_clusters=4&method=agglomerative" \
  -F "file=@data/smartcart_customers.csv"
```

---

## Hot Reload (Development)

The `volumes` in `docker-compose.yml` mount your local `app/` folder into the containers. This means:

- Edit `main.py` or `streamlit_app.py` in VS Code
- FastAPI reloads automatically (`--reload` flag)
- Streamlit reloads automatically on save

No need to rebuild for code changes — only rebuild if you change `requirements.txt`.

---

## Troubleshooting

**Port already in use:**
```bash
# Check what's using the port
lsof -i :8000
lsof -i :8501
```

**Module not found errors:**
```bash
docker compose build --no-cache
```

**Can't connect to API from Streamlit:**
- Make sure both containers are running: `docker compose ps`
- The Streamlit app connects to `http://fastapi:8000` (Docker internal network)

---

## Expected CSV Columns

Your CSV must contain:
`Year_Birth, Education, Marital_Status, Income, Kidhome, Teenhome, Recency, MntWines, MntFruits, MntMeatProducts, MntFishProducts, MntSweetProducts, MntGoldProds, Dt_Customer, Response, NumWebPurchases, NumCatalogPurchases, NumStorePurchases, NumWebVisitsMonth, AcceptedCmp1, AcceptedCmp2, AcceptedCmp3, AcceptedCmp4, AcceptedCmp5`
