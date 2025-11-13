import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional

class AuthService:
    SECRET_KEY = "cardio_secret_key_2024"
    
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), hash.encode())
    
    @staticmethod
    def create_token(user_id: int, login: str) -> str:
        payload = {
            "user_id": user_id,
            "login": login,
            "exp": datetime.utcnow() + timedelta(hours=4)
        }
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm="HS256")
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, AuthService.SECRET_KEY, algorithms=["HS256"])
        except:
            return None