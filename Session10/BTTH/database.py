# Import các thành phần cần thiết của SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# Chuỗi kết nối đến database MySQL
# Cú pháp:
# mysql+pymysql://username:password@host:port/database_name
DATABASE_URL = "mysql+pymysql://root:Kientkls01@localhost:3306/ecommerce_db"

# Tạo Engine - giống như "cầu nối" giữa ứng dụng và database
engine = create_engine(DATABASE_URL)

# Tạo một "nhà máy" sinh ra các Session
# Mỗi Session sẽ dùng để làm việc với database (SELECT, INSERT, UPDATE, DELETE)
SessionLocal = sessionmaker(
    autocommit=False,   # Không tự động lưu dữ liệu, phải gọi db.commit()
    autoflush=False,    # Không tự động gửi thay đổi xuống database
    bind=engine         # Gắn Session với Engine ở trên
)

# Hàm tạo và quản lý kết nối database
def get_db():
    # Tạo một Session mới
    db = SessionLocal()
    try:
        # Trả Session cho FastAPI sử dụng
        # Endpoint sẽ nhận được biến db thông qua Depends(get_db)
        yield db
    finally:
        # Sau khi endpoint chạy xong (dù thành công hay lỗi)
        # luôn đóng kết nối để tránh bị rò rỉ tài nguyên
        db.close()