import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.auth.router import router as auth_router
from modules.catalog.router import router as catalog_router
from modules.booking.router import router as booking_router

app = FastAPI(title="Mesto Tours Monolithic API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Bounded Contexts (Modules)
app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(booking_router)

@app.get("/")
def health_check():
    return {"status": "Monolith is running", "architecture": "Monolithic Layered"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
