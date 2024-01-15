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
    respuesta = "polo"
    client.sendto(respuesta.encode('utf-8'), ip_servidor)
    print(mensaje)

finally:
    # Cerrar el socket después de enviar y recibir
    client.close()

