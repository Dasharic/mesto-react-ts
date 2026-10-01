from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db

router = APIRouter(prefix="/api/tours", tags=["catalog"])

class TourCreate(BaseModel):
    title: str
    image: str
    description: str
    price: int

@router.get("/")
def get_tours():
    conn = get_db()
    tours = conn.execute("SELECT * FROM tours ORDER BY id DESC").fetchall()
    return [dict(t) for t in tours]

@router.post("/")
def create_tour(tour: TourCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tours (title, image, description, price) VALUES (?, ?, ?, ?)",
                   (tour.title, tour.image, tour.description, tour.price))
    conn.commit()
    new_id = cursor.lastrowid
    new_tour = conn.execute("SELECT * FROM tours WHERE id=?", (new_id,)).fetchone()
    return dict(new_tour)

@router.delete("/{tour_id}")
def delete_tour(tour_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tours WHERE id=?", (tour_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tour not found")
    conn.commit()
    return {"status": "ok"}
