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
        # result_msg = crawling.insert_new_newsletter(result_hash)
        print ("insert")

    return {'data': str(page_number) +' '+result_msg}

@app.route("/update/<int:page_number>/<string:update_section>", methods=['POST', 'GET'])
def update(page_number, update_section):

    print(str(page_number) +" extracting...")
    result_hash = crawling.extract_data(page_number)
    if update_section == 'table_of_content':
        crawling.update_table_of_content(result_hash)
    
    elif update_section == 'issue_date':
        crawling.update_issue_date(result_hash)
    
    elif update_section == 'content':
        crawling.update_content(result_hash)

    return {'data': str(page_number) +' update ' + update_section +' success'}

if __name__ == '__main__':
    app.run(debug=True)