from pydantic import BaseModel

class Destination(BaseModel):
    name: str
    country: str
    description: str
    slug: str