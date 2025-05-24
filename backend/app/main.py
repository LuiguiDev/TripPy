from fastapi import FastAPI
from app.routes import destinations

app = FastAPI(title="TripPy Travel API")

app.include_router(destinations.router, prefix="/api", tags=["Destinations"])

@app.get("/")
def root():
    return {"message": "Welcome to TripPy API"}
