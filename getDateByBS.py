import requests
from bs4 import BeautifulSoup
import json


class getDateValue:

    def extract_dateValue(version):
        url = f"https://kimchinchips.stibee.com/"
        header = {'User-agent' : 'Mozila/2.0'}
        response = requests.get(url, headers=header)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        json_data = soup.find("script", id="__NEXT_DATA__")
        site_json=json.loads(json_data.text)

        email_list_data = site_json['props']['pageProps']['emailListData']

        for d in email_list_data:
            if d.get('id') == version:
                date_value = d.get('publishedAt')
                date_value = date_value.split('T')[0]
                break
        
        return date_value
        


        


