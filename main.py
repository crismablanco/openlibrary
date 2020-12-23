from fastapi import FastAPI, Response, status
import json

from settings import ENDPOINTS

from controllers import IsbnController, WorkController, SearchController, EditionController


app = FastAPI()

db = [] #dummy "DB"


@app.get('/')
def index():
  return {'Rocket' : 'Insights'}

@app.get('/books')
def get_books():
  return db

@app.get('/books/{isbn}', status_code=200)
def get_isbn(isbn: str, response: Response):
  b = IsbnController().find_by_isbn(isbn)
  print(b.status_code)
  if b.status_code == 200:
    return b.json()
  
  response.status_code = status.HTTP_404_NOT_FOUND
  return {'error' : 'There was a problem trying to get the book. ISBN not found'}

@app.post('/books', status_code=200)
def create_book(isbn: str, response: Response):
  b = IsbnController().find_by_isbn(isbn)
  if b.status_code == 200:
    db.append(b.json())
    return db[-1]

  response.status_code = status.HTTP_404_NOT_FOUND
  return {'error' : 'There was a problem trying to save. ISBN not found'}

@app.get('/works/{work_id}', status_code = 200)
def get_work(work_id: str, response: Response):
  editions = []
  w = WorkController().find_by_id(work_id)
  if w.status_code == 200:
    search = SearchController().find_by_anything(work_id).json()
    if search['num_found'] == 1:
      doc = search['docs'][0]
      if doc['type'] == 'work':
        for s in doc['seed']:
          if '/books/' in s:
            e = EditionController().find_by_book_id(s[6:])
            if e.status_code == 200:
              editions.append(e.json())

    r = {
      'work' : w.json(),
      'editions' : editions
    }
    return r

  response.status_code = status.HTTP_404_NOT_FOUND
  return {'error' : 'There was a problem trying to get the work. Work ID not found'}