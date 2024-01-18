import socket
import socket


# obtener ip privada del ordenador
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

# PRIMERA CONEXIÓN, BUSCAR QUIEN QUIERE JUGAR
# crear el socket --> IPv4 & UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Modo de difusión: recibira paquetes trasmiridos por los equipos de la red
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Enlaza el socket al puerto 37020 en cualquier dirección IP disponible
client.bind(("", 37020))

try:
    # Espera a recibir un mensaje del servidor
    mensaje, ip_servidor = client.recvfrom(1024)
    print("Mensaje recibido!")

    # Envía una respuesta al servidor
    # respuesta = f"{ip}"
    respuesta = input("Estoy ready!!")
    client.sendto(respuesta.encode('utf-8'), ip_servidor)
    print(mensaje)

finally:
    # Cerrar el socket después de enviar y recibir
    client.close()



import socket

def play_game(socket_juego):
    while True:
        mensaje_servidor = socket_juego.recv(1024).decode()

        if mensaje_servidor.lower() == "win" or mensaje_servidor.lower() == "draw":
            print(mensaje_servidor)
            break

        print("Estado actual del juego:")
        print(mensaje_servidor)

        if "Tu turno" in mensaje_servidor:
            movimiento = input("Selecciona una columna (1-7): ")
            socket_juego.sendall(movimiento.encode())
        else:
            print("Esperando movimiento del oponente...")

if __name__ == "__main__":
    host = '192.168.1.58'  # AQUÍ CAMBIAR POR HOST DEL SERVIDOR!!!
    port = 5555  # Cambiado a un puerto más estándar para TCP

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        print("¡Bienvenido al juego Cuatro en Raya!")
        print("Esperando a que inicie el juego...")

        play_game(client_socket)

        print("¡Gracias por jugar!")
