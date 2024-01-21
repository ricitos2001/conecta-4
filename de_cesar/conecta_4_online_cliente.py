import os
import sys
import socket
import random
import conecta_4_online_servidor

'''
#!ERRORES DEL JUEGO
1.) CUANDO SE DECLAREN LOS RESULTADOS DE LA PARTIDA
EL PROGRAMA DEBE ENVIAR EL MENSAJE DE VICTORIA DEL CLIENTE AL SERVIDOR
DE FORMA QUE LA PARTIDA TERMINE TANTO EN EL CLIENTE COMO EN EL SERVIDOR
2.) SI NO ESPERAS A QUE EL SERVIDOR RECIBA EL MENSAJE DEL CLIENTE
SE IMPRIMIRA EL PRIMER MENSAJE DEL SERVIDOR
POR LO QUE TENDREMOS QUE CERRAR LA CONEXION DEL CLIENTE
3.) TRAS REALIZAR UN TURNO EL JUEGO TE PREGUNTA SI QUIERES VOLVER A JUGAR
Y SI NO LE DICES QUE SI ANTES DE QUE EL SERVIDOR REALICE LA JUGADA 
EL SERVIDOR DEJA DE FUNCIONAR
#*IMPORTANTE: TENED EN CUENTA QUE EL SEGUNDO PROBLEMA HACE POSIBLE 
#*QUE EL CLIENTE RECIBA TODOS LOS MENSAJES DEL SERVIDOR
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
JUGADOR_1 = conecta_4_online_servidor
JUGADOR_2 = 2
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

def iniciar_cliente(jugador_actual, ejecucion):
    """
    Inicia el cliente para el juego de conecta 4 utilizando sockets UDP.

    Args:
        jugador_actual (str): El jugador actual que participa en el juego.
        ejecucion (bool): Indicador para controlar la ejecución del juego.

    Returns:
        None
    """
    # PRIMERA CONEXIÓN, BUSCAR QUIEN QUIERE JUGAR
    # Crear el socket --> IPv4 & UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Modo de difusión: recibira paquetes trasmiridos por los equipos de la red
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Enlaza el socket al puerto 37020 en cualquier dirección IP disponible
    client.bind(("", 37020))
    # Espera a recibir un mensaje del servidor
    mensaje_bytes, ip_servidor = client.recvfrom(1024)
    # Decodifica los bytes a una cadena
    mensaje_str = mensaje_bytes.decode('utf-8')
    if mensaje_str is None:
        print("No se pudo colocar la ficha en el servidor.")
        return
    else:
        # Imprime el mensaje en formato string
        print(f"Mensaje recibido!")
        tablero = crear_tablero(mensaje_str)
        # Envía una respuesta al servidor
        # Respuesta = f"{ip}"
        respuesta = enviar_movimiento_cliente(tablero, jugador_actual, ejecucion)
        client.sendto(respuesta.encode('utf-8'), ip_servidor)
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
    client.close()

#TODO \\FUNCION QUE REALIZA EL ENVIO DE LOS MOVIMIENTOS DEL CLIENTE//
#Funcion que envia los movimientos del cliente al servidor
def enviar_movimiento_cliente(tablero, jugador_actual, ejecucion):
    """
    Envía el movimiento del cliente al servidor y actualiza el estado del tablero.

    Args:
        tablero (list): Una lista bidimensional que representa el tablero del juego.
        jugador_actual (str): El jugador que realiza el movimiento.
        ejecucion (bool): Un indicador para controlar la ejecución del juego.

    Returns:
        str: La representación del tablero como cadena después de realizar el movimiento.
            Devuelve None si no se puede colocar la pieza en la columna especificada.
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

# Pasar el tablero a formato de string para que el cliente lo reciba
def tablero_to_string(tablero):
    """
    Convierte la representación del tablero (lista bidimensional) a una cadena de texto.

    Args:
        tablero (list): Una lista bidimensional que representa el tablero del juego.

    Returns:
        str: Una cadena que representa el tablero en un formato visual.
    """
    result = ""
    for fila in tablero:
        result += "|" + "|".join(fila) + "|\n"
    result += "+-" * len(tablero[0]) + "+\n"
    return result

# Crea el tablero a raiz del mensaje recibido por el servidor
def crear_tablero(mensaje_str):
    """
    Crea un tablero a partir de un mensaje codificado.

    Args:
        mensaje_str (str): Una cadena que representa el estado del tablero codificado.

    Returns:
        list: Una lista bidimensional que representa el tablero del juego.
    """
    # Divide el mensaje en líneas y extrae las filas del tablero
    lineas = mensaje_str.strip().split('\n')[0:-1]
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
    Imprime visualmente el estado actual del tablero.

    Args:
        tablero (list): Una lista bidimensional que representa el tablero del juego.

    Returns:
        None
    """
    # Imprime números de columnas
    print("|", end="")
    for f in range(1, len(tablero[0]) + 1):
        print(f, end="|")
    print("")
    # Datos
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
    # Pie
    print("+", end="")
    for f in range(1, len(tablero[0]) + 1):
        print("-", end="+")
    print("")

def obtener_tiradas_faltantes_en_columna(columna, tablero):
    """
    Obtiene la cantidad de tiradas disponibles en una columna específica del tablero.

    Args:
        columna (int): Índice de la columna en la que se desea contar las tiradas disponibles.
        tablero (list): Una lista bidimensional que representa el tablero del juego.

    Returns:
        int: La cantidad de tiradas disponibles en la columna especificada.
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
    Obtiene la cantidad total de tiradas disponibles en todas las columnas del tablero.

    Args:
        tablero (list): Una lista bidimensional que representa el tablero del juego.

    Returns:
        int: La cantidad total de tiradas disponibles en todas las columnas.
    """
    tiradas = 0
    for columna in range(len(tablero[0])):
        tiradas += obtener_tiradas_faltantes_en_columna(columna, tablero)
    return tiradas

def imprimir_tiradas_faltantes(tablero):
    """
    Imprime la cantidad total de tiradas disponibles en todas las columnas del tablero.

    Args:
        tablero (list): Una lista bidimensional que representa el tablero del juego.

    Returns:
        None
    """
    print("Tiradas faltantes: " + str(obtener_tiradas_faltantes(tablero)))

#TODO \\FUNCIONES PARA REALIZAR LA JUGADA E INSERTAR LA FICHA EN EL TABLERO//
def realizar_jugada(tablero):
    """
    Solicita al usuario que ingrese la columna para colocar una pieza en el tablero.

    Args:
        tablero (list): Una lista bidimensional que representa el tablero del juego.

    Returns:
        int: El índice de la columna donde se desea colocar la pieza.
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
    Imprime información sobre el turno actual y solicita al usuario que realice una jugada.

    Args:
        turno (str): El jugador actual que tiene el turno.
        tablero (list): Una lista bidimensional que representa el tablero del juego.

    Returns:
        int: El índice de la columna donde se desea colocar la pieza, ajustado para la indexación de Python.
    """
    print(f"Jugador 1: {SIMBOLO_JUGADOR_1} | Jugador 2: {SIMBOLO_JUGADOR_2}")
    if turno == JUGADOR_1:
        print(f"Turno del jugador 1 ({SIMBOLO_JUGADOR_1})")
    else:
        print(f"Turno del jugador 2 ({SIMBOLO_JUGADOR_2})")
    return realizar_jugada(tablero)

def obtener_fila_valida_en_columna(columna, tablero):
    """
    Obtiene la fila más baja en una columna específica donde se puede colocar una pieza.

    Args:
        columna (int): Índice de la columna en la que se desea encontrar una fila válida.
        tablero (list): Una lista bidimensional que representa el tablero del juego.

    Returns:
        int: El índice de la fila más baja donde se puede colocar una pieza, o -1 si la columna está llena.
    """
    indice = len(tablero) - 1
    while indice >= 0:
        if tablero[indice][columna] == ESPACIO_VACIO:
            return indice
        indice -= 1
    return -1

def colocar_pieza(columna, jugador, tablero):
    """
    Coloca la pieza de un jugador en una columna específica del tablero.

    Args:
        columna (int): Índice de la columna en la que se desea colocar la pieza.
        jugador (str): El jugador actual que realiza la jugada.
        tablero (list): Una lista bidimensional que representa el tablero del juego.

    Returns:
        bool: True si la pieza se colocó con éxito, False si la columna está llena.
    """
    color = SIMBOLO_JUGADOR_2
    if jugador == JUGADOR_1:
        color = SIMBOLO_JUGADOR_1
    fila = obtener_fila_valida_en_columna(columna, tablero)
    if fila == -1:
        return False
    tablero[fila][columna] = color
    return True

#TODO \\FUNCIONES PARA VERIFICAR SI HAY UN EMPATE O UN GANADOR Y UN PERDEDOR// 
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
    fila (int): Índice de la fila inicial.
    columna (int): Índice de la columna inicial.
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
    fila (int): Índice de la fila inicial.
    columna (int): Índice de la columna inicial.
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
    fila (int): Índice de la fila inicial.
    columna (int): Índice de la columna inicial.
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
    fila (int): Índice de la fila inicial.
    columna (int): Índice de la columna inicial.
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
    fila (int): Índice de la fila inicial.
    columna (int): Índice de la columna inicial.
    color (str): Color de la pieza a contar.
    tablero (list): Una lista bidimensional que representa el tablero del juego.

Returns:
    int: El conteo total de piezas consecutivas en todas las direcciones.
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
Obtiene el color de la pieza asociado a un jugador específico.

Args:
    jugador (str): El identificador del jugador (JUGADOR_1 o JUGADOR_2).

Returns:
    str: El símbolo de la pieza asociado al jugador.
"""
    color = SIMBOLO_JUGADOR_1
    if jugador == JUGADOR_2:
        color = SIMBOLO_JUGADOR_2
    return color

def comprobar_ganador(jugador, tablero):
    """
Comprueba si un jugador ha ganado en el tablero.

Args:
    jugador (str): El identificador del jugador (JUGADOR_1 o JUGADOR_2).
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
Felicita al jugador que ha ganado y notifica al otro jugador.

Args:
    jugador_actual (str): El identificador del jugador que ha ganado (JUGADOR_1 o JUGADOR_2).

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
Indica que el juego ha terminado en empate.

Returns:
    None
"""
    print( COLOR_NARANJA + "empate...\n"+ COLOR_MAGENTA + "A MIMIR! 😴😴😴😴😴" + RESETEO_COLOR + "\n")

#TODO \\FUNCION PARA ELEGIR SI QUIERES VOLVER A JUGAR//
def volver_a_jugar():
    """
Pregunta al usuario si desea volver a jugar.

Returns:
    bool: True si el usuario desea volver a jugar, False si no.
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
                jugador_actual = JUGADOR_2
                iniciar_cliente(jugador_actual, ejecucion)
                if not volver_a_jugar():
                    ejecucion=False
        elif eleccion == "2":
            print("adios")
            os.system("pause")
            borrar_consola()
            ejecucion=False

if __name__=="__main__":
    iniciar_partida()