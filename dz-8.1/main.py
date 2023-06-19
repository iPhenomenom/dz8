from mongoengine import connect
from models import Author, Quote

connect(
    db="cluster0",
    username="user",# использовал свой Username
    password="password", # Использовал свой Password
    host="mongodb+srv://Username:password@cluster0.r636yxn.mongodb.net/?retryWrites=true&w=majority"
)

from load_data import load_authors, load_quotes

load_authors('C:/Users/user/Desktop/GOIT DZ/дз8/authors.json')
load_quotes('C:/Users/user/Desktop/GOIT DZ/дз8/quotes.json')

def search():
    while True:
        command = input("Enter command:")
        if command == 'exit':
            break
        command, value = command.split(':')
        if command == 'name':
            author = Author.objects(fullname=value).first()
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        elif command == 'tag':
            quotes = Quote.objects(tags=value)
            for quote in quotes:
                print(quote.quote)
        elif command == 'tags':
            tags = value.split(',')
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(quote.quote)

search()
