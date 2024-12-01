import random

TAXES = 0.19
MIN_REVIEWS = 0
MAX_REVIEWS = 20
MIN_STOCK = 0
MAX_STOCK = 30

AUTHORS = [
    "Gabriel García Márquez", "Mario Vargas Llosa", "J.K. Rowling", "George Orwell",
    "Jane Austen", "F. Scott Fitzgerald", "Haruki Murakami", "William Shakespeare",
    "Charles Dickens", "Virginia Woolf", "Mark Twain", "Leo Tolstoy",
    "Franz Kafka", "Ernest Hemingway", "Emily Dickinson", "Toni Morrison",
    "Isabel Allende", "Miguel de Cervantes", "Oscar Wilde", "Homer"
]

def getAuthor():
    return random.choice(AUTHORS)

def parseRating(rating):
    if rating == "One":
        return 1
    elif rating == "Two":
        return 2
    elif rating == "Three":
        return 3
    elif rating == "Four":
        return 4
    elif rating == "Five":
        return 5
    else:
        return None  # En caso de que no sea una calificación válida

def process(bookInfo):
    priceBeforeTaxes = bookInfo["priceBeforeTaxes"]
    priceAfterTaxes = bookInfo["priceAfterTaxes"]
    reviews = bookInfo["reviews"]
    quantity = bookInfo["quantity"]
    rating = bookInfo["rating"]

    taxes = priceBeforeTaxes * TAXES
    priceAfterTaxes = priceBeforeTaxes + taxes
    reviews = random.randint(MIN_REVIEWS, MAX_REVIEWS)
    quantity = random.randint(MIN_STOCK, MAX_STOCK)
    author = getAuthor()
    rating = parseRating(rating)

    bookInfo["priceAfterTaxes"] = priceAfterTaxes
    bookInfo["taxes"] = taxes
    bookInfo["reviews"] = reviews
    bookInfo["quantity"] = quantity
    bookInfo["author"] = author
    bookInfo["rating"] = rating