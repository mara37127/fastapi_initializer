from fastapi import Security, Depends

import config.database as database
from config.database import db_state_default

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from services.authService import AuthService

# Dependency
async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


security = HTTPBearer()
authHandler = AuthService()

def isAuthenticated(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(authHandler.decode_token(token)):
        return True
    return False