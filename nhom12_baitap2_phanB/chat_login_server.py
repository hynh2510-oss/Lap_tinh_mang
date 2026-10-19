"""
Bai tap nhom so 2 - Phan B: Server dang nhap giao thuc chat
Nhom: 12 - Huyen, Nguyen, My, Hang, Trang
Thanh vien viet tep nay: (dien ten ban o day)
Cach chay: python chat_login_server.py

Dac ta thong diep (nay tiep giao thuc thiet ke o Bai tap nhom so 1):
    Client gui  : LOGIN|<ten>\n
    Server tra  : OK|Chao <ten>\n
              hoac ERR|<ma_loi>|<mo_ta>\n
    Client gui QUIT\n de chu dong ket thuc phien.

Bang ma loi:
    01  Ten khong hop le (rong, qua 20 ky tu, hoac chua ky tu "|" / "\n")
    02  Ten da ton tai (dang co nguoi khac dung ten nay)
    03  Sai trinh tu (gui lenh khac LOGIN khi chua dang nhap)

Server o bai nay la server TUAN TU: chi xu ly xong mot client (den khi
QUIT hoac dong ket noi) thi moi accept() client tiep theo.
"""

import socket

from config import PORT  # PORT lay tu config.py, khong hard-code o day

BIND_HOST = ""  # rong = lang nghe tren moi network interface cua may

MAX_NAME_LEN = 20


def recv_line(sock, buf=b""):
    """Tra ve (dong_khong_kem_'\n', bo_dem_con_lai).
    Tra ve (None, buf) neu doi phuong da dong ket noi."""
    while b"\n" not in buf:
        chunk = sock.recv(1024)
        if not chunk:  # b"" -> doi phuong da dong
            return None, buf
        buf += chunk
    line, _, rest = buf.partition(b"\n")
    return line.decode("utf-8"), rest


def is_valid_name(name):
    if not name:
        return False
    if len(name) > MAX_NAME_LEN:
        return False
    if "|" in name or "\n" in name:
        return False
    return True


def handle_client(conn, addr, logged_in_names):
    """Xu ly toan bo phien lam viec voi mot client (server tuan tu)."""
    print(f"[+] Ket noi moi: {addr}")
    buf = b""
    name = None
    try:
        while True:
            line, buf = recv_line(conn, buf)

            if line is None:
                print(f"[-] {addr} da dong ket noi (recv tra ve rong)")
                break

            if line == "QUIT":
                print(f"[-] {addr} chu dong gui QUIT")
                break

            if not line.startswith("LOGIN|"):
                # Sai trinh tu: gui lenh khac trong khi chua LOGIN thanh cong
                if name is None:
                    conn.sendall("ERR|03|Ban phai LOGIN truoc\n".encode("utf-8"))
                # Da login roi ma gui linh tinh: Phan B chua xu ly chat, bo qua
                continue

            candidate = line[len("LOGIN|"):]

            if not is_valid_name(candidate):
                conn.sendall("ERR|01|Ten khong hop le\n".encode("utf-8"))
                continue

            if candidate in logged_in_names:
                conn.sendall("ERR|02|Ten da ton tai\n".encode("utf-8"))
                continue

            name = candidate
            logged_in_names.add(name)
            conn.sendall(f"OK|Chao {name}\n".encode("utf-8"))
            print(f"[+] {addr} dang nhap thanh cong voi ten '{name}'")

    except (ConnectionResetError, OSError) as e:
        print(f"[!] Loi voi {addr}: {e}")
    finally:
        if name is not None:
            logged_in_names.discard(name)
            print(f"[-] Da go '{name}' khoi danh sach dang dang nhap")


def main():
    logged_in_names = set()  # danh sach ten dang dang nhap (dung chung cho ca server)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((BIND_HOST, PORT))
        s.listen(5)
        print(f"Server dang lang nghe tai cong {PORT} (server tuan tu, 1 client/lan)...")

        while True:
            conn, addr = s.accept()
            with conn:
                handle_client(conn, addr, logged_in_names)


if __name__ == "__main__":
    main()
