# -*- coding: utf-8 -*-

import sys
import socket
import random


def comprobar_version_python() -> bool:
    version_valida = False

    if sys.version_info[0] == 2:
        print("Actualiza la versión de Python a la más reciente para poder ejecutar el programa...")

    elif sys.version_info[0] == 3:

        if sys.version_info[1] < 11:
            print("Actualiza la versión de Python a la más reciente para poder ejecutar el programa...")

        else:
            version_valida = True

    else:
        print("Versión de Python desconocida...")

    return version_valida


def buscar_para_jugar() -> str:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)

    msj = "marco"
    msj_encode = msj.encode('utf-8')

    respuesta_decode = ""
    while respuesta_decode == "":
        server.sendto(msj_encode, ('<broadcast>', 37020))

        try:
            respuesta, ip_puerto_cliente = server.recvfrom(1024)
            respuesta_decode = respuesta.decode('utf-8')
        except socket.timeout:
            print("Esperando respuesta...")

    server.close()

    ip_cliente = ip_puerto_cliente[0]
    puerto = ip_puerto_cliente[1]

    return ip_cliente, puerto


def mostrar_tablero(tablero):
    for fila in tablero:
        print("|".join(fila))
    print("---------------")

def enviar_tablero(socket_juego, tablero):
    estado_tablero = ""
    for fila in tablero:
        estado_tablero += "|".join(fila) + "\n"
    socket_juego.send(estado_tablero.encode('utf-8'))

def obtener_movimiento_ia(tablero):
    # Lógica avanzada para la IA: elegir la columna que maximiza las posibilidades de alinear fichas y bloquear al oponente
    mejor_columna = None
    mejor_puntaje = -1

    for columna in range(7):
        if tablero[0][columna] == ' ':
            fila = obtener_fila_disponible(tablero, columna)
            tablero[fila][columna] = 'X'  # Supongamos que es el turno de la IA
            puntaje = evaluar_puntaje(tablero, fila, columna, 'X')
            tablero[fila][columna] = ' '  # Deshacer el movimiento

            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_columna = columna

    return mejor_columna

def colocar_ficha(tablero, columna, jugador):
    fila = 5
    while fila >= 0 and tablero[fila][columna] != ' ':
        fila -= 1
    if fila >= 0:
        tablero[fila][columna] = jugador
    return fila

def hay_ganador(tablero, fila, columna, jugador):
    #Verificar en la fila
    if sum(1 for i in range(7) if tablero[fila][i] == jugador) >= 4:
        return True

    #Verificar en la columna
    if sum(1 for i in range(6) if tablero[i][columna] == jugador) >= 4:
        return True

    #Verificar en la diagonal principal
    diagonal_principal = [tablero[fila - i][columna - i] for i in range(1, 5) if 0 <= fila - i < 6 and 0 <= columna - i < 7]
    diagonal_principal.reverse()
    diagonal_principal.append(jugador)
    diagonal_principal.extend([tablero[fila + i][columna + i] for i in range(1, 5) if 0 <= fila + i < 6 and 0 <= columna + i < 7])
    if sum(1 for ficha in diagonal_principal if ficha == jugador) >= 4:
        return True

    #Verificar en la diagonal secundaria
    diagonal_secundaria = [tablero[fila - i][columna + i] for i in range(1, 5) if 0 <= fila - i < 6 and 0 <= columna + i < 7]
    diagonal_secundaria.reverse()
    diagonal_secundaria.append(jugador)
    diagonal_secundaria.extend([tablero[fila + i][columna - i] for i in range(1, 5) if 0 <= fila + i < 6 and 0 <= columna - i < 7])
    if sum(1 for ficha in diagonal_secundaria if ficha == jugador) >= 4:
        return True

    return False

def obtener_fila_disponible(tablero, columna):
    fila = 5
    while fila >= 0 and tablero[fila][columna] != ' ':
        fila -= 1
    return fila

def evaluar_puntaje(tablero, fila, columna, jugador):
    #Evaluar el puntaje considerando la posición de la última ficha colocada
    puntaje = 0

    #Evaluar en la fila
    puntaje += contar_consecutivas(tablero[fila], jugador)

    #Evaluar en la columna
    puntaje += contar_consecutivas([tablero[i][columna] for i in range(6)], jugador)

    #Evaluar en la diagonal principal
    diagonal_principal = [tablero[fila - i][columna - i] for i in range(1, 5) if 0 <= fila - i < 6 and 0 <= columna - i < 7]
    diagonal_principal.reverse()
    diagonal_principal.append(jugador)
    diagonal_principal.extend([tablero[fila + i][columna + i] for i in range(1, 5) if 0 <= fila + i < 6 and 0 <= columna + i < 7])
    puntaje += contar_consecutivas(diagonal_principal, jugador)

    #Evaluar en la diagonal secundaria
    diagonal_secundaria = [tablero[fila - i][columna + i] for i in range(1, 5) if 0 <= fila - i < 6 and 0 <= columna + i < 7]
    diagonal_secundaria.reverse()
    diagonal_secundaria.append(jugador)
    diagonal_secundaria.extend([tablero[fila + i][columna - i] for i in range(1, 5) if 0 <= fila + i < 6 and 0 <= columna - i < 7])
    puntaje += contar_consecutivas(diagonal_secundaria, jugador)

    #Evaluar bloqueo del oponente
    oponente = 'O' if jugador == 'X' else 'X'
    puntaje += contar_consecutivas(tablero[fila], oponente, bloqueo=True)
    puntaje += contar_consecutivas([tablero[i][columna] for i in range(6)], oponente, bloqueo=True)
    puntaje += contar_consecutivas(diagonal_principal, oponente, bloqueo=True)
    puntaje += contar_consecutivas(diagonal_secundaria, oponente, bloqueo=True)

    return puntaje


def contar_consecutivas(linea, jugador, bloqueo=False):
    #Contar fichas consecutivas en una linea, considerando la posibilidad de bloquear al oponente
    contador = 0
    max_consecutivas = 0

    for ficha in linea:
        if ficha == jugador:
            contador += 1
            max_consecutivas = max(max_consecutivas, contador)
        elif not bloqueo:
            contador = 0

    return max_consecutivas

def manejar_turno_jugador(socket_juego, tablero, jugador_actual):
    mostrar_tablero(tablero)
    enviar_tablero(socket_juego, tablero)

    if jugador_actual == 'X':
        columna_elegida = obtener_movimiento_ia(tablero)
    else:
        mensaje_turno = f"Es el turno del Jugador {jugador_actual}. Elige una columna (0-6): "
        socket_juego.send(mensaje_turno.encode('utf-8'))
        columna_elegida = int(socket_juego.recv(1024).decode('utf-8'))

    if not (0 <= columna_elegida <= 6) or tablero[0][columna_elegida] != ' ':
        socket_juego.send("Movimiento inválido. Inténtalo de nuevo.".encode('utf-8'))
        return False

    fila = colocar_ficha(tablero, columna_elegida, jugador_actual)

    if hay_ganador(tablero, fila, columna_elegida, jugador_actual):
        mostrar_tablero(tablero)
        mensaje_ganador = f"¡Felicidades! Jugador {jugador_actual} ha ganado."
        socket_juego.send(mensaje_ganador.encode('utf-8'))
        return True

    return False