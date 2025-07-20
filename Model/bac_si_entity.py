from Model.person import Person
from typing import Optional

class Doctor(Person):
    def __init__(
        self,
        name: str,
        gender: str,
        ngaysinh: str,
        diachi: str,
        sdt: str,
        bac_si_id: Optional[int] = None,
        khoa_id: Optional[int] = None,
    ):
        super().__init__(name, gender, ngaysinh, diachi, sdt)
        self.bac_si_id = bac_si_id
        self.khoa_id = khoa_id