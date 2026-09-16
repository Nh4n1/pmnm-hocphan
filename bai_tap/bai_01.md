# Bài 1.2 — Phân tích trường hợp Redis và Valkey

## 1. Giới thiệu

Redis là một hệ thống lưu trữ dữ liệu key-value trong bộ nhớ, thường được sử dụng cho bộ nhớ đệm, quản lý session, hàng đợi thông điệp và các ứng dụng cần xử lý dữ liệu với độ trễ thấp.

Trong nhiều năm, Redis được phát hành theo giấy phép **BSD 3-Clause**, thuộc nhóm giấy phép mã nguồn mở permissive. Tuy nhiên, vào năm 2024, việc Redis thay đổi giấy phép đã gây ra tranh luận lớn trong cộng đồng và dẫn đến sự xuất hiện của một dự án mới mang tên **Valkey**.

## 2. Nguyên nhân của mâu thuẫn

Ngày 20/03/2024, Redis Inc. thông báo rằng từ Redis 7.4, phần mềm sẽ không còn được phát hành theo BSD 3-Clause mà chuyển sang mô hình cấp phép kép gồm:

- **Redis Source Available License v2 (RSALv2)**
- **Server Side Public License v1 (SSPLv1)**

Redis giải thích rằng thay đổi này nhằm bảo vệ khả năng tiếp tục đầu tư vào dự án, đặc biệt trước trường hợp các nhà cung cấp dịch vụ đám mây sử dụng Redis để kinh doanh nhưng đóng góp hạn chế trở lại cho dự án.

Tuy nhiên, cả RSALv2 và SSPLv1 đều không phải giấy phép được **Open Source Initiative (OSI)** công nhận. RSALv2 hạn chế việc thương mại hóa Redis dưới dạng dịch vụ được quản lý, còn SSPLv1 yêu cầu nhà cung cấp Redis dưới dạng dịch vụ phải công bố thêm mã nguồn của lớp quản lý dịch vụ.

Nguồn: [Redis — Redis Adopts Dual Source-Available Licensing](https://redis.io/blog/redis-adopts-dual-source-available-licensing/)

## 3. Sự ra đời của Valkey

Việc thay đổi giấy phép chỉ áp dụng cho các phiên bản Redis mới. Redis 7.2.x và các phiên bản trước đó vẫn được phát hành theo **BSD 3-Clause**.

Ngày 28/03/2024, chỉ tám ngày sau thông báo của Redis, **Linux Foundation** công bố dự án **Valkey**. Dự án tiếp tục phát triển dựa trên Redis OSS 7.2.4 và giữ giấy phép BSD 3-Clause.

Valkey nhanh chóng nhận được sự tham gia của nhiều contributor và doanh nghiệp như AWS, Google Cloud, Oracle và Ericsson. Sau đó, nhiều tổ chức khác như Alibaba Cloud, Huawei và Percona cũng tham gia hỗ trợ dự án.

Nguồn: [Linux Foundation — Launches Open Source Valkey Community](https://www.linuxfoundation.org/press/linux-foundation-launches-open-source-valkey-community)

## 4. Ý nghĩa của quyền fork

Trường hợp Redis và Valkey thể hiện rõ một quyền quan trọng của phần mềm mã nguồn mở: **quyền fork**.

Khi cộng đồng không đồng thuận với hướng phát triển hoặc chính sách của tổ chức quản lý, họ có thể sử dụng phiên bản mã nguồn vẫn được phát hành theo giấy phép mở để xây dựng một dự án độc lập.

Valkey vì vậy không chỉ là một bản sao của Redis mà dần trở thành một dự án riêng, có mô hình quản trị cộng đồng dưới sự bảo trợ của Linux Foundation. Điều này cũng cho thấy giấy phép có thể ảnh hưởng trực tiếp đến cộng đồng và cách một dự án được quản trị.

## 5. Góc nhìn từ hai phía

Mâu thuẫn này không đơn giản là một bên đúng và một bên sai.

Từ phía Redis Inc., công ty cần nguồn tài chính để duy trì đội ngũ phát triển và muốn hạn chế việc các nhà cung cấp cloud khai thác Redis thương mại mà không đóng góp tương xứng.

Ở phía cộng đồng, nhiều thành viên muốn duy trì một phiên bản với giấy phép mã nguồn mở permissive như BSD 3-Clause. Vì vậy, họ lựa chọn tiếp tục phát triển mã nguồn cũ dưới tên Valkey.

Đáng chú ý, đến Redis 8, Redis đã bổ sung **GNU AGPLv3** bên cạnh RSALv2 và SSPLv1. AGPLv3 là giấy phép được OSI công nhận, đưa Redis trở lại với một lựa chọn giấy phép mã nguồn mở.

Nguồn: [Redis — Licenses](https://redis.io/legal/licenses/)

## 6. Kết luận

Trường hợp Redis và Valkey cho thấy giấy phép mã nguồn mở không chỉ là vấn đề pháp lý mà còn liên quan đến mô hình kinh doanh, quản trị và mối quan hệ giữa doanh nghiệp với cộng đồng.

Redis muốn bảo vệ khả năng kinh doanh và đầu tư vào sản phẩm, trong khi một bộ phận cộng đồng muốn duy trì tính mở của dự án. Khi hai định hướng không còn thống nhất, quyền fork đã giúp cộng đồng tiếp tục phát triển Redis OSS 7.2.4 thành Valkey.

Đây là một ví dụ thực tế cho thấy cộng đồng mã nguồn mở có khả năng tiếp tục duy trì và phát triển phần mềm ngay cả khi tổ chức đứng sau dự án thay đổi định hướng.

## Nguồn tham khảo

1. Redis, *Redis Adopts Dual Source-Available Licensing*, 20/03/2024  
   https://redis.io/blog/redis-adopts-dual-source-available-licensing/

2. Redis, *Licenses*  
   https://redis.io/legal/licenses/

3. Linux Foundation, *Linux Foundation Launches Open Source Valkey Community*, 28/03/2024  
   https://www.linuxfoundation.org/press/linux-foundation-launches-open-source-valkey-community

4. Redis, *Redis is now available under the AGPLv3 open source license*, 01/05/2025  
   https://redis.io/blog/agplv3/

5. AWS Việt Nam, *Công bố ra mắt Amazon MemoryDB cho Valkey*, 08/10/2024  
   https://aws.amazon.com/vi/about-aws/whats-new/2024/10/amazon-memorydb-valkey

