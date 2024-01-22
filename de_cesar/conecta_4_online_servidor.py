import os
import sys
import time
import socket
import random
import conecta_4_online_cliente

'''
#!ERRORES DEL JUEGO
1.) CUANDO SE DECLAREN LOS RESULTADOS DE LA PARTIDA
EL PROGRAMA DEBE ENVIAR EL MENSAJE DE VICTORIA DEL SERVIDOR AL CLIENTE
DE FORMA QUE LA PARTIDA TERMINE TANTO EN EL CLIENTE COMO EN EL SERVIDOR
#*IMPORTANTE: CONSEGUI ARREGLAR UNA PARTE DEL PROBLEMA YA QUE AHORA SI TERMINA LA PARTIDA
#*PERO EL MENSAJE SOLO APARECE EN EL SERVIDOR
'''

#? SI CONSEGUIS SOLUCIONAR ESTOS PROBLEMAS PODRE IMPLEMENTAR EL MODO MAQUINA_VS_MAQUINA Y ACABAR CON ESTO

#TODO \\CONSTANTES//
COLOR_VERDE = "\33[32m"
COLOR_ROJO = "\33[31m"
COLOR_CIAN = "\033[36m"
COLOR_AMARILLO = "\033[1;93m"
COLOR_NARANJA = '\33[33m'
COLOR_MAGENTA = "\033[1;035m"
COLOR_GRIS = "\033[1;90m"
COLOR_BLANCO = "\033[1;39m"
RESETEO_COLOR = '\033[0m'
JUGADOR_1 = 1
JUGADOR_2 = conecta_4_online_cliente
ESPACIO_VACIO = " "
SIMBOLO_JUGADOR_1 = "x"
SIMBOLO_JUGADOR_2 ="o"
CONECTA = 4


#TODO \\FUNCION QUE COMPRUEBA SI LA VERSION DE PYTHON DE TU ORDENADOR ES COMPATIBLE//
def checkear_version_de_python():
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

#TODO \\FUNCION QUE LIMPIA EL TERMINAL PARA QUE SE VEA MAS CLARO//
def borrar_consola():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

#TODO \\FUNCIONES Y ARGUMENTOS QUE INICIAN LA CONEXION DEL CLIENTE//
# obtener ip privada del ordenador
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

def iniciar_servidor(jugador_actual, ejecucion):
    # PRIMERA CONEXIÓN, BUSCAR QUIEN QUIERE JUGAR
    # crear el socket --> IPv4 & UDP
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Modo de difusión: los paquetes se transmitirán a todos los equipos de la red
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Set a timeout so the socket does not block #indefinitely when trying to receive data.
    server.settimeout(0.2)
    # mensaje que enviará el servidor con su dirección IP
    # mensaje = f"{ip}"
    #TODO: A PARTIR DE AQUI ENTRA LA LOGICA DEL JUEGO
    tablero = crear_tablero_inicial()
    mensaje = enviar_primer_movimiento_servidor(tablero, jugador_actual, ejecucion)
    mensaje_encode = mensaje.encode('utf-8')
    print("\nMensaje enviado!")
    while ejecucion != False:
        respuesta_decode = ""
        while (respuesta_decode == ""):
            server.sendto(mensaje_encode, ('<broadcast>', 37020)) # puerto: 37020
            try:
                # Esperar la respuesta
                respuesta, ip_cliente = server.recvfrom(1024)
                # Decodifica los bytes a una cadena
                respuesta_decode = (respuesta.decode('utf-8'))
            except socket.timeout:
                for i in range(4):
                    mensaje = "Esperando respuesta" + "." * i
                    print(f'\r{mensaje}', end='', flush=True)
                    time.sleep(0.5)
                # Reiniciar el mensaje al llegar al final
                print('\r' + ' ' * len(mensaje), end='', flush=True)
        if respuesta_decode is None:
            print("No se pudo colocar la ficha en el servidor.")
            return
        else:
            # Imprime el mensaje en formato string
            print(f"\nRespuesta recibida!")
        # Envía una respuesta al servidor
        # respuesta = f"{ip}"
        tablero=crear_tablero(respuesta_decode)
        respuesta = enviar_movimiento_servidor(tablero, jugador_actual, ejecucion)
        server.sendto(respuesta.encode('utf-8'), ip_cliente)
        
        
        ha_ganado = comprobar_ganador(jugador_actual, tablero)
        if ha_ganado:
            imprimir_tablero(tablero)
            felicitar_jugador(jugador_actual)
            ejecucion = False
        elif es_empate(tablero):
            imprimir_tablero(tablero)
            indicar_empate()
            ejecucion = False
    # Cerrar el socket después de enviar y recibir
    server.close()

