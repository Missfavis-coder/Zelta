"""
ZELTA Backend — Behavioral Quantitative Financial Intelligence
FastAPI + Firebase + Vertex AI

Entry point: initializes Firebase, registers all routes, and starts the server.
"""

import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from config.settings import settings
from core.firebase import initialize_firebase
from middleware.cors import setup_cors
from routes import intelligence, wallet, simulation, copilot, portfolio, profile, dev_auth, behavioral

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def is_debug_mode() -> bool:
    """
    Safe debug check that works even if settings changes later.
    """
    return getattr(settings, "debug", False) or getattr(settings, "app_env", "").lower() == "development"


# ─── Lifespan ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize Firebase on startup."""
    logger.info("ZELTA Backend starting up...")
    try:
        initialize_firebase()
        logger.info("Firebase initialized. BQ Brain ready.")
    except Exception:
        logger.critical("Failed to initialize Firebase.", exc_info=True)
        raise
    yield
    logger.info("ZELTA Backend shutting down.")


# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ZELTA Backend",
    description=(
        "Behavioral Quantitative Financial Intelligence for Nigerian university students. "
        "Powered by Bayse Markets crowd intelligence, Bayesian inference, and Kelly Criterion allocation."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── Middleware ────────────────────────────────────────────────────────────────
setup_cors(app)

# ─── Routes ───────────────────────────────────────────────────────────────────
app.include_router(intelligence.router)
app.include_router(behavioral.router)
app.include_router(wallet.router)
app.include_router(simulation.router)
app.include_router(copilot.router)
app.include_router(portfolio.router)
app.include_router(profile.router)
app.include_router(dev_auth.router)


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "service": "ZELTA Backend",
        "version": "1.0.0",
        "status": "operational",
        "description": "Behavioral Quantitative Financial Intelligence",
        "powered_by": ["Bayse Markets", "Gemini Pro", "Vertex AI", "FastAPI"],
    }


@app.get("/health", tags=["Health"])
async def health():
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "zelta-backend"},
    )


# ─── Global Exception Handler ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.detail},
        )

    logger.error("Unhandled exception on %s", request.url, exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected error occurred.",
            "detail": str(exc) if is_debug_mode() else "Internal Server Error",
        },
    )


# ─── Dev Server ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=is_debug_mode(),
    )
