from flask import request
from query import es_helper
import json

es = es_helper()

"""
/search_author
"""
def search_author_name_affiliation():
    author_name = request.args.get("author_name")
    author_affiliation = request.args.get("author_affiliation")
    size = int(request.args.get("size"))

    if author_affiliation == None:
        if size:
            result = es.search_author(author_name, size = size)
        else:
            result = es.search_author(author_name)
    else:
        if size:
            result = es.search_author_affiliation(author_name, author_affiliation, size = size)
        else:
            result = es.search_author_affiliation(author_name, author_affiliation)

    return json.dumps(result)

"""
/search_paper
"""
def search_author_for_paper():
    author_name = request.args.get("author_name")
    author_affiliation = request.args.get("author_affiliation")
    paper_id = request.args.get("paperID")
    paper_title = request.args.get("paper_title")
    size = int(request.args.get("size"))
    size = 10 if size == None else size

    if paper_title != None:
        result = es.search_paper_title(paper_title, size = size)
        return json.dumps(result)

    if paper_id != None:
        result = es.search_paper(paper_id, size = size)
        return json.dumps(result)

    if author_affiliation == None:
        author_affiliation = ""    
    if author_name == None:
        return "Bad request. You must provide an author name if paper ID is not provided.", 400

    result = es.search_author_for_paper(author_name, author_affiliation, size = size)
    return json.dumps(result)

"""
/search_reference_paper
"""                                                                   
def search_reference_paper():
    paper_id = request.args.get("paperID")
    size = request.args.get("num_paper")
    cited = request.args.get("referencing", default=False, type=lambda v: v.lower() == 'true')
    size = 10 if size == None else int(size)

    if cited != None:
        result = es.search_reference_paper(paper_id, cited = cited, size = size )
    else :
        result = es.search_reference_paper(paper_id, size = size)

    return json.dumps(result)

