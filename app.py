import os
from flask import Flask
from flask_cors import CORS
from crawlingHTML import crawling

app = Flask(__name__)
CORS(app)

@app.route("/<int:page_number>", methods=['POST', 'GET'])
def insert_new_data(page_number):

    print(str(page_number) +" extracting...")
    result_hash = crawling.extract_data(page_number)
    if result_hash is None:
        result_msg = "NOT FOUND"
    else : 
       result_msg = crawling.insert_data_to_ES(result_hash)
    return {'data': str(page_number)+' ' + ''.join(result_msg)}

@app.route("/update/tags/<int:page_number>", methods=['POST', 'GET'])
def update_tags_to_ES(page_number):
    result_hash = crawling.extract_data(page_number)
    crawling.update_tags_in_ES(result_hash)
    
    return {'data': ' success'}

@app.route("/test/get/<int:page_number>", methods=['POST', 'GET'])
def test_get(page_number):    
    result_hash = crawling.extract_data(page_number)
    return {'data': ' success'}

@app.route("/update/<string:type>/<int:page_number>", methods=['POST', 'GET'])
def update(type,page_number):    
    result_hash = crawling.extract_data(page_number)
    if type == 'table_of_content':
        crawling.update_table_of_content_in_ES(result_hash)
    elif type == 'tag':
        crawling.update_tags_in_ES(result_hash)
    elif type == 'all':
        crawling.update_data_in_ES(result_hash)
    
    return {'data': ' success'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')