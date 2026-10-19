"""
Bai tap nhom so 2 - Phan B: Cau hinh chung (KHONG hard-code rai rac o tung file)

Tat ca cac file server/client/test deu import PORT, HOST tu day.
Co the doi gia tri bang 1 trong 2 cach, khong can sua code:

  1) Sua truc tiep 2 dong GROUP_ID / HOST_DEFAULT ben duoi (don gian nhat).
  2) Hoac dat bien moi truong truoc khi chay, vi du tren Windows (cmd):
         set CHAT_GROUP_ID=12
         set CHAT_HOST=127.0.0.1
         python chat_login_server.py
     Bien moi truong (neu co) se duoc uu tien hon gia tri mac dinh ben duoi.
"""

import os

# ---- Gia tri mac dinh cua nhom, sua o day neu can ----
GROUP_ID = 12
HOST_DEFAULT = "127.0.0.1"  # doi thanh IP may chay server khi test 2 may that

# ---- Lay gia tri thuc te: uu tien bien moi truong, khong thi dung mac dinh ----
GROUP_ID = int(os.environ.get("CHAT_GROUP_ID", GROUP_ID))
HOST = os.environ.get("CHAT_HOST", HOST_DEFAULT)
PORT = 9000 + GROUP_ID
