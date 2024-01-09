# -*- codigo: utf-16 -*-

'''from netifaces import interfaces, ifaddresses, AF_INET

for ifaceName in interfaces():
    addresses = [
        i["addr"]
        for i in ifaddresses(ifaceName).setdefault(AF_INET, [{"addr": "No IP addr"}])
    ]
    print(" ".join(addresses))'''

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


print(extract_ip())