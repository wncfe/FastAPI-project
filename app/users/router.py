from fastapi import APIRouter, HTTPException, status, Response
from app.users.schemas import SUserAuth
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash, verify_password, authenticate_user, create_access_token


router = APIRouter(
    prefix='/auth',
    tags=['Auth & Users'],
)

@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    
    if existing_user:
        raise HTTPException(status_code=500)
    
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    

@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    
    if not user:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
    acess_token = create_access_token({"sub": user.id})
    response.set_cookie("booking_acess_token", acess_token, httponly=True)
    
    return acess_token
