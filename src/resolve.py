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
    paper_id = request.args.get("paperID")
    if paper_id != None:
        result = es.search_paper(paper_id)
        return json.dumps(result)

    if author_affiliation == None:
        author_affiliation = ""    
    if author_name == None:
        return 400

    result = es.search_author_for_paper(author_name, author_affiliation)
    return json.dumps(result)
                                                                
def search_reference_paper():
    paper_id = request.args.get("paperID")
    size = request.args.get("num_paper")
    cited = request.args.get("referencing")
    size = 10 if size == None else size

    if cited != None:
        result = es.search_reference_paper(paper_id, cited = cited, size = size )
    else :
        result = es.search_reference_paper(paper_id, size = size)

    return json.dumps(result)

