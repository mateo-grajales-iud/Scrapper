import logging
from .SqlLiteConnector import SqlLiteConnector

class SaveToDatabaseHelper:

    database = None
    __DATABASE_TO_USE = "SQLITE"

    def __init__(self, batchSize):
        self.database = None
        self.batchSize = batchSize

    def saveToDatabase(self, articles):
        logging.debug(f"Saving articles: {len(articles)}")
        sql = self.getConnector()
        sql.openConnection()
        sql.setupTable()
        for article in articles:
            self.saveArticle(sql, article)

    def getConnector(self):
        if self.__DATABASE_TO_USE == "SQLITE":
            return SqlLiteConnector()
        raise ValueError("Invalid connector")
    
    def saveArticle(self, sql, article):
        logging.debug("Running queries")
        sql.insertArticle(article)
