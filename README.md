# Quản Lý Bệnh Nhân (QLBN)
## Cấu trúc thư mục
```
QLBN/
│
├── Controller/
│   ├── patient_controller.py      # Xử lý logic quản lý bệnh nhân
│   ├── khoa_controller.py         # Xử lý logic quản lý khoa
│   └── handlers/                  # Các hàm xử lý thêm/sửa/xóa bệnh nhân
│
├── Model/
│   ├── patient_model.py           # Model thao tác dữ liệu bệnh nhân
│   ├── khoa_model.py              # Model thao tác dữ liệu khoa
│   └── patient_entity.py          # Định nghĩa class Patient
│
├── View/
│   ├── patient_view.py            # Giao diện quản lý bệnh nhân
│   ├── khoa_view.py               # Giao diện quản lý khoa
│   └── patient_table.py           # Bảng hiển thị danh sách bệnh nhân
│
├── main.py                        # Form chính, chọn chức năng quản lý
└── README.md                      # Tài liệu hướng dẫn
```

## Chức năng chính

- Quản lý bệnh nhân:  
  - Thêm, sửa, xóa, tìm kiếm, hiển thị danh sách bệnh nhân.
  - Nhập thông tin: họ tên, giới tính, ngày sinh, địa chỉ, số điện thoại, ngày nhập viện, ngày ra viện, chẩn đoán, khoa.

- Quản lý khoa: 
  - Thêm, sửa, xóa, tìm kiếm, hiển thị danh sách khoa.

- Tìm kiếm:
  - Tìm kiếm bệnh nhân hoặc khoa theo từ khóa.

- Giao diện:
  - Giao diện trực quan với Tkinter, sử dụng bảng (Treeview) để hiển thị danh sách.
 
    
## Hướng dẫn sử dụng

1. Cài đặt thư viện:
   ```
   pip install mysql-connector-python
   ```

2. Cấu hình kết nối database:
   - tạo database có tên là qlbn trên mysql
   - sử dụng file qlbn.sql import vào trong mysql để có thể lấy được dữ liệu 

4. Chạy chương trình:
   ```
   python main.py
   ```
   - Chọn chức năng quản lý khoa và quản lý bệnh nhân 
   


