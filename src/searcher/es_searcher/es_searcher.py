from elasticsearch import Elasticsearch
import csv 
import re

class es_searcher:
    def __init__(self):
        self.es = Elasticsearch([{'host': "128.174.136.27", 'port': 9500}], http_auth = ('elastic', 'forwarddatalab'))

    def hits_processor(self, results):
        """
        Args:
            results: result body from search

        Returns: 
            A list of results in dictionary
        """
        result_list = []
        hits = results["hits"]["hits"]

        if len(hits) != 0:
            for i in range(len(hits)):  
                print("result", i, ":")
                result = hits[i]["_source"]
                print(result)
                result_list.append(result)

        else:
            print("No hits found")

        return result_list

    def search_affiliation(self, affil : str, size = 1) -> list:
        """ 
        Args:
            affil (string): name of affiliation
            size (int): number of result wanted to return

        Returns: 
            A list of result body from elasticsearch whose displayed name matches affil
                that's parsed by hits_processor
        """
        body = {
                "bool": {
                    "must": [
                        {"match": {
                        "DisplayName": affil
                        }}
                    ]
                }
            }
        
        results = self.es.search(query = body, index = "affiliations", size = size)

        return self.hits_processor(results)

    def search_author(self, name : str, size = 1) -> list:
        """ 
        Args:
            name (string): name of author
            size (int): number of result wanted to return

        Returns: 
            A list of result body from elasticsearch whose displayed name matches author
                that's parsed by hits_processor
        """
        body = {
                "bool": {
                    "must": [
                        {"match": {
                        "DisplayName": name
                        }}
                    ]
                }
            }
        results = self.es.search(query = body, index = "authors", size = size)

        return self.hits_processor(results)

    def search_author_affiliation(self, name : str, affil : str, size = 1) -> list:
        """ 
        Args:
            name (string): name of the author
            affil (string): affiliation of the author
            size (int): number of result wanted to return

        Returns:
            the first hit body as a dict in the result body from elasticsearch, else empty dict
        """
        affil_hits = self.search_affiliation(affil)

        if len(affil_hits):
            affil_id = affil_hits[0]["AffiliationId"]

            body = {"bool": {
                            "must": [
                                {"match": {
                                "DisplayName": name
                                }},
                                {
                                "match": {
                                    "LastKnownAffiliationId.keyword": affil_id
                                }
                                }
                            ]
                            }
                        }
            results = self.es.search(query = body, index = "authors", size = size)

            hits = self.hits_processor(results)
            print(type(hits))
            return hits

        else:
            print("Affiliation {} not found".format(affil))

        return dict()
    
    def search_paper_title(self, paper_title : str, size = 10):
        """
        Args:
            paper_title (string): title of paper to be searched
            size (int): default to 10, max size of data returned

        Returns: 
            search resutls of searching given title
        """
        body = {
            "match" : {
                "OriginalTitle" : paper_title
            }
        }
        print(body)

        results = self.es.search(query = body, index = "papers", size = size)

        return self.hits_processor(results)


def get_affil_author():
    """
    Returns: list of [index, affiliation, name] lists of the CS faculty dataset
    """
    with open("R1R2_research_college_cs_faculty.csv") as file:
        reader = csv.reader(file)
        uni_name = list(reader)
    print("successfully get",len(uni_name)," items")
    # first line is the heading 
    return uni_name[1:]

def get_hit_list_faculty(name_idx = "authors", affil_index = "affiliations"):
    """  
    Returns: list of [name, affil, hits from search_author_affiliation] lists of the CS faculty dataset
    """
    result_list = []
    affil_name = get_affil_author()
    es = es_helper()

    for _, affil, name in affil_name:
        hits = es.search_author_affiliation(name = name, affil = affil, name_idx = name_idx, affil_index = affil_index)
        result_list.append([name, affil, hits])

    return result_list

def write_hits_to_file(result_list, file_name_csv = ""):
    """ 
    Args:
        result_list (list): result returns from get_hit_list
        file_name (string): the file that the result list stores to
    
    Returns:
        None
    """
    valid_list = []
    authorid = []
    for result in result_list:    
        name, affil, data = result
        if len(data) != 0:
            valid_list.append(name + ";" + affil + ";" + str(data))
            authorid.append([name,affil,data["LastKnownAffiliationId"], data["AuthorId"]])
    with open(file_name_csv, "w") as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow(["name", "affiliation", "LastKnownAffiliationId", "AuthorId"])
        writer.writerows(authorid)
    
    with open("author_id_with_data", "w") as f:
        for i in valid_list:
            f.write(i+"\n")
    
    print("successfully convert ", len(valid_list) ," items to file {}".format(file_name_csv))
    print("there are " , len(authorid) , " affiliation id")


if __name__ == "__main__":
    es = es_searcher()
    
    # Modify this line for testing purposes
    # print(es.search_reference_paper_id("1977714272", cited = False, size = 20))
    print(es.search_author(name = "abdussalam alawini"))
    # result = es.search_author_for_reference_paper(name = "abdussalam alawini", affil = "university of illinois at urbana champaign")
    # result = es.search_author_for_reference_paper(name = "Marty Banks", affil = "University of california Berkeley")
    # print("**" *20)
    # for i in result:
    #     print(i["PaperReference"])

    
    
    