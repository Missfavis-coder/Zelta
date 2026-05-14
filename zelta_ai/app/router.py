"""
app/router.py — ZELTA AI router registry

Fix 5: main.py already mounts api/routes.py (which has /brain/v1/* and /api/*).
The old app/router.py duplicated the /brain/* prefix from app/router.py,
creating conflicting routes (/brain/intelligence vs /brain/v1/intelligence).

Resolution:
  - main.py is the single mount point (already correct — imports from api.routes)
  - app/router.py is kept for legacy import compatibility but does nothing
  - All real routing lives in api/routes.py (prefix=/brain/v1) and app/router.py (prefix=/brain)
  - The backend optimizer.py tries /brain/v1/intelligence first, then /brain/intelligence as fallback
    so both prefixes work during the transition

If you want to remove /brain/* (old prefix) entirely:
  1. Remove `from app.router import router` from main.py (already done — main.py uses api.routes)
  2. Delete this file
  3. Update optimizer.py to only call /brain/v1/intelligence
"""

# This file is intentionally left as a no-op.
# The active router is in api/routes.py.
# Keeping this file prevents ImportError if anything still imports it.

from fastapi import APIRouter
router = APIRouter()  # empty — not mounted