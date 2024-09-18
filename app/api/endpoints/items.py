from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.item import ItemCreate, ItemRead
from app.crud.item import get_item, create_item
from app.db.session import get_db

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

@router.post("/", response_model=ItemRead)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db=db, item=item)

@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
