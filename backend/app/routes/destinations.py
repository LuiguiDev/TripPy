from fastapi import APIRouter, HTTPException
from app.models.destination import Destination
import json
import os

router = APIRouter()

# Load mock data from JSON
base_path = os.path.dirname(__file__)
data_path = os.path.join(base_path, "..", "data", "destinations.json")

with open(data_path, "r", encoding="utf-8") as f:
    destinations = json.load(f)

@router.get("/explorer")
def get_destinations():
    return destinations

@router.get("/details/{slug}")
def get_destination_details(slug: str):
    for d in destinations:
        if d["slug"] == slug:
            return d
    raise HTTPException(status_code=404, detail="Destination not found")