from flask import request
from searcher.searcher import searcher
import json

seacher = searcher()

def get_affiliation():
    """
    Resolves the path /affiliations
    
    Returns:
        fetched json author object(s)
    """
    affiliation_name = request.args.get("affiliation-name")
    size = request.args.get("size")
    result = seacher.get_affiliation(affiliation_name, size)
    return result

def get_author_name_affiliation():
    """
    Resolves the path /author
    
    Returns:
        fetched json author object(s)
    """
    author_name = request.args.get("name")
    author_affiliation = request.args.get("affiliation")
    size = request.args.get("size")

    result = seacher.get_author(author_name, author_affiliation, size)
    return result

def get_author_for_paper():
    """
    Resolves the path /papers
    
    Returns:
        fetched json paper object(s)
    """
    author_name = request.args.get("author-name")
    author_affiliation = request.args.get("author-affiliation")
    paper_id = request.args.get("paperId")
    paper_title = request.args.get("paper-title")
    size = request.args.get("size")

    if paper_id != None or paper_title != None:
        result = seacher.get_paper(paper_title, paper_id, size)
    elif author_name == None:
        return "Bad request. You must provide an author name if paper ID is not provided.", 400
    else:
        result = seacher.get_paper_by_author(author_name, author_affiliation)
    
    return json.dumps(result)
                                                                  
def get_reference_paper():
    """
    Resolves the path /papers/references
    
    Returns:
        fetched json paper object(s)
    """
    paper_id = request.args.get("paperId")
    size = request.args.get("num-paper")
    cited = request.args.get("cited-by-papers", default=False, type=lambda v: v.lower() == 'true')

    result = seacher.get_reference_paper(paper_id, cited, size)
    return result

def get_papers_by_authors():
    """
    Resolves the path /papers/findByAuthor
    
    Returns:
        fetched json paper object(s)
    """
    names = request.args.get("names").split(',')
    affiliations = request.args.get("affiliations").split(',')
    results = []
    for i in range(len(names)):
        name = names[i].strip()
        affiliation = affiliations[i].strip()
        result = seacher.get_paper_by_author(name, affiliation if len(affiliation) != 0 else None)
        results += result
        print(name, affiliation, result)
    print(results)
    results = list({v['PaperId']:v for v in results}.values())
    return json.dumps(results)