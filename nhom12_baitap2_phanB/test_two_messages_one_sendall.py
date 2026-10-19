"""
Bai tap nhom so 2 - Phan B: Script chung minh xu ly dung ranh gioi thong diep
khi hai thong diep duoc gui trong CUNG MOT lan sendall().
Nhom: 12 - Huyen, Nguyen, My, Hang, Trang
Thanh vien viet tep nay: (dien ten ban o day)
Cach chay:
    1) Chay chat_login_server.py o mot cua so terminal.
    2) Chay script nay o cua so khac: python test_two_messages_one_sendall.py
    3) Chup man hinh: server phai tra ve 2 dong OK|... rieng biet
       (hoac 1 OK + 1 ERR|02 neu 2 ten trung nhau), chung to server
       da tach dung 2 thong diep du chung den trong 1 lan recv().
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

        # Ghep 2 thong diep LOGIN thanh MOT chuoi byte, gui bang 1 lan sendall duy nhat
        two_messages = "LOGIN|An\nLOGIN|Binh\n".encode("utf-8")
        print("Gui mot lan sendall() chua 2 thong diep:", two_messages)
        s.sendall(two_messages)

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
