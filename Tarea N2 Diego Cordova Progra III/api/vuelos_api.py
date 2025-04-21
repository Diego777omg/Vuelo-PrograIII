from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.vuelo import Vuelo as VueloModel, EstadoVuelo, Base
from schemas.vuelo_schema import VueloCreate, VueloOut
from tda.lista_vuelos import ListaDoblementeEnlazada

router = APIRouter()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

lista_vuelos = ListaDoblementeEnlazada()
historial = []  # pila para undo
redo_stack = []  # pila para redo

@router.post("/vuelos/", response_model=VueloOut)
def crear_vuelo(vuelo: VueloCreate, db: Session = Depends(get_db)):
    nuevo_vuelo = VueloModel(**vuelo.dict())
    db.add(nuevo_vuelo)
    db.commit()
    db.refresh(nuevo_vuelo)

    if nuevo_vuelo.estado == EstadoVuelo.emergencia:
        lista_vuelos.insertar_al_frente(nuevo_vuelo)
    else:
        lista_vuelos.insertar_al_final(nuevo_vuelo)

    historial.append(("crear", nuevo_vuelo))
    redo_stack.clear()
    return nuevo_vuelo

@router.get("/vuelos/", response_model=list[VueloOut])
def listar_vuelos(db: Session = Depends(get_db)):
    return db.query(VueloModel).all()

@router.get("/vuelos/primero", response_model=VueloOut)
def obtener_primero():
    vuelo = lista_vuelos.obtener_primero()
    if not vuelo:
        raise HTTPException(status_code=404, detail="Lista vacía")
    return vuelo

@router.get("/vuelos/ultimo", response_model=VueloOut)
def obtener_ultimo():
    vuelo = lista_vuelos.obtener_ultimo()
    if not vuelo:
        raise HTTPException(status_code=404, detail="Lista vacía")
    return vuelo

@router.delete("/vuelos/{posicion}", response_model=VueloOut)
def eliminar_vuelo(posicion: int, db: Session = Depends(get_db)):
    vuelo = lista_vuelos.extraer_de_posicion(posicion)
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelo en esa posición")

    db.delete(vuelo)
    db.commit()

    historial.append(("eliminar", vuelo, posicion))
    redo_stack.clear()
    return vuelo

@router.post("/vuelos/undo")
def deshacer_ultimo(db: Session = Depends(get_db)):
    if not historial:
        raise HTTPException(status_code=400, detail="Nada que deshacer")

    accion = historial.pop()
    redo_stack.append(accion)

    if accion[0] == "crear":
        vuelo = accion[1]
        db.delete(vuelo)
        db.commit()
        # no es necesario quitar de lista, ya se descartó el objeto
        return {"detalle": f"Se deshizo la creación del vuelo {vuelo.codigo}"}

    if accion[0] == "eliminar":
        vuelo, pos = accion[1], accion[2]
        nuevo = VueloModel(
            codigo=vuelo.codigo,
            origen=vuelo.origen,
            destino=vuelo.destino,
            estado=vuelo.estado
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        lista_vuelos.insertar_en_posicion(nuevo, pos)
        return {"detalle": f"Se restauró el vuelo eliminado {vuelo.codigo}"}

@router.post("/vuelos/redo")
def rehacer_ultimo(db: Session = Depends(get_db)):
    if not redo_stack:
        raise HTTPException(status_code=400, detail="Nada que rehacer")

    accion = redo_stack.pop()
    historial.append(accion)

    if accion[0] == "crear":
        vuelo = accion[1]
        nuevo = VueloModel(
            codigo=vuelo.codigo,
            origen=vuelo.origen,
            destino=vuelo.destino,
            estado=vuelo.estado
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)

        if nuevo.estado == EstadoVuelo.emergencia:
            lista_vuelos.insertar_al_frente(nuevo)
        else:
            lista_vuelos.insertar_al_final(nuevo)
        return {"detalle": f"Se rehizo la creación del vuelo {nuevo.codigo}"}

    if accion[0] == "eliminar":
        vuelo, pos = accion[1], accion[2]
        vuelo_db = db.query(VueloModel).filter_by(codigo=vuelo.codigo).first()
        if vuelo_db:
            db.delete(vuelo_db)
            db.commit()
        lista_vuelos.extraer_de_posicion(pos)
        return {"detalle": f"Se volvió a eliminar el vuelo {vuelo.codigo}"}
