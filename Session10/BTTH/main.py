# Import FastAPI và Depends để sử dụng Dependency Injection
from fastapi import FastAPI, Depends

# BaseModel dùng để tạo model nhận dữ liệu từ client
# Field dùng để cấu hình thêm cho các trường dữ liệu (ở đây chưa dùng)
from pydantic import BaseModel, Field

# Import Base
from model import Base

# Import hàm xử lý nghiệp vụ tạo shipment
from service import create_shipment

# Kiểu dữ liệu Session của SQLAlchemy
from sqlalchemy.orm import Session

# Hàm lấy Session kết nối database và lấy Engine để tạo bảng trong database
from database import get_db, engine

# Nếu bảng chưa tồn tại thì tự động tạo
# Nếu bảng đã có thì bỏ qua
Base.metadata.create_all(bind=engine)

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# API tạo mới Shipment
@app.post("/shipments")
def create_ship(

    # tracking_number được truyền qua Query Parameter
    tracking_number: str,

    # FastAPI tự gọi get_db() để lấy Session
    db: Session = Depends(get_db)
):

    # Gọi tầng Service để xử lý nghiệp vụ
    shipment = create_shipment(
        db=db,
        tracking_number=tracking_number
    )

    # Trả về dữ liệu cho client
    return {
        "status": shipment.status,
        "tracking_number": shipment.tracking_number
    }
