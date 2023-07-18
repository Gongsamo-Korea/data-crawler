import json
from elasticsearch import Elasticsearch
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

host = config['DEFAULT']['ELASTIC_HOST'] 
port = config['DEFAULT']['ELASTIC_PORT'] 



es = Elasticsearch('http://'+host+':'+port)
class conectToES:
    def insertData(result_hash):
        index="articles"
        
    
        doc = {
            "title" : result_hash['title'],
            "issueNumber" : result_hash['issue_number'],
            "issueDate" : result_hash['issue_date'],
            "content" : result_hash['content'],
            "tableOfContent" : result_hash['table_of_content'],
            "tags" : []
        }

        if result_hash['tags'] is not None:
            tags_list = []
            for tag in result_hash['tags'] : 
                dict = {"tagName" : tag}
                tags_list.append(dict)

            doc["tags"].extend(tags_list)
        
        es.index(index="articles", body=doc)

    def updateData(result_hash, doc_id):
        update_data = {
            "doc": {
                "content": result_hash['content'],
                "tableOfContent": result_hash['table_of_content'],
                "issueDate" : result_hash['issue_date']
            }
        }

        es.update(index='articles', id=doc_id, body=update_data)
        print(doc_id + ' updated')

    def updateTags(doc_id, tag_list):
        if tag_list is not None:
            update_data = {
                "doc" : {
                    "tags": []
                }
            }
            tags_list = []
            for tag in tag_list : 
                dict = {"tagName" : tag}
                tags_list.append(dict)

            update_data["doc"]["tags"].extend(tags_list)
            es.update(index='articles', id=doc_id, body=update_data)
            print(doc_id+ " 's tag is updated")


    def getDocId(title,issue_number):
        index = "articles"
        query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "title": title
                        }
                    },
                    {
                        "match": {
                            "issueNumber": issue_number
                        }
                    }
                ]
            }
        },
        
            "fields": [
                "articleId"
            ],
            "_source": False
    }

        result = es.search(index=index, body=query)

        doc_id = result["hits"]["hits"][0]["_id"]

        return doc_id