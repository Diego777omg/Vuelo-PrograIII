from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class EstadoVuelo(str, Enum):
    programado = "programado"
    emergencia = "emergencia"
    retrasado = "retrasado"

class VueloBase(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora: datetime
    destino: str
    origen: str

class VueloCreate(VueloBase):
    pass

class VueloUpdate(VueloBase):
    pass

class VueloOut(VueloBase):
    id: int

    class Config:
        orm_mode = True
