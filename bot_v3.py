# 📑 Tóm tắt cấu trúc file `bot_v3.py`

### 1. Khai báo thư viện & Cấu hình AI
* Nhập các thư viện cần thiết: `os`, `discord`, `app_commands`, `commands`, `google.generativeai` và `keep_alive`.
* Cấu hình kết nối với **Google Gemini AI** (sử dụng model `gemini-2.5-pro` với độ sáng tạo `temperature=0.7`).
* Khởi tạo từ điển `user_chats` để lưu trữ phiên trò chuyện riêng biệt (nhớ ngữ cảnh) cho từng người dùng.

### 2. Khởi tạo Discord Bot & Đồng bộ Slash Commands
* Cấu hình quyền `intents` (cho phép bot đọc nội dung tin nhắn).
* Xây dựng lớp `ContinuousChatBot` kế thừa từ `commands.Bot` kết hợp hàm `setup_hook()` để tự động đồng bộ hệ thống lệnh gạch chéo (`/`) với Discord.
* Sự kiện `on_ready()` thông báo trên màn hình console khi bot khởi động thành công.

### 3. Hệ thống lệnh Slash Commands (`/`)
* **/chat [tin_nhan]:** Gửi câu hỏi cho AI, tự động ghi nhớ lịch sử trò chuyện của riêng người dùng đó, và tự động cắt ngắn nếu vượt quá giới hạn 2000 ký tự của Discord.
* **/reset:** Xóa sạch lịch sử chat cũ của người dùng để bắt đầu một cuộc trò chuyện mới từ đầu.
* **/ping:** Kiểm tra trạng thái phản hồi nhanh của bot ("Pong! Bot của Nguyên đây.").

### 4. Khởi chạy ứng dụng (24/7)
* Kích hoạt hàm `keep_alive()` chạy một web server Flask ngầm trên port `8080`.
* Gọi `bot.run("TOKEN_DISCORD")` để chính thức đưa bot lên sóng trực tuyến.
### 5. Kiểm tra phiên bản mới và tự động cập nhật
* Sau vài ngày, tự động cập nhật Python mới!
* Run sau khi lưu file.