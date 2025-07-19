# Quản Lý Bệnh Nhân (QLBN)
## Cấu trúc hướng đối tượng

Dự án được thiết kế theo mô hình hướng đối tượng (OOP):

- **Class**: Mỗi chức năng chính đều được đóng gói thành các class riêng biệt như `PatientController`, `PatientModel`, `PatientView`, `KhoaController`, `KhoaModel`, `KhoaView`, `PatientTable`.
- **Thuộc tính và phương thức**: Các class có thuộc tính (biến thành viên) và phương thức (hàm xử lý) riêng, ví dụ: `show_patients`, `get_selected_id`, `add_patient`, `update_patient`.
- **Đóng gói**: Mỗi class chỉ quản lý dữ liệu và logic liên quan, giúp mã nguồn dễ bảo trì và mở rộng.
- **Kế thừa**: Các class giao diện kế thừa từ `tk.Frame` của Tkinter để tận dụng các chức năng giao diện sẵn có.
- **Trừu tượng**: Controller chỉ gọi các hàm xử lý mà không cần biết chi tiết bên trong, các handler tách biệt logic nghiệp vụ.
- **Đa hình**: Các phương thức có thể được ghi đè hoặc mở rộng khi cần.

Ví dụ về hướng đối tượng trong file `View/patient_table.py`:
- Class `PatientTable` kế thừa từ `tk.Frame`, quản lý bảng hiển thị bệnh nhân.
- Các phương thức như `show_patients`, `get_selected_id`, `get_selected_row_values` giúp thao tác với dữ liệu bảng một cách trực quan và đóng gói.

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
## Mô tả cấu trúc CSDL quan hệ 
<img width="909" height="670" alt="image" src="https://github.com/user-attachments/assets/326ba3ec-63ba-4e40-a859-e96fca18d988" />

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
   
  

