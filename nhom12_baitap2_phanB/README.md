# Bài tập nhóm 2 - Phần B: Giao thức đăng nhập chat (Socket TCP)

**Môn:** Lập trình mạng
**Giảng viên:** Nguyễn Hoàng Hải
**Nhóm:** 12

| STT | Họ và tên | MSSV |
|---|---|---|
| 1 | Phan Thị Thanh Huyền | 3120224071 |
| 2 | Trần Thị Bảo Nguyên | 3120224104 |
| 3 | Trần Thị Hoàng My | 3120224095 |
| 4 | Trần Thanh Hằng | 3120224047 |
| 5 | Nguyễn Thị Thùy Trang | 3120224154 |

## 1. Mô tả

Phần B cài đặt bước **đăng nhập** của một giao thức chat đơn giản trên nền TCP socket, nối tiếp bản đặc tả giao thức của nhóm ở Bài tập nhóm số 1. Server hoạt động theo mô hình **tuần tự** (xử lý trọn vẹn một kết nối rồi mới `accept()` kết nối tiếp theo), chưa xử lý nhiều client đồng thời (phần này sẽ làm ở các bài sau khi học threading/`selectors`).

## 2. Yêu cầu môi trường

- Python 3.9+
- Không cần cài thêm thư viện ngoài (chỉ dùng module `socket` có sẵn)

## 3. Cấu trúc thư mục

```
.
├── config.py                       # Cấu hình chung: PORT, HOST (sửa 1 chỗ, dùng cho mọi file)
├── chat_login_server.py            # Server xử lý đăng nhập
├── chat_login_client.py            # Client đăng nhập (chương trình chính)
├── test_duplicate_same_session.py  # Script test ca lỗi "tên đã tồn tại"
├── test_wrong_order.py             # Script test ca lỗi "sai trình tự"
├── test_two_messages_one_sendall.py# Script chứng minh xử lý đúng khi 2 thông điệp gửi chung 1 sendall()
└── README.md
```

## 4. Cấu hình cổng (PORT) và địa chỉ (HOST)

Quy ước của lớp: cổng server = `9000 + mã nhóm`. Nhóm 12 dùng cổng **9012**.

Toàn bộ `PORT`/`HOST` được đặt tập trung tại **`config.py`** — mọi file `.py` khác đều `import` giá trị từ đây, không khai báo lặp lại từng nơi. Có 2 cách đổi giá trị mà **không cần sửa code**:

**Cách 1 — sửa trực tiếp `config.py`:**
```python
GROUP_ID = 12                  # đổi mã nhóm ở đây
HOST_DEFAULT = "127.0.0.1"     # đổi IP máy chạy server ở đây khi test 2 máy
```

**Cách 2 — đặt biến môi trường trước khi chạy (không cần sửa file nào):**
```bash
# Windows (cmd)
set CHAT_GROUP_ID=12
set CHAT_HOST=127.0.0.1
python chat_login_server.py
```
Biến môi trường nếu có sẽ được ưu tiên hơn giá trị mặc định trong `config.py`.

## 5. Cách chạy

### 5.1. Chạy server

```bash
python chat_login_server.py
```

Thấy dòng sau là server đã sẵn sàng, cứ để cửa sổ này chạy:

```
Server dang lang nghe tai cong 9012 (server tuan tu, 1 client/lan)...
```

### 5.2. Chạy client (ở cửa sổ terminal khác)

```bash
python chat_login_client.py
```

Chương trình sẽ hỏi tên đăng nhập, cho phép nhập lại tối đa 3 lần nếu bị từ chối.

## 6. Đặc tả giao thức

| Chiều | Định dạng | Ví dụ |
|---|---|---|
| Client → Server | `LOGIN|<ten>\n` | `LOGIN|Huyen\n` |
| Server → Client (thành công) | `OK|Chao <ten>\n` | `OK|Chao Huyen\n` |
| Server → Client (thất bại) | `ERR|<ma_loi>|<mo_ta>\n` | `ERR|01|Ten khong hop le\n` |
| Client → Server (kết thúc phiên) | `QUIT\n` | `QUIT\n` |

Mọi thông điệp đều kết thúc bằng ký tự xuống dòng `\n`; bên nhận dùng hàm `recv_line()` để đọc và tách đúng ranh giới thông điệp kể cả khi nhiều thông điệp đến trong cùng một lần `recv()`.

### Bảng mã lỗi

| Mã | Mô tả | Nguyên nhân |
|---|---|---|
| 01 | Tên không hợp lệ | Tên rỗng, dài hơn 20 ký tự, hoặc chứa ký tự `|` / `\n` |
| 02 | Tên đã tồn tại | Đang có người dùng khác (hoặc chính phiên trước) dùng tên này |
| 03 | Sai trình tự | Gửi lệnh khác `LOGIN` khi chưa đăng nhập thành công |

## 7. Các script hỗ trợ kiểm thử

Các file `test_*.py` **không phải chương trình nộp chính**, chỉ dùng để tái hiện các ca lỗi phục vụ viết báo cáo (vì server tuần tự nên không thể dùng 2 client riêng biệt để tạo ra một số ca lỗi).

- **`test_duplicate_same_session.py`**: gửi 2 thông điệp `LOGIN|<tên>` cùng tên trong **cùng một kết nối, cùng một lần `sendall()`**, để tái hiện lỗi `ERR|02` (tên đã tồn tại). Chạy: `python test_duplicate_same_session.py`, nhập một tên bất kỳ khi được hỏi.
- **`test_wrong_order.py`**: gửi thẳng `HELLO\n` (không phải `LOGIN`) ngay sau khi kết nối, để tái hiện lỗi `ERR|03` (sai trình tự). Chạy: `python test_wrong_order.py`.
- **`test_two_messages_one_sendall.py`**: gửi 2 thông điệp `LOGIN|An` và `LOGIN|Binh` gộp trong một lần `sendall()`, chứng minh server tách đúng ranh giới thông điệp theo `\n`. Chạy: `python test_two_messages_one_sendall.py`.

## 8. Quan sát tính tuần tự của server

Mở 2 client cùng lúc: để client A dừng ở bước nhập tên (chưa Enter), rồi mở client B — B sẽ kết nối được nhưng không nhận phản hồi (treo ở `recv()`) cho đến khi A hoàn tất phiên (đăng nhập xong hoặc `QUIT`). Đây là hệ quả của việc server xử lý tuần tự: chỉ `accept()` kết nối tiếp theo sau khi đã xử lý xong trọn vẹn kết nối hiện tại.

## 9. Việc cần điền trước khi nộp/đẩy lên Git

- [ ] Kiểm tra lại `PORT` đúng `9000 + 12` ở tất cả các file
- [ ] Điền tên nhóm/thành viên vào phần `<TODO>` ở đầu mỗi file `.py`
- [ ] Không commit các file log/ảnh chụp không cần thiết lên Git (có thể thêm `.gitignore`)
