# auto-reply-comments-on-youtube
Một script siêu đơn giản để tự động trả lời comment trong một video Youtube
> [!CAUTION]
> Tool này mình đã viết khá là lâu rồi, khoảng 1-2 năm trước. Mình không đảm bảo được liệu script này sẽ có thể sống lâu hay không.<br>Thêm nữa, mình không có ý định duy trì hay phát triển script này thành một app hoàn chỉnh

> UI siêu phèn là vì hồi đó mình viết script để người thân xài :)))

> [!WARNING]
> Bản bạn đang nhìn thấy đây là mình đã sửa lại vài dòng code để nhìn đỡ tàn phế thôi, chứ còn mình ***CHƯA TEST Ở BẤT KÌ VIDEO NÀO CẢ!*** (và mình không biết nên test ở chỗ nào luôn, nên đành chịu)

## Hướng dẫn thiết lập ban đầu
1. Chạy các lệnh sau:
```sh
pip install google-api-python-client
pip install google-auth
```
2. Truy cập vào https://console.cloud.google.com/apis/dashboard
3. Tạo một project mới
4. Ở ngăn bên trái, đảm bảo bạn đang ở product ``APIs & Services``, nếu rồi thì nhấn ``Library``
5. Tìm Youtube Data API v3 và kích hoạt nó lên
6. Quay lại, ở ngăn bên trái, nhấn vào mục ``Credentials``
7. Tạo một API key mới và một OAuth2 client ID mới
8. [TÙY CHỌN] Vào tùy chọn của API key bạn vừa tạo, trượt xuống phần Restrict, chọn chỉ cho xài Youtube Data API v3 thôi!
9. Sao chép API key bạn vừa tạo, tạo một file ``key.txt`` ở chỗ để file script và dán key vào đó.
10. Vào OAuth2 client ID, trượt xuống client secrets, nhấn nút tải xuống ở hàng client secrets để lấy file json, sau đó đổi tên thành ``clientid.json`` và để vào nơi để file script

# Giấy phép
Script này dùng giấy phép The Unlicensed.
