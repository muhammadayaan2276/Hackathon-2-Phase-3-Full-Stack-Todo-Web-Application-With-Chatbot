from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from ..config.settings import settings
from typing import Optional
import uuid


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super(
            JWTBearer, self
        ).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            token = credentials.credentials
            user_id = self.verify_jwt(token)
            if not user_id:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            # Store user_id in request state for later use
            request.state.user_id = user_id
            return token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> Optional[uuid.UUID]:
        try:
            payload = jwt.decode(jwtoken, settings.better_auth_secret, algorithms=[settings.algorithm])
            user_id = payload.get("user_id")

            if user_id:
                return uuid.UUID(user_id)
        except jwt.ExpiredSignatureError:
            print("Expired signature error")
        except jwt.InvalidTokenError:
            print("Invalid token error")
        return None