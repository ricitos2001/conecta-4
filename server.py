import socket


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(("10.255.255.255", 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        st.close()
    return IP


HOST = extract_ip() #mi dirección IP
PORT = 65123       # >1023 son puertos libres(usar como puerto de escucha cualquiera a partir de este)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s: #s es server. Aqui se establece puerta de entrada y salida(IP y puerto)
    s.bind((HOST,PORT)) #asocia el socket con elemento físico, es decir, la tajerta red
    s.listen() #escucha conexiones entrantes
    conn, addr =s.accept() #el sistema se queda esperando, se detiene el script hasta que haya conexión. Se le asigna la conexion y dirección que entra

    with conn:#conexion establecida
        print(f"Conectado a (addr): ")#especifica la ip al que conectamos
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)