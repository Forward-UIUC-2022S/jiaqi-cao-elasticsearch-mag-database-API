from flask import request
from query import es_helper
import json

es = es_helper()

def search_author_name_affiliation():
    author_name = request.args.get("author_name")
    author_affiliation = request.args.get("author_affiliation")
    if author_affiliation == None:
        result = es.search_author(author_name, size = 10)
    else:
        result = es.search_author_affiliation(author_name, author_affiliation)

    return json.dumps(result)

def search_author_for_paper():
    author_name = request.args.get("author_name")
    author_affiliation = request.args.get("author_affiliation")
    if author_affiliation == None:
        author_affiliation = ""
    
    result = es.search_author_for_paper(author_name, author_affiliation)
    return json.dumps(result)