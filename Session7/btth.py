from fastapi import FastAPI, status, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Dữ liệu nội bộ trong bộ nhớ tạm
promo_codes_db = {
    "SUMMER25": {"code": "SUMMER25", "discount_rate": 0.15, "max_budget": 50000000, "is_active": True},
    "WELCOME50": {"code": "WELCOME50", "discount_rate": 0.50, "max_budget": 10000000, "is_active": False}
}

# TODO: Handle Class
# Model nội bộ chứa cả trường ngân sách chiến dịch nhạy cảm (Cấm lộ)
class PromoInternal(BaseModel):
    code: str
    discount_rate: float
    max_budget: int # Trường nhạy cảm - Không được lộ ra Client!
    is_active: bool

class PromoPublic(BaseModel):
    code: str
    discount_rate: float

#TODO: Handle def
def create_reponse(status_code=None,data=None,error=None,message=None,path=None):
    return JSONResponse(status_code=status_code, content={
        "status_code":status_code,
        "data":data,
        "error":error,
        "message":message,
        "timestamp":datetime.now().isoformat(),
        "path":path,
    })

#TODO: API
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return create_reponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, message="Du lieu khong hop le", error=exc.errors()[0]['msg'], path=request.url.path)

@app.exception_handler(HTTPException)
def http_exception_handle(request: Request, exc: HTTPException):
    return create_reponse(status_code=exc.status_code, message=exc.detail, path=request.url.path)

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return create_reponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Data không lệ", path=request.url.path)

@app.get("/promos/{code}", response_model=PromoPublic)
def get_promos(code:str):
    promo_data = [value for value in promo_codes_db.values() if value['code']==code]
    if not promo_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mã giảm giá không tồn tại")
    if not promo_data[0]['is_active']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mã giảm giá đã hết hạn sử dụng")
    return promo_data[0]
