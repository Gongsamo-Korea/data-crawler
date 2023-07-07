from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager



class getDynamicContentData:
    def get_date(page_number):

        # 브라우저 옵션
        chrome_options = Options()
        chrome_options.add_argument('--headless')


        # 불필요한 에러 메시지 없애기 
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # ChromeDriverManager을 통해서 Chrome 자동 설치
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        url = f'https://kimchinchips.stibee.com/p/{page_number}'
        driver.get(url)

        
        
        date_value = driver.find_element(By.CLASS_NAME, "email-content")
        result = str(date_value.get_attribute('innerHTML'))

        driver.close()
        return result;



