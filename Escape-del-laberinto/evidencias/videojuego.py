import sys

# Importar las funciones de cada módulo de nivel que irán construyendo
# from nivel1 import obtener_siguiente_paso_a_estrella
# from nivel2 import obtener_movimiento_minimax
# from nivel3 import turno_agente_nivel3


# -------------------------------------------------------------
# 1. DIBUJO Y VISUALIZACIÓN EN CONSOLA (ASCII)
# -------------------------------------------------------------
def mostrar_tablero(ancho, alto, pos_jugador, pos_agente, pos_meta, muros):
    """
    Imprime el tablero de 10x10 en consola.
    (1,1) es la esquina inferior izquierda y (10,10) la superior derecha.
    """
    print("\n" + "=" * 25)

    for y in range(alto, 0, -1):
        fila = ""

        for x in range(1, ancho + 1):
            pos = (x, y)

            if pos == pos_jugador and pos == pos_agente:
                fila += "X "  # Captura
            elif pos == pos_jugador:
                fila += "P "  # Jugador
            elif pos == pos_agente:
                fila += "G "  # Agente perseguidor
            elif pos == pos_meta:
                fila += "E "  # Salida / Meta
            elif pos in muros:
                fila += "# "  # Obstáculo
            else:
                fila += ". "  # Celda libre

        print(fila)

    print("=" * 25)


# -------------------------------------------------------------
# 2. CONTROL DEL JUGADOR HUMANO
# -------------------------------------------------------------
def obtener_movimiento_jugador(pos_jugador, ancho, alto, muros):
    """
    Solicita la dirección al usuario y valida que el movimiento sea legal.
    """
    movimientos = {
        'w': (0, 1),   # Arriba
        's': (0, -1),  # Abajo
        'a': (-1, 0),  # Izquierda
        'd': (1, 0)    # Derecha
    }

    x, y = pos_jugador

    while True:
        entrada = input(
            "Tu turno (W=Arriba, S=Abajo, A=Izquierda, D=Derecha): "
        ).strip().lower()

        if entrada in movimientos:
            dx, dy = movimientos[entrada]
            nueva_pos = (x + dx, y + dy)

            # Validar límites del tablero 10x10 y que no sea un muro
            nx, ny = nueva_pos

            if (
                1 <= nx <= ancho
                and 1 <= ny <= alto
                and nueva_pos not in muros
            ):
                return nueva_pos
            else:
                print("Movimiento inválido: choca con un muro o sale del tablero.")
        else:
            print("Tecla no válida. Usa W, A, S o D.")


# -------------------------------------------------------------
# 3. BUCLE PRINCIPAL DE UN NIVEL
# -------------------------------------------------------------
def jugar_nivel(num_nivel, pos_inicial_agente, mapa_config):
    ancho = 10
    alto = 10
    pos_jugador = (1, 1)
    pos_meta = (10, 10)
    pos_agente = pos_inicial_agente
    muros = mapa_config["muros"]

    # Estado específico para Nivel 3 (patrullaje)
    idx_patrulla = 0

    print(f"\n==========================================")
    print(f" INICIANDO NIVEL {num_nivel}")
    print(f"==========================================")

    turno = 1

    while True:
        print(f"\n--- Turno {turno} ---")

        mostrar_tablero(
            ancho, alto, pos_jugador, pos_agente, pos_meta, muros
        )

        # -----------------------------------------------------
        # TURNO DEL JUGADOR
        # -----------------------------------------------------
        pos_jugador = obtener_movimiento_jugador(
            pos_jugador, ancho, alto, muros
        )

        # Comprobar si el jugador llegó a la meta
        if pos_jugador == pos_meta:
            mostrar_tablero(
                ancho, alto, pos_jugador, pos_agente, pos_meta, muros
            )
            print(f"\n¡Felicidades! Has superado el Nivel {num_nivel}.")
            return True

        # Comprobar si el jugador se movió a la celda del agente (suicidio/captura)
        if pos_jugador == pos_agente:
            mostrar_tablero(
                ancho, alto, pos_jugador, pos_agente, pos_meta, muros
            )
            print(
                f"\nEL AGENTE TE HA CAPTURADO. HAS PERDIDO EN EL NIVEL {num_nivel}."
            )
            return False

        # -----------------------------------------------------
        # TURNO DEL AGENTE PERSEGUIDOR
        # -----------------------------------------------------
        if num_nivel == 1:
            # Nivel 1: Algoritmo A*
            # pos_agente = obtener_siguiente_paso_a_estrella(
            #     problema, pos_agente, pos_jugador
            # )
            pass

        elif num_nivel == 2:
            # Nivel 2: Minimax con Poda Alfa-Beta
            # estado_juego = {
            #     "pos_agente": pos_agente,
            #     "pos_jugador": pos_jugador
            # }
            # pos_agente = obtener_movimiento_minimax(
            #     estado_juego, problema, profundidad_max=4
            # )
            pass

        elif num_nivel == 3:
            # Nivel 3: Agente Lógico (Patrullaje + Inferencia)
            # pos_agente, idx_patrulla = turno_agente_nivel3(
            #     pos_agente, idx_patrulla, pos_jugador, muros
            # )
            pass

        # Comprobar si el agente capturó al jugador
        if pos_agente == pos_jugador:
            mostrar_tablero(
                ancho, alto, pos_jugador, pos_agente, pos_meta, muros
            )
            print(
                f"\nEL AGENTE TE HA CAPTURADO. HAS PERDIDO EN EL NIVEL {num_nivel}."
            )
            return False

        turno += 1


# -------------------------------------------------------------
# 4. SECUENCIA CONSECUTIVA DEL JUEGO
# -------------------------------------------------------------
def ejecutar_videojuego():

    # Definición de obstáculos según IA-PF.pdf para los 3 niveles
    escenarios = {
        1: {"pos_agente": (8, 9), "muros": set()},  # Cargar muros del Nivel 1
        2: {"pos_agente": (7, 9), "muros": set()},  # Cargar muros del Nivel 2
        3: {"pos_agente": (8, 9), "muros": set()}   # Cargar muros del Nivel 3
    }

    print("==========================================")
    print(" PROYECTO FINAL IA: ESCAPE DEL LABERINTO")
    print("==========================================")

    # Secuencia fija de los tres niveles
    for nivel in [1, 2, 3]:
        exito = jugar_nivel(
            nivel,
            escenarios[nivel]["pos_agente"],
            escenarios[nivel]
        )

        if not exito:
            print("\nJuego Terminado. Debes reiniciar desde el Nivel 1 para ganar.")
            return

    print(
        "\n¡HAS COMPLETADO LOS TRES NIVELES CONSECUTIVAMENTE! ¡VICTORIA TOTAL!"
    )


if __name__ == "__main__":
    ejecutar_videojuego()