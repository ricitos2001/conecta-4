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
    """
    Comprueba si la versión de Python instalada es compatible con la aplicación.

    Args:
        No recibe argumentos directos, utiliza información de sys.version_info.

    Prints:
        Muestra un mensaje indicando si la versión de Python instalada es compatible o no.
        Si no es compatible, proporciona información sobre las versiones requeridas.

    Returns:
        No devuelve ningún valor directamente, pero puede imprimir mensajes en la consola.
    """
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
    """
    Borra la pantalla de la consola, proporcionando una interfaz limpia.

    Args:
        No recibe argumentos directos, utiliza información de os.name.

    Returns:
        No devuelve ningún valor directamente, pero realiza la acción de borrar la consola.
    """
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
    """
Inicia el servidor para un juego de conecta 4 utilizando sockets UDP.

Args:
    jugador_actual (str): El jugador actual que participa en el juego.
    ejecucion (bool): Un indicador para controlar la ejecución del juego.

Returns:
    None
"""
    # PRIMERA CONEXIÓN, BUSCAR QUIEN QUIERE JUGAR
    # Crear el socket --> IPv4 & UDP
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Modo de difusión: los paquetes se transmitirán a todos los equipos de la red
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Establezca un tiempo de espera para que el socket no se bloquee #indefinidamente al intentar recibir datos.
    server.settimeout(0.2)
    # Mensaje que enviará el servidor con su dirección IP
    # Mensaje = f"{ip}"
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
        # Respuesta = f"{ip}"
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
# Funcion que envia el primer movimiento del servidor
def enviar_primer_movimiento_servidor(tablero, jugador_actual, ejecucion):
    """
Envía el primer movimiento del servidor al cliente.

Args:
    tablero (list): Una lista bidimensional que representa el tablero del juego.
    jugador_actual (str): El jugador actual que participa en el juego.
    ejecucion (bool): Un indicador para controlar la ejecución del juego.

Returns:
    str: La representación en cadena del tablero después del primer movimiento.
"""
    while ejecucion:
        imprimir_tablero_inicial(tablero)
        imprimir_tiradas_faltantes(tablero)
        columna = imprimir_y_solicitar_turno(jugador_actual, tablero)
        pieza_colocada = colocar_pieza(columna, jugador_actual, tablero)
        if not pieza_colocada:
            print("No se puede colocar en esa columna")
            return None
        return tablero_to_string(tablero)

#Funcion que envia los movimientos del servidor al cliente
def enviar_movimiento_servidor(tablero, jugador_actual, ejecucion):
    """
Envía un movimiento del servidor al cliente.

Args:
    tablero (list): Una lista bidimensional que representa el tablero del juego.
    jugador_actual (str): El jugador actual que participa en el juego.
    ejecucion (bool): Un indicador para controlar la ejecución del juego.

Returns:
    str: La representación en cadena del tablero después del movimiento.
"""
    while ejecucion:
        imprimir_tablero(tablero)
        imprimir_tiradas_faltantes(tablero)
        columna = imprimir_y_solicitar_turno(jugador_actual, tablero)
        pieza_colocada = colocar_pieza(columna, jugador_actual, tablero)
        if not pieza_colocada:
            print("No se puede colocar en esa columna")
            return None
        return tablero_to_string(tablero)

#TODO \\FUNCION QUE CREA EL TABLERO VACIO//
# crea el tablero vacio o tablero inicial
def crear_tablero_inicial():
    """
Crea y devuelve un tablero inicial vacío para el juego de Conecta 4.

Returns:
    list: Una lista bidimensional que representa el tablero del juego.
"""
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
    """
Imprime el tablero inicial del juego de Conecta 4.

Args:
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    None
"""
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

