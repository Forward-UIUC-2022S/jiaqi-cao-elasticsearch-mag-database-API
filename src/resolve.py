from flask import request
from searcher.searcher import searcher
import json

seacher = searcher()

def search_affiliation():
    """
    Resolves the path /search_author
    
    Returns:
        fetched json author object(s)
    """
    affiliation_name = request.args.get("affiliation_name")
    size = request.args.get("size")
    result = seacher.get_affiliation(affiliation_name, size)
    return result

def search_author_name_affiliation():
    """
    Resolves the path /search_author
    
    Returns:
        fetched json author object(s)
    """
    author_name = request.args.get("author_name")
    author_affiliation = request.args.get("author_affiliation")
    size = request.args.get("size")
    result = seacher.get_author(author_name, author_affiliation, size)
    return result

def search_author_for_paper():
    """
    Resolves the path /search_paper
    
    Returns:
        fetched json paper object(s)
    """
    author_name = request.args.get("author_name")
    author_affiliation = request.args.get("author_affiliation")
    paper_id = request.args.get("paperID")
    paper_title = request.args.get("paper_title")
    size = request.args.get("size")

    if paper_id != None or paper_title != None:
        result = seacher.get_paper(paper_title, paper_id, size)
    elif author_name == None:
        return "Bad request. You must provide an author name if paper ID is not provided.", 400
    else:
        result = seacher.get_paper_by_author(author_name, author_affiliation, size = size)
    
    return result

"""
/search_reference_paper
"""                                                                   
def search_reference_paper():
    paper_id = request.args.get("paperID")
    size = request.args.get("num_paper")
    cited = request.args.get("cited_by_papers", default=False, type=lambda v: v.lower() == 'true')

    result = seacher.get_reference_paper(paper_id, cited, size)
    return result
