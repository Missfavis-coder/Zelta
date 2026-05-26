# ZELTA — Behavioral Quantitative Financial Intelligence

> **Stop making financial decisions on emotion. Let the math decide. In plain English.**

ZELTA is the Anti-Sapa App for Nigerian university students. It uses Bayesian inference, crowd intelligence from Bayse Markets, and Gemini AI to detect financial stress in real time and intercept emotional spending before it happens.

---

## What's Actually Built

This repo is a monorepo with three independently deployable services:

| Service | Path | Stack | Role |
|---|---|---|---|
| **ZELTA AI Brain** | `zelta_ai/` | FastAPI + LangGraph + Gemini | Multi-agent intelligence layer |
| **ZELTA Backend** | `zelta_backend/` | FastAPI + Firebase + Vertex AI | Data, auth, wallet, portfolio |
| **ZELTA Frontend** | `/` (root) | Next.js 16 + React 19 + Tailwind | Student-facing web app |

---

## Architecture

```
Student Request
      │
      ▼
┌─────────────┐     ┌──────────────────────────────────────────┐
│  Next.js    │────▶│           ZELTA Backend (FastAPI)         │
│  Frontend   │     │  /intelligence  /wallet  /behavioral      │
└─────────────┘     │  /simulation    /copilot /portfolio       │
                    └────────────────────┬─────────────────────┘
                                         │ internal API key
                                         ▼
                    ┌──────────────────────────────────────────┐
                    │         ZELTA AI Brain (FastAPI)          │
                    │                                           │
                    │  ZeltaPipeline → LangGraph AgentLoop      │
                    │                                           │
                    │  ┌──────────┐  ┌──────────┐             │
                    │  │  Bayse   │  │  NLP     │             │
                    │  │  Markets │  │  Scraper │             │
                    │  └────┬─────┘  └────┬─────┘             │
                    │       └──────┬───────┘                   │
                    │        ┌─────▼──────┐                    │
                    │        │  Stress    │                    │
                    │        │  Index     │                    │
                    │        └─────┬──────┘                    │
                    │        ┌─────▼──────┐                    │
                    │        │  Bayesian  │                    │
                    │        │  Engine    │                    │
                    │        └─────┬──────┘                    │
                    │        ┌─────▼──────┐                    │
                    │        │  Kelly     │                    │
                    │        │  Allocator │                    │
                    │        └─────┬──────┘                    │
                    │        ┌─────▼──────┐                    │
                    │        │  Gemini    │                    │
                    │        │  Copilot   │                    │
                    │        └────────────┘                    │
                    └──────────────────────────────────────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   Firebase Firestore  │
                              │   Google Cloud Run    │
                              │   Vertex AI           │
                              └─────────────────────┘
```

---

## The BQ Framework — 4 Layers

### Layer 1 — Bayse Intelligence
Pulls live order book data from Bayse Markets (REST + WebSockets). The `LiveStressMonitor` in `zelta_ai/brain/bayse/stress_signal.py` runs a background polling loop, computing a **Crowd Fear Score** from YES/NO price imbalance and bid-ask spread.

```
Stress Score = (distance × 0.7 + spread × 0.3) × 100
```

Levels: `CALM` (0–30) → `MODERATE` (30–60) → `HIGH STRESS` (60–80) → `EXTREME PANIC` (80+)

### Layer 2 — Stress Detector
Combines market stress with NLP sentiment from campus news scraping (`zelta_ai/brain/nlp/`). Uses a `cardiffnlp/twitter-roberta-base-sentiment-latest` transformer model pre-loaded in the Docker image. Outputs a composite stress index.

### Layer 3 — Bayesian Bias Corrector
Detects **Panic Selling** and **FOMO Buying** patterns in transaction history (`zelta_ai/brain/bias/detector.py`). Applies posterior probability corrections via the Bayesian engine (`zelta_ai/brain/bayesian/engine.py`) to upcoming allocation decisions.

### Layer 4 — Quant Allocator
Modified Kelly Criterion with an academic time-decay modifier **λt**:

```
f* = (λt × b×p − q) / b

where λt = 1 − (days_to_exam / semester_length)
```

λt reduces capital exposure as exams approach — this factor is novel to student fintech. Implemented in `zelta_ai/brain/kelly/allocator.py`.

---

## LangGraph Agent Loop

