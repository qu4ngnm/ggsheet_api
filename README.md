# Tổng quan về HTTP
- HTTP là một giao thức được sử dụng để nạp tài nguyên như kiểu HTML, chính vì vậy nó còn được gọi là `Giao Thức Truyền Tải Siêu Văn Bản`
- Giao thức này sử dụng một mô hình thông điệp tại đó `Clients` sẽ tạo một `HTTP Request` tới một `web server` nào đó và `web server` đó respons với một tài nguyên được hiển thị trên browser người dùng
- HTTP là giao thức ở lớp ứng dụng được gửi thông qua nền tảng là `TCP/IP`, nói rõ ràng hơn thì chính là kết nối `TCP/IP` nhưng được mã hoá `TLS`, đây là giao thức người ta hay dùng nhất tuy nhiên không có nghĩa là duy nhất vì người ta vẫn có thể dùng các giao thức truyền tải đáng tin cậy khác vẫn được.
- 