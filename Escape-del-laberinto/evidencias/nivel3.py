# ----------------------------------------------------------
# Funciones reutilizadas de la sección de material de apoyo
# ----------------------------------------------------------

def decir(BC, sentencia):
    """
    Operación TELL de un agente lógico.
    Combina la Base de Conocimiento actual con una nueva sentencia mediante conjunción (AND).
    """
    return lambda m: BC(m) and sentencia(m)


def extender(p, valor, modelo):
    """
    Construye un modelo parcial extendido asignando un valor booleano a la proposición p.
    """
    nuevo_modelo = modelo.copy()
    nuevo_modelo[p] = valor
    return nuevo_modelo


def comprobar_tv(BC, alfa, simbolos, modelo):
    """
    Algoritmo recursivo de comprobación de modelos mediante tablas de verdad.
    Verifica si BC ⊨ alfa (si alfa es consecuencia lógica de la Base de Conocimiento).
    """
    # Caso base: modelo completo
    if len(simbolos) == 0:
        if BC(modelo):
            return alfa(modelo)
        else:
            return True  # Si la BC es falsa en el modelo, no invalida la implicación

    # Caso recursivo: ramificación de valores de verdad (True / False)
    p = simbolos[0]
    resto = simbolos[1:]

    return (
        comprobar_tv(BC, alfa, resto, extender(p, True, modelo))
        and
        comprobar_tv(BC, alfa, resto, extender(p, False, modelo))
    )

# ----------------------------------------------------------

RUTA_PATRULLA = [(8, 9), (9, 9), (9, 8), (8, 8)]

def casillas_adyacentes(pos, ancho=10, alto=10, muros=set()):
    x, y = pos
    candidatos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    return [
        (cx, cy)
        for cx, cy in candidatos
        if 1 <= cx <= ancho
        and 1 <= cy <= alto
        and (cx, cy) not in muros
    ]


def inferir_movimiento_captura(pos_agente, pos_jugador, muros):
    adyacentes = casillas_adyacentes(pos_agente, muros=muros)

    # 1. Detección: ¿El jugador está en las celdas adyacentes?
    if pos_jugador in adyacentes:

        # Construir Base de Conocimiento y verificar implicación lógica
        BC = lambda m: True

        # Asignar hecho: El jugador está en pos_jugador
        for celda in adyacentes:
            es_jugador = (celda == pos_jugador)

            BC = decir(
                BC,
                lambda m, c=celda, val=es_jugador: m[f"J_{c}_{c[1]}"] == val
            )

        simbolos = [f"J_{c}_{c[1]}" for c in adyacentes]

        # Verificar para cuál casilla adyacente se demuestra que contiene al jugador
        for celda in adyacentes:
            alfa = lambda m, c=celda: m[f"J_{c}_{c[1]}"] == True

            if comprobar_tv(BC, alfa, simbolos, {}):
                return celda

        # Moverse directamente a capturarlo

    return None


def turno_agente_nivel3(pos_agente, idx_patrulla, pos_jugador, muros):
    # Intentar inferencia de captura
    movimiento_captura = inferir_movimiento_captura(
        pos_agente, pos_jugador, muros
    )

    if movimiento_captura is not None:
        return movimiento_captura, idx_patrulla

    # Interrumpe patrullaje y captura

    # Si no detecta al jugador, continuar patrullaje cíclico
    siguiente_idx = (idx_patrulla + 1) % len(RUTA_PATRULLA)
    siguiente_pos = RUTA_PATRULLA[siguiente_idx]

    return siguiente_pos, siguiente_idx