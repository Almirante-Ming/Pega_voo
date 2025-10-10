from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional, List, Annotated, TYPE_CHECKING
from http import HTTPStatus as HttpStatusCodes

from tinto import models
from .auth import SECRET_KEY, ALGORITHM
from .types import User_Status
from .database import DBSession

if TYPE_CHECKING:
    from tinto.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=HttpStatusCodes.UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]) -> "TokenData":
    from tinto.schemas import TokenData as RuntimeTokenData
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #type: ignore
        name: Optional[str] = payload.get("sub")
        user_id: Optional[int] = payload.get("user_id")
        acc_level: Optional[int] = payload.get("acc_level")
        if name is None or user_id is None or acc_level is None:
            raise credentials_exception
        token_data_obj = RuntimeTokenData(name=name, user_id=user_id, acc_level=acc_level)
    except JWTError:
        raise credentials_exception
    return token_data_obj

async def get_current_active_user(
    token_data: Annotated["TokenData", Depends(get_token_data)],
    db: DBSession
) -> models.Person:
    user = db.query(models.Person).filter(models.Person.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    if user.state != User_Status.ACTIVE: #type: ignore
        raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="Inactive user")
    return user

def require_acc_level(allowed_acc_levels: List[int]):
    async def _require_acc_level_dependency(
        token_data: Annotated["TokenData", Depends(get_token_data)]
    ):
        if token_data.acc_level not in allowed_acc_levels:
            raise HTTPException(
                status_code=HttpStatusCodes.FORBIDDEN,
                detail="You do not have permission to perform this action."
            )
        return token_data
    return _require_acc_level_dependency

require_sysadmin = require_acc_level([2])
require_c_admin = require_acc_level([1])
require_customer = require_acc_level([0])
require_c_admin_or_sysadmin = require_acc_level([1, 2])
require_authenticated_user = require_acc_level([0, 1, 2])