from .es_searcher.es_searcher import es_searcher
from .sql_searcher.sql_searcher import sql_searcher
import json

class searcher:
    def __init__(self):
        self.sql = sql_searcher()
        self.es = es_searcher()
    
    def get_author(self, author_name, author_affiliation : str, size : str):
        """
        Args:
            author_name (string): name of author to be searched for 
            author_affiliation (string): optional affiliation of the author
            size (string): optional number of objects to return 
        
        Returns:
            Author object(s) matching the name and/or affiliation
        """
        if author_affiliation == None:
            result = self.es.search_author(author_name, size = int(size) if size != None else 1)
        else:
            result = self.es.search_author_affiliation(author_name, author_affiliation,size = int(size) if size != None else 1)
        return json.dumps(result)
    
    def get_paper(self, paper_title : str, paper_id : str, size : str):
        """
        Args:
            paper_title (string): optional title of paper to be searched for 
            paper_id (string): optional if of the paper
            size (string): optional number of objects to return 
        
        Returns:
            Paper object(s) matching the title or id
        """
        if paper_id != None:
            result = self.sql.search_paper_id(paper_id)
        else:
            result = self.es.search_paper_title(paper_title, size = int(size) if size != None else 10)
        
        return json.dumps(result)
    
    def get_paper_by_author(self, author_name, author_affiliation : str, size : str):
        """
        Args:
            author_name (string): name of author to be searched for 
            author_affiliation (string): optional affiliation of the author
            size (string): optional number of objects to return 
        
        Returns:
            Paper object(s) 
        """
        if author_affiliation == None:
            authors = self.es.search_author(author_name, size = int(size) if size != None else 1)
        else:
            authors = self.es.search_author_affiliation(author_name, author_affiliation,size = int(size) if size != None else 1)
        
        if len(authors):
            result = self.sql.search_author_id_for_papers(authors[0]["AuthorId"])
            return json.dumps(result)
        
        return list()
    
    def get_reference_paper(self, paper_id : str, cited_by : bool, size : str):
        """
        Args:
            paper_id (string): optional if of the paper
            cited_by (bool): whether the papers cited the given paper are wanted 
            size (string): optional number of objects to return 
        
        Returns:
            Paper object(s) 
        """
        size = int(size) if size != None else 10
        result = self.sql.search_paper_for_references(paper_id, size, cited_by)
        return json.dumps(result)

