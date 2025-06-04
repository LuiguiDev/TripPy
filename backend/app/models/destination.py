from pydantic import BaseModel
from typing import List, Optional

# Destination Model
# This model is used to represent a destination with its attributes.
class Destination(BaseModel):
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
# DestinationSearch Model
# This model is used to represent the search criteria for destinations.
class DestinationSearch(BaseModel):
    q: str = ""
    estado: str = ""
    min_price: int = 0
    max_price: int = 999999
# DestinationResponse Model
# This model is used to represent a response containing a list of destinations.
class DestinationResponse(BaseModel):
    total: int
    destinations: List[Destination]
# DestinationStats Model
## This model is used to represent statistics about destinations.
class DestinationStats(BaseModel):
    total_destinations: int
    destinations_with_prices: int
    price_stats: dict
    states: dict
    destinations_with_images: int