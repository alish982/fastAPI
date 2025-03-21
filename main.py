from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id: UUID
    author: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)

BOOKS = []

@app.get('/')
def read_api():
    return BOOKS

Books = []

@app.post('/')
def create_api(book: Book):
    BOOKS.append(book)
    return book

@app.delete('/{book_id}')
def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"deleted book of id: {book_id}"
    raise HTTPException(
        status_code=404,
        detail=f"couldn't find {book_id}"
    )

@app.put('/{book_id}')
def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1 ] = book
            return BOOKS[counter - 1]
    raise HTTPException(
        status_code = 404,
        detail=f"Book of {book_id} updated successfully"
    )