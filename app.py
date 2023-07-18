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
       
    return {'data': str(page_number) +' '+result_msg}

@app.route("/update/tags/<int:page_number>", methods=['POST', 'GET'])
def update_tags_to_ES(page_number):
    result_hash = crawling.extract_data(page_number)
    crawling.update_tags_in_ES(result_hash)
    
    return {'data': ' success'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')