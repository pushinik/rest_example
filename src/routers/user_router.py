from typing import Annotated
from fastapi import APIRouter, Depends

from auth import get_current_active_user
from orm.user import User

user_router = APIRouter()

@user_router.get('/user')
def get_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {
        'id': current_user.id,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'phone': current_user.phone
    }
