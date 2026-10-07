# Bài tập Chương 3 — Sổ điểm

## 1. Kết quả liệt kê route

Lệnh: `flask --app sodiem routes`

| Endpoint | Methods | Rule |
| --- | --- | --- |
| api_student_detail | GET | `/api/students/<mssv>` |
| api_student_list | GET | `/api/students` |
| home | GET | `/` |
| search | GET | `/search` |
| static | GET | `/static/<path:filename>` |
| student_detail | GET | `/students/<mssv>` |
| student_export | GET | `/students/<mssv>/export` |
| student_list | GET | `/students` |
| student_score | DELETE, GET, PUT | `/api/students/<mssv>/scores/<course>` |
| student_short | GET | `/sv/<mssv>` |

Kết quả: **10 route, tính cả static**, đúng yêu cầu.

## 2. Kết quả kiểm thử curl

Trong bảng, `S` là `/api/students/23T1020005/scores`.

| Yêu cầu | Dòng trạng thái | Header hoặc body quan trọng |
| --- | --- | --- |
| GET /sv/23T1020001 | HTTP/1.1 301 MOVED PERMANENTLY | `Location: /students/23T1020001` |
| GET /students/23T1020001/export | HTTP/1.1 200 OK | `Content-Type: text/csv; charset=utf-8`; `Content-Disposition: attachment; filename=diem_23T1020001.csv` |
| GET /api/students?lop=k47a&min_avg=7 | HTTP/1.1 200 OK | JSON chỉ có Nguyễn Văn An, lớp K47A, trung bình 8.17, xếp loại Khá. |
| GET /api/students?min_avg=abc | HTTP/1.1 400 BAD REQUEST | `{"detail":"min_avg phải là một số.","error":"Dữ liệu không hợp lệ"}` |
| GET /api/students/999 | HTTP/1.1 404 NOT FOUND | `{"detail":"Không có sinh viên với MSSV = 999.","error":"Không tìm thấy"}` |
| PUT S/web?score=9 | HTTP/1.1 201 CREATED | `Location: /api/students/23T1020005/scores/WEB`; `{"average":9.0,"course":"WEB","mssv":"23T1020005","score":9.0}` |
| PUT S/WEB?score=7.5 | HTTP/1.1 200 OK | `{"average":7.5,"course":"WEB","mssv":"23T1020005","score":7.5}` |
| PUT S/WEB?score=11 | HTTP/1.1 400 BAD REQUEST | `{"detail":"Điểm phải là số từ 0 đến 10.","error":"Dữ liệu không hợp lệ"}` |
| DELETE S/WEB | HTTP/1.1 204 NO CONTENT | Body rỗng. |
| POST S/WEB | HTTP/1.1 405 METHOD NOT ALLOWED | `{"detail":"The method is not allowed for the requested URL.","error":"Phương thức không được hỗ trợ"}` |
| POST /students | HTTP/1.1 405 METHOD NOT ALLOWED | `Content-Type: text/html; charset=utf-8`; trang HTML hiển thị lỗi 405. |

Body CSV:

```csv
hoc_phan,diem
PMMNM,8.5
CSDL,7.0
MMT,9.0
```

Body JSON khi lọc lớp và điểm:

```json
[
  {
    "average": 8.17,
    "lop": "K47A",
    "mssv": "23T1020001",
    "name": "Nguyễn Văn An",
    "rank": "Khá",
    "scores": {
      "CSDL": 7.0,
      "MMT": 9.0,
      "PMMNM": 8.5
    }
  }
]
```

Nội dung chính của trang lỗi khi POST vào `/students`:

```html
<h1>405 — Phương thức không được hỗ trợ</h1>
<p>The method is not allowed for the requested URL.</p>
```


## 3. Trả lời câu hỏi

### Vì sao Câu 4 dùng 301, còn Câu 8 dùng 201 kèm Location?

Câu 4 dùng 301 để chuyển từ link rút gọn sang trang chi tiết. Location chứa địa chỉ cần chuyển đến.

Câu 8 dùng 201 vì vừa thêm điểm cho học phần chưa có điểm. Location chứa đường dẫn để xem điểm vừa thêm.

### Thêm điểm rồi khởi động lại server, điểm đó còn không? Vì sao?

Không còn. Điểm mới chỉ được lưu trong biến STUDENTS khi chương trình chạy. Khi khởi động lại server, chương trình lấy lại dữ liệu mẫu ban đầu nên điểm vừa thêm sẽ mất.

### Vì sao dùng được request trong error handler?

Error handler đang xử lý lỗi của yêu cầu hiện tại nên vẫn truy cập được request. Nhờ đó, hàm biết đường dẫn đang được truy cập để trả lỗi dạng JSON hoặc HTML.