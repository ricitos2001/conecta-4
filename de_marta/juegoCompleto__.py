# -*- coding: utf-8 -*-

import socket
import time

#--------------------------------------------------------
# FUNCIONES DE CONEXIÓN SERVER-CLIENTE

# obtener ip privada del ordenador
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()



# PRIMERA CONEXIÓN, BUSCAR QUIEN QUIERE JUGAR
# crear el socket --> IPv4 & UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Modo de difusión: los paquetes se transmitirán a todos los equipos de la red
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)

# mensaje que enviará el servidor con su dirección IP
# msj = f"{ip}"
msj = input("introduce un mensaje: ")
msj_encode = msj.encode('utf-8') # codificación del mensaje

print("\nBuscando alguien para jugar")
respuesta_decode = ""
while (respuesta_decode == ""):
    server.sendto(msj_encode, ('<broadcast>', 37020)) # puerto: 37020
    

    try:
        # Esperar la respuesta
        respuesta, ip_cliente = server.recvfrom(1024)
        respuesta_decode = respuesta.decode('utf-8')
        print(respuesta_decode)
    except socket.timeout:
        for i in range(4):
            mensaje = "Esperando respuesta" + "." * i
            print(f'\r{mensaje}', end='', flush=True)
            time.sleep(0.5)
        
        # Reiniciar el mensaje al llegar al final
        print('\r' + ' ' * len(mensaje), end='', flush=True)
#---------------------------------------------------------------
# FIN FUNCIONES CONEXION


#---------------------------------------------------------------
# A PARTIR DE AQUI ENTRAN FUNCIONES DEL JUEGO
        
def imprimir_tablero(tablero):
    for fila in tablero:
        print("|".join(fila))
        print("-----")
    print(" 1 2 3 4 5 6 7")

def es_movimiento_valido(columna, tablero):
    return tablero[0][columna] == ' '

def realizar_movimiento(columna, jugador, tablero):
    for fila in reversed(range(6)):
        if tablero[fila][columna] == ' ':
            tablero[fila][columna] = jugador
            break

def comprobar_ganador(jugador, tablero):
    # Comprobar filas
    for fila in range(6):
        for columna in range(4):
            if (
                tablero[fila][columna] == tablero[fila][columna + 1] == tablero[fila][columna + 2] == tablero[fila][columna + 3] == jugador
            ):
                return True

    # Comprobar columnas
    for columna in range(7):
        for fila in range(3):
            if (
                tablero[fila][columna] == tablero[fila + 1][columna] == tablero[fila + 2][columna] == tablero[fila + 3][columna] == jugador
            ):
                return True

    # Comprobar diagonales ascendentes
    for fila in range(3):
        for columna in range(4):
            if (
                tablero[fila][columna] == tablero[fila + 1][columna + 1] == tablero[fila + 2][columna + 2] == tablero[fila + 3][columna + 3] == jugador
            ):
                return True

    # Comprobar diagonales descendentes
    for fila in range(3, 6):
        for columna in range(4):
            if (
                tablero[fila][columna] == tablero[fila - 1][columna + 1] == tablero[fila - 2][columna + 2] == tablero[fila - 3][columna + 3] == jugador
            ):
                return True

    return False

def realizar_movimiento_automatico(tablero, jugador):
    import random
    columna = random.randint(0, 6)
    while not es_movimiento_valido(columna, tablero):
        columna = random.randint(0, 6)
    realizar_movimiento(columna, jugador, tablero)

def jugar_cuatro_en_raya(socket_entrada):
    tablero = [[' ' for _ in range(7)] for _ in range(6)]
    jugadores = ['X', 'O']
    jugador_actual = jugadores[0]
    ganador = False
    empate = False

    while not ganador and not empate:
        imprimir_tablero(tablero)

        if jugador_actual == 'X':
            # El cliente 'X' realiza un movimiento
            mov_cliente = socket_entrada.recv(1024).decode()
            try:
                columna = int(mov_cliente) - 1
                if 0 <= columna <= 6 and es_movimiento_valido(columna, tablero):
                    realizar_movimiento(columna, jugador_actual, tablero)
                    ganador = comprobar_ganador(jugador_actual, tablero)
                    if ganador:
                        imprimir_tablero(tablero)
                        print(f'¡El jugador {jugador_actual} ha ganado!')
                        socket_entrada.sendall("win".encode())
                    else:
                        jugador_actual = jugadores[1]
                else:
                    print("Movimiento no válido. Inténtalo de nuevo.")
                    socket_entrada.sendall("invalid".encode())
            except ValueError:
                print("Entrada no válida. Debe ser un número del 1 al 7.")
                socket_entrada.sendall("invalid".encode())

        elif jugador_actual == 'O':
            # El servidor realiza un movimiento automático para 'O'
            realizar_movimiento_automatico(tablero, jugador_actual)
            ganador = comprobar_ganador(jugador_actual, tablero)
            if ganador:
                imprimir_tablero(tablero)
                print(f'¡El jugador {jugador_actual} ha ganado!')
                socket_entrada.sendall("win".encode())
            else:
                jugador_actual = jugadores[0]

        empate = all(tablero[0][i] != ' ' for i in range(7))

    if not ganador and empate:
        imprimir_tablero(tablero)
        print("¡La partida ha terminado en empate!")
        socket_entrada.sendall("draw".encode())

#------------------------------------------------------------
# FIN FUNCIONES DEL JUEGO


#--------------------------------------------------------------
# MAIN
def main():
    ip_servidor = ip
    ip_cliente, puerto = #rellenar

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_juego:
        socket_juego.bind((ip_servidor, 5555))
        socket_juego.listen()
        socket_entrada, _ = socket_juego.accept()

        with socket_entrada:
            print("-- EMPIEZA LA PARTIDA --")
            jugar_cuatro_en_raya(socket_entrada)

    print("-- FIN DE LA PARTIDA --")

if __name__ == '__main__':
    main()
