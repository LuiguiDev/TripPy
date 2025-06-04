"""
Módulo Principal de TripPy API
Autor: Akuma
Versión: 2.0

Este módulo inicializa la aplicación FastAPI y configura:
- Rutas principales
- Middleware CORS
- Documentación de la API
- Manejo de excepciones global
- Endpoints de estado y salud

La API provee acceso a:
- Catálogo de destinos turísticos en México
- Paquetes vacacionales
- Búsqueda y filtrado avanzado
- Estadísticas de destinos y paquetes
"""
#tengo hambre we

# Importaciones necesarias
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes import destinations

ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Frontend en desarrollo
    "http://localhost:3000",  # Frontend alternativo
    "https://trippy.mx"      # Producción (ejemplo)
]

app = FastAPI(
    title="TripPy API",
    description="""
    API para explorar destinos turísticos en México
    y paquetes vacacionales promocionales.
    """,
    # Configuración de documentación OpenAPI
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración CORS más segura
# Permite solicitudes desde orígenes específicos
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],# Métodos permitidos
    allow_headers=["*"],
    max_age=100  # Tiempo de cache para preflight requests o en español, solicitudes de pre-vuelo
)

# Incluir rutas
app.include_router(destinations.router, prefix="/api", tags=["Destinations"])

# Incluir otros routers si es necesario
#permite agregar más módulos de rutas
@app.get("/")
def root():
    return {
        "message": "Welcome to TripPy API - Descubre México",
        "version": "1.0.0",
        "endpoints": {
            "destinations": "/api/explorer",
            "destination_details": "/api/details/{slug}",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "TripPy API"}