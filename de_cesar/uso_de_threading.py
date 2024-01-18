from threading import Thread
import primera_conexion_servidor
import primera_conexion_cliente

if __name__=="__main__":
    ejecucion=True
    while ejecucion:
        JUGADOR_1 = Thread(target=primera_conexion_servidor)
        JUGADOR_2 = Thread(target=primera_conexion_cliente)