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

crearSocket() -- Retorna un nuevo socket siguiendo el esquema del
                 protocolo TCP

conectarse (host, port, s) -- Su nombre lo dice todo

intentoConexion(host, port, s) -- Si el puerto no esta tomado y
                                  la direccion sumistrada es correcta
                                  se conectara al servidor

enviar(s) -- Gestiona los mensajes que seran enviados al servidor.
             Esta funcion llama a recibir una vez que el mensaje es
             enviado al cliente

recibir(s) -- Hilo que se ejecuta una vez y muere. Recibe los mensajes
              del servidor

recibirEspecial(s) -- Recibe un numero. Este sera el numero del cliente

"""


#######################################################################
##                            LIBRERIAS                              ##
#######################################################################

from socket import *
import time
from _thread import *

#######################################################################
##                            FUNCIONES                              ##
#######################################################################

def ini():
    host = input("Server Address: ")
    port = int(input("Port: "))
    return host, port

def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

def conectarse (host, port, s):
    s.connect((host, port))

def intentoConexion(host, port, s):

        while True:
            print("\nTrying to connect to:", host + ":" + str(port))
            try:
                conectarse(host, port, s)
                break
            except:
                print("There is no Server at:", host + ":" + str(port))
                print("Trying again in 5 Seconds\n")
                time.sleep(5)

def enviar(s):

    while True:

        global exit

        try:
            msg = input("")
            msg = client +": " + msg
            if msg == client+": salir":
                exit = True
                msg = "The "+client+" Client is gone"
                s.send(msg.encode("UTF-8"))
                s.close
                break
            else:
                s.send(msg.encode("UTF-8"))
                start_new_thread(recibir,(s,))


        except:
            print("Something happend\n")
            print("Trying in 5 seg")
            time.sleep(5)

def recibir(s):
    while True:

        try:
          reply = s.recv(2048)
          print(reply.decode("UTF-8"))
          break


        except:
            print("Cant recieve response\n")
            print("Trying in 5 seg")
            time.sleep(5)

def recibirEspecial(s):
    global client
    client = s.recv(2048).decode("UTF-8")

#######################################################################
##                          VARIABLES GLOBALES                       ##
#######################################################################

exit=False      # Si el cliente envia salir, exit se pone en true y el
                # el programa termina
client = ""

#######################################################################
##                                MAIN                               ##
#######################################################################

def main():

    host, port = ini()
    s = crearSocket()
    intentoConexion(host,port,s)
    recibirEspecial(s)
    print("\nConnection To Server Established!\nThe server is:", host+":"+str(port)+"\n")
    print("Write your messages\n")
    start_new_thread(enviar,(s,))

    while exit!=True:   # Necesarios para que los hilos no mueran
        pass

    print("\nSorry something went wrong! You have lost connection to the server.:(")
    print("Closing the windows in 5 seg")
    time.sleep(10)

main()


