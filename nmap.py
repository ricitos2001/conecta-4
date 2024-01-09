'''
#TODO\\ESCANER DE IP Y PUERTOS//  
#*1-. recibe una ip al ejecutar el fichero desde la terminal.
    - comprueba que sea una ip correcta
    - iidentificar si la clase de ip es de clase A, clase B, clase C, clase D o clase C
#*2.- comprobar si la ip está presente en la red
#*3.- comprobar los puertos abiertos del ordenador con esa IP
>python3 ip.py 192.168.0.1. 22:53:80:443
'''

import os
import sys
import socket
import platform
import subprocess

def checkear_version_de_python():
    '''
    Comprueba la versión de Python instalada en el sistema.
    :returns: Indica si la versión instalada es compatible o no.
    '''
    version_requerida = [(3, 10), (3, 11), (3, 12)]
    version_instalada = sys.version_info[:2]
    if version_instalada in version_requerida:
        verificacion="version de python: "+str(version_instalada)+"\nla version de python instalada es compatible."
        print(verificacion)
        os.system("pause")
        borrar_consola()
    else:
        verificacion="la version de python instalada es compatible\nes necesario tener instalado Python3.10, 3.11, o 3.12"
        print(verificacion)

def borrar_consola():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

def comprobar_formato_ip(ip):
    '''comprueba que la ip dada por el usuario este formada por 4 octetos numericos que estan entre 0 y 255 o sino sea asi mostrara un mensaje de error
    Args:
        ip (str): ip dada por el usuario
    Return:
        bool: True si el formato es correcto // False si el formato es incorrecto
    '''
    # comprobar que la ip esta formada por 4 octetos
    octetos = ip.split('.')
    if len(octetos) == 4:
        try:
            for byte in octetos:
                cont = 0
                # comprobar si los octetos estan formados por caracteres numericos
                if byte.isdecimal() == True:
                    # comprobar si cada uno de los octetos estan entre 0 y 255
                    if int(byte) >= 0 and int(byte) <= 255:
                        cont += 1
                    elif int(byte) < 0 or int(byte) > 255:
                        raise ValueError
                else:
                    raise TypeError 
            if cont == 4:
                return True
        except TypeError:
            print("los octetos han de ser numericos")
            return False
        except ValueError:
            print("los octetos no pueden ser menores que 0 o mayores que 255")
            return False
    else:
        print('La IP tiene que estar formada por 4 octetos')
        return False
    return True

def identificar_clase_ip(ip):
    '''Teniendo en cuenta los octetos de la IP informa de su clase (A, B o C)
    Args:
        ip (str): ip dada por el usuario
    Return:
        str: Si es una IP privada o pública. Si es privada informa de su clase
    '''
    octetos = ip.split('.')
    if int(octetos[0]) < 128:
        print("La ip es de clase A")
    elif int(octetos[0]) < 192:
        print("La ip es de clase B")
    elif int(octetos[0]) < 224:
        print("La ip es de clase C")
    elif int(octetos[0]) < 240:
        print("La ip es de clase D")
    else:
        print("La ip es de clase E")

def crear_lista_puertos(entrada):
    '''Crear una lista con los puertos dados por el usuario
    Args:
        entrada (str): puertos dados por el usuario separados por "."
    Return:
        list: lista con los puertos
    '''
    lista_puertos = []
    if entrada.count(':') > 0:
        puertos = entrada.split(':')
        for puerto in puertos:
            puerto = int(puerto)
            lista_puertos.append(puerto)
    else:
        puerto = int(entrada)
        lista_puertos.append(puerto)
    return lista_puertos

def realizar_ping(ip):
    '''Hace ping al ip dada por el usuario
    Args:
        ip (str): ip dada por el usuario
    Return:
        int: 0 si el host es está en la red o es accesible // 1 si no está en la red o es inaccesible
    '''
    if platform.system() == 'Windows':
        respuesta = subprocess.run(['ping', '-n', '1', ip], stdout=subprocess.DEVNULL)
    elif platform.system() == 'Linux':
        respuesta = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL)
    return respuesta.returncode

def escanear_puertos(ip, lista_puertos):
    '''comprueba los puertos abiertos. Si alguno de los puertos dados por el usuario está abierto se guardan en una lista.
    Args:
        ip (str): ip de la máquina
        lista_puertos (list): lista con los puertos
    Return:
        list: lista con los puertos abiertos
    '''
    puertos_abiertos = []
    for puerto in lista_puertos:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        respuesta = sock.connect_ex((ip, puerto))
        sock.close()
        if respuesta == 0:
            puertos_abiertos.append(puerto)
    return puertos_abiertos

def main():
    #? ENTRADA
    # borrar el terminal limpiando la basura de contenido
    borrar_consola()
    # verificar la version de python y su compatibilidad
    checkear_version_de_python()
    entrada = sys.argv
    # tomar la ip
    ip = entrada[1]
    #? PROCESO
    sistema_operativo="nombre y version del sistema operativo: "+platform.system()+" "+platform.release()
    print(sistema_operativo)
    if comprobar_formato_ip(ip) == True:
        # identificar la clase de ip
        identificar_clase_ip(ip)
        if (realizar_ping(ip)) == 0:
            ip_verificada="la ip "+str(ip)+" es accesible...\nel equipo esta presente"
            print(ip_verificada)
            # escanear los puertos
            try:
                lista_puertos = crear_lista_puertos(entrada[2])
                puertos_abiertos = escanear_puertos(ip, lista_puertos)
                puerto=len(puertos_abiertos)
                #? SALIDA 1: mostrar el mensaje de salida del puerto
                if puerto == 0:
                    puerto_verificado="el puerto "+str(puerto)+" no esta abierto\nlos servicios del puerto no existen"
                    print(puerto_verificado)
                else:
                    for puerto in puertos_abiertos:
                        servicio = socket.getservbyport(puerto)
                        puerto_verificado="el puerto "+str(puerto)+" esta abierto\nServicios del puerto: "+str(servicio)
                        print(puerto_verificado)
            except IndexError:
                print('los octetos de los puertos deben estar separados por ":"')
            except ValueError:
                print('los puertos solo deben estar formados por caracteres numericos')
        else:
            #? SALIDA 2: mostrar el mensaje de salida del puerto
            ip_verificada="la ip "+str(ip)+" no es accesible...\nel equipo no esta presente"
            print(ip_verificada)
    else:
        print('ip invalida, incorrecta o mal escrita')

if __name__ == '__main__':
    main()