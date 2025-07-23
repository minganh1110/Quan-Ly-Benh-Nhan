from Model.room_entity import RoomEntity
from db.connect import get_connection
from typing import List, Dict

class RoomModel:
    def __init__(self):
        self.connection = get_connection()
    
    def add_room(self, so_phong: str, loai_phong: str, khoa_id: int, so_giuong:str) -> bool:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return False
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO phong (so_phong, loai_phong, khoa_id, so_giuong) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (so_phong, loai_phong, khoa_id,so_giuong))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Loi khi them phong:", e)
            return False
    def get_all_rooms(self) -> List[Dict]:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM phong"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print("Loi khi lay danh sach phong:", e)
            return []
    
    def delete_room(self, room_id: int) -> bool:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return False
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM phong WHERE id = %s"
            cursor.execute(query, (room_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Loi khi xoa phong:", e)
            return False
    
    def get_room_by_khoa_id(self, khoa_id: int) -> List[dict]:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, so_phong , loai_phong, so_giuong, khoa_id FROM phong WHERE khoa_id = %s"
            cursor.execute(query, (khoa_id,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print("Loi khi lay danh sach phong theo khoa:", e)
            return []
    def update_room(self, id: int, so_phong: str, loai_phong: str, khoa_id: int, so_giuong: str) -> bool:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return False
        try:
            cursor = self.connection.cursor()
            query = "UPDATE phong SET so_phong = %s, loai_phong = %s, khoa_id = %s, so_giuong = %s WHERE id = %s "
            cursor.execute(query, (so_phong, loai_phong, khoa_id,so_giuong, id))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Loi khi cap nhat phong:", e)
            return False
            
    def get_loai_phong_by_id(self, id: int) -> str:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return ""
        try:
            cursor = self.connection.cursor()
            query = "SELECT loai_phong FROM phong WHERE id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else ""
        except Exception as e:
            print("Loi khi lay loai phong theo id:", e)
            return ""
    def get_rooms_by_khoa_and_loai(self, khoa_id: int, loai_phong: str) -> List[Dict]:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, so_phong FROM phong WHERE khoa_id = %s AND loai_phong = %s"
            cursor.execute(query, (khoa_id, loai_phong))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print("Loi khi lay phong theo khoa_id va loai_phong:", e)
            return []
    
    def get_giuong_by_phong_id(self, phong_id: int) -> List[Dict]:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id FROM giuong WHERE phong_id = %s"
            cursor.execute(query, (phong_id,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print("Loi khi lay giuong theo phong_id:", e)
            return []

    def count_beds_in_room(self, room_id: int) -> int:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return 0
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM giuong WHERE phong_id = %s"
            cursor.execute(query, (room_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except Exception as e:
            print("Loi khi dem so giuong trong phong:", e)
            return 0
    
    def add_bed_to_room(self, phong_id: int) -> bool:
        if self.connection is None:
            print("Khong the ket noi co so du lieu.")
            return False
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO giuong (phong_id) VALUES (%s)"
            cursor.execute(query, (phong_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Loi khi them giuong vao phong:", e)
            return False