from flask import request
from query import es_helper
import json

es = es_helper()

def search_author_name(author_name):
    print("Searching for author {} in path {}".format(author_name, request.path))
    result = es.search_author(name = author_name)
    return json.dumps(result)

def search_author_name_affiliation(author_name, author_affiliation):
    print("Searching for author {} from {} in path {}".format(author_name, author_affiliation, request.path))
    result = es.search_author_affiliation(author_name, author_affiliation)
    return json.dumps(result)