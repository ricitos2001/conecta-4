import socket
import time

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


server.close()