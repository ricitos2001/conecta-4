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

def hay_ganador(tablero, fila, columna, jugador):
    # Verificar en la fila
    if sum(1 for i in range(7) if tablero[fila][i] == jugador) >= 4:
        return True

    # Verificar en la columna
    if sum(1 for i in range(6) if tablero[i][columna] == jugador) >= 4:
        return True

    # Verificar en la diagonal principal
    diagonal_principal = [tablero[fila - i][columna - i] for i in range(1, 5) if 0 <= fila - i < 6 and 0 <= columna - i < 7]
    diagonal_principal.reverse()
    diagonal_principal.append(jugador)
    diagonal_principal.extend([tablero[fila + i][columna + i] for i in range(1, 5) if 0 <= fila + i < 6 and 0 <= columna + i < 7])
    if sum(1 for ficha in diagonal_principal if ficha == jugador) >= 4:
        return True

    # Verificar en la diagonal secundaria
    diagonal_secundaria = [tablero[fila - i][columna + i] for i in range(1, 5) if 0 <= fila - i < 6 and 0 <= columna + i < 7]
    diagonal_secundaria.reverse()
    diagonal_secundaria.append(jugador)
    diagonal_secundaria.extend([tablero[fila + i][columna - i] for i in range(1, 5) if 0 <= fila + i < 6 and 0 <= columna - i < 7])
    if sum(1 for ficha in diagonal_secundaria if ficha == jugador) >= 4:
        return True

    return False