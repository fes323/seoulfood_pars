from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time, random


proxy = ''
options = Options()
options.add_argument(f'--proxy-server={proxy}')


driver = webdriver.Chrome(options=options)

detail_urls = []

page = 0
agree_btn = False
for i in range(0, 81):
    page += 1
    cards = None

    driver.get(f"https://seoulfood.kotra.biz/fairOnline.do?hl=ENG&selAction=single_page&SYSTEM_IDX=66&FAIRMENU_IDX=15068#/?queryDynamicIndex=&selOrder=cfair_nm_replace&selDynamicInput_fair=%5B%22_select_mod4521_in55%22,%22_select_mod4521_in71%22,%22_select_mod4521_in83%22,%22_select_mod4521_in89%22,%22_select_mod4521_in99%22,%22_select_mod4522_in41%22%5D&SYSTEM_IDX=66&selPageNo={page}") 
    time.sleep(random.randint(5, 10))
    if agree_btn == False:
        agree_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div[2]/div/div/a'))
        )
        agree_btn.click()
        agree_btn = True


    try:
        cards = driver.find_elements(By.CLASS_NAME, 'list-area')
    except:
        print('[ERROR] элементы не найдены!')
        break
    finally:
        for card in cards:
            urls = card.find_elements(By.XPATH, '//a[contains(@href, "/detail?")]')

            for url in urls:
                url = url.get_attribute('href')
                if url in detail_urls:
                    print('[WARNING] Duplicate! URL in list!')
                detail_urls.append(url)


data_list = []
for url in detail_urls:
    data = {}
    driver.get(url)
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".company-tbl"))
    )

    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        try:
            key = row.find_element(By.TAG_NAME, "th").text.strip()
        except:
            continue
        try:
            value = row.find_element(By.TAG_NAME, "td").text.strip()
        except:
            continue
        finally:
            if key in data:
                data[key].append(value)
            else:
                data[key] = value

    data_list.append(data)


driver.quit()

df = pd.DataFrame(data_list)
with pd.ExcelWriter('Exhibitor List 2024.xlsx') as writer:
    df.to_excel(writer)
