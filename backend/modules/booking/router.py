from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from database import get_db
from typing import List, Optional
import time
import json

router = APIRouter(prefix="/api/booking", tags=["booking"])

def get_email_from_token(authorization: str):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.replace("Bearer ", "")
    email = token.replace("token_", "")
    return email

# -- Cart --
@router.get("/cart")
def get_cart(authorization: Optional[str] = Header(None)):
    email = get_email_from_token(authorization)
    conn = get_db()
    # Join to get full tour details
    tours = conn.execute('''
        SELECT t.* FROM tours t
        JOIN cart_items c ON t.id = c.tour_id
        WHERE c.email = ?
    ''', (email,)).fetchall()
    return [dict(t) for t in tours]

@router.post("/cart/{tour_id}")
def add_to_cart(tour_id: int, authorization: Optional[str] = Header(None)):
    email = get_email_from_token(authorization)
    conn = get_db()
    try:
        conn.execute("INSERT INTO cart_items (email, tour_id) VALUES (?, ?)", (email, tour_id))
        conn.commit()
    except Exception:
        pass # Already exists
    return {"status": "ok"}

@router.delete("/cart/{tour_id}")
def remove_from_cart(tour_id: int, authorization: Optional[str] = Header(None)):
    email = get_email_from_token(authorization)
    conn = get_db()
    conn.execute("DELETE FROM cart_items WHERE email=? AND tour_id=?", (email, tour_id))
    conn.commit()
    return {"status": "ok"}

# -- Favorites --
@router.get("/favorites")
def get_favorites(authorization: Optional[str] = Header(None)):
    email = get_email_from_token(authorization)
    conn = get_db()
    favs = conn.execute("SELECT tour_id FROM favorites WHERE email=?", (email,)).fetchall()
    return [f["tour_id"] for f in favs]

@router.post("/favorites/{tour_id}")
def toggle_favorite(tour_id: int, authorization: Optional[str] = Header(None)):
    email = get_email_from_token(authorization)
    conn = get_db()
    existing = conn.execute("SELECT 1 FROM favorites WHERE email=? AND tour_id=?", (email, tour_id)).fetchone()
    if existing:
        conn.execute("DELETE FROM favorites WHERE email=? AND tour_id=?", (email, tour_id))
    else:
        conn.execute("INSERT INTO favorites (email, tour_id) VALUES (?, ?)", (email, tour_id))
    conn.commit()
    
    favs = conn.execute("SELECT tour_id FROM favorites WHERE email=?", (email,)).fetchall()
    return {"favorites": [f["tour_id"] for f in favs]}

# -- Checkout / Orders --
@router.get("/orders")
def get_orders(authorization: Optional[str] = Header(None)):
    email = get_email_from_token(authorization)
    conn = get_db()
    orders = conn.execute("SELECT * FROM orders WHERE email=? ORDER BY id DESC", (email,)).fetchall()
    result = []
    for o in orders:
        d = dict(o)
        d["items"] = json.loads(d["items_json"])
        del d["items_json"]
        result.append(d)
    return result

@router.post("/checkout")
def checkout(authorization: Optional[str] = Header(None)):
    email = get_email_from_token(authorization)
    conn = get_db()
    
    cart_tours = conn.execute('''
        SELECT t.* FROM tours t
        JOIN cart_items c ON t.id = c.tour_id
        WHERE c.email = ?
    ''', (email,)).fetchall()
    
    if not cart_tours:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    items = [dict(t) for t in cart_tours]
    total = sum(t["price"] for t in items)
    date = time.strftime("%d.%m.%Y")
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (email, date, total, items_json) VALUES (?, ?, ?, ?)",
                   (email, date, total, json.dumps(items)))
    new_id = cursor.lastrowid
    
    cursor.execute("DELETE FROM cart_items WHERE email=?", (email,))
    conn.commit()
    
    return {
        "id": new_id,
        "email": email,
        "date": date,
        "items": items,
        "total": total
    }
