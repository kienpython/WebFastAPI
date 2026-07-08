from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, status
from main import app
from service import create_response

@app.exception_handler(RequestValidationError)
def validation_exception_handle(request: Request, exc: RequestValidationError):
    return create_response(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, message="Data không hợp lệ!", path=request.url.path)

@app.exception_handler(HTTPException)
def http_exception_handle(request: Request, exc: HTTPException):
    return create_response(status_code=exc.status_code, errors=exc.detail, path=request.url.path)

@app.exception_handler(Exception)
def exception_handle(request: Request, exc: Exception):
    return create_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, errors="Lỗi hệ thống!", path=request.url.path)
