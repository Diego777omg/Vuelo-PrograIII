
from sqlalchemy import Column, String, Enum, Integer, DateTime
from database import Base
import enum
from datetime import datetime

class EstadoVuelo(enum.Enum):
    programado = "programado"
    emergencia = "emergencia"
    retrasado = "retrasado"

class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    estado = Column(Enum(EstadoVuelo), default=EstadoVuelo.programado)
    hora = Column(DateTime, default=datetime.utcnow)
    destino = Column(String)
    origen = Column(String)

    def __repr__(self):
        return f"<Vuelo {self.codigo} - {self.estado.name}>"
