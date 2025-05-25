from fastapi import FastAPI
from app.routes import destinations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TripPy Travel API")

app.include_router(destinations.router, prefix="/api", tags=["Destinations"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to TripPy API"}
