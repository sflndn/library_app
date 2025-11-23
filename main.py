from fastapi import FastAPI, Request, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
import routes.books as books_routes
from fastapi.templating import Jinja2Templates
import urllib.parse

templates = Jinja2Templates(directory="templates")

def urlencode_filter(s):
    return urllib.parse.quote_plus(str(s))

templates.env.filters["urlencode"] = urlencode_filter

app = FastAPI(
    title="Personal Library API",
    description="API для управления персональной библиотекой книг",
    version="1.0.0"
)

app.include_router(books_routes.router, prefix="/api/books", tags=["books"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/books/add", response_class=HTMLResponse)
async def add_book_page(request: Request):
    return templates.TemplateResponse("add_book.html", {
        "request": request,
        "title": "Добавить книгу"
    })


@app.post("/books/add")
async def add_book_submit(
        request: Request,
        title: str = Form(...),
        author: str = Form(...),
        year: int = Form(...),
        genre: str = Form(...),
        description: str = Form(""),
        rating: str = Form("")
):
    from routes.books import books_db
    from models.books import Book

    try:
        book_rating = int(rating) if rating else None

        new_book = Book(
            id=len(books_db) + 1,
            title=title,
            author=author,
            year=year,
            genre=genre,
            description=description,
            rating=book_rating,
            is_read=False
        )

        books_db.append(new_book)

        return RedirectResponse(f"/books/{new_book.id}?success=true", status_code=303)

    except Exception as e:
        return templates.TemplateResponse("add_book.html", {
            "request": request,
            "error": f"Ошибка при добавлении книги: {str(e)}",
            "form_data": {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "description": description,
                "rating": rating
            }
        })


@app.get("/books", response_class=HTMLResponse)
async def books_page(
        request: Request,
        is_read: Optional[bool] = Query(None),
        genre: Optional[str] = Query(None),
        author: Optional[str] = Query(None)
):
    from routes.books import books_db

    filtered_books = books_db
    if is_read is not None:
        filtered_books = [book for book in filtered_books if book.is_read == is_read]
    if genre:
        filtered_books = [book for book in filtered_books if genre.lower() in book.genre.lower()]
    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book.author.lower()]

    return templates.TemplateResponse("books.html", {
        "request": request,
        "books": filtered_books
    })


@app.get("/books/{book_id}/edit", response_class=HTMLResponse)
async def edit_book_page(request: Request, book_id: int):
    from routes.books import books_db

    book = next((book for book in books_db if book.id == book_id), None)
    if not book:
        return RedirectResponse("/books")

    return templates.TemplateResponse("edit_book.html", {
        "request": request,
        "book": book,
        "title": f"Редактировать {book.title}"
    })


@app.post("/books/{book_id}/edit")
async def edit_book_submit(
        request: Request,
        book_id: int,
        title: str = Form(...),
        author: str = Form(...),
        year: int = Form(...),
        genre: str = Form(...),
        description: str = Form(""),
        rating: str = Form(""),
        is_read: bool = Form(False)
):
    from routes.books import books_db
    from models.books import Book

    book = next((book for book in books_db if book.id == book_id), None)
    if not book:
        return RedirectResponse("/books")

    try:
        book_rating = int(rating) if rating else None

        updated_book = Book(
            id=book_id,
            title=title,
            author=author,
            year=year,
            genre=genre,
            description=description,
            rating=book_rating,
            is_read=is_read
        )

        books_db[books_db.index(book)] = updated_book

        return RedirectResponse(f"/books/{book_id}?success=true", status_code=303)

    except Exception as e:
        return templates.TemplateResponse("edit_book.html", {
            "request": request,
            "book": book,
            "error": f"Ошибка при обновлении книги: {str(e)}"
        })


@app.get("/books/{book_id}", response_class=HTMLResponse)
async def book_detail(request: Request, book_id: int):
    from routes.books import books_db

    book = next((book for book in books_db if book.id == book_id), None)
    if not book:
        return RedirectResponse("/books")

    return templates.TemplateResponse("book_detail.html", {
        "request": request,
        "book": book
    })


@app.get("/books/{book_id}/read")
async def mark_book_read_web(book_id: int):
    from routes.books import books_db
    for index, book in enumerate(books_db):
        if book.id == book_id:
            updated_data = book.model_dump()
            updated_data["is_read"] = True
            from models.books import Book
            books_db[index] = Book(**updated_data)
            break
    return RedirectResponse(f"/books/{book_id}")


@app.get("/books/{book_id}/unread")
async def mark_book_unread_web(book_id: int):
    from routes.books import books_db
    for index, book in enumerate(books_db):
        if book.id == book_id:
            updated_data = book.model_dump()
            updated_data["is_read"] = False
            from models.books import Book
            books_db[index] = Book(**updated_data)
            break
    return RedirectResponse(f"/books/{book_id}")


@app.get("/books/author/{author}", response_class=HTMLResponse)
async def books_by_author_page(request: Request, author: str):
    from routes.books import books_db

    import urllib.parse
    author_decoded = urllib.parse.unquote(author)

    author_books = [
        book for book in books_db
        if author_decoded.lower() in book.author.lower()
    ]

    return templates.TemplateResponse("books.html", {
        "request": request,
        "books": author_books,
        "title": f"Книги автора: {author_decoded}"
    })


@app.get("/books/genre/{genre}", response_class=HTMLResponse)
async def books_by_genre_page(request: Request, genre: str):
    from routes.books import books_db

    import urllib.parse
    genre_decoded = urllib.parse.unquote(genre)

    genre_books = [
        book for book in books_db
        if genre_decoded.lower() in book.genre.lower()
    ]

    return templates.TemplateResponse("books.html", {
        "request": request,
        "books": genre_books,
        "title": f"Книги жанра: {genre_decoded}"
    })


@app.get("/stats", response_class=HTMLResponse)
async def stats_page(request: Request):
    from routes.books import books_db

    total_books = len(books_db)
    read_books = len([book for book in books_db if book.is_read])
    unread_books = total_books - read_books

    genre_stats = {}
    for book in books_db:
        if book.genre in genre_stats:
            genre_stats[book.genre] += 1
        else:
            genre_stats[book.genre] = 1

    author_stats = {}
    for book in books_db:
        if book.author in author_stats:
            author_stats[book.author] += 1
        else:
            author_stats[book.author] = 1

    return templates.TemplateResponse("stats.html", {
        "request": request,
        "total_books": total_books,
        "read_books": read_books,
        "unread_books": unread_books,
        "completion_rate": f"{(read_books / total_books) * 100:.1f}%" if total_books > 0 else "0%",
        "genre_stats": genre_stats,
        "author_stats": author_stats
    })


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Personal Library API работает!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)