# Crea el tablero a raiz del mensaje recibido por el cliente
def crear_tablero(respuesta_decode):
    """
Crea y devuelve un tablero a partir de la respuesta decodificada del servidor.

Args:
    respuesta_decode (str): La respuesta del servidor decodificada que contiene la representación del tablero.

Returns:
    list: Una lista bidimensional que representa el tablero del juego.
"""
    # Divide el mensaje en líneas y extrae las filas del tablero
    lineas = respuesta_decode.strip().split('\n')[0:-1]
    # Inicializa el tablero con espacios en blanco
    tablero = [[' ' for _ in range(7)] for _ in range(6)]
    # Llena el tablero con las fichas correspondientes
    for i, linea in enumerate(lineas):
        for j, caracter in enumerate(linea[1::2]):
            tablero[i][j] = caracter
    return tablero

# Imprime el tablero a raiz del mensaje recibido
def imprimir_tablero(tablero):
    """
Imprime el tablero del juego de Conecta 4.

Args:
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    None
"""
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
def tablero_to_string(tablero):
    """
Convierte el tablero en una cadena de texto.

Args:
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    str: Una cadena de texto que representa el tablero.
"""
    result = ""
    for fila in tablero:
        result += "|" + "|".join(fila) + "|\n"
    result += "+-" * len(tablero[0]) + "+\n"
    return result

def obtener_tiradas_faltantes_en_columna(columna, tablero):
    """
Obtiene la cantidad de tiradas faltantes en una columna específica.

Args:
    columna (int): Índice de la columna.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad de tiradas faltantes en la columna.
"""
    indice = len(tablero) - 1
    tiradas = 0
    while indice >= 0:
        if tablero[indice][columna] == ESPACIO_VACIO:
            tiradas += 1
        indice -= 1
    return tiradas

def obtener_tiradas_faltantes(tablero):
    """
Obtiene la cantidad total de tiradas faltantes en todo el tablero.

Args:
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad total de tiradas faltantes en el tablero.
"""
    tiradas = 0
    for columna in range(len(tablero[0])):
        tiradas += obtener_tiradas_faltantes_en_columna(columna, tablero)
    return tiradas

def imprimir_tiradas_faltantes(tablero):
    """
Imprime la cantidad total de tiradas faltantes en todo el tablero.

Args:
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    None
"""
    print("Tiradas faltantes: " + str(obtener_tiradas_faltantes(tablero)))

#TODO \\FUNCIONES PARA REALIZAR LA JUGADA E INSERTAR LA FICHA EN EL TABLERO//
def realizar_jugada(tablero):
    """
Solicita al jugador ingresar el número de la columna para colocar la pieza en el tablero.

Args:
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La columna seleccionada por el jugador (índice basado en 0).
"""
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
    """
Imprime información sobre el turno actual y solicita al jugador realizar una jugada.

Args:
    turno (str): Indica el jugador actual (JUGADOR_1 o JUGADOR_2).
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La columna seleccionada por el jugador (índice basado en 0).
"""
    print(f"Jugador 1: {SIMBOLO_JUGADOR_1} | Jugador 2: {SIMBOLO_JUGADOR_2}")
    if turno == JUGADOR_1:
        print(f"Turno del jugador 1 ({SIMBOLO_JUGADOR_1})")
    else:
        print(f"Turno del jugador 2 ({SIMBOLO_JUGADOR_2})")
    return realizar_jugada(tablero)

def obtener_fila_valida_en_columna(columna, tablero):
    """
Obtiene la fila válida más baja en la columna especificada del tablero.

Args:
    columna (int): Índice de la columna en la que se desea obtener la fila válida.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: El índice de la fila válida más baja en la columna. Devuelve -1 si la columna está llena.
"""
    indice = len(tablero) - 1
    while indice >= 0:
        if tablero[indice][columna] == ESPACIO_VACIO:
            return indice
        indice -= 1
    return -1

def colocar_pieza(columna, jugador, tablero):
    """
Coloca la pieza del jugador en la columna especificada del tablero.

Args:
    columna (int): Índice de la columna en la que se desea colocar la pieza.
    jugador (str): Jugador actual que coloca la pieza (JUGADOR_1 o JUGADOR_2).
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    bool: True si la pieza se coloca con éxito, False si la columna está llena.
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
def obtener_conteo_arriba(fila, columna, color, tablero):
    """
