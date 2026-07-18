from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash

# --- Users ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Products ---
def get_products(db: Session, skip: int = 0, limit: int = 100, category: str = None):
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category == category)
    return query.offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

# --- Cart ---
def get_cart_items(db: Session, user_id: int):
    return db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    existing = db.query(models.CartItem).filter(
        models.CartItem.user_id == user_id,
        models.CartItem.product_id == product_id
    ).first()
    if existing:
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing
    db_item = models.CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_cart_item(db: Session, item_id: int, quantity: int):
    item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if item:
        item.quantity = quantity
        db.commit()
        db.refresh(item)
    return item

def remove_from_cart(db: Session, item_id: int):
    item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

def clear_cart(db: Session, user_id: int):
    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()