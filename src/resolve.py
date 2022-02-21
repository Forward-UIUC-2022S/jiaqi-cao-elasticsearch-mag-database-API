from flask import request
from query import es_helper

def search_author_name():
    print("Searching...")
    return 200