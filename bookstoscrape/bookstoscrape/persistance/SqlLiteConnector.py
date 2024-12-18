import logging
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float

class SqlLiteConnector:

    engine = None
    database = "bookScraper.db"
    meta = MetaData()
    books = None

    def openConnection(self):
        self.engine = create_engine(f"sqlite:///{self.database}", echo=False)

    def setupTable(self):
        logging.debug("Setting up table")
        logging.debug("Connected to database")
        self.createTable()

    def setBooksTable(self):
        self.books = Table("books", self.meta,
                      Column("title", String, nullable=False),
                      Column("upc", String, nullable=False, primary_key=True),
                      Column("type", String, nullable=False),
                      Column("priceBeforeTaxes", Float, nullable=True),
                      Column("priceAfterTaxes", Float, nullable=True),
                      Column("taxes", Float, nullable=True),
                      Column("quantity", Integer, nullable=True),
                      Column("reviews", Integer, nullable=True),
                      Column("rating", Integer, nullable=True),
                      Column("author", String, nullable=True))

    def createTable(self):
        logging.debug("Creating table")
        self.setBooksTable()
        self.meta.create_all(self.engine)

    def insertArticle(self, article):
        logging.debug("Creating query")
        with self.engine.connect() as connection:
            upsert = self.createUpsert(connection, article)
            connection.execute(upsert)
            connection.commit()
        logging.debug("Query commited")

    def createUpsert(self, connection, article):
        if self.bookExists(connection, article):
            return self.createUpdate(article)
        else:
            return self.createInsert(article)

    def createUpdate(self, article):
        return self.books.update().where(self.books.c.upc == article["upc"]).values(article)
    
    def createInsert(self, article):
        return self.books.insert().values(article)

    def bookExists(self, connection, article):
        select = self.books.select().where(self.books.c.upc == article["upc"])
        result = connection.execute(select).fetchall()
        return len(result) > 0