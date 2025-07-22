import tkinter as tk
from tkinter import ttk
from Model.khoa_model import KhoaModel
from Model.bac_si_model import DoctorModel
from Model.room_model import RoomModel
class PatientForm(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Thông tin bệnh nhân")
        self.entries = {}
        self.khoa_map = {}          # ánh xạ tên khoa → id
        self.khoa_map_reverse = {}  # ánh xạ id → tên khoa
        self.doctor_map = {}        # ánh xạ tên bác sĩ → id
        self.doctor_map_reverse = {}# ánh xạ id → tên bác sĩ
        self.room_map = {}           # tên phòng → id
        self.room_map_reverse = {}   # id → tên phòng

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


        # Combobox Loại phòng
        tk.Label(stay_frame, text="Loại phòng").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.room_type_cb = ttk.Combobox(stay_frame, values=["VIP", "Normal", "Hồi sức"], state="readonly")
        self.room_type_cb.grid(row=1, column=1, padx=5, pady=2)
        self.room_type_cb.bind("<<ComboboxSelected>>", self.on_loai_phong_selected)
        self.entries["loai_phong"] = self.room_type_cb


        # Combobox Phòng
        tk.Label(stay_frame, text="Phòng").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.room_cb = ttk.Combobox(stay_frame, state="readonly")
        self.room_cb.grid(row=0, column=1, padx=5, pady=2)
        self.room_cb.bind("<<ComboboxSelected>>", self.on_phong_selected)
        self.entries["phong_id"] = self.room_cb  # vẫn dùng key là phong_id để get_data đồng nhất

        # Entry Giường ID giữ nguyên
        tk.Label(stay_frame, text="Giường ID").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.giuong_cb = ttk.Combobox(stay_frame, state="readonly")
        self.giuong_cb.grid(row=2, column=1, padx=5, pady=2)
        self.entries["giuong_id"] = self.giuong_cb  # key giữ nguyên để dễ dùng


    # Sự kiện chọn khoa
    def on_khoa_selected(self, event):
        ten_khoa = self.entries["khoa"].get()
        khoa_id = self.khoa_map.get(ten_khoa)
        self.load_doctors_by_khoa(khoa_id)
        self.load_rooms_by_khoa(khoa_id)

    # Sự kiện chọn loại phòng
    def on_loai_phong_selected(self, event):
        ten_khoa = self.entries["khoa"].get()
        loai_phong = self.entries["loai_phong"].get()

        if not ten_khoa or not loai_phong:
            return  # Không có khoa hoặc loại phòng thì không làm gì

        khoa_id = self.khoa_map.get(ten_khoa)
        if khoa_id is None:
            return

        room_model = RoomModel()
        ds_phong = room_model.get_rooms_by_khoa_and_loai(khoa_id, loai_phong)
        print(">>> Danh sách phòng theo khoa và loại:", ds_phong)

        self.room_map.clear()
        self.room_map_reverse.clear()
        phong_names = []

        for p in ds_phong:
            so_phong = p["so_phong"]
            phong_id = p["id"]
            self.room_map[so_phong] = phong_id
            self.room_map_reverse[phong_id] = so_phong
            phong_names.append(so_phong)

        self.room_cb['values'] = phong_names
        self.room_cb.set("")
    # Sự kiện chọn phòng
    def on_phong_selected(self, event):
        so_phong = self.entries["phong_id"].get()
        print(">>> Sự kiện chọn phòng:", so_phong)
        if not so_phong:
            return
        sophongint = int(so_phong)  # Chuyển đổi sang int nếu cần
        phong_id = self.room_map.get(sophongint)
        print(">>> ID phòng đã chọn:", phong_id)
        if not phong_id:
            return

        room_model = RoomModel()
        ds_giuong = room_model.get_giuong_by_phong_id(phong_id)
        print(">>> Danh sách giường theo phòng:", ds_giuong)
        giuong_values = [str(gid['id']) for gid in ds_giuong]
        self.giuong_cb['values'] = giuong_values
        self.giuong_cb.set(giuong_values[0] if giuong_values else "")



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
    # Load danh sách phòng theo khoa
    def load_rooms_by_khoa(self, khoa_id):
        room_model = RoomModel()
        ds_phong = room_model.get_room_by_khoa_id(khoa_id)
        print(">>> Danh sách phòng lấy theo khoa:", ds_phong)
        self.room_map.clear()
        self.room_map_reverse.clear()
        phong_names = []

        for p in ds_phong:
            sophong = p["so_phong"]
            phong_id = p["id"]
            self.room_map[sophong] = phong_id
            self.room_map_reverse[phong_id] = sophong
            phong_names.append(sophong)

        self.room_cb['values'] = phong_names
        self.room_cb.set("")

    # Lấy dữ liệu từ form
    def get_data(self):
        data = {k: e.get() for k, e in self.entries.items()}
        ten_khoa = data.get("khoa")
        data["khoa"] = self.khoa_map.get(ten_khoa)

        ten_bs = data.get("bac_si_id")
        data["bac_si_id"] = self.doctor_map.get(ten_bs)

        sophong = data.get("phong_id")
        so_phongint= int(sophong)
        data["phong_id"] = self.room_map.get(so_phongint)
        
        
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
                self.load_rooms_by_khoa(v)
            elif k == "bac_si_id":
                ten_bs = self.doctor_map_reverse.get(v, "")
                self.entries[k].set(ten_bs)
            elif k == "phong_id":
                so_phong = self.room_map_reverse.get(v, "")
                self.entries[k].set(so_phong)

                if v:
                    room_model = RoomModel()
                    loai_phong = room_model.get_loai_phong_by_id(v)
                    self.entries["loai_phong"].set(loai_phong)
            elif k == "giuong_id":
                self.entries[k].set(str(v))
            else:
                self.entries[k].delete(0, tk.END)
                self.entries[k].insert(0, str(v) if v is not None else "")

    # Xóa trắng form
    def clear(self):
        for k, e in self.entries.items():
            if isinstance(e, ttk.Combobox):
                e.set("")
                if k in ["bac_si_id","phong_id"]:
                    e['values'] = []
            else:
                e.delete(0, tk.END)
