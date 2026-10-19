"""
Bai tap nhom so 2 - Phan B: Script HO TRO KIEM THU (khong nop, chi de test)
Muc dich: chung minh ERR|02|Ten da ton tai.

Vi server la SERVER TUAN TU (khong luong), 2 ket noi rieng biet khong the
"dung do" nhau de tao loi trung ten (client sau luon phai doi client truoc
ngat han, luc do ten da duoc giai phong). Cach dung de tao ra loi 02 la
gui HAI lan LOGIN cung mot ten trong CUNG MOT ket noi: lan dau thanh cong
(ten duoc them vao danh sach), lan hai bi tu choi vi ten do (chinh no)
van con trong danh sach.

Cach chay: python test_duplicate_same_session.py
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
    name = input("Nhap ten muon test trung (se gui LOGIN 2 lan voi ten nay): ").strip()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Gui 2 thong diep LOGIN cung ten trong 1 lan sendall duy nhat
        payload = f"LOGIN|{name}\nLOGIN|{name}\n".encode("utf-8")
        print("Gui:", payload)
        s.sendall(payload)

        buf = b""
        for _ in range(2):
            line, buf = recv_line(s, buf)
            if line is None:
                print("Server da dong ket noi som hon du kien.")
                break
            print("Nhan duoc:", line)

        s.sendall(b"QUIT\n")


if __name__ == "__main__":
    main()
