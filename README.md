<div align="center">

# ZELTA
### The Anti-Sapa App for Nigerian University Students

**Stop going broke mid-semester. Let the math decide what to do with your money.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-zelta.app-10b981?style=for-the-badge)](https://zelta-878473667930.europe-west1.run.app)
[![Backend API](https://img.shields.io/badge/API%20Docs-Swagger-orange?style=for-the-badge)](https://zelta-878473667930.us-central1.run.app/docs)
[![Built with Gemini](https://img.shields.io/badge/Built%20with-Gemini%201.5%20Pro-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev)
[![Powered by Bayse](https://img.shields.io/badge/Powered%20by-Bayse%20Markets-f97316?style=for-the-badge)](https://bayse.io)

</div>

---

## What is ZELTA?

Nigerian university students receive money in lump sums — allowances, bursaries, parent transfers. By week two, it is usually gone. Not because students are careless. Because no tool has ever watched how they spend, detected when they are making an emotional decision, and stopped them before it was too late.

ZELTA does exactly that.

It reads live market sentiment from Bayse prediction markets, detects your active cognitive bias from your spending patterns, and tells you one thing every week: **how much is safe to spend, how much to protect, and how many days your money will last.**

When you are about to make a dangerous spending decision, ZELTA intercepts it before the money leaves.

> **This is not a prototype. ZELTA is live and deployed at a public URL today.**

---

## The Problem We Solve

| The Problem | What Causes It | What ZELTA Does |
|---|---|---|
| Running out of money mid-semester (*Sapa*) | Irregular lump-sum income + no velocity tracking | Runway counter — shows exactly how many days your money will last |
| Impulse spending under stress | Exam pressure + peer influence impairs decisions | Intercept screen — blocks dangerous purchases before they happen |
| Following peers into bad financial decisions | Herd behaviour + no independent signal | Bayse crowd fear signal — shows when the crowd is panicking irrationally |
| Starting a campus business and losing everything | No risk modelling framework | Bayesian Monte Carlo simulator — runs 1,000 projections before you commit |
| Not knowing where your money went | Manual tracking is tedious | Gemini-powered co-pilot — ask anything, get a personalised answer in plain English |

---

## What's Actually Built

This is a monorepo with three independently deployed services:

| Service | Path | Stack | Role |
|---|---|---|---|
| **ZELTA Frontend** | `/` (root) | Next.js 15 · React · Tailwind CSS · TypeScript | Student-facing web app |
| **ZELTA Backend** | `zelta_backend/` | FastAPI · Firebase · Vertex AI · Python 3.11 | Data, auth, wallet, portfolio, behavioral analysis |
| **ZELTA AI Brain** | `zelta_ai/` | FastAPI · LangGraph · Gemini 1.5 Pro · Python 3.11 | Multi-agent intelligence and decision engine |

---

## Architecture

```
Student Opens App
       │
       ▼
┌─────────────────┐
│  Next.js 15     │  ← Firebase Auth (session cookie)
│  Frontend       │  ← TypeScript hooks → typed API responses
└────────┬────────┘
         │ Bearer token (Firebase ID token)
         ▼
┌─────────────────────────────────────────────────────┐
│              ZELTA Backend  (FastAPI)                │
│                                                     │
│  /api/intelligence   /api/wallet    /api/behavioral │
│  /api/simulation     /api/copilot   /api/portfolio  │
│  /api/profile        /api/bayse     /api/stress     │
└────────────────────────┬────────────────────────────┘
                         │ Internal API key
                         ▼
┌─────────────────────────────────────────────────────┐
│              ZELTA AI Brain  (FastAPI)               │
│                                                     │
│         ZeltaPipeline → LangGraph AgentLoop         │
│                                                     │
│   Bayse Markets ──► Stress Index ──► Bayesian       │
│   NLP Scraper   ──► Bias Detector ──► Engine        │
│   Student Model ──► Kelly Allocator ──► Copilot     │
│                                                     │
│   EMERGENCY mode │ SURVIVAL mode │ NORMAL mode      │
└────────────────────────┬────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │  Firebase Firestore  │
              │  Google Cloud Run    │
              │  Vertex AI           │
              └─────────────────────┘
```

---

## The BQ Intelligence Framework

ZELTA's brain runs in four sequential layers. Each layer feeds the next.

### Layer 1 — Bayse Market Intelligence
Connects to [Bayse Markets](https://bayse.io) via REST and WebSocket. A background monitor (`zelta_ai/brain/bayse/stress_signal.py`) continuously computes a **Crowd Fear Score** from the live YES/NO price imbalance and bid-ask spread.

```
Crowd Fear Score = (price_distance_from_0.5 × 0.7 + spread × 0.3) × 100

CALM        0 – 30    Market behaving rationally
MODERATE   30 – 60    Some tension, stay cautious
HIGH       60 – 80    Significant crowd panic
EXTREME    80 – 100   Full fear — hold all money
```

### Layer 2 — Composite Stress Index
Fuses the Bayse fear score with NLP sentiment extracted from Nigerian financial news headlines (via `cardiffnlp/twitter-roberta-base-sentiment-latest`). Produces a single 0–100 stress index that represents the actual financial environment a student is operating in right now.

### Layer 3 — Behavioral Bias Detector
Analyses the student's real transaction history and detects which of five cognitive biases is currently active:

| Bias | Student form | What triggers it |
|---|---|---|
| **Present Bias** | Spending rent money on food today | Impulse purchase while obligation is due |
| **Loss Aversion** | Panic-withdrawing cash when stressed | Cash withdrawal during high stress |
| **Mental Accounting** | Treating side hustle money as "extra" | Spending spike after income receipt |
| **Herd Behaviour** | Following friends into mass purchases | Spending cluster matching peer patterns |
| **Overconfidence** | Overspending when market is calm | Spending surge during low-stress period |

### Layer 4 — Modified Kelly Allocator
Calculates the mathematically optimal spending and saving split using a student-specific Kelly formula with an **academic time-decay modifier (λt)**:

```
f* = λt × (b·p − q) / b

where:
  b  = expected return ratio
  p  = probability of safe outcome (from Bayesian engine)
  q  = 1 − p
  λt = 1 − (days_to_exam / semester_length)   ← novel student factor
```

`λt` automatically reduces capital exposure as exams approach — shifting ZELTA from opportunity mode to preservation mode without any user input. This factor is novel to student fintech.

---

## The LangGraph Agent Loop

`zelta_ai/brain/agent/loop.py` runs a full stateful `StateGraph` with mode-based routing:

```
StudentModel
     │
     ├── EMERGENCY ──► emergency_tools_node ──► check_purchase_safety
     │                                       └► get_hustle_templates
     │
     ├── SURVIVAL ───► survival_tools_node ───► check_purchase_safety
     │                                       └► get_hustle_templates
     │
     └── NORMAL ─────► [fetch_market_data] ──► [run_stress_index]
                     ──► [detect_bias] ────────► [run_bayesian_engine]
                     ──► [run_confidence] ───────► [run_kelly]
                     ──► [run_sharpe] ─────────────► [run_copilot]
                     ──► [guardrail_reflection] ────► Output
```

The guardrail reflection node validates Gemini's output against financial safety rules before it reaches the student. If it fails, it re-routes and regenerates.

---

## Key Features

### Sapa Health Bar
Visual survival score — the first thing a student sees on the dashboard. Computed from free cash, runway, bias strength, and market stress. Green above 60%, amber 30–60%, red below 30%. Shows the exact number of days money will last at the current spending pace.

### Intercept Screen
Before any expense that would drop runway below 7 days or cost more than 20% of free cash, ZELTA blocks the screen:
> *"Chief, this drops your runway from 14 days to 9 days. Your 4-day streak will break. Are you sure?"*

The student can cancel (streak protected) or proceed anyway (flagged as `impulse_flagged: true` and fed to the bias detector as real evidence).

### Zé — Autonomous Agent
ZELTA's AI character proactively pushes alerts without the student asking:
- When runway drops below 7 days
- When Bayse fear spikes above 70%
- When a spending pattern matches an active bias
- When a new campus gig matches the student's skills
- After streak milestones

Zé is not just a chatbot — it monitors and acts.

### What If? Simulator
Runs 1,000 Bayesian Monte Carlo projections on a side hustle idea before the student commits money. Takes inputs (investment amount, expected revenue range, fixed costs, time horizon), applies the Kelly formula, and returns a probabilistic outcome with success probability, expected return, and a verdict: Go For It / Hold / Protect Your Money.

### Floating Co-Pilot
Available on every dashboard page. Answers plain-English questions with the student's actual financial situation pre-loaded as context:
- "Will my money last till month end?"
- "Can I afford to go out this weekend?"
- "My mum sent ₦15,000 — what do I do first?"

### Decision History
Logs every ZELTA recommendation with its outcome. Tracks accuracy rate, net P&L (vs doing nothing), and shows which decisions were CORRECT, INCORRECT, or still TRACKING.

---

## Project Structure

```
ZELTA/
│
├── app/                            # Next.js frontend (App Router)
│   ├── (auth)/                     # Login + Signup pages
│   │   ├── login/
│   │   └── sign-up/
│   ├── dashboard/                  # All authenticated pages
│   │   ├── behavioral/             # Bias analysis + 8-week pattern
│   │   │   └── components/         # bayse, active, decision, five, weeks, zelta
│   │   ├── co-pilot/               # Gemini chat interface
│   │   ├── history/                # Decision history + accuracy tracking
│   │   ├── profile/                # Student profile + settings
│   │   ├── simulations/            # What-if financial simulator
│   │   │   └── components/         # SimulationResults
│   │   ├── wallet/                 # Wallet, transactions, locked goals
│   │   ├── BiasAlertCard.tsx
│   │   ├── DecisionScoreCard.tsx
│   │   ├── MarketAlert.tsx
│   │   ├── StressIndexCard.tsx
│   │   ├── WeeklyVerdictCard.tsx
│   │   ├── Sidebar.tsx
│   │   ├── dashboard.tsx
│   │   └── layout.tsx
│   ├── form/                       # Onboarding form (new student setup)
│   └── page.tsx                    # Landing page
│
├── components/                     # Shared components
│   ├── FloatingCopilot.tsx         # Persistent Zé chat on every page
│   ├── SurvivalBanner.tsx          # Emergency/survival mode alert
│   ├── DashboardHeader.tsx
│   ├── OnboardingOverlay.tsx
│   ├── PageHeader.tsx
│   └── ui/                         # State, button, error components
│
├── context/
│   ├── authContext.tsx             # Firebase Auth + session cookie
│   ├── zeltaContext.tsx            # Global dashboard data provider
│   └── BehavioralSnapshotContext.tsx
│
├── hooks/
│   ├── useFetch.ts                 # Authenticated apiFetch utility
│   └── zelta.ts                   # All data hooks (useWallet, useStress, etc.)
│
├── types/
│   └── zelta.ts                   # Full TypeScript type definitions
│
├── firebase/                       # Firebase client init
│
│
├── zelta_ai/                       # AI Brain service — deploy separately
│   ├── main.py                     # FastAPI app + Bayse monitor lifespan
│   ├── security.py                 # Internal API key verification
│   ├── api/routes.py               # /brain/v1/* endpoints
│   ├── app/router.py               # Legacy router (no-op, see api/routes.py)
│   ├── brain/
│   │   ├── agent/
│   │   │   ├── loop.py             # LangGraph StateGraph — core agent
│   │   │   └── student_model.py    # ZeltaStudentModel: survival signals
│   │   ├── bayesian/               # Bayesian engine + confidence scorer
│   │   ├── bayse/                  # Bayse Markets client + LiveStressMonitor
│   │   ├── bias/                   # Cognitive bias detector (5 biases)
│   │   ├── copilot/                # Gemini 1.5 Pro integration + prompts
│   │   ├── kelly/                  # Modified Kelly with λt
│   │   ├── nlp/                    # Sentiment scraper + RoBERTa scorer
│   │   ├── pipeline.py             # ZeltaPipeline orchestrator
│   │   ├── sharpe/                 # Decision quality scorer
│   │   ├── stress/                 # Composite stress index
│   │   └── tools/                  # check_purchase_safety, get_hustle_templates
│   ├── config/settings.py
│   ├── requirements.txt            # langgraph>=0.2.0,<1.0.0
│   └── Dockerfile
│
├── zelta_backend/                  # Data + auth service — deploy separately
│   ├── main.py                     # FastAPI app + Firebase init
│   ├── config/settings.py          # Pydantic settings
│   ├── core/
│   │   ├── auth.py                 # Firebase ID token verification
│   │   ├── firebase.py             # Firestore client
│   │   └── dependencies.py
│   ├── middleware/cors.py
│   ├── optimizer.py                # Brain response normalizer
│   ├── routes/                     # All API routes
│   │   ├── intelligence.py
│   │   ├── wallet.py
│   │   ├── simulation.py
│   │   ├── copilot.py
│   │   ├── portfolio.py
│   │   ├── profile.py
│   │   └── behavioral.py
│   ├── schemas/                    # Pydantic request/response models
│   ├── services/                   # Business logic
│   │   ├── intelligence_service.py # Enriches wallet_data with survival signals
│   │   ├── behavioral_service.py
│   │   ├── copilot_service.py
│   │   ├── portfolio_service.py
│   │   ├── simulation_service.py
│   │   ├── wallet_service.py
│   │   └── profile_service.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── package.json                    # Next.js 15, React, Tailwind CSS 4
├── middleware.ts                   # Route protection (session cookie)
├── .env.example                    # All required env vars documented
└── tsconfig.json
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+ with `pnpm`
- Firebase project (Firestore + Auth enabled)
- Google Cloud project (Vertex AI enabled)
- Bayse Markets account ([bayse.io](https://bayse.io))
- NewsAPI key (optional — for NLP fallback)

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
GOOGLE_CLOUD_PROJECT=your_gcp_project_id
GOOGLE_CLOUD_LOCATION=us-central1
VERTEX_GEMINI_MODEL=gemini-1.5-flash
NEWS_API_KEY=your_newsapi_key
INTERNAL_API_KEY=a_shared_secret_between_services
DEBUG=true
PORT=8081
```

**`zelta_backend/.env`**
```env
GEMINI_API_KEY=your_gemini_api_key
FIREBASE_SERVICE_ACCOUNT_JSON='{...your service account json...}'
AI_BRAIN_URL=http://localhost:8081
INTERNAL_API_KEY=same_shared_secret_as_above
APP_ENV=development
DEBUG=true
PORT=8080
```

**`.env.local` (frontend root)**
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
NEXT_PUBLIC_FIREBASE_APIKEY=your_firebase_api_key
NEXT_PUBLIC_FIREBASE_AUTHDOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECTID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

### 3. Run the AI Brain

```bash
cd zelta_ai
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8081 --reload
# Swagger: http://localhost:8081/docs
```

### 4. Run the Backend

```bash
cd zelta_backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
# Swagger: http://localhost:8080/docs
```

### 5. Run the Frontend

```bash
# from repo root
pnpm install
pnpm dev
# App: http://localhost:3000
```

---

## API Reference

### AI Brain — port 8081

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check + live Bayse stress score |
| `GET` | `/api/stress` | Current composite stress index (0–100) |
| `GET` | `/api/bayse/stress` | Raw Bayse crowd fear score |
| `GET` | `/api/bayse/sentiment` | Market sentiment direction |
| `GET` | `/api/bayse/markets` | Live Bayse market data |
| `POST` | `/brain/v1/analyze` | Full BQ analysis — student model + allocation |
| `POST` | `/brain/v1/copilot/ask` | Ask Zé a question with full context |
| `GET` | `/brain/v1/hustle-templates` | Campus hustle ideas by agent mode |

**Sample `/brain/v1/analyze` request:**
```json
{
  "wallet_data": {
    "free_cash": 26500,
    "locked_total": 18500,
    "total_balance": 45000,
    "weekly_burn_rate": 8500,
    "upcoming_obligations": 58000
  },
  "transactions": [
    { "amount": 5000, "category": "food", "type": "expense", "date": "2026-05-28" }
  ],
  "user_context": {
    "days_to_exam": 14,
    "semester_length": 120,
    "risk_tolerance": "conservative"
  }
}
```

### Backend — port 8080

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/intelligence` | Weekly verdict + full BQ score |
| `GET` | `/api/wallet` | Balance, transactions, spending heat, goals |
| `POST` | `/api/wallet/income` | Log income (source + amount) |
| `POST` | `/api/wallet/expense` | Log expense (category + amount) |
| `POST` | `/api/wallet/lock` | Lock a savings goal |
| `POST` | `/api/simulation/side-hustle` | Run Monte Carlo side hustle projection |
| `POST` | `/api/simulation/savings` | Run savings trajectory simulation |
| `POST` | `/api/copilot` | Gemini co-pilot with full student context |
| `GET` | `/api/behavioral/snapshot` | Bias snapshot + evidence |
| `GET` | `/api/behavioral/pattern` | 8-week behavioral pattern |
| `GET` | `/api/portfolio` | Decision history + accuracy + P&L |
| `GET` | `/api/profile` | Student profile |
| `PATCH` | `/api/profile` | Update profile |
| `GET` | `/api/bayse/stress` | Bayse crowd fear (proxied) |
| `GET` | `/api/bayse/sentiment` | Bayse sentiment (proxied) |
| `GET` | `/api/bayse/markets` | Bayse market list (proxied) |

All backend routes require `Authorization: Bearer <firebase_id_token>`.

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

> The AI Brain Dockerfile pre-downloads `cardiffnlp/twitter-roberta-base-sentiment-latest` at build time to eliminate cold-start delays on Cloud Run.

---

## Deployment (Google Cloud Run)

```bash
# AI Brain
gcloud run deploy zelta-ai \
  --source zelta_ai/ \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars BAYSE_PUBLIC_KEY=...,GEMINI_API_KEY=...,INTERNAL_API_KEY=...

# Backend
gcloud run deploy zelta-backend \
  --source zelta_backend/ \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FIREBASE_SERVICE_ACCOUNT_JSON=...,INTERNAL_API_KEY=...,AI_BRAIN_URL=https://zelta-ai-...run.app
```

Override the AI Brain URL on the backend via `AI_BRAIN_URL` env var.

---

## Financial Constants

Configurable via environment variables:

| Constant | Default | Meaning |
|---|---|---|
| `KELLY_FRACTION` | `0.5` | Half-Kelly conservative sizing |
| `MAX_INVEST_RATIO` | `0.25` | Max 25% of balance per allocation |
| `SAVINGS_FLOOR_RATIO` | `0.60` | Warn when free cash drops below 60% |
| `BUFFER_RESERVE_NGN` | `5000` | Always protect ₦5,000 minimum |
| `STRESS_HIGH_THRESHOLD` | `60` | Trigger HIGH STRESS mode |
| `STRESS_CRISIS_THRESHOLD` | `80` | Trigger EXTREME PANIC mode |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15 · React 19 · Tailwind CSS 4 · TypeScript |
| Backend API | FastAPI 0.111 · Python 3.11 · Pydantic v2 |
| AI Orchestration | LangGraph · LangChain Core · Gemini 1.5 Pro + Flash |
| NLP | cardiffnlp/twitter-roberta-base-sentiment-latest |
| Market Data | Bayse Markets REST + WebSocket |
| Auth + Database | Firebase Auth · Cloud Firestore |
| Cloud | Google Cloud Run · Vertex AI · Cloud Build |
| Containerization | Docker (multi-stage · Python 3.11-slim) |

---

## Roadmap

- [ ] **Mono Connect** — automatic bank transaction import (read-only)
- [ ] **Squad Wallet** — virtual account per student, real locked vaults
- [ ] **Intercept Screen** — blocks dangerous spending before it happens
- [ ] **Sapa Health Bar** — visual survival score on dashboard
- [ ] **Gig Marketplace** — campus micro-gigs posted via WhatsApp, accepted in-app
- [ ] **Zé Agent Cards** — proactive autonomous alerts on every dashboard load
- [ ] **Firebase Cloud Messaging** — push notifications when stress spikes
- [ ] **Academic Calendar** — semester dates fed to λt automatically
- [ ] **Peer Spending Aggregates** — anonymised campus spending comparison

---

## Team

Built for the **OPay Innovation Challenge 2026** by the ZELTA team at Obafemi Awolowo University, Ile-Ife.

---

<div align="center">

**ZELTA — Know your money. Before it's gone.**

</div>
