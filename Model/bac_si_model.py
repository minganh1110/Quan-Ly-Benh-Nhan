from db.connect import get_connection
from Model.bac_si_entity import Doctor
from typing import List, Dict

class DoctorModel: 
    def __init__(self):
        self.connection = get_connection()
    
    def add_doctor(self, doctor: Doctor) -> bool:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return False

        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO thongtinbacsi
                (name, gender, ngaysinh, diachi, sdt, khoa_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                doctor.name,
                doctor.gender,
                doctor.ngaysinh,
                doctor.diachi,
                doctor.sdt,
                doctor.khoa_id
            ))
            self.connection.commit()
            cursor.close()
            return True

        except Exception as e:
            print("Loi khi them bac si:", e)
            return False
    
    def get_all_doctors(self) -> List[Dict]:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM thongtinbacsi"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result

        except Exception as e:
            print("Loi khi lay danh sach bac si:", e)
            return []
    
    def get_doctors_by_khoa_id(self, khoa_id: int) -> List[Dict]:
        if self.connection is None:
            print("Không thể kết nối đến cơ sở dữ liệu.")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, name FROM thongtinbacsi WHERE khoa_id = %s"
            cursor.execute(query, (khoa_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print("Lỗi khi lấy danh sách bác sĩ theo khoa:", e)
            return []
    
    def update_doctor(self, doctor: Doctor) -> bool:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return False
        try:
            cursor = self.connection.cursor()
            query = """
                UPDATE thongtinbacsi
                SET name = %s, gender = %s, ngaysinh = %s, diachi = %s, sdt = %s, khoa_id = %s
                WHERE bac_si_id = %s
            """
            cursor.execute(query, (
                doctor.name,
                doctor.gender,
                doctor.ngaysinh,
                doctor.diachi,
                doctor.sdt,
                doctor.khoa_id,
                doctor.bac_si_id
            ))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Loi khi cap nhat bac si:", e)
            return False
    def delete_doctor(self, doctor_id: int) -> bool:
        if self.connection is None:
            print("Khong the ket noi den co so du lieu.")
            return False
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM thongtinbacsi WHERE bac_si_id = %s"
            cursor.execute(query, (doctor_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Loi khi xoa bac si:", e)
            return False        