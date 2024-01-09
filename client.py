# -*- codigo: utf-16 -*-

import socket

HOST = "172.26.2.205" #dirección servidor
PORT = 65123 #puerto de envío

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b"Hola mundo") #convierte en binario los datos
    data = s.recv(1024)
print("Recibido" + repr(data))