Obtiene el conteo de piezas consecutivas hacia arriba desde una posición específica.

Args:
    fila (int): Índice de la fila inicial.
    columna (int): Índice de la columna.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad de piezas consecutivas hacia arriba.
"""
    contador = 0
    for i in range(fila, -1, -1):
        if contador >= CONECTA:
            return contador
        if contador >= CONECTA:
            return contador
        if tablero[i][columna] == color:
            contador += 1
        else:
            contador = 0
    return contador

def obtener_conteo_abajo(fila, columna, color, tablero):
    """
Obtiene el conteo de piezas consecutivas hacia abajo desde una posición específica.

Args:
    fila (int): Índice de la fila inicial.
    columna (int): Índice de la columna.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad de piezas consecutivas hacia abajo.
"""
    fin_filas = len(tablero)
    contador = 0
    for i in range(fila, fin_filas):
        if contador >= CONECTA:
            return contador
        if tablero[i][columna] == color:
            contador += 1
        else:
            contador = 0
    return contador

def obtener_conteo_izquierda(fila, columna, color, tablero):
    """
Obtiene el conteo de piezas consecutivas hacia la izquierda desde una posición específica.

Args:
    fila (int): Índice de la fila.
    columna (int): Índice de la columna inicial.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad de piezas consecutivas hacia la izquierda.
"""
    contador = 0
    for i in range(columna, -1, -1):
        if contador >= CONECTA:
            return contador
        if tablero[fila][i] == color:
            contador += 1
        else:
            contador = 0
    return contador

def obtener_conteo_derecha(fila, columna, color, tablero):
    """
Obtiene el conteo de piezas consecutivas hacia la derecha desde una posición específica.

Args:
    fila (int): Índice de la fila.
    columna (int): Índice de la columna inicial.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad de piezas consecutivas hacia la derecha.
"""
    fin_columnas = len(tablero[0])
    contador = 0
    for i in range(columna, fin_columnas):
        if contador >= CONECTA:
            return contador
        if tablero[fila][i] == color:
            contador += 1
        else:
            contador = 0
    return contador

def obtener_conteo_arriba_izquierda(fila, columna, color, tablero):
    """
Obtiene el conteo de piezas consecutivas en la diagonal superior izquierda desde una posición específica.

Args:
    fila (int): Índice de la fila.
    columna (int): Índice de la columna.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad de piezas consecutivas en la diagonal superior izquierda.
"""
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila >= 0 and numero_columna >= 0:
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila -= 1
        numero_columna -= 1
    return contador

def obtener_conteo_arriba_derecha(fila, columna, color, tablero):
    """
Obtiene el conteo de piezas consecutivas en la diagonal superior derecha desde una posición específica.

Args:
    fila (int): Índice de la fila.
    columna (int): Índice de la columna.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad de piezas consecutivas en la diagonal superior derecha.
"""
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila >= 0 and numero_columna < len(tablero[0]):
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila -= 1
        numero_columna += 1
    return contador

def obtener_conteo_abajo_izquierda(fila, columna, color, tablero):
    """
Obtiene el conteo de piezas consecutivas en la diagonal inferior izquierda desde una posición específica.

Args:
    fila (int): Índice de la fila.
    columna (int): Índice de la columna.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad de piezas consecutivas en la diagonal inferior izquierda.
"""
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila < len(tablero) and numero_columna >= 0:
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila += 1
        numero_columna -= 1
    return contador

def obtener_conteo_abajo_derecha(fila, columna, color, tablero):
    """
Obtiene el conteo de piezas consecutivas en la diagonal inferior derecha desde una posición específica.

