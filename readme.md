# Food Order Module

## Mô tả
Module `FoodOrder` cho phép các công ty dễ dàng quản lý việc đặt đồ ăn cho nhân viên. Với module này, bạn có thể tạo các đơn đặt hàng, quản lý các món ăn, tính toán tổng chi phí, và theo dõi tình trạng thanh toán.

## Tính năng
- Tạo và quản lý đơn đặt đồ ăn.
- Tính toán tổng chi phí dựa trên giá cả các món ăn và phí ship, giảm giá theo đầu người.
- Theo dõi tình trạng thanh toán cho từng món ăn.
- Gửi thông báo đến các thành viên  về các món ăn chưa thanh toán.


## Cấu hình
Sau khi cài đặt, bạn có thể cấu hình module từ menu `Food Orders` trong giao diện Odoo.

## Sử dụng
- Để tạo một đơn đặt hàng mới, truy cập menu `Food Orders` và nhấn `Create`.
- Thêm các món ăn và thông tin cần thiết.
- Thiết lập phí ship và giảm giá nếu có.
- Xác nhận đơn hàng và theo dõi tình trạng thanh toán của các thành viên.

## Phân Quyền 
- Mọi người  đều có quyền tạo, xem đơn đặt hàng , chỉ có người tạo phiếu đặt đồ ăn mới có thêm quyền sửa, xóa các thông tin của chính mình.

## Chú ý
Khi sử dụng module này, hãy đảm bảo rằng bạn đã thêm thông tin QR Code, Số Tài Khoản (STK) và Ngân Hàng cho mỗi người dùng trong hệ thống. Để thêm hoặc cập nhật thông tin này:
1. Truy cập `Food Order > thông tin thanh toán `.
2. Thêm hoặc cập nhật thông tin QR Code, Số Tài Khoản và Ngân Hàng tại đây.
3. Lưu lại các thay đổi.
Thông tin này sẽ được sử dụng khi gửi thông báo về các món ăn chưa thanh toán, giúp người nhận dễ dàng thực hiện thanh toán.

