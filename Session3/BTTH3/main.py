from fastapi import FastAPI

app = FastAPI()

books = [{
    "id": 6,
    "title": "FastAPI Basic",
    "author": "Nguyen Van A",
    "category": "abc",
    "year": 2026,
    "is_available": True
},
{
    "id": 2,
    "title": "FastAPI Basic",
    "author": "Nguyen Van A",
    "category": "web",
    "year": 2023,
    "is_available": False
},
{
    "id": 1,
    "title": "FastAPI Basic",
    "author": "Nguyen Van A",
    "category": "web",
    "year": 2024,
    "is_available": True
},
{
    "id": 3,
    "title": "FastAPI Basic",
    "author": "Nguyen Van A",
    "category": "web",
    "year": 2021,
    "is_available": False
}]
@app.get("/books/statistics")
def get_statistics():
    available_books = 0
    borrowed_books = 0
    total_books = 0
    for book in books:
        total_books += 1
        if book['is_available']:
            available_books += 1
        else:
            borrowed_books += 1
    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books
    }

@app.get("/books/categories")
def get_categories():
    categories_data = []
    for book in books:
        categories_data.append(book['category'])
    return {
        "categories":list(set(categories_data))
    }

@app.get("/books/latest")
def get_book():
    if not books:
        return {
                "message": "No books available"
            }
    yearly_book = books[0]
    for book in books:
        if yearly_book['year'] < book['year']:
            yearly_book = book
    return yearly_book
