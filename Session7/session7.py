from fastapi import FastAPI, status, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
app = FastAPI()

# Dữ liệu nội bộ trong bộ nhớ tạm
promo_codes_db = {
    "SUMMER25": {"code": "SUMMER25", "discount_rate": 0.15, "max_budget": 50000000, "is_active": True},
    "WELCOME50": {"code": "WELCOME50", "discount_rate": 0.50, "max_budget": 10000000, "is_active": False}
}

# Model nội bộ chứa cả trường ngân sách chiến dịch nhạy cảm (Cấm lộ)
class PromoInternal(BaseModel):
    code: str
    discount_rate: float
    max_budget: int # Trường nhạy cảm - Không được lộ ra Client!
    is_active: bool

class PromoPublic(BaseModel):
    code: str
    discount_rate: float

def create_reponse(status_code, data=None, error=None, message=None, path=None):
    return JSONResponse(content={
        "status_code":status_code,
        "data":data,
        "error":error,
        "message":message,
        "timestamp":datetime.utcnow().isoformat(),
        "path":path,
    },
    status_code=status_code)

@app.exception_handler(HTTPException)
def http_exception_handle(request:Request, exc:HTTPException):
    return create_reponse(exc.status_code, message=exc.detail, path = request.url.path)

@app.exception_handler(Exception)
def global_exception_handle(request:Request, exc:Exception):
    return create_reponse(500, message="Hệ thống gặp sự số, vui lòng thử lại sau!", path=request.url.path)

@app.exception_handler(RequestValidationError)
def validation_exception_handle(request:Request, exc: HTTPException):
    return create_reponse(422, message="Dữ liệu không hợp lệ!", error=exc.errors(), path=request.url.path)

@app.get("/promos/{code}", response_model=PromoPublic)
def get_promos(code:str):
    check = False
    for key, value in promo_codes_db.items():
        if not (value['code'] == code):
            continue
        check = True
        if not value['is_active']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã giảm giá đã hết hạn sử dụng")
        return value
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mã giảm giá không tồn tại")
