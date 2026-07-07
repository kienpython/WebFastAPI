from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from model import ShipmentModel

# Get_db => chay đến khi nào gặp yield => tạm dừng => Chạy hàm xử lý CS => đoạn sau của yield
def create_shipment(tracking_number:str, db:Session):
    check_exits_shipment = db.query(ShipmentModel).filter(ShipmentModel.tracking_number == tracking_number).first()
    if check_exits_shipment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã vận đơn này đã được khởi tạo trước đó")
    new_shipment = ShipmentModel(tracking_number=tracking_number)
    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)
    return new_shipment
