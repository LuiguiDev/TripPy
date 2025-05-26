from fastapi import APIRouter, HTTPException
from app.models.destination import Destination
import json
import os

router = APIRouter()

# Load destinations data from JSON
base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, "..", "data", "destinations.json")

def load_destinations():
    """Load and normalize destination data from JSON file"""
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        
        normalized_destinations = []
        
        for dest in raw_data:
            # Normalize the data structure - handle both formats
            normalized_dest = {
                "id": dest.get("id") or dest.get("slug"),
                "nombre": dest.get("nombre"),
                "codigo_iata": dest.get("codigo_iata"),
                "slug": dest.get("slug") or dest.get("id"),
                "estado": dest.get("estado"),
                "descripcion": dest.get("descripcion"),
                "imagenes": dest.get("imagenes", []),
                "precio_ida": dest.get("precio_ida"),
                "precio_vuelta": dest.get("precio_vuelta"),
                "enlace": dest.get("enlace")
            }
            
            # Only add destinations with required fields
            if normalized_dest["nombre"] and normalized_dest["slug"]:
                normalized_destinations.append(normalized_dest)
        
        return normalized_destinations
    
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Destinations data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON format in destinations file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading destinations: {str(e)}")

# Load destinations once at startup
destinations = load_destinations()

@router.get("/explorer")
def get_destinations():
    """Get all available destinations"""
    return {
        "total": len(destinations),
        "destinations": destinations
    }

@router.get("/explorer/search")
def search_destinations(q: str = "", estado: str = "", min_price: int = 0, max_price: int = 999999):
    """Search destinations by name, state, or price range"""
    filtered_destinations = destinations
    
    # Filter by search query (name or description)
    if q:
        q_lower = q.lower()
        filtered_destinations = [
            dest for dest in filtered_destinations 
            if q_lower in dest["nombre"].lower() or 
               (dest["descripcion"] and q_lower in dest["descripcion"].lower())
        ]
    
    # Filter by state
    if estado:
        filtered_destinations = [
            dest for dest in filtered_destinations 
            if dest["estado"] and estado.lower() in dest["estado"].lower()
        ]
    
    # Filter by price range
    filtered_destinations = [
        dest for dest in filtered_destinations 
        if dest["precio_ida"] and min_price <= dest["precio_ida"] <= max_price
    ]
    
    return {
        "query": {
            "search": q,
            "estado": estado,
            "price_range": {"min": min_price, "max": max_price}
        },
        "total": len(filtered_destinations),
        "destinations": filtered_destinations
    }

@router.get("/details/{slug}")
def get_destination_details(slug: str):
    """Get detailed information for a specific destination"""
    for dest in destinations:
        if dest["slug"] == slug or dest["id"] == slug:
            return dest
    
    raise HTTPException(status_code=404, detail=f"Destination with slug '{slug}' not found")

@router.get("/destinations/cheapest")
def get_cheapest_destinations(limit: int = 5):
    """Get the cheapest destinations sorted by price"""
    # Filter destinations with valid prices and sort by price
    destinations_with_prices = [
        dest for dest in destinations 
        if dest["precio_ida"] is not None
    ]
    
    sorted_destinations = sorted(destinations_with_prices, key=lambda x: x["precio_ida"])
    
    return {
        "total": len(sorted_destinations),
        "destinations": sorted_destinations[:limit]
    }

@router.get("/destinations/by-state/{estado}")
def get_destinations_by_state(estado: str):
    """Get all destinations from a specific state"""
    state_destinations = [
        dest for dest in destinations 
        if dest["estado"] and estado.lower() in dest["estado"].lower()
    ]
    
    if not state_destinations:
        raise HTTPException(status_code=404, detail=f"No destinations found for state '{estado}'")
    
    return {
        "estado": estado,
        "total": len(state_destinations),
        "destinations": state_destinations
    }

@router.get("/destinations/stats")
def get_destinations_stats():
    """Get general statistics about destinations"""
    destinations_with_prices = [d for d in destinations if d["precio_ida"]]
    prices = [d["precio_ida"] for d in destinations_with_prices]
    
    states = {}
    for dest in destinations:
        if dest["estado"]:
            states[dest["estado"]] = states.get(dest["estado"], 0) + 1
    
    return {
        "total_destinations": len(destinations),
        "destinations_with_prices": len(destinations_with_prices),
        "price_stats": {
            "min_price": min(prices) if prices else None,
            "max_price": max(prices) if prices else None,
            "avg_price": round(sum(prices) / len(prices), 2) if prices else None
        },
        "states": states,
        "destinations_with_images": len([d for d in destinations if d["imagenes"]])
    }