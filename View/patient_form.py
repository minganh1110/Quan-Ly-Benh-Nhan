import tkinter as tk
from tkinter import ttk
from Model.khoa_model import KhoaModel
from Model.bac_si_model import DoctorModel

class PatientForm(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Thông tin bệnh nhân")
        self.entries = {}
        self.khoa_map = {}          # ánh xạ tên khoa → id
        self.khoa_map_reverse = {}  # ánh xạ id → tên khoa
        self.doctor_map = {}        # ánh xạ tên bác sĩ → id
        self.doctor_map_reverse = {}# ánh xạ id → tên bác sĩ
        self.khoa_cb = None
        self.doctor_cb = None
        self.create_form()

    def create_form(self):
        # Giao diện theo layout ngang: chia 3 cột

        # ----- Frame 1: Thông tin cá nhân -----
        personal_frame = tk.LabelFrame(self, text="Thông tin cá nhân")
        personal_frame.grid(row=0, column=0, sticky="n", padx=10, pady=5)

        personal_fields = [
            ("Họ tên", "name"),
            ("Giới tính", "gender"),
            ("Ngày sinh", "ngaysinh"),
            ("Địa chỉ", "diachi"),
            ("SĐT", "sdt"),
        ]

        for i, (label, key) in enumerate(personal_fields):
            tk.Label(personal_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entry = tk.Entry(personal_frame)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[key] = entry

        # ----- Frame 2: Thông tin điều trị -----
        treatment_frame = tk.LabelFrame(self, text="Thông tin điều trị")
        treatment_frame.grid(row=0, column=1, sticky="n", padx=10, pady=5)

        treatment_fields = [
            ("Ngày nhập viện", "ngaynhapvien"),
            ("Ngày ra viện", "ngayravien"),
            ("Chẩn đoán", "chuandoan"),
        ]

        for i, (label, key) in enumerate(treatment_fields):
            tk.Label(treatment_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entry = tk.Entry(treatment_frame)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[key] = entry

        # Combobox Khoa
        tk.Label(treatment_frame, text="Khoa").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        khoa_model = KhoaModel()
        ds_khoa = khoa_model.get_all_khoa()

        khoa_names = []
        for k in ds_khoa:
            ten = k['ten_khoa']
            ma = k['khoa_id']
            self.khoa_map[ten] = ma
            self.khoa_map_reverse[ma] = ten
            khoa_names.append(ten)

        self.khoa_cb = ttk.Combobox(treatment_frame, values=khoa_names, state="readonly")
        self.khoa_cb.grid(row=3, column=1, padx=5, pady=2)
        self.khoa_cb.bind("<<ComboboxSelected>>", self.on_khoa_selected)
        self.entries["khoa"] = self.khoa_cb

        # Combobox Bác sĩ
        tk.Label(treatment_frame, text="Bác sĩ").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.doctor_cb = ttk.Combobox(treatment_frame, state="readonly")
        self.doctor_cb.grid(row=4, column=1, padx=5, pady=2)
        self.entries["bac_si_id"] = self.doctor_cb

        # ----- Frame 3: Thông tin chỗ ở -----
        stay_frame = tk.LabelFrame(self, text="Thông tin chỗ ở")
        stay_frame.grid(row=0, column=2, sticky="n", padx=10, pady=5)

        stay_fields = [
            ("Phòng ID", "phong_id"),
            ("Giường ID", "giuong_id"),
        ]

        for i, (label, key) in enumerate(stay_fields):
            tk.Label(stay_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entry = tk.Entry(stay_frame)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.entries[key] = entry

    # Sự kiện chọn khoa
    def on_khoa_selected(self, event):
        ten_khoa = self.entries["khoa"].get()
        khoa_id = self.khoa_map.get(ten_khoa)
        self.load_doctors_by_khoa(khoa_id)

    # Load danh sách bác sĩ theo khoa
    def load_doctors_by_khoa(self, khoa_id):
        doctor_model = DoctorModel()
        ds_bac_si = doctor_model.get_doctors_by_khoa_id(khoa_id)

        self.doctor_map.clear()
        self.doctor_map_reverse.clear()
        bac_si_names = []

        for bs in ds_bac_si:
            ten = bs['name']
            ma = bs['id']
            self.doctor_map[ten] = ma
            self.doctor_map_reverse[ma] = ten
            bac_si_names.append(ten)

        self.doctor_cb['values'] = bac_si_names
        self.doctor_cb.set("")

    # Lấy dữ liệu từ form
    def get_data(self):
        data = {k: e.get() for k, e in self.entries.items()}
        ten_khoa = data.get("khoa")
        data["khoa"] = self.khoa_map.get(ten_khoa)

        ten_bs = data.get("bac_si_id")
        data["bac_si_id"] = self.doctor_map.get(ten_bs)

        for key in ["phong_id", "giuong_id"]:
            try:
                data[key] = int(data[key]) if data[key] else None
            except ValueError:
                data[key] = None
        return data

    # Gán dữ liệu vào form
    def set_data(self, data):
        for k, v in data.items():
            if k not in self.entries:
                continue
            if k == "khoa":
                ten_khoa = self.khoa_map_reverse.get(v, "")
                self.entries[k].set(ten_khoa)
                self.load_doctors_by_khoa(v)  # Load bác sĩ tương ứng với khoa
            elif k == "bac_si_id":
                ten_bs = self.doctor_map_reverse.get(v, "")
                self.entries[k].set(ten_bs)
            else:
                self.entries[k].delete(0, tk.END)
                self.entries[k].insert(0, str(v) if v is not None else "")

    # Xóa trắng form
    def clear(self):
        for k, e in self.entries.items():
            if isinstance(e, ttk.Combobox):
                e.set("")
                if k == "bac_si_id":
                    e['values'] = []
            else:
                e.delete(0, tk.END)
