import requests
from bs4 import BeautifulSoup
import emoji
import re
from datetime import datetime
from getDateByBS import getDateValue
from connectToElasticSearch import connectToES


def split_count(text):
    return ''.join(c for c in text if c in emoji.UNICODE_EMOJI['en'])

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


class crawling:
        
    def find_table_of_content(target_span):
        result = ''
        bullet_point = "\u2022"
        name_of_table = target_span.text
        if target_span is None:
            return None

        if name_of_table == '오늘의 주요 MENU':
            
            table_menu = target_span.find_parent().find_next_siblings()
            for r in table_menu:
                result += "{} {} {}".format( bullet_point, r.text, "\n")

        else : 
            ul_list = target_span.find_parents(name="td")[0].find_all('ul')
            for ul in ul_list: 
                li_list = ul.find_all('li')
                for li in li_list:
                    result += "{} {} {}".format( bullet_point, li.text, "\n")
        
        return result
                    
    def extract_data(version):
        result_hash = {}
        url = f"https://kimchinchips.stibee.com/p/{version}/"
        header = {'User-agent' : 'Mozila/2.0'}
        response = requests.get(url, headers=header, verify=False)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        ## 만약 뉴스레터 페이지를 찾을수 없는 경우
        not_found_msg = "뉴스레터를 찾지 못했습니다"
        if not_found_msg in soup.get_text():
            print(not_found_msg)
            return None
        else : 
            
            # title
            whole_title = soup.title.text
            print(whole_title)
            split_title = ''
            if "🍟" not in whole_title:
                emoji_list = split_count(whole_title)
                split_title = whole_title.strip(emoji_list[1]).split(emoji_list[1])
            else : 
                split_title = whole_title.split("🍟")

            title = split_title[1][1:]

            # issue_number
            issue_number = ''
            if has_numbers(split_title[0]):
                issue_number  = re.findall(r'\d\.\d|\d+', split_title[0])[0]
                
            else : 
                issue_number = split_title[0][1:]

            # issue date
            issue_date_format = getDateValue.extract_dateValue(version)
            date_format = '%Y-%m-%d'
            formatted_date = datetime.strptime(issue_date_format, date_format)
            issue_date = formatted_date.strftime('%Y-%m-%d %H:%M:%S')

            print(issue_date)

            # tag 135회부터 있음
            mail_content_not_found_text = "이 메일이 잘 안보이시나요?"
            try:
                tags_parent = soup.find(lambda tag:tag.name=="a" and mail_content_not_found_text in tag.text)
                whole_tags_list = tags_parent.findChild().text.replace(' ','')
                tags_list = whole_tags_list.split("#")[1:]
                print(tags_list)
                result_hash['tags'] = tags_list


            except (AttributeError, NameError):
                print("tags not found")
                result_hash['tags'] = None
                
            # table of content
            target_span = soup.find(lambda tag:tag.name=="span" and "오늘의 " in tag.text)
            table_of_content = None
            if target_span is not None:
                table_of_content = crawling.find_table_of_content(target_span)

            # content
            content = soup.find("div", "email-content").prettify()


            result_hash['title'] = title
            result_hash['issue_number'] = issue_number
            result_hash['issue_date'] = issue_date
            result_hash['table_of_content'] = table_of_content
            result_hash['content'] = content

            return result_hash 

    
    #By ElasticSearch 
    def get_doc_id_by_ES(title, issue_number):
        doc_id = connectToES.getDocId(title, issue_number)
        return doc_id

    def update_data_in_ES(result_hash):
        doc_id = crawling.get_doc_id_by_ES(result_hash['title'], result_hash['issue_number'])
        connectToES.updateData(result_hash, doc_id)
        return 'success'
    
    def insert_data_to_ES(result_hash):
        connectToES.insertData(result_hash)
        return 'success'
    
    def insert_data_to_ES(result_hash, articleId):
        connectToES.insertDataFromScratch(result_hash, articleId)
        return articleId
    
    def update_tags_in_ES(result_hash):
        doc_id = crawling.get_doc_id_by_ES(result_hash['title'], result_hash['issue_number'])
        connectToES.updateTags(doc_id, result_hash['tags'])
        return 'success'
    
    def update_table_of_content_in_ES(result_hash):
        doc_id = crawling.get_doc_id_by_ES(result_hash['title'], result_hash['issue_number'])
        connectToES.updateTableOfContent(doc_id, result_hash['table_of_content'])
        return 'success'
        
    

#result_hash = crawling.extract_data(94) #오늘의 김침 165, 오늘의 깁치앤칩스 134, 오늘의 주요소식 94, 오늘의 주요 MENU 65
#print("---------------------")#
#print(result_hash['table_of_content'])
