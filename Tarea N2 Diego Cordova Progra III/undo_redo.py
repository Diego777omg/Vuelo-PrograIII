undo_stack = []
redo_stack = []

def registrar_accion(accion, datos):
    undo_stack.append((accion, datos))
    redo_stack.clear()

def undo(lista):
    if not undo_stack:
        return {"mensaje": "Nada para deshacer"}
    accion, datos = undo_stack.pop()
    if accion == "insertar":
        lista.extraer_de_posicion(datos["posicion"])
        redo_stack.append(("insertar", datos))
    elif accion == "eliminar":
        lista.insertar_en_posicion(datos["vuelo"], datos["posicion"])
        redo_stack.append(("eliminar", datos))
    return {"mensaje": f"Deshecho: {accion}"}

def redo(lista):
    if not redo_stack:
        return {"mensaje": "Nada para rehacer"}
    accion, datos = redo_stack.pop()
    if accion == "insertar":
        lista.insertar_en_posicion(datos["vuelo"], datos["posicion"])
        undo_stack.append(("insertar", datos))
    elif accion == "eliminar":
        lista.extraer_de_posicion(datos["posicion"])
        undo_stack.append(("eliminar", datos))
    return {"mensaje": f"Rehecho: {accion}"}
