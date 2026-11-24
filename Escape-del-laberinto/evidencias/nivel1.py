import heapq

# ----------------------------------------------------------
# Funciones reutilizadas de la sección de material de apoyo
# ----------------------------------------------------------

# Acciones de movimiento en la cuadrícula
acciones = {
    "izquierda": (-1, 0),
    "abajo": (0, -1),
    "arriba": (0, 1),
    "derecha": (1, 0)
}


def es_valido(x, y, muros=set(), ancho=10, alto=10):
    """Verifica que la posición esté dentro del tablero 10x10 y no sea un muro."""
    return (
        1 <= x <= ancho
        and 1 <= y <= alto
        and (x, y) not in muros
    )


def sucesor_fn(estado, muros=set()):
    """Genera las acciones legales y los estados resultantes desde el estado actual."""
    x, y = estado
    sucesores = []

    for accion, (dx, dy) in acciones.items():
        nuevo_x, nuevo_y = x + dx, y + dy

        if es_valido(nuevo_x, nuevo_y, muros):
            sucesores.append((accion, (nuevo_x, nuevo_y)))

    return sucesores


def costo_accion(estado, accion, estado_sucesor):
    """Costo uniforme de cada movimiento."""
    return 1


def hacer_nodo(estado, padre, accion, costo_camino, profundidad):
    """Crea la estructura de diccionario de un nodo en el árbol de búsqueda."""
    return {
        "estado": estado,
        "padre": padre,
        "accion": accion,
        "costo_camino": costo_camino,
        "profundidad": profundidad
    }


def expandir(nodo, problema):
    """Expande un nodo utilizando la función sucesora del problema."""
    sucesores = []

    for accion, estado in problema["funcion_sucesora"](nodo["estado"]):
        nuevo_nodo = hacer_nodo(
            estado,
            nodo,
            accion,
            nodo["costo_camino"] + problema["costo_accion"](
                nodo["estado"], accion, estado
            ),
            nodo["profundidad"] + 1
        )

        sucesores.append(nuevo_nodo)

    return sucesores


def solucion(nodo):
    """Reconstruye el camino desde el nodo inicial siguiendo la referencia a los padres."""
    camino = []

    while nodo["padre"] is not None:
        camino.append((nodo["padre"]["estado"], nodo["accion"]))
        nodo = nodo["padre"]

    camino.reverse()
    return camino

# ----------------------------------------------------------

# 1. Distancia Manhattan
def heuristica_manhattan(estado_actual, estado_jugador):
    x, y = estado_actual
    xj, yj = estado_jugador
    return abs(x - xj) + abs(y - yj)


# 2. Frontera con prioridad f(n) = g(n) + h(n)
class FronteraAEstrella:
    def __init__(self, estado_jugador):
        self.heap = []
        self.contador = 0
        self.estado_jugador = estado_jugador

    def pendientes(self):
        return len(self.heap) > 0

    def get(self):
        _, _, nodo = heapq.heappop(self.heap)
        return nodo

    def put(self, nodos):
        if not isinstance(nodos, list):
            nodos = [nodos]

        for nodo in nodos:
            g = nodo["costo_camino"]
            h = heuristica_manhattan(nodo["estado"], self.estado_jugador)
            f = g + h
            heapq.heappush(self.heap, (f, self.contador, nodo))
            self.contador += 1


# 3. Búsqueda A* en Grafos
def obtener_siguiente_paso_a_estrella(problema, pos_agente, pos_jugador):
    if pos_agente == pos_jugador:
        return pos_agente

    # Actualizar estado inicial y objetivo dinámicamente
    problema_actual = problema.copy()
    problema_actual["estado_inicial"] = pos_agente
    problema_actual["test_objetivo"] = lambda s: s == pos_jugador

    cerrado = set()
    frontera = FronteraAEstrella(pos_jugador)

    nodo_inicial = hacer_nodo(pos_agente, None, None, 0, 0)
    frontera.put([nodo_inicial])

    while frontera.pendientes():
        nodo = frontera.get()

        if problema_actual["test_objetivo"](nodo["estado"]):
            camino = solucion(nodo)

            # Devolver el estado del primer movimiento
            if camino:
                _, primer_paso = camino
                return primer_paso

            return pos_agente

        if nodo["estado"] not in cerrado:
            cerrado.add(nodo["estado"])
            sucesores = expandir(nodo, problema_actual)
            frontera.put(sucesores)

    return pos_agente

# Si no hay camino, se queda en su lugar