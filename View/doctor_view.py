import tkinter as tk
from tkinter import ttk, messagebox

class DoctorView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.pack(fill="both", expand=True)
        self.selected_doctor_id = None
        self.khoa_map = {}
        self.create_widgets()

    def create_widgets(self):
        # Tìm kiếm và lọc theo khoa
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill="x", padx=10, pady=5)
        tk.Label(filter_frame, text="Tìm kiếm:").pack(side="left")
        self.search_entry = tk.Entry(filter_frame)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(filter_frame, text="Tìm", command=self.on_search).pack(side="left", padx=5)

        tk.Label(filter_frame, text="Lọc theo khoa:").pack(side="left", padx=10)
        self.khoa_cb = ttk.Combobox(filter_frame, state="readonly")
        self.khoa_cb.pack(side="left")
        self.khoa_cb.bind("<<ComboboxSelected>>", self.on_filter_by_khoa)

        # Form nhập
        form = tk.LabelFrame(self, text="Thông tin bác sĩ")
        form.pack(fill="x", padx=10, pady=5)
        labels = ["Tên", "Giới tính", "Ngày sinh", "Địa chỉ", "SĐT", "Khoa"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(form, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            if label == "Khoa":
                self.khoa_form_cb = ttk.Combobox(form, state="readonly")
                self.khoa_form_cb.grid(row=i, column=1, padx=5, pady=2)
                self.entries["khoa"] = self.khoa_form_cb
            else:
                entry = tk.Entry(form)
                entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries[label.lower()] = entry

        # Nút chức năng
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(btn_frame, text="Thêm", command=self.on_add).pack(side="left")
        tk.Button(btn_frame, text="Cập nhật", command=self.on_update).pack(side="left")
        tk.Button(btn_frame, text="Xóa", command=self.on_delete).pack(side="left")
        tk.Button(btn_frame, text="Làm mới", command=self.clear_form).pack(side="left")

        # Bảng danh sách bác sĩ
        self.tree = ttk.Treeview(self, columns=("ID", "Tên", "Giới tính", "Ngày sinh", "Địa chỉ", "SĐT", "Khoa"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def set_khoa_list(self, ds_khoa):
        self.khoa_map = {k["ten_khoa"]: k["khoa_id"] for k in ds_khoa}
        khoa_names = list(self.khoa_map.keys())
        self.khoa_cb["values"] = ["Tất cả"] + khoa_names
        self.khoa_cb.set("Tất cả")
        self.khoa_form_cb["values"] = khoa_names

    def show_doctors(self, doctors):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for d in doctors:
            self.tree.insert("", "end", values=(
                d["id"], d["name"], d["gender"], d["ngaysinh"], d["diachi"], d["sdt"], d["khoa_id"]
            ))

    def get_form_data(self):
        data = {
            "name": self.entries["tên"].get(),
            "gender": self.entries["giới tính"].get(),
            "ngaysinh": self.entries["ngày sinh"].get(),
            "diachi": self.entries["địa chỉ"].get(),
            "sdt": self.entries["sđt"].get(),
            "khoa_id": self.khoa_map.get(self.entries["khoa"].get()),
        }
        if self.selected_doctor_id:
            data["bac_si_id"] = self.selected_doctor_id
        return data

    def clear_form(self):
        for e in self.entries.values():
            if isinstance(e, ttk.Combobox):
                e.set("")
            else:
                e.delete(0, tk.END)
        self.selected_doctor_id = None

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        vals = item["values"]
        self.selected_doctor_id = vals[0]
        self.entries["tên"].delete(0, tk.END)
        self.entries["tên"].insert(0, vals[1])
        self.entries["giới tính"].delete(0, tk.END)
        self.entries["giới tính"].insert(0, vals[2])
        self.entries["ngày sinh"].delete(0, tk.END)
        self.entries["ngày sinh"].insert(0, vals[3])
        self.entries["địa chỉ"].delete(0, tk.END)
        self.entries["địa chỉ"].insert(0, vals[4])
        self.entries["sđt"].delete(0, tk.END)
        self.entries["sđt"].insert(0, vals[5])
        # Tìm tên khoa theo id
        ten_khoa = ""
        for k, v in self.khoa_map.items():
            if v == vals[6]:
                ten_khoa = k
                break
        self.entries["khoa"].set(ten_khoa)

    def on_add(self):
        data = self.get_form_data()
        if not all(data.values()):
            self.show_message("Vui lòng nhập đầy đủ thông tin!", error=True)
            return
        self.controller.add_doctor(data)

    def on_update(self):
        if not self.selected_doctor_id:
            self.show_message("Vui lòng chọn bác sĩ để cập nhật!", error=True)
            return
        data = self.get_form_data()
        self.controller.update_doctor(data)

    def on_delete(self):
        if not self.selected_doctor_id:
            self.show_message("Vui lòng chọn bác sĩ để xóa!", error=True)
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa bác sĩ này?"):
            self.controller.delete_doctor(self.selected_doctor_id)

    def on_search(self):
        keyword = self.search_entry.get()
        if not keyword:
            self.controller.load_doctors()
        else:
            self.controller.load_doctors(keyword=keyword)

    def on_filter_by_khoa(self, event):
        ten_khoa = self.khoa_cb.get()
        if ten_khoa == "Tất cả":
            self.controller.load_doctors()
        else:
            khoa_id = self.khoa_map.get(ten_khoa)
            self.controller.load_doctors(khoa_id=khoa_id)

    def show_message(self, msg, error=False):
        if error:
            messagebox.showerror("Lỗi", msg)
        else:
            messagebox.showinfo("Thông báo", msg)