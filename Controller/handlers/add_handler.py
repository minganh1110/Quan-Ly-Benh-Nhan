import tkinter as tk
from Model.patient_entity import Patient

def handle_add_patient(view, model, khoa_model):
    data = view.get_form_data()
    
    # Kiểm tra người dùng có chọn khoa không
    if not data['khoa']:
        tk.messagebox.showerror("Lỗi", "Vui lòng chọn khoa trước khi thêm!")
        return False

    # Tìm khoa_id tương ứng
    khoa_list = khoa_model.get_all_khoa()
    khoa_id = None
    for k in khoa_list:
        if (k['khoa_id']) == data['khoa'] or k['ten_khoa'] == data['khoa']:
            khoa_id = k['khoa_id']
            break
       

    if khoa_id is None:
        tk.messagebox.showerror("Lỗi", f"Khoa '{data['khoa']}' không hợp lệ.")
        return False
    # Kiểm tra các trường bắt buộc
    giuong_id_list= model.get_all_patients()
    for patient in giuong_id_list:
        print(patient['giuong_id'], data['giuong_id'])
        if int(patient['giuong_id']) == int(data['giuong_id']):
            if patient["ngay_ra_vien"] is None:
                tk.messagebox.showerror("Lỗi", "Giường đã có người. Vui lòng chọn giường khác.")
                return False
          
    # Tạo đối tượng Patient
    patient = Patient(
        name=data['name'],
        gender=data['gender'],
        ngaysinh=data['ngaysinh'],
        diachi=data['diachi'],
        sdt=data['sdt'],
        ngaynhapvien=data['ngaynhapvien'],
        ngayravien=data['ngayravien'],
        chuandoan=data['chuandoan'],
        khoa_id=khoa_id,
        benhnhan_id=None,
        bac_si_id=data['bac_si_id'],
        phong_id=data['phong_id'],
        giuong_id=data['giuong_id']

    )

    if model.add_patient(patient):
        tk.messagebox.showinfo("Thành công", "Thêm bệnh nhân thành công!")
        return True
    else:
        tk.messagebox.showerror("Lỗi", "Thêm bệnh nhân thất bại!")
        return False
