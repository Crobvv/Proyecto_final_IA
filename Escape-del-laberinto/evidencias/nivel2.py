# ----------------------------------------------------------
# Funciones reutilizadas de la sección de material de apoyo
# ----------------------------------------------------------

# 1. Diccionario de acciones de movimiento (desplazamientos dx, dy)
acciones = {
    "arriba": (0, 1),
    "abajo": (0, -1),
    "izquierda": (-1, 0),
    "derecha": (1, 0)
}


# 2. Función de validación de casillas dentro del tablero 10x10 sin colisionar con muros
def es_valido(x, y, muros=set(), ancho=10, alto=10):
    return (
        1 <= x <= ancho
        and 1 <= y <= alto
        and (x, y) not in muros
    )


# 3. Generación de sucesores para el Agente (MAX)
def obtener_sucesores_agente(pos_agente, problema):
    sucesores = []
    muros = problema.get("muros", set())
    x, y = pos_agente

    for accion, (dx, dy) in acciones.items():
        nx, ny = x + dx, y + dy

        if es_valido(nx, ny, muros):
            sucesores.append((accion, (nx, ny)))

    return sucesores


# 4. Generación de sucesores para el Jugador Humano (MIN)
def obtener_sucesores_jugador(pos_jugador, problema):
    sucesores = []
    muros = problema.get("muros", set())
    x, y = pos_jugador

    for accion, (dx, dy) in acciones.items():
        nx, ny = x + dx, y + dy

        if es_valido(nx, ny, muros):
            sucesores.append((accion, (nx, ny)))

    return sucesores

# ----------------------------------------------------------

# Función de evaluación heurística para estados no terminales (Profundidad = 0)
def eval_estado_persecucion(estado_juego):
    pos_agente = estado_juego["pos_agente"]
    pos_jugador = estado_juego["pos_jugador"]

    # Captura
    if pos_agente == pos_jugador:
        return 1000  # Victoria MAX (Agente)

    # Escape del jugador
    if pos_jugador == (10, 10):
        return -1000  # Victoria MIN (Jugador)

    distancia = abs(pos_agente[0] - pos_jugador[0]) + abs(pos_agente[1] - pos_jugador[1])

    # A menor distancia, mayor utilidad para MAX
    return 100 - distancia


def obtener_movimiento_minimax(estado_juego, problema, profundidad_max=4):
    alfa = -float('inf')
    beta = float('inf')
    mejor_valor = -float('inf')
    mejor_movimiento = estado_juego["pos_agente"]

    # MAX es el agente perseguidor
    for accion, pos_sucesor in obtener_sucesores_agente(estado_juego["pos_agente"], problema):
        nuevo_estado = {
            "pos_agente": pos_sucesor,
            "pos_jugador": estado_juego["pos_jugador"]
        }

        v = min_valor_ab(nuevo_estado, alfa, beta, profundidad_max - 1, problema)

        if v > mejor_valor:
            mejor_valor = v
            mejor_movimiento = pos_sucesor

        alfa = max(alfa, mejor_valor)

    return mejor_movimiento


def max_valor_ab(estado_juego, alfa, beta, profundidad, problema):
    if estado_juego["pos_agente"] == estado_juego["pos_jugador"]:
        return 1000

    if profundidad == 0:
        return eval_estado_persecucion(estado_juego)

    v = -float('inf')

    for accion, pos_sucesor in obtener_sucesores_agente(estado_juego["pos_agente"], problema):
        nuevo_estado = {
            "pos_agente": pos_sucesor,
            "pos_jugador": estado_juego["pos_jugador"]
        }

        v = max(
            v,
            min_valor_ab(nuevo_estado, alfa, beta, profundidad - 1, problema)
        )

        if v >= beta:
            return v

        alfa = max(alfa, v)

    return v


def min_valor_ab(estado_juego, alfa, beta, profundidad, problema):
    if estado_juego["pos_agente"] == estado_juego["pos_jugador"]:
        return 1000

    if estado_juego["pos_jugador"] == (10, 10):
        return -1000

    if profundidad == 0:
        return eval_estado_persecucion(estado_juego)

    v = float('inf')

    # MIN es el jugador humano
    for accion, pos_sucesor in obtener_sucesores_jugador(estado_juego["pos_jugador"], problema):
        nuevo_estado = {
            "pos_agente": estado_juego["pos_agente"],
            "pos_jugador": pos_sucesor
        }

        v = min(
            v,
            max_valor_ab(nuevo_estado, alfa, beta, profundidad - 1, problema)
        )

        if v <= alfa:
            return v

        beta = min(beta, v)

    return v