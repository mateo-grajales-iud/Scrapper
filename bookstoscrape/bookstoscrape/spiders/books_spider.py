import scrapy
import json
import logging
from ..persistance.SaveToDatabaseHelper import SaveToDatabaseHelper
from pathlib import Path

# Clase principal que define el spider de Scrapy para extraer información de libros.
class BooksSpiderSpider(scrapy.Spider):

    name = "books_spider"
    pattern = r"page-(\d+)\.html"
    baseUrl = "http://books.toscrape.com/catalogue/"

    articlesList = []
    
    # Método que se ejecuta al iniciar el spider, se encarga de hacer la primera solicitud.
    def start_requests(self):
        urls = [
            "http://books.toscrape.com/catalogue/page-1.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Método que se encarga de procesar la respuesta de cada página del catálogo.
    def parse(self, response):
        logging.debug(f"Parsing catalog site {response.url}")
        articles = response.css("article.product_pod")
        for article in articles:
            bookUrl = article.css("div.image_container a::attr(href)").get()
            yield scrapy.Request(url=self.baseUrl + bookUrl, callback=self.parseBook)
        pager = response.css("ul.pager")
        next = pager.css("li.next")
        href = next.css("a::attr(href)").get()
        if href:
            newUrl = self.baseUrl + href
            yield scrapy.Request(url=newUrl, callback=self.parse)
        else:
            self.saveArticles()
        pass

    # Método que se encarga de procesar la respuesta de cada página de libro individual.
    def parseBook(self, response):
        logging.debug(f"Parsing book site {response.url}")
        title = self.getBookTitle(response)
        rows = response.css("table.table.table-striped tr")
        self.cleanAndSave(title, rows)

    # Método para extraer el título del libro desde la página.
    def getBookTitle(self, response):
        title = response.css("h1::text").get()
        return title

    # Método que organiza y guarda la información del libro.
    def cleanAndSave(self, title, rows):
        newArticle = { "title" : title}
        for row in rows:
            key, value = self.cleanRow(row)
            newArticle[key] = value
        self.save(newArticle)

    # Método que procesa cada fila de la tabla, limpiando la clave y el valor.
    def cleanRow(self, row):
        key =  self.cleanKey(row.css("th::text").get())
        value = self.cleanValue(key, row.css("td::text").get())
        return key, value
    
    # Método para limpiar las claves de la tabla y normalizarlas.
    def cleanKey(self, key):
        if key == "UPC":
            return "upc"
        elif key == "Product Type":
            return "type"
        elif key == "Price (excl. tax)":
            return "priceBeforeTaxes"
        elif key == "Price (incl. tax)":
            return "priceAfterTaxes"
        elif key == "Tax":
            return "taxes"
        elif key == "Availability":
            return "quantity"
        elif key == "Number of reviews":
            return "reviews"
        return key
    
    # Método para limpiar los valores de la tabla según la clave.
    def cleanValue(self, key, value):
        try: 
            if key.startswith("price") or key == "taxes":
                return float(value.replace("\u00a3", ""))
            elif key == "quantity":
                return int(value.replace("In stock (", "").replace(" available)", ""))
            elif key == "reviews":
                return int(value)
            return value
        except Exception as e:
            logging.error(f"Error cleaning {key} : {value}")
            return None
    
    # Método que guarda un artículo en la lista interna de artículos.
    def save(self, newArticle):
        logging.debug(f"Parsed {newArticle}")
        self.articlesList.append(newArticle)

    # Método que guarda todos los artículos extraídos en un archivo y en la base de datos.
    def saveArticles(self):
        self.saveToFile()
        self.saveToDatabase()

    # Método que guarda los artículos en un archivo JSON.
    def saveToFile(self):
        logging.debug("Saving to file")
        output_file = Path("scraped_books.json")
        with open(output_file, 'w') as f:
            json.dump(self.articlesList, f, indent=4)
        logging.debug(f"Saved {len(self.articlesList)} articles in {output_file}")

    # Método que guarda los artículos en la base de datos.
    def saveToDatabase(self):
        logging.debug("Saving to database")
        saver = SaveToDatabaseHelper(10)
        saver.saveToDatabase(self.articlesList)