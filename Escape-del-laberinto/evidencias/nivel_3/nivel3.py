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

def extender(p, valor, modelo):
    nuevo_modelo = modelo.copy()
    nuevo_modelo[p] = valor
    return nuevo_modelo

def comprobar_tv(BC, alfa, simbolos, modelo):

    # Caso base
    if len(simbolos) == 0:
        if BC(modelo):
            return alfa(modelo)
        else:
            return True
        
    # Caso recursivo
    p = simbolos[0]
    resto = simbolos[1:]

    return (
        comprobar_tv(BC, alfa, resto, extender(p, True, modelo))
        and
        comprobar_tv(BC, alfa, resto, extender(p, False, modelo))
    )

# verificación
modelo = {'P_8_9': False}

nuevo = extender('A_8_9', True, modelo)

print("Modelo original:", modelo)
print("Modelo extendido:", nuevo)

def comprobar_tv(BC, alfa, simbolos, modelo):

    # Caso base
    if len(simbolos) == 0:
        if BC(modelo):
            return alfa(modelo)
        else:
            return True
        
    # Caso recursivo
    p = simbolos[0]
    resto = simbolos[1:]

    return (
        comprobar_tv(BC, alfa, resto, extender(p, True, modelo))
        and
        comprobar_tv(BC, alfa, resto, extender(p, False, modelo))
    )


def regla_percepcion(i, j, brisa, hedor, N):

    adyacentes = casillas_adyacentes(i, j, N)

    return lambda m: (
        (any(m[f'P_{x}_{y}'] for x, y in adyacentes) == brisa)
        and
        (any(m[f'T_{x}_{y}'] for x, y in adyacentes) == hedor)
    )

def verificar_trayectoria(trayectoria):

    BC = lambda m: True
    simbolos = set()

    # Conocimiento inicial: la casilla (1,1) es segura
    BC = decir(BC, lambda m: not m['P_1_1'])
    BC = decir(BC, lambda m: not m['T_1_1'])

    simbolos.update(['P_1_1', 'T_1_1'])

    for paso in range(len(trayectoria) - 1):

        actual = trayectoria[paso]
        siguiente = trayectoria[paso + 1]

        i, j = actual

        brisa, hedor = percibir(actual)

        # Incorporar la percepción a la BC
        sentencia = regla_percepcion(i, j, brisa, hedor, N)
        BC = decir(BC, sentencia)

        # Actualizar símbolos
        simbolos = agregar_simbolos(simbolos, i, j, N)

        # Completa la verificación del movimiento
        sig_i, sig_j = siguiente
        segura = es_segura(sig_i, sig_j, BC, simbolos)

        print("Posición actual:", actual)
        print("Percepción:", (brisa, hedor))
        print("Siguiente casilla:", siguiente)
        print("¿Es segura?:", segura)
        print()

        if not segura:
            print("Movimiento no autorizado.")
            break

    else:
        print("Trayectoria completada.")