import socket, sys
 
name = sys.argv[1] if len(sys.argv) > 1 else "www.python.org"

try:
    # ten may
    print(socket.gethostname())

    # IP thật của máy trong mạng LAN
    u = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM)
    u.connect(("8.8.8.8", 80))
    print(u.getsockname()[0])
    u.close()

    # IPv4
    print("IPv4 :", socket.gethostbyname(name))

    # thong tin
    for res in socket.getaddrinfo(
            name, 80,
            type=socket.SOCK_STREAM):
        fam, typ, _, _, addr = res
        print(fam.name, addr)

        results = socket.getaddrinfo(
        name, 80,
        socket.AF_UNSPEC,
        socket.SOCK_STREAM
    )
        print("So dong getaddrinfo:", len(results))

    # Tra nguoc IP -> ten
    ip = socket.gethostbyname(name)
    print("Tra nguoc:",
          socket.gethostbyaddr(ip)[0])

except socket.herror as e:
    print("Loi tra nguoc IP:", e)

#phan biet loi
except socket.gaierror as e:
    print("Khong phan giai :", e)

except OSError as e:
    print("Loi socket:", e)