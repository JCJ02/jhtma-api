from jose import JWTError, jwt
from api.configurations.configuration import configuration
from datetime import datetime, timedelta
from typing import Union, Dict, Any

ALGORITHM = "HS256"

class TokenManager:
    @staticmethod
    async def generate_access_token(payload: Union[str, Dict[str, Any]]) -> str:
        secret_key = configuration["key"]["secretKey"]
        expires_in = int(configuration["key"]["expiresIn"])
        expiration = datetime.utcnow() + timedelta(seconds=expires_in)

        # Add expiration time to payload
        if isinstance(payload, dict):
            payload["expiration"] = int(expiration.timestamp())
        else:
            payload = {"expiration": expiration, "data": payload}

        return jwt.encode(payload, secret_key, algorithm=ALGORITHM)
    
    @staticmethod
    async def generate_refresh_token(payload: Union[str, Dict[str, Any]]) -> str:
        secret_key = configuration["key"]["refreshKey"]
        expires_in = int(configuration["key"]["refreshExpiresIn"])
        expiration = datetime.utcnow() + timedelta(seconds=expires_in)

        # Add expiration time to payload
        if isinstance(payload, dict):
            payload["expiration"] = int(expiration.timestamp())
        else:
            payload = {"expiration": expiration, "data": payload}

        return jwt.encode(payload, secret_key, algorithm=ALGORITHM)
    
    @staticmethod
    async def verify_access_token(access_token: str) -> Dict[str, Any]:
        secret_key = configuration["key"]["secretKey"]

        try:
            return jwt.decode(access_token, secret_key, algorithms=[ALGORITHM])
        except JWTError as error:
            raise ValueError(f"Access Token Validation Failed: {str(error)}")
    
    @staticmethod
    async def verify_refresh_token(refresh_token: str) -> Dict[str, Any]:
        secret_key = configuration["key"]["refreshKey"]

        try:
            return jwt.decode(refresh_token, secret_key, algorithms=[ALGORITHM])
        except JWTError as error:
            raise ValueError(f"Refresh Token Validation Failed: {str(error)}")