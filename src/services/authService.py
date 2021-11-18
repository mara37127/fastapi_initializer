import os # For environment variables
import jwt  # used for encoding and decoding jwt tokens
from fastapi import HTTPException  # used to handle error handling
from passlib.context import CryptContext  # used for hashing the password
from datetime import datetime, timedelta # used to handle expiry time for tokens
from dotenv import load_dotenv # used to load environment variables from .env file




class AuthService:
    """
    AuthService class
    """
    def __init__(self):
        load_dotenv()
        self.secret = os.getenv('JWT_SECRET')
        self.JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
        self.hasher = CryptContext(schemes=['bcrypt'])
        

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': username,
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=self.JWT_ALGORITHM
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[
                                 self.JWT_ALGORITHM])
            if (payload['scope'] == 'access_token'):
                return payload['sub']
            raise HTTPException(
                status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def encode_refresh_token(self, username):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=10),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=self.JWT_ALGORITHM
        )

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(
                refresh_token, self.secret, algorithms=[self.JWT_ALGORITHM])
            if (payload['scope'] == 'refresh_token'):
                username = payload['sub']
                refresh_token = self.encode_refresh_token(username)
                access_token = self.encode_token(username)
                return {'access_token': access_token, 'refresh_token': refresh_token}
            raise HTTPException(
                status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401, detail='Invalid refresh token')
