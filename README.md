# Tổng quan về HTTP
- HTTP là một giao thức được sử dụng để nạp tài nguyên như kiểu HTML, chính vì vậy nó còn được gọi là `Giao Thức Truyền Tải Siêu Văn Bản`
- Giao thức này sử dụng một mô hình thông điệp tại đó `Clients` sẽ tạo một `HTTP Request` tới một `web server` nào đó và `web server` đó respons với một tài nguyên được hiển thị trên browser người dùng
- HTTP là giao thức ở lớp ứng dụng được gửi thông qua nền tảng là `TCP/IP`, nói rõ ràng hơn thì chính là kết nối `TCP/IP` nhưng được mã hoá `TLS`, đây là giao thức người ta hay dùng nhất tuy nhiên không có nghĩa là duy nhất vì người ta vẫn có thể dùng các giao thức truyền tải đáng tin cậy khác vẫn được.

# HTTP Request & Response
- Với mỗi HTTP Request thì sẽ gồm có 3 phần đó là Request Line, Header và Body.
- Method: Trong http Request thì gồm các phương thức như `GET, POST, HEAD, PUT, DELETE` và thông dụng nhất người ta hay dùng đó là phương thức `GET` để gửi yêu cầu lấy dữ liệu từ phía server và `POST` để gửi yêu cầu chứa dữ liệu lên server để xử lý và những phương thức này nằm ở phần `Request Line` của 1 HTTP Request
- Tiếp đó là về phần `HEADER` sẽ gồm có các thông tin như `Host`, `Accept`, `Connection`, `Cookie`,...
- Và phần cuối cùng đó chính là HTTP Body, đây là nơi sẽ chứa dữ liệu gửi từ client tới server đối với http request và ngược lại đối với http respons.  Đa số các gói tin gửi theo phương thức GET sẽ có Body trống, các phương thức như POST hay PUT thường dùng để gửi dữ liệu nên sẽ có bao gồm dữ liệu trong trường Body.

![](/SimpleWebServer/assets/httprequest.png)

    Cấu trúc của một Request GET

# Một số mã trạng thái trong Request line
- `1xx: Informational`  Request đã được tiếp nhận, tiếp tục tiến trình xử lý
- `2xx: Success`  Request đã được server tiếp nhận và xử lý thành công
- `3xx: Redirect`  Cho biết người dùng phải thực hiện chuyển hướng để hoàn thành request
- `4xx: Client Error` Sai cú pháp hoặc yêu cầu không hợp lệ 
- `5xx: Server Error` Lỗi này thì là do phía máy chủ gặp sự cố