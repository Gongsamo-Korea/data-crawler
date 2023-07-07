from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager



class getDynamicData:
    def get_date(page_number):

        # 브라우저 옵션
        chrome_options = Options()
        #        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument('--headless')


        # 불필요한 에러 메시지 없애기 
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # ChromeDriverManager을 통해서 Chrome 자동 설치
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 웹페이지 해당 주소 이동
        #driver.implicitly_wait(5) #웹페이지가 로딩 될때까지 5초 기다림 
        #driver.maximize_window()

        url = 'https://kimchinchips.stibee.com/'
        driver.get(url)

        
        
        #더보기 끝까지 누르기 
        for i in range(13):
            driver.find_element(By.XPATH, value=("//span[contains(text(),'더보기')]")).click();
            
                                                  

        xpath_expression = f'//a[@href="/p/{page_number}/"]'
        element = driver.find_element(by=By.XPATH, value=xpath_expression)
        date_value = element.find_element(By.CLASS_NAME, "date").text
        driver.close()
        return date_value;
    

