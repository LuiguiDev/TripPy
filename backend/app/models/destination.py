<<<<<<< HEAD
from pydantic import BaseModel

class Destination(BaseModel):
    name: str
    country: str
    description: str
=======
from pydantic import BaseModel

class Destination(BaseModel):
    name: str
    country: str
    description: str
>>>>>>> b327c882a0657d81db6a6071791f34401482a7a8
    slug: str