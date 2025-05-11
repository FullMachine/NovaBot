"""
Baseball data router.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List

router = APIRouter(
    prefix="/api/v1/baseball",
    tags=["Baseball"]
)

@router.get("/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "baseball"} 