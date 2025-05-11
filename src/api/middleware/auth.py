from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from src.utils.logger import setup_logger

logger = setup_logger("auth", "api.log")

# TODO: Move to config
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if self._should_skip_auth(request.url.path):
            return await call_next(request)

        try:
            # Extract token from header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication credentials"
                )
            
            token = auth_header.split(" ")[1]
            payload = self._decode_token(token)
            
            # Add user info to request state
            request.state.user = payload
            
            # Process request
            response = await call_next(request)
            return response

        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail="Authentication failed"
            )

    def _should_skip_auth(self, path: str) -> bool:
        """Paths that don't require authentication"""
        public_paths = [
            "/",
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/register"
        ]
        return any(path.startswith(skip_path) for skip_path in public_paths)

    def _decode_token(self, token: str) -> dict:
        """Decode and validate JWT token"""
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    @staticmethod
    def create_access_token(data: dict):
        """Create a new JWT token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 