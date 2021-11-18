from services.authService import AuthService
from services.userService import UserService
from schemas import AuthModel, User
from fastapi import FastAPI, HTTPException, Security, APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer




router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {"description": "Not found"}}
)

security = HTTPBearer()
auth_handler = AuthService()
user_service = UserService()


@router.post("/login")
def login(user_details: AuthModel):
    user = user_service.get_user_by_username(user_details.username)
    if (user is None):
        return HTTPException(status_code=401, detail='Invalid username')
    if (not auth_handler.verify_password(user_details.password, user['password'])):
        return HTTPException(status_code=401, detail='Invalid password')

    access_token = auth_handler.encode_token(user['username'])
    refresh_token = auth_handler.encode_refresh_token(user['username'])
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post("/signup")
def signup(user_details: AuthModel):
    
    if user_service.get_user(user_details.username) != None:
        return 'Account already exists'
    try:
        user = User.parse_obj(user_details)
        usr = user_service.create_user(user)
        return {'message': f'Account {usr} created successfully'}
    except Exception as _:
        error_msg = 'Failed to signup user'
        return {'message': error_msg}


@router.get("/refresh_token")
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return new_token
