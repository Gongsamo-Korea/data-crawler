from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager


# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메시지 없애기 
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# ChromeDriverManager을 통해서 Chrome 자동 설치
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.implicitly_wait(5) #웹페이지가 로딩 될때까지 5초 기다림 
driver.maximize_window()

def get_num_list():
    url = 'https://kimchinchips.stibee.com/'
    driver.get(url)

    #더보기 끝까지 누르기 
    for i in range(13):
            driver.find_element(By.XPATH, value=("//span[contains(text(),'더보기')]")).click();

    #parent_element = driver.find_element(By.CSS_SELECTOR, "#__next > div.styles__NewsLettersLayout-sc-1081fac-0.khBsEd > div.styles__NewsletterList-sc-1081fac-2.cERffU")
    parent_element = driver.find_element(By.XPATH, value=("//div[starts-with(@class, 'styles__NewsletterList')]"))

    children = parent_element.find_elements(By.CSS_SELECTOR, "a")
    num_list = []
    substring = "https://kimchinchips.stibee.com/p/"



    for child in children:
        link =  child.get_attribute('href')
        result = link.replace(substring, "")
        num_list.append(result[:-1])
    
    return num_list
        


print(get_num_list())