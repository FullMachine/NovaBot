from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from src.api.middleware.auth import AuthMiddleware
from src.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger("auth_router", "api.log")

# TODO: Replace with actual user database
MOCK_USERS = {}

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    if user.username in MOCK_USERS:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # TODO: Hash password before storing
    MOCK_USERS[user.username] = {
        "username": user.username,
        "password": user.password,
        "email": user.email
    }
    
    # Create access token
    token_data = {"sub": user.username}
    access_token = AuthMiddleware.create_access_token(token_data)
    
    logger.info(f"New user registered: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = MOCK_USERS.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    # Create access token
    token_data = {"sub": form_data.username}
    access_token = AuthMiddleware.create_access_token(token_data)
    
    logger.info(f"User logged in: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"} 