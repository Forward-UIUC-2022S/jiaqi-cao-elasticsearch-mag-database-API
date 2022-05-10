import mysql.connector
import os
import time
from tqdm import trange
import json

class sql_searcher:
    def __init__(self):
        self.db = mysql.connector.connect(
            user=os.getenv('MYSQL_USER'), 
            password=os.getenv('MYSQL_PASS'), 
            host="mag-2020-09-14.mysql.database.azure.com", 
            port=3306, 
            database=os.getenv('MYSQL_DB'), 
            ssl_ca="DigiCertGlobalRootCA.crt.pem", 
            ssl_disabled=False
        )

    def write_table_to_csv(self, table : str, path : str):
        """
        Args:
            table : name of the table 
            path : path the csv goes
        """
        sql = "SELECT * FROM {};".format(table)
        with self.db.cursor(dictionary=True) as cursor: 
            cursor.execute(sql)
            rows = cursor.fetchmany(size = 1000)
            with open(path, 'w') as f:
                while rows is not None:
                    for row in rows:
                        json.dump(row, f)
                        f.write('\n')
                    rows = cursor.fetchmany(size = 1000)

    def search_paper_id(self, paper_id : str) -> list:
        """
        Args:
            paper_id (string): Id of paper to be searched
        
        Returns:
            Fetched paper of the given ID 
        """
        sql = "SELECT * FROM papers WHERE PaperId = " +  paper_id + ";"
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def search_author_id(self, author_id : str) -> list:
        """
        Args:
            author_id (string): Id of author to be searched
        
        Returns:
            Fetched author of the given ID 
        """
        sql = "SELECT * FROM authors WHERE AuthorId = " +  author_id + ";"
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    
    def search_affiliation_id(self, affiliation_id : str) -> list:
        """
        Args:
            affiliation_id (string): Id of affiliation to be searched
        
        Returns:
            Fetched affiliation of the given ID 
        """
        sql = "SELECT * FROM affiliations WHERE AffiliationId = " +  affiliation_id + ";"
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    
    def search_author_id_for_papers(self, author_id : str) -> list:
        """
        Args:
            author_id (string): Id of author to be searched
        
        Returns:
            Fetched paper objects that are published by the author
        """
        sql = "SELECT * FROM papers p INNER JOIN (SELECT PaperId from paperauthoraffiliations where AuthorId = {}) AS pa ON p.PaperId = pa.PaperId;".format(author_id)
        with self.db.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    
    def search_paper_for_references(self, paper_id : str, size : str, cited_by = False) -> list:
        """
        Args:
            paper_id (string): Id of paper to be searched
            cited_by (bool): whether the papers cited the given paper are wanted
            size (string): number of objects to return 
        
        Returns:
            Fetched paper objects that are referenced/referencing by the given paper
        """
        sql = "SELECT * FROM papers p INNER JOIN (SELECT {} FROM paperreferences WHERE {} = {}) pr ON p.PaperId = pr.{} LIMIT {};".format("PaperId" if cited_by else "PaperReferenceId", "PaperReferenceId" if cited_by else "PaperId", paper_id, "PaperId" if cited_by else "PaperReferenceId", size)
        # sql = "describe paperreferences"
        with self.db.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
                           
# path = "/srv/local/data/scratch/jiaqic7/paper_abstract.txt"
# table = "paperabstracts"
# searcher = sql_searcher()
# searcher.write_table_to_csv(table, path)

# print(searcher.search_paper_id("197771427"))
#print(searcher.search_author_id_for_papers("69314847"))
#print(searcher.search_paper_for_references("1977714272", False))

