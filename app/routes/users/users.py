from fastapi import APIRouter, HTTPException, Response, status, Depends
from ...utils import schemas, database, models, utils, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(database.get_db),
    current_user: schemas.UserResponse = Depends(oauth2.get_current_user),
):

    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserResponse = Depends(oauth2.get_current_user),
):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account with this email already exists.",
        )
    user.password = utils.hash_password(user.password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserResponse = Depends(oauth2.get_current_user),
):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
