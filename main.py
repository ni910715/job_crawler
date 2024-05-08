from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

def crawl(page):
    count = 0
    while count < page:
        all_jobs = []

        jobs = driver.find_elements(By.TAG_NAME, "article")
        for job in jobs:
            try:
                title = job.find_elements(By.TAG_NAME, "a")[0].text
                # print(title.text)

                company = job.find_elements(By.TAG_NAME, "a")[1].text
                # print(company.text)

                locate = job.find_element(By.CLASS_NAME, "job-list-intro").find_elements(By.TAG_NAME, "li")[0].text
                # print(locate.text)

                experience = job.find_element(By.CLASS_NAME, "job-list-intro").find_elements(By.TAG_NAME, "li")[1].text
                # print(experience.text)

                degree = job.find_element(By.CLASS_NAME, "job-list-intro").find_elements(By.TAG_NAME, "li")[2].text
                # print(degree.text)

                # print("-" * 30)

                all_jobs.append({"職缺名稱":title, "公司名稱":company, "位置":locate, "經驗":experience, "學位":degree})

            except Exception:
                break
        count += 1
        next_btn = driver.find_element(By.CLASS_NAME, "js-next-page")
        next_btn.click()
        time.sleep(3)
    
    return pd.DataFrame(all_jobs)



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

data = crawl(2)
print(data)

data.to_excel("job.xlsx")

driver.close()