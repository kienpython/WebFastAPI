# Import các kiểu dữ liệu để tạo bảng trong database
from sqlalchemy import Column, Integer, String

# Import class Base để các Model kế thừa
from sqlalchemy.orm import declarative_base

# Tạo class Base
# Mọi Model (bảng) trong project sẽ kế thừa từ Base này
Base = declarative_base()


# Tạo Model tương ứng với bảng "shipments" trong database
class ShipmentModel(Base):

    # Tên bảng trong MySQL
    __tablename__ = "shipments"

    # Cột id
    # Integer: kiểu số nguyên
    # primary_key=True: khóa chính của bảng
    id = Column(Integer, primary_key=True)

    # Cột tracking_number
    # String(50): chuỗi tối đa 50 ký tự
    # unique=True: không được phép trùng nhau
    # nullable=False: bắt buộc phải có dữ liệu (không được để NULL)
    tracking_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    # Cột status
    # Nếu không truyền giá trị khi tạo mới,
    # SQLAlchemy sẽ tự gán là "PREPARING"
    status = Column(
        String(50),
        default="PREPARING"
    )