#TODO \\FUNCION QUE REALIZA EL ENVIO DE LOS MOVIMIENTOS DEL SERVIDOR//
# funcion que envia el primer movimiento del servidor
def enviar_primer_movimiento_servidor(tablero, jugador_actual, ejecucion):
    while ejecucion:
        imprimir_tablero_inicial(tablero)
        imprimir_tiradas_faltantes(tablero)
        columna = imprimir_y_solicitar_turno(jugador_actual, tablero)
        pieza_colocada = colocar_pieza(columna, jugador_actual, tablero)
        if not pieza_colocada:
            print("No se puede colocar en esa columna")
            return None
        return conversion_de_tablero_a_string(tablero)

#funcion que envia los movimientos del servidor al cliente
def enviar_movimiento_servidor(tablero, jugador_actual, ejecucion):
    while ejecucion:
        imprimir_tablero(tablero)
        imprimir_tiradas_faltantes(tablero)
        columna = imprimir_y_solicitar_turno(jugador_actual, tablero)
        pieza_colocada = colocar_pieza(columna, jugador_actual, tablero)
        if not pieza_colocada:
            print("No se puede colocar en esa columna")
            return None
        return conversion_de_tablero_a_string(tablero)

#TODO \\FUNCION QUE CREA EL TABLERO VACIO//
# crea el tablero vacio o tablero inicial
def crear_tablero_inicial():
    tablero = []
    filas=6
    columnas=7
    for fila in range(filas):
        tablero.append([])
        for _ in range(columnas):
            tablero[fila].append(ESPACIO_VACIO)
    return tablero

# imprime el tablero vacio o tablero inicial
def imprimir_tablero_inicial(tablero):
    print("|", end="")
    for f in range(1, len(tablero[0]) + 1):
        print(f, end="|")
    print("")
    for fila in tablero:
        print("|", end="")
        for valor in fila:
            color_terminal = COLOR_VERDE
            if valor == SIMBOLO_JUGADOR_2:
                color_terminal = COLOR_ROJO
            print(color_terminal + valor, end="")
            print(RESETEO_COLOR, end="")
            print("|", end="")
        print("")
    print("+", end="")
    for f in range(1, len(tablero[0]) + 1):
        print("-", end="+")
    print("")

# crea el tablero a raiz del mensaje recibido por el cliente
def crear_tablero(respuesta_decode):
    # Divide el mensaje en líneas y extrae las filas del tablero
    lineas = respuesta_decode.strip().split('\n')[0:-1]
    # Inicializa el tablero con espacios en blanco
    tablero = [[' ' for _ in range(7)] for _ in range(6)]
    # Llena el tablero con las fichas correspondientes
    for i, linea in enumerate(lineas):
        for j, caracter in enumerate(linea[1::2]):
            tablero[i][j] = caracter
    return tablero

# imprime el tablero a raiz del mensaje recibido
def imprimir_tablero(tablero):
    print("|", end="")
    for f in range(1, len(tablero[0]) + 1):
        print(f, end="|")
    print("")
    for fila in tablero:
        print("|", end="")
        for valor in fila:
            color_terminal = COLOR_VERDE
            if valor == SIMBOLO_JUGADOR_2:
                color_terminal = COLOR_ROJO
            print(color_terminal + valor, end="")
            print(RESETEO_COLOR, end="")
            print("|", end="")
        print("")
    print("+", end="")
    for f in range(1, len(tablero[0]) + 1):
        print("-", end="+")
    print("")

# pasar el tablero a formato de string 
# para que el cliente lo reciba correctamente como mensaje
def conversion_de_tablero_a_string(tablero):
    resultado = ""
    for fila in tablero:
        resultado += "|" + "|".join(fila) + "|\n"
    resultado += "+-" * len(tablero[0]) + "+\n"
    return resultado

def obtener_tiradas_faltantes_en_columna(columna, tablero):
    indice = len(tablero) - 1
    tiradas = 0
    while indice >= 0:
        if tablero[indice][columna] == ESPACIO_VACIO:
            tiradas += 1
        indice -= 1
    return tiradas

def obtener_tiradas_faltantes(tablero):
    tiradas = 0
    for columna in range(len(tablero[0])):
        tiradas += obtener_tiradas_faltantes_en_columna(columna, tablero)
    return tiradas

def imprimir_tiradas_faltantes(tablero):
    print("Tiradas faltantes: " + str(obtener_tiradas_faltantes(tablero)))

#TODO \\FUNCIONES PARA REALIZAR LA JUGADA E INSERTAR LA FICHA EN EL TABLERO//
def realizar_jugada(tablero):
    while True:
        try:
            jugada = int(input("Ingresa el numero de la columna para colocar la pieza: "))    
            '''jugada = random.randint(1,7)'''
            if jugada <= 0 or jugada > len(tablero[0]):
                print("Columna no válida")
            elif tablero[0][jugada - 1] != ESPACIO_VACIO:
                print("Esa columna ya está llena")
            else:
                return jugada - 1
        except ValueError:
            continue

