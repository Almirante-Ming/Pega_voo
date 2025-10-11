from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import and_
from typing import Annotated, List, Optional
from http import HTTPStatus as HttpStatusCodes

from tinto import schemas, models
from tinto.utils import DBSession, Purchase_Status, require_authenticated_user, require_c_admin_or_sysadmin, get_current_active_user

router = APIRouter(prefix="/purchase-history", tags=["Purchase History"])

@router.post("/", response_model=schemas.PurchaseHistory, dependencies=[Depends(require_authenticated_user)])
def create_purchase_history(
    purchase_history: schemas.PurchaseHistoryCreate, 
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    user = db.query(models.Person).filter(models.Person.id == purchase_history.user_id).first()
    if not user:
        raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="User not found")
    
    if str(current_user.p_type.value) == "customer" and int(current_user.id) != int(purchase_history.user_id):#type: ignore
        raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You can only create purchase history for yourself")
    
    new_purchase_history = models.PurchaseHistory(**purchase_history.model_dump())
    db.add(new_purchase_history)
    db.commit()
    db.refresh(new_purchase_history)
    return new_purchase_history

@router.get("/", response_model=List[schemas.PurchaseHistory], dependencies=[Depends(require_c_admin_or_sysadmin)])
def get_all_purchase_history(
    db: DBSession,
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    query = db.query(models.PurchaseHistory)
    
    if user_id:
        query = query.filter(models.PurchaseHistory.user_id == user_id)
    if status:
        try:
            status_enum = Purchase_Status(status.lower())
            query = query.filter(models.PurchaseHistory.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Invalid status")
    
    return query.all()

@router.get("/my-purchases", response_model=List[schemas.PurchaseHistory], dependencies=[Depends(require_authenticated_user)])
def get_my_purchase_history(
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user),
    status: Optional[str] = Query(None, description="Filter by status")
):
    query = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.user_id == current_user.id)
    
    if status:
        try:
            status_enum = Purchase_Status(status.lower())
            query = query.filter(models.PurchaseHistory.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="Invalid status")
    
    return query.all()

@router.get("/{purchase_id}", response_model=schemas.PurchaseHistory, dependencies=[Depends(require_authenticated_user)])
def get_purchase_history(
    purchase_id: Annotated[int, Path(title="The ID of the purchase history to retrieve")],
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    purchase_history = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.id == purchase_id).first()
    if not purchase_history:
        raise HTTPException(status_code=HttpStatusCodes.NOT_FOUND, detail="Purchase history not found")
    
    if str(current_user.p_type.value) == "customer" and int(current_user.id) != int(purchase_history.user_id): #type:ignore
        raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You can only access your own purchase history")
    
    return purchase_history

@router.put("/{purchase_id}", response_model=schemas.PurchaseHistory, dependencies=[Depends(require_authenticated_user)])
def update_purchase_history(
    purchase_id: Annotated[int, Path(title="The ID of the purchase history to update")],
    purchase_update: schemas.PurchaseHistoryUpdate,
    db: DBSession,
    current_user: models.Person = Depends(get_current_active_user)
):
    db_purchase = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.id == purchase_id).first()
    if not db_purchase:
        raise HTTPException(status_code=HttpStatusCodes.NOT_FOUND, detail="Purchase history not found")
    
    if str(current_user.p_type.value) == "customer" and int(current_user.id) != int(db_purchase.user_id): #type:ignore
        raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You can only update your own purchase history")
    
    update_data = purchase_update.model_dump(exclude_unset=True)
    
    if "user_id" in update_data:
        user = db.query(models.Person).filter(models.Person.id == update_data["user_id"]).first()
        if not user:
            raise HTTPException(status_code=HttpStatusCodes.BAD_REQUEST, detail="User not found")
        
        if str(current_user.p_type.value) == "customer" and int(update_data["user_id"]) != int(current_user.id): #type:ignore
            raise HTTPException(status_code=HttpStatusCodes.FORBIDDEN, detail="You cannot transfer purchase history to another user")
    
    for key, value in update_data.items():
        setattr(db_purchase, key, value)
    
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@router.delete("/{purchase_id}", dependencies=[Depends(require_c_admin_or_sysadmin)])
def delete_purchase_history(
    purchase_id: Annotated[int, Path(title="The ID of the purchase history to delete")],
    db: DBSession
):
    purchase_history = db.query(models.PurchaseHistory).filter(models.PurchaseHistory.id == purchase_id).first()
    if not purchase_history:
        raise HTTPException(status_code=HttpStatusCodes.NOT_FOUND, detail="Purchase history not found")
    
    db.delete(purchase_history)
    db.commit()
    return {"message": "Purchase history deleted"}