`zelta_ai/brain/agent/loop.py` — the full `StateGraph`:

```
StudentModel → [BayseData, NLPData] → StressIndex → BiasDetection
            → BayesianEngine → ConfidenceScorer → KellyAllocator
            → SharpeScorer → Copilot → Output
```

The agent routes by `agent_mode` computed from the student model:
- `EMERGENCY` — runway critically low, spending freeze
- `SURVIVAL` — below safety floor, conservative allocation
- `NORMAL` — standard BQ analysis

Guardrail reflection is wired before final output — if Gemini's response fails validation it re-routes.

---

## Project Structure

```
ZELTA/
├── app/                        # Next.js frontend (App Router)
│   ├── auth/                   # Login + Signup pages
│   ├── dashboard/              # Main student dashboard
│   │   ├── behavioral/         # Bias analysis UI
│   │   ├── co-pilot/           # Gemini chat interface
│   │   ├── simulations/        # What-if financial scenarios
│   │   └── wallet/             # Wallet + transactions
│   ├── form/                   # Onboarding form
│   └── page.tsx                # Landing page
├── components/
│   ├── Button.tsx
│   ├── IntroTab.tsx
│   └── PageHeader.tsx
│
├── zelta_ai/                   # AI Brain service (deploy separately)
│   ├── main.py                 # FastAPI entry point, Bayse monitor lifespan
│   ├── security.py             # Internal API key verification
│   ├── api/routes.py           # /brain/v1/* and /api/* endpoints
│   ├── brain/
│   │   ├── agent/
│   │   │   ├── loop.py         # LangGraph StateGraph (core)
│   │   │   └── student_model.py
│   │   ├── bayesian/           # Bayesian engine + confidence
│   │   ├── bayse/              # Bayse Markets client + stress monitor
│   │   ├── bias/               # FOMO/panic bias detector
│   │   ├── copilot/            # Gemini 1.5 Pro integration
│   │   ├── kelly/              # Modified Kelly with λt
│   │   ├── nlp/                # Sentiment scraper + scorer
│   │   ├── sharpe/             # Decision quality scorer
│   │   ├── stress/             # Composite stress index
│   │   └── tools/              # Hustle templates, spending guard
│   ├── config/settings.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── zelta_backend/              # Data + auth service (deploy separately)
│   ├── main.py                 # FastAPI entry point, Firebase init
│   ├── config/settings.py      # Pydantic settings (all env vars)
│   ├── core/
│   │   ├── auth.py             # Firebase token verification
│   │   ├── firebase.py         # Firestore client init
│   │   └── dependencies.py
│   ├── middleware/cors.py
│   ├── routes/                 # intelligence, wallet, simulation,
│   │   │                       # copilot, portfolio, profile, behavioral
│   ├── schemas/                # Pydantic request/response models
│   ├── services/               # Business logic layer
│   │   ├── behavioral_service.py
│   │   ├── copilot_service.py
│   │   ├── intelligence_service.py
│   │   ├── portfolio_service.py
│   │   ├── simulation_service.py
│   │   ├── wallet_service.py
│   │   └── profile_service.py
│   ├── optimizer.py            # Portfolio optimization
│   ├── requirements.txt
│   └── Dockerfile
│
├── package.json                # Next.js 16, React 19, Tailwind 4
├── pnpm-workspace.yaml
└── tsconfig.json
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+ with pnpm
- Firebase project with Firestore enabled
- Google Cloud project with Vertex AI enabled
- Bayse Markets account (API keys)
- NewsAPI key (optional, for NLP layer)

### 1. Clone

```bash
git clone https://github.com/Tioluwanim/ZELTA
cd ZELTA
```

### 2. Environment Variables

**`zelta_ai/.env`**
```env
BAYSE_PUBLIC_KEY=your_bayse_public_key
BAYSE_PRIVATE_KEY=your_bayse_private_key
GEMINI_API_KEY=your_gemini_api_key
NEWS_API_KEY=your_newsapi_key
INTERNAL_API_KEY=a_shared_secret_between_services
DEBUG=true
PORT=8080
```

**`zelta_backend/.env`**
```env
GEMINI_API_KEY=your_gemini_api_key
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_SERVICE_ACCOUNT_JSON='{...your service account json...}'
INTERNAL_API_KEY=same_shared_secret_as_above
APP_ENV=development
DEBUG=true
```

**`.env.local`** (frontend root)
```env
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_api_key
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
```

### 3. Run the AI Brain

```bash
cd zelta_ai
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8081 --reload
```

Docs available at `http://localhost:8081/docs`

