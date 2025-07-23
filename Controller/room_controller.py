from Model.room_model import RoomModel
from Model.khoa_model import KhoaModel
from View.room_view import RoomView

class RoomController:
    def __init__(self, root):
        self.model = RoomModel()
        self.khoa_model = KhoaModel()
        self.view = RoomView(root, self)
        self.load_khoa()
        self.load_rooms()

    def load_khoa(self):
        ds_khoa = self.khoa_model.get_all_khoa()
        self.view.set_khoa_list(ds_khoa)

    def load_rooms(self, khoa_id=None, keyword=None):
        if khoa_id:
            rooms = self.model.get_room_by_khoa_id(khoa_id)
        elif keyword:
            rooms = [r for r in self.model.get_all_rooms() if keyword.lower() in str(r["so_phong"]).lower()]
        else:
            rooms = self.model.get_all_rooms()
        self.view.show_rooms(rooms)

    def add_room(self, data):
        if self.model.add_room(data["so_phong"], data["loai_phong"], data["khoa_id"], data["so_giuong"]):
            self.view.show_message("Thêm phòng thành công!")
            self.load_rooms()
            self.view.clear_form()
        else:
            self.view.show_message("Thêm phòng thất bại!", error=True)

    def update_room(self, data):
        if self.model.update_room(data["id"], data["so_phong"], data["loai_phong"], data["khoa_id"], data["so_giuong"]):
            self.view.show_message("Cập nhật phòng thành công!")
            self.load_rooms()
            self.view.clear_form()
        else:
            self.view.show_message("Cập nhật phòng thất bại!", error=True)


    def delete_room(self, room_id):
        if self.model.delete_room(room_id):
            self.view.show_message("Xóa phòng thành công!")
            self.load_rooms()
            self.view.clear_form()
        else:
            self.view.show_message("Xóa phòng thất bại!", error=True)
    
    def add_bed_to_room(self, room_id, so_giuong_them):
        # Lấy số giường tối đa từ bảng phong
        room = next((r for r in self.model.get_all_rooms() if r["id"] == room_id), None)
        if not room:
            self.view.show_message("Không tìm thấy phòng!", error=True)
            return
        try:
            so_giuong_toi_da = int(room["so_giuong"])
        except Exception:
            self.view.show_message("Dữ liệu số giường tối đa không hợp lệ!", error=True)
            return

        # Đếm số giường hiện tại trong DB
        so_giuong_hien_tai = self.model.count_beds_in_room(room_id)
        if so_giuong_hien_tai + so_giuong_them > so_giuong_toi_da:
            self.view.show_message(
                f"Phòng đã đủ giường ({so_giuong_hien_tai}/{so_giuong_toi_da}). Không thể thêm {so_giuong_them} giường!",
                error=True
            )
            return

        # Thêm giường vào DB (chỉ cần truyền phong_id)
        if not self.model.add_bed_to_room(room_id):
            self.view.show_message("Có lỗi khi thêm giường!", error=True)
        else:
            self.view.show_message("Đã thêm 1 giường vào phòng.")
            self.load_rooms()