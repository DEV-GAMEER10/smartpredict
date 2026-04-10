# 🧠 SmartPredict AI

**Transform raw data into clear insights, predictions, and actionable recommendations.**

SmartPredict is an AI-powered platform that helps non-technical business users easily understand data, predict trends, and make decisions through a simple, intuitive dashboard.

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ 
- **Python** 3.10+
- **pip** (Python package manager)

### 1. Start the Backend (FastAPI)

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --port 8000
```

### 2. Start the Frontend (Next.js)

```bash
cd frontend

# Install dependencies (already done during setup)
npm install

# Start dev server
npm run dev
```

### 3. Open the App

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📊 Features

| Feature | Description |
|---------|-------------|
| **Data Upload** | Drag & drop CSV/Excel files |
| **Auto-Cleaning** | Handles missing values, duplicates, type detection |
| **Trend Prediction** | ML-powered forecasting for numeric columns |
| **Pattern Detection** | Finds correlations, clusters, and seasonal patterns |
| **Risk Analysis** | Anomaly detection and volatility warnings |
| **AI Chat** | Ask questions about your data in plain English |
| **Recommendations** | Actionable suggestions based on analysis |

## 🏗️ Tech Stack

- **Frontend:** Next.js 14 (App Router), Recharts
- **Backend:** FastAPI (Python)
- **ML:** scikit-learn (Linear Regression, Random Forest, Isolation Forest, K-Means)
- **NLP:** OpenAI API (optional) + rule-based fallback
- **Database:** SQLite (via SQLAlchemy)

## 🔑 Environment Variables

### Backend (`backend/.env`)
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for chat feature | No |
| `CORS_ORIGINS` | Allowed frontend origins | No (defaults to localhost:3000) |
| `MAX_UPLOAD_SIZE_MB` | Max upload file size | No (defaults to 50) |

### Frontend (`frontend/.env.local`)
| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | No (defaults to http://localhost:8000) |

---

## 📁 Project Structure

```
OFFGRID/
├── frontend/              # Next.js 14 App
│   ├── src/app/           # Pages (App Router)
│   ├── src/components/    # UI Components
│   └── src/lib/           # API client, utils
├── backend/               # FastAPI Backend
│   ├── app/api/routes/    # API endpoints
│   ├── app/services/      # ML engine, data cleaner, NLP
│   └── app/db/            # Database models
└── README.md
```

## 🎨 Demo

Upload the included `backend/demo_data.csv` file to see the dashboard in action with sample business data.
