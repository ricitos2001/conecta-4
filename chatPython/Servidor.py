#######################################################################
##                                                                   ##
##                    UNIVERSIDAD SIMON BOLIVAR                      ##
##                     REDES DE COMPUTADORAS                         ##
##                                                                   ##
## PROFESOR: Luis G. Uribe C.                                        ##
##                                                                   ##
## INTEGRANTES: BRUNO BARONE   10-10058                              ##
##              VINCENZO MIALE 10-10457                              ##
##                                                                   ##
#######################################################################


#######################################################################
##                          DESCRIPCION                              ##
#######################################################################

"""\

El presente proyecto se basa en la ejecucion de un servidor que espera
respuesta de un max de 2 clientes. Sera simulado el comportamiento de
un chat. En su ejecucion, el servidor sera el esclavo mientras con que
clientes seran los maestros, es decir, el servidor estara en la "espera"
de que los clientes le "hablen". El servidor no podra responder a un
cliente si este no le hablo en primer lugar. De tener muchos mensajes,
el servidor respondera segun el orden de peticion, es decir, si el
cliente 1 y 2 escriben, el servidor atendera en primer lugar al cliente 1
y luego al 2 ( cola ).

El servidor estara ejecutandose de por vida. Los clientes podran salirse
mandando el mensaje "salir" y podran volverse a conectar si el no se
ha cerrado el servidor.


Funciones:

ini() -- Pide al usuario el host y puerto.

crearSocket() -- Retorna un nuevo socket siguiendo el esquema del protocolo TCP

ligarSocket(s, host, port) -- Intenta ligar un socket a los parametros host y port

conexiones(s) -- Espera por la conexion de clientes externos. Retorna la direccion del cliente en una tupla

enviar(conn) -- Envia un mensaje codificado a la direccion del cliente 1

enviar2(conn) -- Envia un mensaje codificado a la direccion del cliente 2

recibir(conn) -- Gestiona los mensajes recibidos de los distintos clientes. Llama a la funcion enviar una vez que recibe mensajes

enviarEspecial(conn) -- El servidor asigna un numero y lo envia al cliente
                        respectivo

"""

#######################################################################
##                            LIBRERIAS                              ##
#######################################################################

from socket import *
from _thread import *
import time
import sys

#######################################################################
##                            FUNCIONES                              ##
#######################################################################

def ini():
    host = input("Host: ")
    port = int(input("Port: "))
    return host, port

def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

def ligarSocket(s, host, port):
    while True:
        try:
            s.bind((host, port))
            break

        except error as e:
            print("ERROR:", e)

def conexiones(s):

    conn, addr = s.accept()
    print("\nEstablished Connection.\nThe client is:", addr[0] + ":" + str(addr[1])+"\n")
    return conn, addr

def enviar(conn):

        msg = input("")
        msg = "Servidor: " + msg
        try:

            conn.send(msg.encode("UTF-8"))

        except:
            print("\nSomething happend")
            print("Try in 5 seg\n")
            time.sleep(5)

def enviar2(conn):

        msg = input("")
        msg = "Servidor: " + msg
        try:

            conn.send(msg.encode("UTF-8"))

        except:
            print("\nSomething happend")
            print("Try in 5 seg\n")
            time.sleep(5)

def recibir(conn):
    while True:
        global bandera
        try:
            reply = conn.recv(2048)
            reply = reply.decode("UTF-8")

            if reply[0] == "1":
                print("Cliente", reply)
                start_new_thread(enviar, (conn,))

            elif reply[0] == "2":
                print("Cliente", reply)
                start_new_thread(enviar2, (conn,))

            else:
                lista_de_clientes.append(reply[4])
                print("\nThe client "+reply[4]+" is gone")
                bandera = True
                break



        except:
            print("\nCant recieve response")
            print("Trying in 5 seg\n")
            time.sleep(5)


def enviarEspecial(conn):
    global lista_de_clientes,client
    client = lista_de_clientes.pop()
    conn.send(client.encode("UTF-8"))

#######################################################################
##                          VARIABLES GLOBALES                       ##
#######################################################################

bandera = False      # Utilizada en la desconexion/conexion de clientes

lista_de_clientes = ["2","1"]   # El servidor le asigna un numero a los
                                # clientes segun esta lista

client = ""     # Numero del cliente


#######################################################################
##                                MAIN                               ##
#######################################################################

def main():

    global bandera
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(2)     # Espero 2 clientes

    print("\nW A R N I N G : THE SERVER IS A SLAVE. DON'T WRITE IF THE SERVER DOESN'T HAVE ANY MESSAGE TO RESPONSE")
    print("\nWaiting for clients")

    conn,addr = conexiones(s)
    enviarEspecial(conn)               # Espero conexion del 1 cliente
    start_new_thread(recibir,(conn,))

    conn2,addr2 = conexiones(s)
    enviarEspecial(conn2)              # Espero conexion del 2 cliente
    start_new_thread(recibir,(conn2,))

    while True: # Necesario para que los hilos no mueran

        if bandera != True:     # En caso de desconectarse un cliente,
                                # esperara a que otro vuelve a conectarse
            conn3,addr3 = conexiones(s)
            enviarEspecial(conn3)
            start_new_thread(recibir,(conn3,))
            bandera = False


main()
