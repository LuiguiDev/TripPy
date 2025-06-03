"""
Módulo de Rutas de Destinos TripPy
Autor: Akuma
Versión: 2.0

Este módulo maneja todas las rutas relacionadas con:
- Consulta de destinos turísticos
- Gestión de paquetes vacacionales
- Búsqueda y filtrado
- Estadísticas y reportes

Características principales:
- Carga y normalización de datos
- Validación de parámetros
- Manejo de errores personalizado
- Agrupación y filtrado avanzado
"""

from fastapi import APIRouter, HTTPException, Query  # Agregar Query
from app.models.destination import (
    Destino,
    BusquedaDestino,
    RespuestaDestino,
    EstadisticasDestino,
    Itinerario,
    PaqueteTuristico
)
from typing import List, Dict, Optional, Union  # Agregar Union
import json
import os

# Inicialización del router
router = APIRouter()

# Configuración de rutas de archivos
base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, "..", "data", "destinations.json")
packages_path = os.path.join(base_path, "..", "data", "paquetes_turisticos.json")

def load_destinations() -> List[Dict]:
    """
    Carga y procesa los destinos desde archivo JSON.
    
    Proceso:
    1. Lee el archivo de destinos
    2. Normaliza la estructura de datos
    3. Valida campos requeridos
    4. Aplica valores por defecto
    
    Returns:
        List[Dict]: Lista de destinos procesados
    
    Raises:
        HTTPException: Si hay errores de lectura o formato
    """
    try:
        # Lectura del archivo JSON
        with open(data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        
        normalized_destinations = []
        
        # Procesamiento de cada destino
        for dest in raw_data:
            # Normalización de estructura de datos
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
            
            # Validación de campos requeridos
            if normalized_dest["nombre"] and normalized_dest["slug"]:
                normalized_destinations.append(normalized_dest)
        
        return normalized_destinations
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=500, 
            detail="Error: No se encontró el archivo de destinos"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, 
            detail="Error: Formato JSON inválido en archivo de destinos"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al cargar destinos: {str(e)}"
        )

# Carga inicial de datos
destinations = load_destinations()

def load_packages() -> List[Dict]:
    """
    Carga los paquetes turísticos desde el archivo JSON.
    
    Returns:
        List[Dict]: Lista de paquetes turísticos disponibles.
    
    Raises:
        HTTPException: Si hay problemas al cargar o procesar el archivo.
    """
    try:
        with open(packages_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("paquetes", [])
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al cargar paquetes: {str(e)}"
        )

# Carga inicial de paquetes
packages = load_packages()

# Rutas para Destinos
@router.get("/destinos", response_model=List[Destino])
async def obtener_destinos():
    """Obtiene todos los destinos disponibles."""
    return destinations

@router.get("/destinos/{destino_id}", response_model=Destino)
async def obtener_destino(destino_id: str):
    """Obtiene un destino específico por su ID."""
    destino = next(
        (d for d in destinations if d["id"] == destino_id),
        None
    )
    if not destino:
        raise HTTPException(
            status_code=404,
            detail=f"Destino {destino_id} no encontrado"
        )
    return destino

# Rutas para Paquetes
@router.get("/paquetes", response_model=List[PaqueteTuristico])
async def obtener_paquetes():
    """Obtiene todos los paquetes turísticos disponibles."""
    return packages

@router.get("/paquetes/{paquete_id}", response_model=PaqueteTuristico)
async def obtener_paquete(paquete_id: str):
    """Obtiene un paquete específico por su ID."""
    paquete = next((p for p in packages if p["id"] == paquete_id), None)
    if not paquete:
        raise HTTPException(
            status_code=404,
            detail=f"Paquete {paquete_id} no encontrado"
        )
    return paquete

@router.get("/destinos/{destino_id}/paquetes")
async def obtener_paquetes_por_destino(destino_id: str):
    """Obtiene paquetes disponibles para un destino específico."""
    paquetes_destino = [
        p for p in packages 
        if p["destino_id"] == destino_id and p["disponible"]
    ]
    return {
        "destino_id": destino_id,
        "total_paquetes": len(paquetes_destino),
        "paquetes": paquetes_destino
    }

