"""
Esports data router.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List

router = APIRouter(
    prefix="/api/v1/esports",
    tags=["Esports"]
)

@router.get("/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "esports"} 