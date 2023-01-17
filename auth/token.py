import jwt
import datetime
import os

def create_token(user_id: int) -> str:
    """
    Creates a JWT token with the given user id.
    """

    secret = os.getenv("SECRET_KEY")

    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def verify_token(token: str) -> int:
    """
    Verifies the given JWT token and returns the user id.
    """
    try:
        secret = os.getenv("SECRET_KEY")

        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.DecodeError:
        raise ValueError("Invalid token")
