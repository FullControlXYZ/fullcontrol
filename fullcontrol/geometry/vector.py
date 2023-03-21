from typing import Optional
from pydantic import BaseModel


class Vector(BaseModel):
    'vector defined by x y and z distances'
    x: Optional[float]
    y: Optional[float]
    z: Optional[float]
