import json
from models import Author, Quote

def load_authors(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        for author_data in data:
            author = Author(**author_data)
            author.save()

def load_quotes(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        for quote_data in data:
            author = Author.objects(fullname=quote_data['author']).first()
            quote = Quote(author=author, quote=quote_data['quote'], tags=quote_data['tags'])
            quote.save()
