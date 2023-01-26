# RM NOTE: I generated this file along with auth_handler.py largely from this: https://testdriven.io/blog/fastapi-jwt-auth/

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth_handler import decodeJWT
from loguru import logger
import sys

logger.add("logs/log.json", format="Log {level} at {time} has message: {message}", serialize=True)
logger.add(sys.stdout, format="Log {level} at {time} has message: {message} (Extra data below) \n{extra}", serialize=False) 

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = None
        try:
          credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
          if credentials:
              if not credentials.scheme == "Bearer":
                  raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
              if not self.verify_jwt(credentials.credentials):
                  raise HTTPException(status_code=403, detail="Invalid token or expired token.")
              return credentials.credentials
          else:
              raise HTTPException(status_code=403, detail="Invalid authorization code.")
        except Exception as e:
          logger.error("JWT Authentication failed.", error=e, credentials=credentials)
          raise HTTPException(status_code=403, detail="JWT Authentication failed.") 

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid