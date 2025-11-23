from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.books import Book, BookCreate, BookUpdate

router = APIRouter()

books_db = [
    Book(
        id=1,
        title="Преступление и наказание",
        author="Федор Достоевский",
        year=1866,
        genre="Роман",
        is_read=True,
        rating=5,
        description="Философский роман о моральных дилеммах"
    ),
    Book(
        id=2,
        title="Мастер и Маргарита",
        author="Михаил Булгаков",
        year=1967,
        genre="Роман",
        is_read=False,
        rating=None,
        description="Мистический роман о добре и зле"
    ),
    Book(
        id=3,
        title="Война и мир",
        author="Лев Толстой",
        year=1869,
        genre="Роман-эпопея",
        is_read=True,
        rating=4,
        description="Масштабное произведение о войне 1812 года"
    )
]


@router.get("/", response_model=List[Book])
def get_all_books(
        is_read: Optional[bool] = Query(None, description="Фильтр по статусу прочтения"),
        genre: Optional[str] = Query(None, description="Фильтр по жанру"),
        author: Optional[str] = Query(None, description="Фильтр по автору")
):
    filtered_books = books_db

    if is_read is not None:
        filtered_books = [book for book in filtered_books if book.is_read == is_read]

    if genre:
        filtered_books = [book for book in filtered_books if genre.lower() in book.genre.lower()]

    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book.author.lower()]

    return filtered_books


@router.get("/{book_id}", response_model=Book)
def get_book_by_id(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail=f"Книга с ID {book_id} не найдена"
    )


@router.post("/", response_model=Book, status_code=201)
def create_new_book(book_data: BookCreate):
    new_book = Book(
        id=len(books_db) + 1,
        **book_data.model_dump()
    )

    books_db.append(new_book)
    return new_book


@router.put("/{book_id}", response_model=Book)
def update_book_info(book_id: int, book_update: BookUpdate):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            update_data = book_update.model_dump(exclude_unset=True)
            updated_data = book.model_dump()
            updated_data.update(update_data)
            updated_book = Book(**updated_data)
            books_db[index] = updated_book
            return updated_book

    raise HTTPException(
        status_code=404,
        detail=f"Книга с ID {book_id} не найдена"
    )


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            books_db.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Книга с ID {book_id} не найдена"
    )


@router.get("/search/{title}", response_model=List[Book])
def search_books_by_title(title: str):
    found_books = [
        book for book in books_db
        if title.lower() in book.title.lower()
    ]

    if not found_books:
        raise HTTPException(
            status_code=404,
            detail=f"Книги с названием '{title}' не найдены"
        )

    return found_books


@router.get("/author/{author}", response_model=List[Book])
def get_books_by_author(author: str):
    author_books = [
        book for book in books_db
        if author.lower() in book.author.lower()
    ]

    if not author_books:
        raise HTTPException(
            status_code=404,
            detail=f"Книги автора '{author}' не найдены"
        )

    return author_books


@router.get("/genre/{genre}", response_model=List[Book])
def get_books_by_genre(genre: str):
    genre_books = [
        book for book in books_db
        if genre.lower() in book.genre.lower()
    ]

    if not genre_books:
        raise HTTPException(
            status_code=404,
            detail=f"Книги жанра '{genre}' не найдены"
        )

    return genre_books


@router.patch("/{book_id}/read", response_model=Book)
def mark_book_as_read(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            updated_data = book.model_dump()
            updated_data["is_read"] = True
            updated_book = Book(**updated_data)
            books_db[index] = updated_book
            return updated_book

    raise HTTPException(
        status_code=404,
        detail=f"Книга с ID {book_id} не найдена"
    )


@router.patch("/{book_id}/unread", response_model=Book)
def mark_book_as_unread(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            updated_data = book.model_dump()
            updated_data["is_read"] = False
            updated_book = Book(**updated_data)
            books_db[index] = updated_book
            return updated_book

    raise HTTPException(
        status_code=404,
        detail=f"Книга с ID {book_id} не найдена"
    )