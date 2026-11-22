# Parámetros del entorno GridWorld
# Tamaño de la cuadrícula
N = 10

# Acciones disponibles para el agente
# Cada acción corresponde a un desplazamiento (dx, dy)
acciones = {
    "izquierda": (-1, 0),
    "abajo": (0, -1),
    "arriba": (0, 1),
    "derecha": (1, 0)
}

# Estado inicial del agente
estado_inicial = (N, N)

# Funciones del problema
def es_valido(x, y):
    return 1 <= x <= N and 1 <= y <= N

def sucesor_fn(estado):
    x, y = estado
    sucesores = []

    for accion, (dx, dy) in acciones.items():
        nuevo_x = x + dx
        nuevo_y = y + dy

        if es_valido(nuevo_x, nuevo_y):
            sucesores.append((accion, (nuevo_x, nuevo_y)))

    return sucesores

def test_objetivo(estado):
    return estado == estado_objetivo

def costo_accion(estado, accion, estado_sucesor):
    return 1

# Definición del problema
problema = {
    "estado_inicial": estado_inicial,
    "funcion_sucesora": sucesor_fn,
    "test_objetivo": test_objetivo,
    "costo_accion": costo_accion
}


def hacer_nodo(estado, padre, accion, costo_camino, profundidad):
    return {
        "estado": estado,
        "padre": padre,
        "accion": accion,
        "costo_camino": costo_camino,
        "profundidad": profundidad
    }

def expandir(nodo, problema):
    sucesores = []

    for accion, estado in problema["funcion_sucesora"](nodo["estado"]):

        nuevo_nodo = hacer_nodo(
            estado,
            nodo,
            accion,
            nodo["costo_camino"] + problema["costo_accion"](
                nodo["estado"],
                accion,
                estado
            ),
            nodo["profundidad"] + 1
        )

        sucesores.append(nuevo_nodo)

    return sucesores


def solucion(nodo):
    camino = []

    while nodo["padre"] is not None:
        camino.append(
            (nodo["padre"]["estado"], nodo["accion"])
        )
        nodo = nodo["padre"]

    camino.reverse()
    return camino

# Algoritmo general de búsqueda en árboles
def busqueda_arbol(problema, frontera):

    frontera.put([
        hacer_nodo(
            problema["estado_inicial"],
            None,
            None,
            0,
            0
        )
    ])

    while frontera.pendientes():

        nodo = frontera.get()

        if problema["test_objetivo"](nodo["estado"]):
            return solucion(nodo)

        frontera.put(expandir(nodo, problema))

    return None


### CREACIÓN DE ESCENARIOS ALEATORIOS
import random

def crear_escenario(ancho=10, alto=10, prob_muro=0.2, semilla=7, inicio=(1, 1)):
    random.seed(semilla)

    celdas = [
        (x, y)
        for x in range(1, ancho + 1)
        for y in range(1, alto + 1)
        if (x, y) != inicio
    ]

    muros = {
        celda
        for celda in celdas
        if random.random() < prob_muro
    }

    libres = [celda for celda in celdas if celda not in muros]
    meta = random.choice(libres)

    return {
        "ancho": ancho,
        "alto": alto,
        "muros": muros,
        "inicio": inicio,
        "meta": meta
    }

problema = crear_escenario(
    ancho=10,
    alto=10,
    prob_muro=0.2,
    semilla=1984,
    inicio=(1, 1)
)

print("Inicio:", problema["estado_inicial"])
print("Meta:", problema["estado_objetivo"])
print("Obstáculos:", problema["muros"])


# FI UNAM
# Inteligencia Artificial
# Carlos Roberto Vázquez Villegas

# Clase para la frontera con UCS
import heapq

class FronteraUCS:

    def __init__(self):
        self.heap = []
        self.contador = 0

    def pendientes(self):
        return len(self.heap)

    def get(self):
        prioridad, contador, nodo = heapq.heappop(self.heap)
        return nodo


    def put(self, nodos):
        for nodo in nodos:
            prioridad = nodo["costo_camino"]
            heapq.heappush(self.heap, (prioridad, self.contador, nodo))
            self.contador += 1

import heapq

class FronteraPrioridad:
    def __init__(self, f):
        self.heap = []
        self.f = f
        self.contador = 0

    def pendientes(self):
        return len(self.heap) > 0

    def get(self):
        # heapq.heappop devuelve la tupla (prioridad, contador, nodo)
        # Solo nos interesa regresar el nodo
        _, _, nodo = heapq.heappop(self.heap)
        return nodo

    def put(self, nodos):            
        for nodo in nodos:
            prioridad = self.f(nodo)
            # Insertamos una tupla con la prioridad, el desempate y el nodo
            heapq.heappush(self.heap, (prioridad, self.contador, nodo))
            self.contador += 1

def h(nodo):
    x, y = nodo["estado"]
    x_G, y_G = estado_objetivo
    
    # Distancia Manhattan: |x - x_G| + |y - y_G|
    return abs(x - x_G) + abs(y - y_G)
