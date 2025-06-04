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
# Importación de modelos de datos
from app.models.destination import (
    Destino,
    PaqueteTuristico,
    BusquedaDestino,  
    RespuestaDestino  
)

# Configuración de seguridad adicional
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Frontend en desarrollo
    "http://localhost:3000",  # Frontend alternativo
    "https://trippy.mx"      # Producción (ejemplo)
]

# Inicialización única de FastAPI
# esto permite evitar problemas de importación circular
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
    allow_methods=["GET", "POST"],  # Métodos permitidos
    allow_headers=["*"],
    max_age=100  # Tiempo de cache para preflight requests o en español, solicitudes de pre-vuelo
)

# Incluir rutas de la aplicación
#permite organizar las rutas en módulos separados
app.include_router(
    destinations.router, 
    prefix="/api", 
    tags=["Destinos y Paquetes"]
)

# Incluir otros routers si es necesario
#permite agregar más módulos de rutas
@app.get("/")
def root():
    """
    Endpoint raíz que muestra la documentación de la API.
    """
    return {
        "mensaje": "Bienvenido a TripPy API - Descubre México",
        "version": "2.0.0",
        "endpoints": {
            # Destinos
            "destinos": "/api/destinos",
            "detalle_destino": "/api/destinos/{destino_id}",
            # Paquetes
            "paquetes": "/api/paquetes",
            "detalle_paquete": "/api/paquetes/{paquete_id}",
            "buscar_paquetes": "/api/paquetes/buscar",
            "estadisticas_paquetes": "/api/estadisticas/paquetes",
            "paquetes_por_destino": "/api/destinos/{destino_id}/paquetes",
            "paquetes_mejor_valorados": "/api/paquetes/mejor-valorados",
            "paquetes_por_precio": "/api/paquetes/por-precio",
            # Documentación
            "documentacion": "/docs",
            "documentacion_alt": "/redoc"
        }
    }

#esto sirve para verificar que la API está activa
@app.get("/health")
def health_check():
    """
    Verificación del estado de la API.
    """
    return {
        "estado": "activo",
        "servicio": "TripPy API",
        "version": "2.0.0",
        "funcionalidades": [
            "destinos",
            "paquetes",
            "busqueda",
            "estadisticas"
        ],
        "endpoints_disponibles": True
    }

# Manejador de excepciones globales para errores no controlados
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejador personalizado de excepciones HTTP."""
    return {
        "error": True,
        "mensaje": exc.detail,
        "codigo": exc.status_code
    }