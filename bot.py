import telegram
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from datetime import datetime

TELEGRAM_BOT_TOKEN = 'TOKEN'
TELEGRAM_CHAT_ID = 'CHAT ID'
URL = 'ECLASS WEBSITE'
USR = 'USERNAME'
PASS = 'PASSWORD'
PATH_TO_DRIVER = 'PATH FOR BROWSER DRIVER'


months = {
    "Ιανουαρίου": 1,
    "Φεβρουαρίου": 2,
    "Μαρτίου": 3,
    "Απριλίου": 4,
    "Μαΐου": 5,
    "Ιουνίου": 6,
    "Ιουλίου": 7,
    "Αυγούστου": 8,
    "Σεπτεμβρίου": 9,
    "Οκτωβρίου": 10,
    "Νοεμβρίου": 11,
    "Δεκεμβρίου": 12,
}


class Announcement:
    def __init__(self):
        self.title = "NOT_SET"
        self.body = "NOT_SET"
        self.course = "NOT_SET"
        self.date = "NOT_SET"


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
options.add_argument('--headless')
s = Service(PATH_TO_DRIVER)
driver = webdriver.Chrome(service=s, options=options)
driver.get(URL)
temp = driver.find_element(By.ID, 'uname')
temp.send_keys(USR)
temp = driver.find_element(By.ID, 'pass')
temp.send_keys(PASS)
temp.send_keys(Keys.RETURN)
time.sleep(0.2)
temp = driver.find_element(By.CLASS_NAME, 'panel')
button = temp.find_element(By.XPATH, '//a[@href="../modules/announcements/myannouncements.php"]')
button.click()
time.sleep(0.5)
# temp = driver.find_element(By.CLASS_NAME, 'tablelist')
soup = BeautifulSoup(driver.page_source, 'html.parser')
# print(soup.find_all(["ul"]))

temp = soup.find_all("div", class_='table_td')

anakoinoseis = []
for div in temp:
    tmp = Announcement()
    tmp.title = div.div.a.string
    tmp.course = div.small.string
    div_tmp = div.find("div", class_="table_td_body")
    tmp.body = div_tmp['title'].rstrip("\n")
    date = div.parent.parent.find_all('td')[1]
    tmp.date = date.string
    anakoinoseis.append((tmp))
    # print(f'\ntitlos: {tmp.title}')
    # print(f'mathima: {tmp.course}')
    # print(f'anakoinosi: {tmp.body}')
    # print(f'date: {tmp.date}')

now = datetime.now()
month = now.strftime("%m")
day = now.strftime("%d")

for each in anakoinoseis:
    check_date = each.date.split(" ")
    if month == months[check_date[2]] and day == check_date[1]:
    # if True:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f'ΤΙΤΛΟΣ: {each.title}\nΜΑΘΗΜΑ: {each.course}\n'
                                                  f'ΑΝΑΚΟΙΝΩΣΗ: {each.body}\n'f'ΗΜΕΡΟΜΗΝΙΑ: {each.date}\n')

print("day:", day)
# time.sleep(5)
driver.quit()
