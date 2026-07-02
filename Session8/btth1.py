from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI()

carriers = [
    {"id": 1, "code": "GHN", "name": "Giao Hang Nhanh", "max_weight_capacity": 5000, "status": "ACTIVE"},
    {"id": 2, "code": "GHTK", "name": "Giao Hang Tiet Kiem", "max_weight_capacity": 3000, "status": "ACTIVE"},
    {"id": 3, "code": "VTP", "name": "Viettel Post", "max_weight_capacity": 10000, "status": "SUSPENDED"}
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]

#TODO: Handle Class
class CarrierStatus(str, Enum):
    ACTIVE= "ACTIVE"
    INACTIVE= "INACTIVE"
    SUSPENDED= "SUSPENDED"

class ShiftStatus(str, Enum):
    MORNING= "MORNING"
    AFTERNOON= "AFTERNOON"
    NIGHT= "NIGHT"

class CarrierCreate(BaseModel):
    code: str 
    name: str = Field(min_length=3)
    max_weight_capacity: int = Field(gt=0)
    status: CarrierStatus

class CarrierUpdate(BaseModel):
    code: str
    name: str = Field(min_length=3)
    max_weight_capacity: int = Field(gt=0)
    status: CarrierStatus

class ShipmentCreate(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(gt=0)
    dispatch_date: str
    shift: ShiftStatus

class ShipmentOut(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(gt=0)
    dispatch_date: str
    shift: ShiftStatus

#TODO: Handle Def
def generate_carrier_id(carriers):
    if not carriers:
        return 1
    carrier_id = max([carrier['id'] for carrier in carriers]) + 1
    return carrier_id    


#TODO: Handle API
@app.post("/carriers")
def create_carrier(carrier:CarrierCreate):

    check = [data for data in carriers if data['code'] == carrier.code]
    if check:
        raise HTTPException(500,detail="Code đã tồn tại!")
    
    if not carrier.name.strip():
        raise HTTPException(500, detail="Tên phải lớn hơn 3 và không được bỏ trống!")
    
    carriers.append({"id": generate_carrier_id(carriers), "code": carrier.code, 
                     "name": carrier.name, "max_weight_capacity": carrier.max_weight_capacity, "status": carrier.status})
    return {
        "message": "Tạo mới thành công!",
        "data": carrier
    }

@app.get("/carriers")
def get_carriers(keyword:str=None, status:str=None, min_weight:int=None):
    result = carriers
    if not result:
        raise HTTPException(200, f"Danh sách rỗng!")
    if keyword:
        result = [carrier for carrier in carriers if (keyword.upper().strip() in carrier['code'].upper().strip()
                                                       or keyword.upper().strip()) in carrier['name'].upper().strip()]
    if status:
        result = [carrier for carrier in carriers if carrier['status']==status]
    if min_weight:
        result = [carrier for carrier in carriers if carrier['max_weight_capacity']>=min_weight]
    return result

@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id:int):
    carrier = [carrier for carrier in carriers if carrier['id']==carrier_id]
    if not carrier:
        raise HTTPException(404, detail="Carrier not found")
    return carrier

@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id:int, carrier_data:CarrierUpdate):
    carrier = [carrier for carrier in carriers if carrier['id']==carrier_id]
    if not carrier:
        raise HTTPException(404, f"Không tìm thấy carrier có id là {carrier_id}")
    carrier[0]['code'] = carrier_data.code
    carrier[0]['name'] = carrier_data.name
    carrier[0]['max_weight_capacity'] = carrier_data.max_weight_capacity
    carrier[0]['status'] = carrier_data.status
    return carrier[0]

@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id:int):
    carrier = [carrier for carrier in carriers if carrier['id']==carrier_id]
    if not carrier:
        raise HTTPException(404, f"Không tìm thấy carrier có id là {carrier_id}")
    carriers.remove(carrier[0])
    return {
        "message":"Đã xóa thành công!"
    }

@app.post("/shipments")
def create_shipment(shipment:ShipmentCreate):
    carrier = [carrier for carrier in carriers if carrier['id'] == shipment.carrier_id]
    if not carrier:
        raise HTTPException(404, f"Không tìm thấy carrier có id là {shipment.carrier_id}")
    if shipment.total_weight > carrier[0]['max_weight_capacity']:
        raise HTTPException(500, f"Total weight phải nhỏ hơn {carrier['max_weight_capacity']}")
    if not(carrier[0]['status'] == "ACTIVE"):
        raise HTTPException(500, f"Carrier này đang không hoạt động!")
    shipments.append(shipment)
    return {
        "Message": "Thêm thành công!"
    }

@app.get("/shipments", response_model=list[ShipmentOut])
def get_shipments():
    return shipments