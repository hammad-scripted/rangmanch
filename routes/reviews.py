from fastapi import APIRouter, Depends
from sqlmodel import Session,select,func
from db import get_session
from models import Review,ReviewCreate,ReviewRead,ReviewUpdate

router=APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@router.post("/",response_model=ReviewRead)
def create_review(review:ReviewCreate,session:Session=Depends(get_session)):
    db_review=Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

