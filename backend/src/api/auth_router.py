from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from ..services.auth_service import create_access_token
from ..middleware.auth_middleware import JWTBearer
import uuid


auth_router = APIRouter()


@auth_router.post("/token")
async def login(username: str, password: str):
    # This is a simplified example - in a real application,
    # you would verify the username/password against a database
    # For now, we'll just generate a token for demonstration purposes
    user_id = str(uuid.uuid4())  # In a real app, this would come from DB after validation
    access_token = create_access_token(data={"user_id": user_id})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    return {"message": "This is a protected route", "credentials": credentials.credentials}