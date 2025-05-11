from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str

    @classmethod
    def from_mongo(cls, mongo_user):
        if not mongo_user:
            return None
        user_dict = {
            "id": str(mongo_user["_id"]),
            "email": mongo_user["email"],
            "username": mongo_user["username"],
            "is_active": mongo_user.get("is_active", True),
            "hashed_password": mongo_user["hashed_password"],
            "created_at": mongo_user.get("created_at", datetime.utcnow()),
            "updated_at": mongo_user.get("updated_at", datetime.utcnow())
        }
        return cls(**user_dict)

class UserService:
    def __init__(self, db):
        self.db = db
        self.collection = db["users"]

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def get_user_by_email(self, email: str):
        user = await self.collection.find_one({"email": email})
        return UserInDB.from_mongo(user) if user else None

    async def get_user_by_id(self, user_id: str):
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            return UserInDB.from_mongo(user) if user else None
        except:
            return None

    async def create_user(self, user: UserCreate):
        hashed_password = self.get_password_hash(user.password)
        user_dict = user.dict()
        user_dict.pop("password")
        user_dict["hashed_password"] = hashed_password
        
        result = await self.collection.insert_one(user_dict)
        created_user = await self.get_user_by_id(str(result.inserted_id))
        return created_user

    async def authenticate_user(self, email: str, password: str):
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user 