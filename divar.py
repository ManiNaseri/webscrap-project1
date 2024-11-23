from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.timeouts import Timeouts
from bs4 import BeautifulSoup
import time
import csv

# set webdriver
service = Service("C:/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# get data from site
url = "https://divar.ir/s/tehran/mobile-phones"
driver.get(url)

# set timer 
time.sleep(10)

# get HTML data 
html_content = driver.page_source


soup = BeautifulSoup(html_content, "html.parser")
result = soup.find_all("div", class_="post-list-eb562")

posts = soup.find_all("div", class_="post-list__items-container-e44b2")

    
with open("divar.csv", mode='w', encoding='utf-8', newline="") as file :
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Location', 'Link'])

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True :
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(5)
        
        # update HTML source
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        posts = soup.find_all("div", class_="post-list__items-container-e44b2")


        for post in posts :
            title = post.find("h2", class_="kt-post-card__title")
            price = post.find_all("div", class_="kt-post-card__description")
            location = post.find("span", class_="kt-post-card__bottom-description kt-text-truncate")
            link_element = post.find("a", class_="kt-post-card__action")
            if link_element:
                link = "https://divar.ir" + link_element["href"]
            else :
                link = "no link"   
            


            writer.writerow([title.text.strip(), price[1].get_text(strip=True), location.text.strip(), link])

        new_height = driver.execute_script("return document.body.scrollHeight")

        if last_height == new_height :
            break
        last_height = new_height











        
       