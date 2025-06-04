from pydantic import BaseModel, Field  # Agregar Field
from typing import List, Optional

"""
Módulo de Modelos de Datos TripPy
Autor: Akuma
Versión: 2.0

Este módulo define las estructuras de datos principales usando Pydantic:
- Destinos turísticos
- Paquetes vacacionales
- Criterios de búsqueda
- Estadísticas

Los modelos garantizan la validación de datos y documentación OpenAPI.
"""

# Modelo de Destino
class Destino(BaseModel):
    """
    Modelo de destino turístico.
    
    Atributos:
        id: Identificador único del destino
        nombre: Nombre oficial del destino
        codigo_iata: Código de aeropuerto IATA
        slug: URL amigable del destino
        estado: Estado de México donde se ubica
        descripcion: Descripción detallada del destino
        imagenes: Lista de URLs de imágenes
        precio_ida: Precio base del vuelo de ida
        precio_vuelta: Precio base del vuelo de regreso
        enlace: URL para reservar vuelos
    """
    id: Optional[str] = None
    nombre: str
    codigo_iata: Optional[str] = None
    slug: str
    estado: Optional[str] = None
    descripcion: Optional[str] = None
    imagenes: List[str] = []
    precio_ida: Optional[int] = None
    precio_vuelta: Optional[int] = None
    enlace: Optional[str] = None

# Modelo para Búsqueda de Destinos
class BusquedaDestino(BaseModel):
    """
    Criterios para búsqueda de destinos.
    
    Atributos:
        consulta: Término de búsqueda
        estado: Filtro por estado
        precio_min: Precio mínimo a considerar
        precio_max: Precio máximo a considerar
    """
    consulta: str = ""
    estado: str = ""
    precio_min: int = 0
    precio_max: int = 999999

# Modelo para Respuesta de Búsqueda
class RespuestaDestino(BaseModel):
    """Estructura de respuesta para búsquedas de destinos."""
    total: int
    destinos: List[Destino]

# Modelo para Estadísticas
class EstadisticasDestino(BaseModel):
    """Estadísticas agregadas de destinos turísticos."""
    total_destinos: int
    destinos_con_precios: int
    estadisticas_precios: dict
    estados: dict
    destinos_con_imagenes: int

# Modelo para Itinerario
class Itinerario(BaseModel):
    """Representa las actividades diarias de un paquete turístico."""
    dia: int                    # Número del día en el itinerario
    actividades: List[str]      # Lista de actividades para ese día

# Modelo para Paquete Turístico
class PaqueteTuristico(BaseModel):
    """Representa un paquete vacacional completo."""
    id: str                     # Identificador único del paquete
    destino_id: str            # Referencia al destino al que pertenece
    nombre: str                # Nombre del paquete turístico
    duracion_dias: int = Field(default=6, ge=1)     # Duración predeterminada en días
    duracion_noches: int = Field(default=5, ge=1)   # Duración predeterminada en noches
    calificacion: float = Field(ge=0, le=5)        # Calificación del paquete (1.0 a 5.0)
    precio_paquete: float = Field(gt=0)      # Precio total del paquete en MXN
    hotel_nombre: str          # Nombre del hotel asociado
    hotel_enlace: str          # Enlace verificado al sitio web del hotel
    imagen_paquete: str        # URL verificada de la imagen del paquete
    itinerario: List[Itinerario] # Actividades diarias
    disponible: bool = True    # Estado de disponibilidad del paquete