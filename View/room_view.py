import tkinter as tk
from tkinter import ttk, messagebox

class RoomView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.pack(fill="both", expand=True)
        self.selected_room_id = None
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
        form = tk.LabelFrame(self, text="Thông tin phòng")
        form.pack(fill="x", padx=10, pady=5)
        labels = ["Số phòng", "Loại phòng", "Số giường", "Khoa"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(form, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            if label == "Khoa":
                self.khoa_form_cb = ttk.Combobox(form, state="readonly")
                self.khoa_form_cb.grid(row=i, column=1, padx=5, pady=2)
                self.entries["khoa"] = self.khoa_form_cb
            elif label == "Loại phòng":
                self.loai_phong_cb = ttk.Combobox(form, values=["Normal", "VIP", "Hồi Sức"], state="readonly")
                self.loai_phong_cb.grid(row=i, column=1, padx=5, pady=2)
                self.entries["loai_phong"] = self.loai_phong_cb
            elif label == "Số giường":
                entry = tk.Entry(form)
                entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries["so_giuong"] = entry
            else:
                entry = tk.Entry(form)
                entry.grid(row=i, column=1, padx=5, pady=2)
                self.entries["so_phong"] = entry

        # Nút chức năng
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(btn_frame, text="Thêm", command=self.on_add).pack(side="left")
        tk.Button(btn_frame, text="Cập nhật", command=self.on_update).pack(side="left")
        tk.Button(btn_frame, text="Xóa", command=self.on_delete).pack(side="left")
        tk.Button(btn_frame, text="Làm mới", command=self.clear_form).pack(side="left")

        # Bảng danh sách phòng
        self.tree = ttk.Treeview(self, columns=("ID", "Số phòng", "Loại phòng", "Số giường", "Khoa"), show="headings")
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

    def show_rooms(self, rooms):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rooms:
            self.tree.insert("", "end", values=(
                r["id"], r["so_phong"], r["loai_phong"], r["so_giuong"], r["khoa_id"]
            ))

    def get_form_data(self):
        data = {
            "so_phong": self.entries["so_phong"].get(),
            "loai_phong": self.entries["loai_phong"].get(),
            "khoa_id": self.khoa_map.get(self.entries["khoa"].get()),
            "so_giuong": self.entries["so_giuong"].get(),
        }
        if self.selected_room_id:
            data["id"] = self.selected_room_id
        return data

    def clear_form(self):
        for e in self.entries.values():
            if isinstance(e, ttk.Combobox):
                e.set("")
            else:
                e.delete(0, tk.END)
        self.selected_room_id = None

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        vals = item["values"]
        self.selected_room_id = vals[0]
        self.entries["so_phong"].delete(0, tk.END)
        self.entries["so_phong"].insert(0, vals[1])
        self.entries["loai_phong"].set(vals[2])
        self.entries["so_giuong"].delete(0, tk.END)
        self.entries["so_giuong"].insert(0, vals[3])
        # Tìm tên khoa theo id
        ten_khoa = ""
        for k, v in self.khoa_map.items():
            if v == vals[4]:
                ten_khoa = k
                break
        self.entries["khoa"].set(ten_khoa)

    def on_add(self):
        data = self.get_form_data()
        if not all([data["so_phong"], data["loai_phong"], data["khoa_id"], data["so_giuong"]]):
            self.show_message("Vui lòng nhập đầy đủ thông tin!", error=True)
            return
        self.controller.add_room(data)

    def on_update(self):
        if not self.selected_room_id:
            self.show_message("Vui lòng chọn phòng để cập nhật!", error=True)
            return
        data = self.get_form_data()
        self.controller.update_room(data)

    def on_delete(self):
        if not self.selected_room_id:
            self.show_message("Vui lòng chọn phòng để xóa!", error=True)
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa phòng này?"):
            self.controller.delete_room(self.selected_room_id)

    def on_search(self):
        keyword = self.search_entry.get()
        if not keyword:
            self.controller.load_rooms()
        else:
            self.controller.load_rooms(keyword=keyword)

    def on_filter_by_khoa(self, event):
        ten_khoa = self.khoa_cb.get()
        if ten_khoa == "Tất cả":
            self.controller.load_rooms()
        else:
            khoa_id = self.khoa_map.get(ten_khoa)
            self.controller.load_rooms(khoa_id=khoa_id)

    def show_message(self, msg, error=False):
        if error:
            messagebox.showerror("Lỗi", msg)
        else:
            messagebox.showinfo("Thông báo", msg)