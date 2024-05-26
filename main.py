from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import csv

def crawl_detail(driver, title):
    # window
    main_window = driver.current_window_handle
    title.click()
    time.sleep(2)

    new_window = driver.window_handles[1]

    driver._switch_to.window(new_window)
    skill_list = []
    try:
        skills = driver.find_elements(By.CSS_SELECTOR, "a[class='tools text-gray-deep-dark d-inline-block']")
        if skills:
            for skill in skills:
                skill_list.append(skill.text)
        else:
            table = driver.find_elements(By.CSS_SELECTOR, "div[class='job-requirement-table row'] div[class='list-row row mb-2']")[4]
            skill = table.find_element(By.CSS_SELECTOR, "div[class='t3 mb-0']")
            skill_list.append(skill.text)
        
    except Exception as e:
        print(f"detail page:{e}")
    
    time.sleep(3)
    driver.close()
    driver.switch_to.window(main_window)

    skill_str = ', '.join(skill_list)

    return skill_str

def crawl_jobs(driver, page):
    count = 0
    all_jobs = []

    print("[INFO] Finding jobs...")

    while count < page:

        # find all the jobs (TAG_NAME:article)
        jobs = driver.find_elements(By.CSS_SELECTOR, "div#js-job-content article")

        for job in jobs:
            try:

                title = job.find_elements(By.TAG_NAME, "a")[0]
                link = title.get_attribute('href')

                job_name = title.text

                company = job.find_elements(By.TAG_NAME, "a")[1].text

                locate = job.find_element(By.CLASS_NAME, "job-list-intro").find_elements(By.TAG_NAME, "li")[0].text

                experience = job.find_element(By.CLASS_NAME, "job-list-intro").find_elements(By.TAG_NAME, "li")[1].text

                degree = job.find_element(By.CLASS_NAME, "job-list-intro").find_elements(By.TAG_NAME, "li")[2].text

                skill = crawl_detail(driver, title)

                all_jobs.append({"職缺名稱":job_name, "公司名稱":company, "位置":locate, "經驗":experience, "學位":degree, "技能":skill, "連結":link})

            except Exception as e:
                print(f"main page:{e}")
                # print(len(jobs))
        print(f"Page {count+1} completed!")

        count += 1
        if count < page:
            next_btn = driver.find_element(By.CLASS_NAME, "js-next-page")
            next_btn.click()
            time.sleep(5)

    return pd.DataFrame(all_jobs)

def setup_crawler():
    # driver path
    options = Options()
    options.executable_chrome_path = "/Users/nidawei/git-repos/104-job-crawler/chromedriver"

    # url path
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.104.com.tw/jobs/main/")
    time.sleep(2)

    area = driver.find_element(By.XPATH,"//button/span[contains(text(), '地區')]")
    area.click()
    time.sleep(2)
    taipei = driver.find_element(By.CSS_SELECTOR, "input[value='6001001000']")
    taipei.click()
    new_taipei = driver.find_element(By.CSS_SELECTOR, "input[value='6001002000']")
    new_taipei.click()
    time.sleep(2)
    area_confirm_btn = driver.find_element(By.CLASS_NAME, "category-picker-btn-primary")
    area_confirm_btn.click()
    time.sleep(2)
    category = driver.find_element(By.XPATH, "//button/span[contains(text(), '職務類別')]")
    category.click()
    time.sleep(2)
    information = driver.find_element(By.LINK_TEXT, "資訊軟體系統類")
    information.click()
    software = driver.find_element(By.CSS_SELECTOR, "input[value='2007001000']")
    software.click()
    time.sleep(2)
    information_confirm = driver.find_element(By.CLASS_NAME, "category-picker-btn-primary")
    information_confirm.click()
    time.sleep(2)
    search = driver.find_element(By.CLASS_NAME, "btn-secondary")
    search.click()
    time.sleep(5)

    # job crawler
    data = crawl_jobs(driver, 1)
    # print(tabulate(data, headers='keys', tablefmt='psql'))
    driver.close()

    # save to excel
    data.to_csv('all_jobs.csv', index=False)

def analyze(input_skill):
    data = pd.read_csv('all_jobs.csv', header=0)
    # filter
    # condition1 = (data["經驗"] == "經歷不拘") & (data["學位"] != "碩士")
    # new_data = data[condition1]
    # print(new_data)
    data['技能'] = data['技能'].str.split(', ') # 將原本以 , 分隔的技能字串轉換回list
    condition2 = data['技能'].apply(lambda skills: input_skill in skills) # 將list的每一項確認是否包含指定技能
    best_skill = data[condition2]
    print(f'{input_skill}相關的職缺有{best_skill.shape[0]}個') # .shape[0]代表印出列數量

def main():
    # setup_crawler()

    input_skill = input('輸入搜尋技能：')
    analyze(input_skill)



if __name__ == '__main__':
    main()