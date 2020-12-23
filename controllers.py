import requests
from settings import ENDPOINTS

class IsbnController():
  def find_by_isbn(self, isbn: str):
    r = requests.get(f'{ENDPOINTS["isbn"]}{isbn}.json')
    return r

class WorkController():
  def find_by_id(self, id: str):
    r = requests.get(f'{ENDPOINTS["work"]}{id}.json')
    return r

class EditionController():
  def find_by_book_id(self, book_id: str):
    r = requests.get(f'{ENDPOINTS["edition"]}{book_id}.json')
    return r

class SearchController():
  def find_by_anything(self, to_search: str):
    r = requests.get(f'{ENDPOINTS["search"]}{to_search}')
    return r
    