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

@app.route("/update/all", methods=['POST', 'GET'])
def update_all_to_ES():
    num_list = ['159', '158', '156', '155', '154', '153', '152', '151', '150', '149', '147', '146', '145', '144', '143', '142', '141', '139', '138', '140', '137', '136', '135', '134', '133', '132', '131', '130', '129', '128', '127', '126', '125', '124', '123', '122', '121', '120', '119', '118', '117', '116', '115', '114', '113', '112', '111', '110', '109', '108', '107', '106', '105', '104', '103', '102', '101', '100', '99', '98', '97', '96', '95', '94', '93', '92', '91', '90', '89', '88', '87', '86', '85', '84', '83', '82', '81', '80', '79', '78', '77', '15', '4', '14', '3', '61', '5', '36', '13', '35', '48', '76', '54', '34', '75', '42', '47', '41', '57', '2', '74', '28', '56', '46', '23', '73', '55', '71', '60', '22', '70', '1', '33', '63', '62', '19', '11', '10', '45', '59', '53', '69', '72', '18', '27', '68', '44', '40', '9', '67', '26', '8', '52', '39', '21', '25', '32', '58', '51', '31', '7', '38', '50', '12', '20', '66', '65', '30', '64', '29', '49', '37', '17', '24', '16', '6', '43']
    for num in reversed(num_list) : 
        result_hash = crawling.extract_data(int(num))
        crawling.update_data_in_ES(result_hash)
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
        crawling.update_table_of_content_in_ES(result_hash)
    elif type == 'all':
        crawling.update_data_in_ES(result_hash)
    
    return {'data': ' success'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')