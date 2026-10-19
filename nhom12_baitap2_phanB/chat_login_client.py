"""
Bai tap nhom so 2 - Phan B: Client dang nhap giao thuc chat
Nhom: 12 - Huyen, Nguyen, My, Hang, Trang
Thanh vien viet tep nay: (dien ten ban o day)
Cach chay: python chat_login_client.py

Client nhap ten tu ban phim, gui LOGIN|<ten>\n cho server.
Neu nhan ERR thi cho nhap lai, toi da 3 lan roi thoat.
"""

import socket

from config import HOST, PORT  # HOST/PORT lay tu config.py, khong hard-code o day

MAX_TRIES = 3


def recv_line(sock, buf=b""):
    """Tra ve (dong_khong_kem_'\n', bo_dem_con_lai).
    Tra ve (None, buf) neu doi phuong da dong ket noi."""
    while b"\n" not in buf:
        chunk = sock.recv(1024)
        if not chunk:
            return None, buf
        buf += chunk
    line, _, rest = buf.partition(b"\n")
    return line.decode("utf-8"), rest


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((HOST, PORT))
            s.settimeout(None)  # bo timeout, chuyen sang cho nguoi dung go ban phim

            buf = b""
            for attempt in range(1, MAX_TRIES + 1):
                name = input(f"Nhap ten dang nhap (lan {attempt}/{MAX_TRIES}): ").strip()
                s.sendall(f"LOGIN|{name}\n".encode("utf-8"))

                line, buf = recv_line(s, buf)
                if line is None:
                    print("Server da dong ket noi bat ngo.")
                    return

                print("Server tra loi:", line)

                if line.startswith("OK|"):
                    print("Dang nhap thanh cong!")
                    s.sendall(b"QUIT\n")  # ket thuc phien gon gang (Phan B chua can chat)
                    return
                # neu la ERR thi vong lap se cho nhap lai (neu con luot)

            print("Da het so lan thu, thoat chuong trinh.")

    except ConnectionRefusedError:
        print("Khong the ket noi: server chua chay hoac sai dia chi/cong.")
    except socket.timeout:
        print("Qua han ket noi toi server.")
    except OSError as e:
        print(f"Loi socket: {e}")


if __name__ == "__main__":
    main()
