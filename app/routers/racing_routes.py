"""
Racing data router.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List

router = APIRouter(
    prefix="/api/v1/racing",
    tags=["Racing"]
)

@router.get("/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "racing"} 