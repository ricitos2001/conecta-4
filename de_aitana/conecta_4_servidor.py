# -*- coding: utf-8 -*-

'''
Conecta 4 - servidor
'''

import sys
import socket


def comprobar_version_python() -> bool:
    '''Comprobar la versión de Python del ordenador

    Return:
        bool: True si la versión es válida // False si la versión no es válida
    '''
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


def saber_mi_ip() -> str:
    '''Obtener ip privada del ordenador

    Return:
        str: ip de este equipo, servidor
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_servidor = s.getsockname()[0]
    s.close()

    return ip_servidor


def buscar_para_jugar() -> str:
    '''PRIMERA CONEXIÓN, BUSCAR QUIEN QUIERE JUGAR

    Return:
        str: ip del cliente y el puerto usado en el socket
    '''
    # crear el socket --> IPv4 & UDP
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Modo de difusión: los paquetes se transmitirán a todos los equipos de la red
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    server.settimeout(0.2)

    # mensaje que enviará el servidor con su dirección IP
    # msj = f"{ip}"
    msj = "marco"
    msj_encode = msj.encode('utf-8') # codificación del mensaje

    respuesta_decode = ""
    while (respuesta_decode == ""):
        server.sendto(msj_encode, ('<broadcast>', 37020)) # puerto: 37020
        # mensaje enviado

        try:
            # Esperar la respuesta
            respuesta, ip_puerto_cliente = server.recvfrom(1024)
            respuesta_decode = respuesta.decode('utf-8') 
            # mensaje recibido
        except socket.timeout:
            print("Esperando respuesta...")


    server.close()

    ip_cliente = ip_puerto_cliente[0]
    puerto= ip_puerto_cliente[1]

    return ip_cliente, puerto


def main():
    # Comprobar la versión de python
    version_valida = comprobar_version_python()

    # si la versión es válida empieza a ejecutarse el programa
    if version_valida:

        # saber mi ip
        ip_servidor = saber_mi_ip()

        # buscar con quien jugar
        ip_cliente, puerto = buscar_para_jugar() # el puerto es 37020
        
        # conexión directa con el cliente
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_juego:
            socket_juego.bind((ip_servidor, puerto))
            socket_juego.listen()

            socket_entrada, ip_cliente = socket_juego.accept() # block, espera conexión entrante del cliente

            with socket_entrada:
                print("-- EMPIEZA LA PARTIDA --")
                
                ganador = False
                while ganador == False:
                    
                    # empieza la partida el cliente
                    mov_cliente = socket_entrada.recv(1024) # block, espera a que el cliente envie su movimiento

                    # lo pone en el tablero o compueba si es un mensaje para terminar la partida

                    # elige una columna donde colocar su ficha

                    # comprueba si ha ganado o el tablero esta lleno

                    # el servidor envía su movimiento
                    socket_entrada.sendall("movimeinto del servidor")

        socket_juego.close()

        print("-- FIN DE LA PARTIDA --")


if __name__ == '__main__':
    main()