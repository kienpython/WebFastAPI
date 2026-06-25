# 1. Định nghĩa Enum để giới hạn danh mục hợp lệ (Ngăn chặn nhập bậy)
class Genre(str, Enum):
    action = "action"
    romance = "romance"
    comedy = "comedy"

# Sử dụng Path Parameter kết hợp Enum
@app.get("/genres/{genre_name}")
def get_comics_by_genre(genre_name: Genre):
    # Nếu client truyền vào /genres/horror, FastAPI sẽ báo lỗi 422 ngay lập tức
    return {"genre": genre_name, "message": f"Thể loại {genre_name} hợp lệ."}

# 2. Sử dụng Path Parameter kết hợp Validation chuyên sâu với class Path
@app.get("/comics/{comic_id}")
def get_comic_detail(
    # Bắt buộc truyền (...), phải lớn hơn hoặc bằng 1 (ge=1)
    comic_id: int = Path(..., title="Mã truyện", ge=1, description="ID phải là số dương")
):
    # Nhờ FastAPI tự động validate, code tại đây đảm bảo 100% comic_id là số hợp lệ
    return {"status": "success", "comic_id": comic_id}