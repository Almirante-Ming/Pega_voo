from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import or_
from typing import Annotated, List
from http import HTTPStatus as HttpStatusCodes

from tinto import schemas, models
from tinto.utils import DBSession, User_Status, get_password_hash, require_sysadmin

router = APIRouter(prefix="/persons", tags=["Persons (Admin/Internal)"], dependencies=[Depends(require_sysadmin)])

@router.post("/", response_model=schemas.Person)
def create_person_internal(person: schemas.PersonCreateInternal, db: DBSession):
    db_person_check = db.query(models.Person).filter(
        or_(
            models.Person.email == person.email,
            models.Person.cpf == person.cpf
            )
        ).first()
    if db_person_check:
        raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Email or CPF already registered.")
    
    if not person.password:
        raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Password is required.")

    person_data_dict = person.model_dump(exclude={"password"}) 
    hashed_password = get_password_hash(person.password)
    
    new_person = models.Person(**person_data_dict, hashed_password=hashed_password)
    
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

@router.get("/", response_model=List[schemas.Person])
def get_persons(db: DBSession):
    return db.query(models.Person).filter(models.Person.id != 0).all()

@router.get("/{email}", response_model=schemas.Person)
def get_person(
    email: Annotated[str, Path(title="The email of the person to retrieve")],
    db: DBSession
):
    person = db.query(models.Person).filter(models.Person.email == email).first()
    if not person:
        raise HTTPException(status_code=HttpStatusCodes.NOT_FOUND, detail="Person not found with this email")
    return person

@router.put("/{email}", response_model=schemas.Person)
def update_person(
    email: Annotated[str, Path(title="The email of the person to update")],
    person_update: schemas.PersonUpdate,
    db: DBSession
):
    db_person = db.query(models.Person).filter(models.Person.email == email).first()
    if not db_person:
        raise HTTPException(status_code=HttpStatusCodes.NOT_FOUND, detail="Person not found with this email")
    
    update_data = person_update.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] != email:
        existing_email_check = db.query(models.Person).filter(models.Person.email == update_data["email"]).first()
        if existing_email_check and getattr(existing_email_check, 'id', None) != getattr(db_person, 'id', None):
             raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="New email already registered by another user")
    
    if "password" in update_data and update_data["password"] is not None:
        setattr(db_person, 'hashed_password', get_password_hash(update_data.pop("password")))

    for key, value in update_data.items():
        setattr(db_person, key, value)
    
    db.commit()
    db.refresh(db_person)
    return db_person

@router.delete("/{email}")
def delete_person(
    email: Annotated[str, Path(title="The email of the person to delete")],
    db: DBSession
):
    person = db.query(models.Person).filter(models.Person.email == email).first()
    if not person:
        raise HTTPException(status_code=HttpStatusCodes.NOT_FOUND, detail="Person not found with this email")
    
    setattr(person, 'state', User_Status.DELETED)
    db.commit()
    return {"message": "Person marked as deleted"}