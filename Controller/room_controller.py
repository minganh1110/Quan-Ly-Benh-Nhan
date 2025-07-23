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