from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func

from db import get_session
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["reviews"])


# --------------------------------------------------
# Create Review
# --------------------------------------------------
@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
    db_review = Review(**review.model_dump())

    session.add(db_review)
    session.commit()
    session.refresh(db_review)

    return db_review


# --------------------------------------------------
# List Reviews
# --------------------------------------------------
@router.get("/", response_model=list[ReviewRead])
def list_reviews(
    play_name: str | None = Query(None, description="Filter by play name"),
    skip: int = Query(0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(10, ge=1, description="Number of reviews to return"),
    session: Session = Depends(get_session),
):
    query = select(Review)

    if play_name:
        query = query.where(Review.play_name == play_name)
        if not session.exec(query).first():
            raise HTTPException(
                status_code=404, detail=f"No reviews found for {play_name}"
            )

    query = query.offset(skip).limit(limit)

    return session.exec(query).all()


# --------------------------------------------------
# Get Average Rating
# --------------------------------------------------
@router.get("/average/{play_name}")
def get_average_rating(play_name: str, session: Session = Depends(get_session)):
    statement = select(func.avg(Review.rating), func.count(Review.rating)).where(
        Review.play_name == play_name
    )

    result = session.exec(statement).one()

    avg_rating, total_reviews = result

    if total_reviews == 0:
        raise HTTPException(status_code=404, detail=f"No reviews found for {play_name}")

    return {
        "average_rating": round(float(avg_rating), 2),
        "total_reviews": total_reviews,
        "play_name": play_name,
    }


# --------------------------------------------------
# Get Single Review
# --------------------------------------------------
@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)

    if not review:
        raise HTTPException(
            status_code=404, detail=f"Review with id {review_id} not found"
        )

    return review


# --------------------------------------------------
# Update Review
# --------------------------------------------------
@router.put("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int, review: ReviewUpdate, session: Session = Depends(get_session)
):
    db_review = session.get(Review, review_id)

    if not db_review:
        raise HTTPException(
            status_code=404, detail=f"Review with id {review_id} not found"
        )

    review_data = review.model_dump(exclude_unset=True)

    for key, value in review_data.items():
        setattr(db_review, key, value)

    session.add(db_review)
    session.commit()
    session.refresh(db_review)

    return db_review


# --------------------------------------------------
# Delete Review
# --------------------------------------------------
@router.delete("/{review_id}")
def delete_review(review_id: int, session: Session = Depends(get_session)):
    db_review = session.get(Review, review_id)

    if not db_review:
        raise HTTPException(
            status_code=404, detail=f"Review with id {review_id} not found"
        )

    session.delete(db_review)
    session.commit()

    return {"message": "Review deleted successfully"}
