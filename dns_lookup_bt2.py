import socket
import sys

name = sys.argv[1] if len(sys.argv) > 1 else "www.python.org"

try:

    # IPv4
    ip = socket.gethostbyname(name)
    print("IPv4 :", ip)

    # getaddrinfo
    results = socket.getaddrinfo(
        name, 80,
        socket.AF_UNSPEC,
        socket.SOCK_STREAM
    )

    for res in results:
        fam, typ, _, _, addr = res
        print(fam.name, addr)

    # Dem tong so dong
    print("So dong getaddrinfo:", len(results))

    # Tra nguoc IP -> ten
    try:
        print("Tra nguoc:",
              socket.gethostbyaddr(ip)[0])
    except socket.herror as e:
        print("Loi tra nguoc IP:", e)

except socket.gaierror as e:
    print("Khong phan giai ten mien:", e)

except OSError as e:
    print("Loi socket:", e)