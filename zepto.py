from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

s=Service("C:\\Users\\athir\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
driver=webdriver.Chrome(service=s)
url='https://www.zeptonow.com/'
driver.get(url)
driver.maximize_window()
time.sleep(3)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
wait=WebDriverWait(driver,20)

names,prices,discounts,old_prices=[],[],[],[]
links,titles=[],[]

for i in range(1,8):
    a=wait.until(EC.presence_of_element_located((By.XPATH,f'//ul[@class="mt-5 grid gap-4"]//div[{i}]//a')))
    res=a.get_attribute('href')
    title=a.get_attribute('aria-label')
    a.click()
    time.sleep(3)

    name=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="mt-2 !h-12 lg:!h-16"]')))
    for i in name:
        names+=[i.find_element(By.XPATH,'.//div//h5').text]

    price=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="flex items-baseline gap-1"]')))
    for i in price:
        prices+=[i.find_element(By.XPATH,'.//h4').text]
        try:
            old_prices+=[i.find_element(By.XPATH,'.//p').text]
        except:
            old_prices+=[None]

    dis=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="relative z-0 rounded-xl bg-gray-200"]')))
    
    for i in dis:
        try:
            p= i.find_element(By.XPATH,'.//div[2]/p')
            discounts+=[i.find_element(By.XPATH,'.//div[@class="z-[100] absolute overflow-hidden top-0 left-0 rounded-tl-xl"]//p').text]

        except:
            discounts+=[None]
    
    link=[res for i in range(len(name))]
    links+=link
    cat=[title for i in range(len(name))]
    titles+=cat
    
    driver.get(url)
    time.sleep(2)

driver.quit()

# print(len(names),len(prices),len(discounts),len(old_prices))
df=pd.DataFrame({'Name':names,'Price':prices,'Discount':discounts,'Old_Price':old_prices,'Category':titles,'Link':links})
df.to_excel('zepto.xlsx',header=True,index=False)

