from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import ast

def crawl_detail(driver, link):
    # window
    main_window = driver.current_window_handle
    driver.execute_script(f"window.open('{link}');")

    new_window = driver.window_handles[1]

    driver._switch_to.window(new_window)
    skill_list = []
    try:
        skills = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[class='tools text-gray-deep-dark d-inline-block']")))
        if len(skills) > 0:
            for skill in skills:
                skill_list.append(skill.text)
        
    except TimeoutException:
        try:
            table = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class='job-requirement-table row'] div[class='list-row row mb-2']")))[4]
            skill  = WebDriverWait(table, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='t3 mb-0']")))
            skill_list.append(skill.text)

        except Exception as e:
            print(f"detail page:{e}")
    
    # time.sleep(3)
    driver.close()
    driver.switch_to.window(main_window)

    skill_str = ', '.join(skill_list)

    return skill_list

def crawl_jobs(driver, page):
    count = 0
    all_jobs = []

    print("[INFO] Finding jobs...")

    while count < page:
        # find all the jobs (TAG_NAME:article)
        jobs = WebDriverWait(driver, 20).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "div#js-job-content article"))) # jobs

        for job in jobs:
            try:
                title = WebDriverWait(job, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))[0] 

                link = title.get_attribute('href')
                job_name = title.text
                
                company = WebDriverWait(job, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))[1].text

                intro = WebDriverWait(job, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "job-list-intro")))
                locate = WebDriverWait(intro, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))[0].text
                experience = WebDriverWait(intro, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))[1].text
                degree = WebDriverWait(intro, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "li")))[2].text

               
                skill = crawl_detail(driver, link)

                all_jobs.append({"職缺名稱":job_name, "公司名稱":company, "位置":locate, "經驗":experience, "學位":degree, "技能":skill, "連結":link})

            except Exception as e:
                print(f"main page:{e}")
                break

        count += 1
        print(f"Page {count} completed!")
        
        if count < page:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "js-next-page"))).click() # next btn

    return pd.DataFrame(all_jobs)

def setup_crawler(page):
    # driver path
    options = Options()
    options.executable_chrome_path = "/Users/nidawei/git-repos/104-job-crawler/chromedriver"

    # url path
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.104.com.tw/jobs/main/")
    # time.sleep(2)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//button/span[contains(text(), '地區')]"))).click() # area
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='6001001000']"))).click() # taipei
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='6001002000']"))).click() # new taipei
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "category-picker-btn-primary"))).click() # area confirm btn
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button/span[contains(text(), '職務類別')]"))).click() # category
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "資訊軟體系統類"))).click() # information
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='2007001000']"))).click() # software
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "category-picker-btn-primary"))).click() # information confirm
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-secondary"))).click() # search btn

    # job crawler
    data = crawl_jobs(driver, page)
    driver.close()

    # save to excel
    data.to_csv('all_jobs.csv', index=False)

def analyze(data, input_skill):
    # filter
    # condition1 = (data["經驗"] == "經歷不拘") & (data["學位"] != "碩士")
    # new_data = data[condition1]

    data['技能'] = data['技能'].apply(ast.literal_eval) # 使用函式讓字串轉換回列表
    # data['技能'] = data['技能'].str.split(', ') # 將原本以 , 分隔的技能字串轉換回list
    condition2 = data['技能'].apply(lambda skills: input_skill in skills) # 將list的每一項確認是否包含指定技能
    best_skill = data[condition2]
    print(f'{input_skill}相關的職缺有{best_skill.shape[0]}個') # .shape[0]代表印出列數量

def proportion(data):
    skill_list = {}
    def check(x):
        if x not in skill_list:
            skill_list[x] = 1
        else:
            skill_list[x] += 1

    shape = data['技能'].shape[0] # 計算總共有幾列
    data['技能'] = data['技能'].apply(ast.literal_eval)
    
    for i in range(shape):
        skills = data.loc[i, '技能']
        for skill in skills:
            check(skill)

    return skill_list

def plot(skill_list):
    import matplotlib.pyplot as plt

    sorted_skills = sorted(skill_list.items(), key=lambda x: x[1], reverse=True)[:10] # 今過sorted後，資料將轉變為tuple的鍵值對
    skills = [skill[0] for skill in sorted_skills]
    counts = [skill[1] for skill in sorted_skills]
    # skills = list(skill_list.keys())
    # counts = list(skill_list.values())
    plt.rcParams['font.sans-serif'] = ['Arial Unicode Ms']
    plt.rcParams['axes.unicode_minus'] = False

    
    plt.figure(figsize=(10, 5))
    plt.barh(skills, counts, color='skyblue')

    plt.title('Top 10 Skills Frequency')
    plt.xlabel('Frequecy')
    plt.ylabel('Skills')

    plt.show()

        

def main():
    page = int(input('輸入爬取頁數：'))
    setup_crawler(page)

    data = pd.read_csv('all_jobs.csv', header=0)
    # input_skill = input('輸入搜尋技能：')
    # analyze(data, input_skill)

    skill_list = proportion(data)
    plot(skill_list)



if __name__ == '__main__':
    main()