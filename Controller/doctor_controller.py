from Model.bac_si_model import DoctorModel
from Model.khoa_model import KhoaModel
from View.doctor_view import DoctorView

class DoctorController:
    def __init__(self, root):
        self.model = DoctorModel()
        self.khoa_model = KhoaModel()
        self.view = DoctorView(root, self)
        self.load_doctors()
        self.load_khoa()

    def load_doctors(self, khoa_id=None, keyword=None):
        if khoa_id:
            doctors = self.model.get_doctors_by_khoa_id(khoa_id)
        elif keyword:
            doctors = [d for d in self.model.get_all_doctors() if keyword.lower() in d["name"].lower()]
        else:
            doctors = self.model.get_all_doctors()
        self.view.show_doctors(doctors)

    def load_khoa(self):
        ds_khoa = self.khoa_model.get_all_khoa()
        self.view.set_khoa_list(ds_khoa)

    def add_doctor(self, data):
        from Model.bac_si_entity import Doctor
        doctor = Doctor(**data)
        if self.model.add_doctor(doctor):
            self.view.show_message("Thêm bác sĩ thành công!")
            self.load_doctors()
            self.view.clear_form()
        else:
            self.view.show_message("Thêm bác sĩ thất bại!", error=True)

    def update_doctor(self, data):
        from Model.bac_si_entity import Doctor
        doctor = Doctor(**data)
        if self.model.update_doctor(doctor):
            self.view.show_message("Cập nhật bác sĩ thành công!")
            self.load_doctors()
            self.view.clear_form()
        else:
            self.view.show_message("Cập nhật bác sĩ thất bại!", error=True)

    def delete_doctor(self, doctor_id):
        if self.model.delete_doctor(doctor_id):
            self.view.show_message("Xóa bác sĩ thành công!")
            self.load_doctors()
            self.view.clear_form()
        else:
            self.view.show_message("Xóa bác sĩ thất bại!", error=True)