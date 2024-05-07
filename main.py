from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def crawl(page):
    count = 0
    while count < page:
        jobs = driver.find_elements(By.TAG_NAME, "article")
        for job in jobs:
            try:
                title = job.find_element(By.TAG_NAME, "a")
                print(title.text)
            except Exception:
                break
        count += 1
        next_btn = driver.find_element(By.CLASS_NAME, "js-next-page")
        next_btn.click()
        time.sleep(3)



options = Options()
options.executable_chrome_path = "/Users/nidawei/git-repos/104-job-crawler/chromedriver"

driver = webdriver.Chrome(options=options)
driver.get("https://www.104.com.tw/jobs/main/")
time.sleep(1)

area = driver.find_element(By.XPATH,"//button/span[contains(text(), '地區')]")
area.click()
time.sleep(1)
taipei = driver.find_element(By.CSS_SELECTOR, "input[value='6001001000']")
taipei.click()
new_taipei = driver.find_element(By.CSS_SELECTOR, "input[value='6001002000']")
new_taipei.click()
time.sleep(1)
area_confirm_btn = driver.find_element(By.CLASS_NAME, "category-picker-btn-primary")
area_confirm_btn.click()
time.sleep(1)
category = driver.find_element(By.XPATH, "//button/span[contains(text(), '職務類別')]")
category.click()
time.sleep(1)
information = driver.find_element(By.LINK_TEXT, "資訊軟體系統類")
information.click()
software = driver.find_element(By.CSS_SELECTOR, "input[value='2007001000']")
software.click()
time.sleep(1)
information_confirm = driver.find_element(By.CLASS_NAME, "category-picker-btn-primary")
information_confirm.click()
time.sleep(1)
search = driver.find_element(By.CLASS_NAME, "btn-secondary")
search.click()
time.sleep(3)

crawl(2)








time.sleep(100)
driver.close()