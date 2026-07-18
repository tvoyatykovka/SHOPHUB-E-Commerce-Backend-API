from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=schemas.CartOut)
def get_cart(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = crud.get_cart_items(db, current_user.id)
    total = sum(item.product.price * item.quantity for item in items if item.product)
    return {"items": items, "total": total}

@router.post("/add", response_model=schemas.CartItemOut)
def add_to_cart(
    item: schemas.CartItemCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = crud.get_product(db, item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    return crud.add_to_cart(db, current_user.id, item.product_id, item.quantity)

@router.put("/update/{item_id}", response_model=schemas.CartItemOut)
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = crud.update_cart_item(db, item_id, quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return item

@router.delete("/remove/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not crud.remove_from_cart(db, item_id):
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}

@router.delete("/clear")
def clear_cart(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    crud.clear_cart(db, current_user.id)
    return {"message": "Cart cleared"}