### 4. Run the Backend

```bash
cd zelta_backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

Docs available at `http://localhost:8080/docs`

### 5. Run the Frontend

```bash
# from repo root
pnpm install
pnpm dev
```

App available at `http://localhost:3000`

---

## API Reference

### AI Brain (`zelta_ai`) — port 8081

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check + live stress score |
| `GET` | `/api/stress` | Current Bayse Markets stress signal |
| `POST` | `/brain/v1/analyze` | Full BQ analysis (wallet + transactions) |
| `POST` | `/brain/v1/copilot/ask` | Ask the Gemini copilot a question |

**Sample `/brain/v1/analyze` request:**
```json
{
  "wallet_data": {
    "free_cash": 26500,
    "locked_total": 18500,
    "total_balance": 45000
  },
  "transactions": [
    { "amount": 5000, "category": "food", "type": "debit", "description": "Bukka" }
  ],
  "user_context": {
    "days_to_exam": 14,
    "semester_length": 120
  }
}
```

### Backend (`zelta_backend`) — port 8080

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/intelligence` | BQ score + stress summary |
| `GET` | `/api/wallet` | Wallet balance + transactions |
| `POST` | `/api/simulation` | Run a what-if financial scenario |
| `POST` | `/api/copilot` | Gemini financial copilot |
| `GET` | `/api/behavioral` | Bias detection report |
| `GET` | `/api/portfolio` | Portfolio optimization |
| `GET` | `/api/profile` | Student profile |

---

## Docker

Each service has its own Dockerfile. Build and run independently:

```bash
# AI Brain
cd zelta_ai
docker build -t zelta-ai .
docker run -p 8081:8080 --env-file .env zelta-ai

# Backend
cd zelta_backend
docker build -t zelta-backend .
docker run -p 8080:8080 --env-file .env zelta-backend
```

> The AI Brain image pre-downloads the `cardiffnlp/twitter-roberta-base-sentiment-latest` transformer model at build time to avoid cold-start delays on Cloud Run.

---

## Deployment (Google Cloud Run)

Both Python services are designed for Cloud Run. The `PORT` env var is respected dynamically.

```bash
# AI Brain
gcloud run deploy zelta-ai \
  --source zelta_ai/ \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars BAYSE_PUBLIC_KEY=...,GEMINI_API_KEY=...

# Backend
gcloud run deploy zelta-backend \
  --source zelta_backend/ \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=...,FIREBASE_SERVICE_ACCOUNT_JSON=...
```

The backend is configured to talk to the AI Brain at:
```
https://zelta-ai-990094999937.us-central1.run.app
```
Override via the `AI_BRAIN_URL` env var if you redeploy the brain.

---

## Financial Constants (configurable via env)

| Constant | Default | Meaning |
|---|---|---|
| `KELLY_FRACTION` | `0.5` | Half-Kelly conservative sizing |
| `MAX_INVEST_RATIO` | `0.25` | Max 25% of balance in any allocation |
| `SAVINGS_FLOOR_RATIO` | `0.60` | Warn if free cash drops below 60% |
| `BUFFER_RESERVE_NGN` | `5000` | Always keep ₦5,000 untouched |
| `STRESS_HIGH_THRESHOLD` | `60` | Trigger HIGH STRESS mode |
| `STRESS_CRISIS_THRESHOLD` | `80` | Trigger EXTREME PANIC mode |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, React 19, Tailwind CSS 4, TypeScript |
| Backend API | FastAPI 0.111, Python 3.11, Pydantic v2 |
| AI Orchestration | LangGraph, LangChain Core, Gemini 1.5 Pro |
| NLP | `cardiffnlp/twitter-roberta-base-sentiment-latest` (Transformers) |
| Market Data | Bayse Markets REST + WebSocket API |
| Database + Auth | Firebase Auth, Cloud Firestore |
| Cloud | Google Cloud Run, Vertex AI, Cloud Build |
| Containerization | Docker (multi-stage, Python 3.11-slim) |

---

## Team

Built for the 2025 Hackathon by the ZELTA team at OAU.
