from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from model import ShipmentModel


# Hàm tạo mới một mã vận đơn
def create_shipment(tracking_number: str, db: Session):

    # Kiểm tra xem mã vận đơn đã tồn tại trong database hay chưa
    # db.query(...)      : Truy vấn bảng ShipmentModel
    # .filter(...)       : Điều kiện WHERE tracking_number = ...
    # .first()           : Lấy bản ghi đầu tiên nếu có, không có thì trả về None
    check_exists_shipment = (
        db.query(ShipmentModel)
        .filter(ShipmentModel.tracking_number == tracking_number)
        .first()
    )

    # Nếu tìm thấy mã vận đơn thì báo lỗi
    if check_exists_shipment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã vận đơn này đã được khởi tạo trước đó"
        )

    # Tạo một đối tượng Shipment mới
    # Lúc này dữ liệu mới chỉ nằm trong RAM, chưa lưu xuống database
    new_shipment = ShipmentModel(
        tracking_number=tracking_number
    )

    # Đưa đối tượng vào Session
    db.add(new_shipment)

    # Ghi dữ liệu xuống database (INSERT)
    db.commit()

    # Đọc lại dữ liệu từ database
    # Để lấy các giá trị được database tự sinh (ví dụ: id)
    db.refresh(new_shipment)

    # Trả về dữ liệu vừa tạo
    return new_shipment