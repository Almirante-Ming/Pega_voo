from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from typing import Annotated
from datetime import timedelta
from http import HTTPStatus

from tinto import schemas, models
from tinto.utils import (
    DBSession,
    verify_password,
    create_access_token,
    get_password_hash,
    User_Status,
    User_Type,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=schemas.Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DBSession
):
    identifier = form_data.username
    password = form_data.password

    user = db.query(models.Person).filter(
        or_(
            models.Person.email == identifier,
            models.Person.phone_number == identifier
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect identifier or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
 
    db.refresh(user)
    
    hashed_password = getattr(user, 'hashed_password', None)
    if not hashed_password:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect identifier or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    password_str = str(hashed_password) if hashed_password else ""
    if not verify_password(password, password_str):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect identifier or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_state = getattr(user, 'status', None)
    if user_state != User_Status.ACTIVE:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="User account is not active. Please contact support.",
        )

    acc_level = 0 
    user_type = getattr(user, 'person_type', None)
    if user_type == User_Type.COMPANY_ADMIN:
        acc_level = 1
    elif user_type == User_Type.SYSADMIN:
        acc_level = 2
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.full_name, "user_id": user.id, "acc_level": acc_level},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register/", response_model=schemas.Person)
def register_person(person_data: schemas.PersonRegister, db: DBSession):
    db_person_check = db.query(models.Person).filter(
        or_(
            models.Person.email == person_data.email,
            models.Person.cpf == person_data.cpf
        )
    ).first()
    if db_person_check:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="already registered.")
    
    if not person_data.password:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Password is required for registration.")
        
    hashed_password = get_password_hash(person_data.password)
    
    new_person_dict = person_data.model_dump(exclude={"password"}) 
    
    registered_person = models.Person(
        **new_person_dict,
        hashed_password=hashed_password,
        status=User_Status.ACTIVE,
        person_type=User_Type.CUSTOMER
    )
    
    db.add(registered_person)
    db.commit()
    db.refresh(registered_person)
    
    from tinto.tasks.send_greeting_email import send_greeting_email
    send_greeting_email.delay(registered_person.id)
    
    return registered_person