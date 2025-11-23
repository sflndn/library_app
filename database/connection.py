from models.books import Book

books_storage = []
current_book_id = 1

def get_all_books():
    return books_storage

def get_book_by_id(book_id: int):
    for book in books_storage:
        if book.id == book_id:
            return book
    return None

def create_book(book_data: dict):
    global current_book_id
    book_data["id"] = current_book_id
    book = Book(**book_data)
    books_storage.append(book)
    current_book_id += 1
    return book

def update_book(book_id: int, update_data: dict):
    for index, book in enumerate(books_storage):
        if book.id == book_id:
            updated_data = book.model_dump()
            updated_data.update({k: v for k, v in update_data.items() if v is not None})
            updated_book = Book(**updated_data)
            books_storage[index] = updated_book
            return updated_book
    return None

def delete_book(book_id: int):
    for index, book in enumerate(books_storage):
        if book.id == book_id:
            return books_storage.pop(index)
    return None

def search_books_by_title(title: str):
    return [book for book in books_storage if title.lower() in book.title.lower()]

def get_books_by_author(author: str):
    return [book for book in books_storage if author.lower() in book.author.lower()]

def get_books_by_genre(genre: str):
    return [book for book in books_storage if genre.lower() in book.genre.lower()]

def get_books_by_read_status(is_read: bool):
    return [book for book in books_storage if book.is_read == is_read]

if not books_storage:
    test_books = [
        {
            "id": 1,
            "title": "Преступление и наказание",
            "author": "Федор Достоевский", 
            "year": 1866,
            "genre": "Роман",
            "is_read": True,
            "rating": 5,
            "description": "Философский роман о моральных дилеммах"
        },
        {
            "id": 2, 
            "title": "Мастер и Маргарита",
            "author": "Михаил Булгаков",
            "year": 1967,
            "genre": "Роман",
            "is_read": False,
            "rating": None,
            "description": "Мистический роман о добре и зле"
        },
        {
            "id": 3,
            "title": "Война и мир",
            "author": "Лев Толстой",
            "year": 1869,
            "genre": "Роман-эпопея", 
            "is_read": True,
            "rating": 4,
            "description": "Масштабное произведение о войне 1812 года"
        }
    ]
    for book_data in test_books:
        books_storage.append(Book(**book_data))
    current_book_id = 4