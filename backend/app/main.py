from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import destinations
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TripPy Travel API",
    description="API para explorar destinos turísticos en México",
    version="1.0.0"
)

# CORS para conectar con el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Incluir rutas
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