Args:
    fila (int): Índice de la fila.
    columna (int): Índice de la columna.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad de piezas consecutivas en la diagonal inferior derecha.
"""
    contador = 0
    numero_fila = fila
    numero_columna = columna
    while numero_fila < len(tablero) and numero_columna < len(tablero[0]):
        if contador >= CONECTA:
            return contador
        if tablero[numero_fila][numero_columna] == color:
            contador += 1
        else:
            contador = 0
        numero_fila += 1
        numero_columna += 1
    return contador

def obtener_conteo(fila, columna, color, tablero):
    """
Obtiene el conteo total de piezas consecutivas en todas las direcciones desde una posición específica.

Args:
    fila (int): Índice de la fila.
    columna (int): Índice de la columna.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: La cantidad total de piezas consecutivas en todas las direcciones.
"""
    direcciones = ['arriba','abajo','izquierda','derecha','arriba_izquierda','arriba_derecha','abajo_izquierda','abajo_derecha']
    for direccion in direcciones:
        funcion = globals()['obtener_conteo_' + direccion]
        conteo = funcion(fila, columna, color, tablero)
        if conteo >= CONECTA:
            return conteo
    return 0

def obtener_color_de_jugador(jugador):
    """
Obtiene el color de la pieza correspondiente a un jugador.

Args:
    jugador (str): Identificador del jugador.

Returns:
    str: Símbolo que representa el color de la pieza del jugador.
"""
    color = SIMBOLO_JUGADOR_1
    if jugador == JUGADOR_2:
        color = SIMBOLO_JUGADOR_2
    return color

def comprobar_ganador(jugador, tablero):
    """
Verifica si un jugador ha ganado el juego.

Args:
    jugador (str): El jugador que se está verificando.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    bool: True si el jugador ha ganado, False en caso contrario.
"""
    color = obtener_color_de_jugador(jugador)
    for f, fila in enumerate(tablero):
        for c, _ in enumerate(fila):
            conteo = obtener_conteo(f, c, color, tablero)
            if conteo >= CONECTA:
                return True
    return False

def felicitar_jugador(jugador_actual):
    """
Felicita al jugador que ha ganado y muestra un mensaje personalizado.

Args:
    jugador_actual (str): El jugador que ha ganado.

Returns:
    None
"""
    if jugador_actual == JUGADOR_1:
        mensaje=(COLOR_CIAN + "enhorabuena! Jugador 1  has ganado 🏆" + RESETEO_COLOR) + "\n" + (COLOR_AMARILLO +  "Jugador 2 has perdido! pipipi pipipi 😱" + RESETEO_COLOR)
        print(mensaje)
    elif jugador_actual == JUGADOR_2:
        mensaje=(COLOR_CIAN + "enhorabuena! Jugador 2  has ganado 🏆" + RESETEO_COLOR) + "\n" + (COLOR_AMARILLO +  "Jugador 1 has perdido! pipipi pipipi 😱" + RESETEO_COLOR)
        print(mensaje)

def es_empate(tablero):
    """
Verifica si el juego ha terminado en empate.

Args:
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    bool: True si el juego ha terminado en empate, False en caso contrario.
"""
    for columna in range(len(tablero[0])):
        if obtener_fila_valida_en_columna(columna, tablero) != -1:
            return False
    return True

def indicar_empate():
    """
Imprime un mensaje indicando que el juego ha terminado en empate.
"""
    print( COLOR_NARANJA + "empate...\n"+ COLOR_MAGENTA + "A MIMIR! 😴😴😴😴😴" + RESETEO_COLOR + "\n")

#TODO \\FUNCION PARA ELEGIR SI QUIERES VOLVER A JUGAR//
def volver_a_jugar():
    """
Solicita al usuario que decida si quiere volver a jugar o salir del programa.

Returns:
    bool: True si el usuario elige volver a jugar, False si elige salir.
"""
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
    """
Inicia la partida y permite al jugador decidir si jugar o salir del juego.

Returns:
    None
"""
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