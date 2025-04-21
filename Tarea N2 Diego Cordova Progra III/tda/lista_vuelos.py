class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self._longitud = 0

    def insertar_al_frente(self, vuelo):
        nodo = Nodo(vuelo)
        if not self.primero:
            self.primero = self.ultimo = nodo
        else:
            nodo.siguiente = self.primero
            self.primero.anterior = nodo
            self.primero = nodo
        self._longitud += 1

    def insertar_al_final(self, vuelo):
        nodo = Nodo(vuelo)
        if not self.ultimo:
            self.primero = self.ultimo = nodo
        else:
            nodo.anterior = self.ultimo
            self.ultimo.siguiente = nodo
            self.ultimo = nodo
        self._longitud += 1

    def obtener_primero(self):
        return self.primero.vuelo if self.primero else None

    def obtener_ultimo(self):
        return self.ultimo.vuelo if self.ultimo else None

    def longitud(self):
        return self._longitud

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion <= 0:
            self.insertar_al_frente(vuelo)
        elif posicion >= self._longitud:
            self.insertar_al_final(vuelo)
        else:
            nodo = Nodo(vuelo)
            actual = self.primero
            for _ in range(posicion):
                actual = actual.siguiente
            nodo.anterior = actual.anterior
            nodo.siguiente = actual
            actual.anterior.siguiente = nodo
            actual.anterior = nodo
            self._longitud += 1

    def extraer_de_posicion(self, posicion):
        if self._longitud == 0:
            return None
        if posicion < 0 or posicion >= self._longitud:
            return None
        actual = self.primero
        for _ in range(posicion):
            actual = actual.siguiente
        if actual.anterior:
            actual.anterior.siguiente = actual.siguiente
        else:
            self.primero = actual.siguiente
        if actual.siguiente:
            actual.siguiente.anterior = actual.anterior
        else:
            self.ultimo = actual.anterior
        self._longitud -= 1
        return actual.vuelo