@router.get("/paquetes/buscar")
async def buscar_paquetes(
    precio_min: float = Query(default=0, ge=0),  # Agregar validación
    precio_max: float = Query(default=999999, gt=0),
    calificacion_min: float = Query(default=0, ge=0, le=5),
    destino: Optional[str] = Query(default=None)
):
    """
    Búsqueda avanzada de paquetes turísticos.
    
    Parámetros:
        precio_min: Precio mínimo del paquete
        precio_max: Precio máximo del paquete
        calificacion_min: Calificación mínima requerida
        destino: ID del destino específico (opcional)
    
    Validaciones:
    - Precios no negativos
    - Precio mínimo menor al máximo
    - Calificación entre 0 y 5
    - Destino existente (si se especifica)
    
    Returns:
        dict: Resultados filtrados y metadata
    """
    # Validar rangos de precios
    if precio_min < 0 or precio_max < 0:
        raise HTTPException(
            status_code=400,
            detail="Los precios no pueden ser negativos"
        )
    if precio_min > precio_max:
        raise HTTPException(
            status_code=400,
            detail="El precio mínimo no puede ser mayor al máximo"
        )
    
    # Validar calificación
    if not 0 <= calificacion_min <= 5:
        raise HTTPException(
            status_code=400,
            detail="La calificación debe estar entre 0 y 5"
        )

    # Validar destino si se proporciona
    if destino and not any(d["id"] == destino for d in destinations):
        raise HTTPException(
            status_code=404,
            detail=f"Destino {destino} no encontrado"
        )

    filtrados = [
        p for p in packages
        if (precio_min <= p["precio_paquete"] <= precio_max and
            p["calificacion"] >= calificacion_min and
            p["disponible"] and
            (destino is None or p["destino_id"] == destino))
    ]
    
    return {
        "total_encontrados": len(filtrados),
        "criterios_busqueda": {
            "precio_min": precio_min,
            "precio_max": precio_max,
            "calificacion_min": calificacion_min,
            "destino": destino
        },
        "paquetes": filtrados
    }

@router.get("/stats/packages")
async def get_package_stats():
    """Obtiene estadísticas generales de los paquetes turísticos."""
    try:
        available_packages = [p for p in packages if p["disponible"]]
        if not packages:
            raise HTTPException(
                status_code=404,
                detail="No hay paquetes disponibles para analizar"
            )
        
        # Cálculo de promedios y totales
        stats = {
            "total_paquetes": len(packages),
            "paquetes_disponibles": len(available_packages),
            "precio_promedio": sum(p["precio_paquete"] for p in packages) / len(packages),
            "calificacion_promedia": sum(p["calificacion"] for p in packages) / len(packages),
            "por_destino": {},
            "rango_precios": {
                "min": min(p["precio_paquete"] for p in packages),
                "max": max(p["precio_paquete"] for p in packages)
            }
        }
        
        # Agregación por destino
        for package in packages:
            destino = package["destino_id"]
            if destino not in stats["por_destino"]:
                stats["por_destino"][destino] = {
                    "total": 0,
                    "disponibles": 0
                }
            stats["por_destino"][destino]["total"] += 1
            if package["disponible"]:
                stats["por_destino"][destino]["disponibles"] += 1
        
        return stats

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al calcular estadísticas: {str(e)}"
        )

@router.get("/packages/top-rated")
async def get_top_rated_packages(limit: int = 5):
    """
    Obtiene los paquetes mejor calificados.
    
    Args:
        limit (int): Número máximo de paquetes a retornar.
    
    Returns:
        List[PaqueteTuristico]: Lista de paquetes ordenados por calificación.
    """
    sorted_packages = sorted(
        [p for p in packages if p["disponible"]],
        key=lambda x: x["calificacion"],
        reverse=True
    )
    return sorted_packages[:limit]

@router.get("/packages/by-price-range")
async def get_packages_by_price_range(
    ranges: List[Dict[str, float]] = [
        {"min": 0, "max": 10000},
        {"min": 10001, "max": 15000},
        {"min": 15001, "max": 20000},
        {"min": 20001, "max": float('inf')}
    ]
):
    """
    Agrupa paquetes por rangos de precios.
    
    Args:
        ranges (List[Dict]): Lista de rangos de precios a considerar.
    
    Returns:
        dict: Paquetes agrupados por rango de precio.
        
    Raises:
        HTTPException: Si los rangos son inválidos o se superponen.
    """
    # Validar rangos
    for r in ranges:
        if r["min"] > r["max"]:
            raise HTTPException(
                status_code=400,
                detail="Los rangos de precios deben tener min <= max"
            )
    
    # Ordenar rangos por precio mínimo
    ranges = sorted(ranges, key=lambda x: x["min"])
    
    # Verificar superposición
    for i in range(len(ranges)-1):
        if ranges[i]["max"] > ranges[i+1]["min"]:
            raise HTTPException(
                status_code=400,
                detail="Los rangos de precios no deben superponerse"
            )
    
    result = {}
    for r in ranges:
        packages_in_range = [
            p for p in packages
            if r["min"] <= p["precio_paquete"] <= r["max"] and p["disponible"]
        ]
        
        range_key = (
            f"{int(r['min']):,}-{int(r['max']):,}" 
            if r["max"] != float('inf') 
            else f"Más de {int(r['min']):,}"
        )
        
        result[range_key] = {
            "cantidad": len(packages_in_range),
            "paquetes": packages_in_range
        }
    
    return result