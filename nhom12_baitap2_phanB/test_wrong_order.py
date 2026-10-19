"""
Bai tap nhom so 2 - Phan B: Script HO TRO KIEM THU (khong nop, chi de test)
Muc dich: gui mot lenh KHONG PHAI LOGIN ngay khi vua ket noi, de kiem tra
server co tra ve dung ERR|03|Ban phai LOGIN truoc hay khong.

Cach chay: python test_wrong_order.py
"""

import socket

from config import HOST, PORT  # HOST/PORT lay tu config.py, khong hard-code o day


def recv_line(sock, buf=b""):
    while b"\n" not in buf:
        chunk = sock.recv(1024)
        if not chunk:
            return None, buf
        buf += chunk
    line, _, rest = buf.partition(b"\n")
    return line.decode("utf-8"), rest


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Da ket noi. Gui thang HELLO\\n (khong phai LOGIN)...")
        s.sendall(b"HELLO\n")

        buf = b""
        line, buf = recv_line(s, buf)
        print("Server tra loi:", line)

        s.sendall(b"QUIT\n")


if __name__ == "__main__":
    main()
