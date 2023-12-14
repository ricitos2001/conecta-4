import sys
import subprocess
import platform

# esto es un ejemplo del envio de paquetes de red desde un router a otro
if __name__ == "__main__":
    sys_argv_length=len(sys.argv)
    octetos =sys.argv[1].split(".")
    try:
        print("nombre y version del sistema operativo: ", platform.system()+" "+platform.release())
        if platform.system() == "Windows":
            HOST_UP = True if subprocess.run("ping -n 1 " + sys.argv[1]) == 0 else False
        elif platform.system() == "Linux":
            HOST_UP = True if subprocess.run("ping -c 1 " + sys.argv[1]) == 0 else False
        if len(octetos) == 4:
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
            for i in octetos:
                if i.isnumeric():
                    if int(i) >= 0 or int(i) <= 255:
                        salida = subprocess.run(["ping", sys.argv[1]], stdout=subprocess.DEVNULL)
                        if salida.returncode == 1:
                            print(sys.argv[1], "el equipo no esta presente")
                        else:
                            print(sys.argv[1], "el equipo esta presente")
                    elif int(i) < 0 or int(i) > 255:
                        raise ValueError
                elif not i.isnumeric():
                    raise TypeError
    except TypeError:
        print("los octetos han de ser numericos")
    except ValueError:
        print("los octetos no pueden ser menores que 0 o mayores que 255")