def imprimir_y_solicitar_turno(turno, tablero):
    print(f"Jugador 1: {SIMBOLO_JUGADOR_1} | Jugador 2: {SIMBOLO_JUGADOR_2}")
    if turno == JUGADOR_1:
        print(f"Turno del jugador 1 ({SIMBOLO_JUGADOR_1})")
    else:
        print(f"Turno del jugador 2 ({SIMBOLO_JUGADOR_2})")
    return realizar_jugada(tablero)

def obtener_fila_valida_en_columna(columna, tablero):
    indice = len(tablero) - 1
    while indice >= 0:
        if tablero[indice][columna] == ESPACIO_VACIO:
            return indice
        indice -= 1
    return -1

def colocar_pieza(columna, jugador, tablero):
    """
    Coloca una pieza en el tablero. La columna debe
    comenzar en 0
    """
    color = SIMBOLO_JUGADOR_1
    if jugador == JUGADOR_2:
        color = SIMBOLO_JUGADOR_2
    fila = obtener_fila_valida_en_columna(columna, tablero)
    if fila == -1:
        return False
    tablero[fila][columna] = color
    return True

#TODO \\FUNCIONES PARA VERIFICAR SI HAY UN EMPATE O GANADOR Y UN PERDEDOR// 
def obtener_conteo_vertical(fila, columna, color, tablero):
    contador = 0
    for i in range(fila, -1, -1):
        if contador >= CONECTA:
            return contador
        if tablero[i][columna] == color:
            contador += 1
        else:
            contador = 0
    return contador

def obtener_conteo_horizontal(fila, columna, color, tablero):
    contador = 0
    for i in range(columna, -1, -1):
        if contador >= CONECTA:
            return contador
        if tablero[fila][i] == color:
            contador += 1
        else:
            contador = 0
    return contador

def obtener_conteo_diagonal(fila, columna, color, tablero):
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while (numero_fila >= 0 and numero_columna >= 0) and (numero_fila >= 0 and numero_columna < len(tablero[0])):
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila -= 1
        numero_columna -= 1
    return contador

def obtener_conteo(fila, columna, color, tablero):
    direcciones = ['vertical','horizontal','diagonal']
    for direccion in direcciones:
        funcion = globals()['obtener_conteo_' + direccion]
        conteo = funcion(fila, columna, color, tablero)
        if conteo >= CONECTA:
            return conteo
    return 0

def obtener_color_de_jugador(jugador):
    color = SIMBOLO_JUGADOR_1
    if jugador == JUGADOR_2:
        color = SIMBOLO_JUGADOR_2
    return color

def comprobar_ganador(jugador, tablero):
    color = obtener_color_de_jugador(jugador)
    for f, fila in enumerate(tablero):
        for c, _ in enumerate(fila):
            conteo = obtener_conteo(f, c, color, tablero)
            if conteo >= CONECTA:
                return True
    return False

def felicitar_jugador(jugador_actual):
    if jugador_actual == JUGADOR_1:
        mensaje=(COLOR_CIAN + "henorabuena! Jugador 1  has ganado 🏆" + RESETEO_COLOR) + "\n" + (COLOR_AMARILLO +  "Jugador 2 has perdido! pipipi pipipi 😱" + RESETEO_COLOR)
        print(mensaje)
    elif jugador_actual == JUGADOR_2:
        mensaje=(COLOR_CIAN + "henorabuena! Jugador 2  has ganado 🏆" + RESETEO_COLOR) + "\n" + (COLOR_AMARILLO +  "Jugador 1 has perdido! pipipi pipipi 😱" + RESETEO_COLOR)
        print(mensaje)

def es_empate(tablero):
    for columna in range(len(tablero[0])):
        if obtener_fila_valida_en_columna(columna, tablero) != -1:
            return False
    return True

def indicar_empate():
    print(COLOR_NARANJA + "empate...\n"+ COLOR_MAGENTA + "A MIMIR! 😴😴😴😴😴" + RESETEO_COLOR)

#TODO \\FUNCION PARA ELEGIR SI QUIERES VOLVER A JUGAR//
def volver_a_jugar():
    while True:
        eleccion = input(COLOR_GRIS + "¿Quieres volver a jugar? [s/n]: " + RESETEO_COLOR).lower()
        if eleccion == "s":
            borrar_consola()
            return True
        elif eleccion == "n":
            print(COLOR_BLANCO + "adios" + RESETEO_COLOR)
            os.system("pause")
            borrar_consola()
            return False

#TODO \\FUNCION QUE EJECUTARA EL PROGRAMA EN PYTHON//
def iniciar_partida():
    borrar_consola()
    checkear_version_de_python()
    ejecucion=True
    while ejecucion:
        eleccion = input("1- Iniciar partida\n2- Salir del juego\nElige: ")
        if eleccion == "1":
            ejecucion=True
            while ejecucion:
                jugador_actual = JUGADOR_1
                iniciar_servidor(jugador_actual, ejecucion)
                if not volver_a_jugar():
                    ejecucion=False
        elif eleccion == "2":
            print("adios")
            os.system("pause")
            borrar_consola()
            ejecucion=False

if __name__=="__main__":
    iniciar_partida()