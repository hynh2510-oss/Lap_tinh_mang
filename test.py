import socket

try:
    results = socket.getaddrinfo(
        "google.com",
        80,
        socket.AF_INET6,
        socket.SOCK_STREAM
    )

    print("So ket qua:", len(results))

    for r in results:
        print(r)

except Exception as e:
    print(e)