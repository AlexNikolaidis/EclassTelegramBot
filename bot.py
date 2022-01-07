import telegram
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from datetime import datetime

TELEGRAM_BOT_TOKEN = '####'
TELEGRAM_CHAT_ID = '#####'
***REMOVED***
URL = '####'
USR = '####'
PASS = '####'
PATH_TO_DRIVER = '####'

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
chars = [['(', '\('], [')', '\)'], ['-', '\-'], ['.', '\.'], ['!', '\!']]


class Announcement:
    def __init__(self):
        self.title = "NOT_SET"
        self.body = "NOT_SET"
        self.course = "NOT_SET"
        self.date = "NOT_SET"


def get(url, usr, password, path_to_driver):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    options.add_argument('--headless')
    s = Service(path_to_driver)
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(url)
    temp = driver.find_element(By.ID, 'uname')
    temp.send_keys(usr)
    temp = driver.find_element(By.ID, 'pass')
    temp.send_keys(password)
    temp.send_keys(Keys.RETURN)
    time.sleep(0.2)
    temp = driver.find_element(By.CLASS_NAME, 'panel')
    button = temp.find_element(By.XPATH, '//a[@href="../modules/announcements/myannouncements.php"]')
    button.click()
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    temp = soup.find_all("div", class_='table_td')
    _list = []
    for div in temp:
        tmp = Announcement()
        tmp.title = div.div.a.string
        tmp.course = div.small.string
        div_tmp = div.find("div", class_="table_td_body")
        tmp.body = div_tmp['title'].rstrip("\n")
        date = div.parent.parent.find_all('td')[1]
        tmp.date = date.string
        _list.append(tmp)

    return _list


def send(_list, token, chat_id, param, course_filter):
    # param gives different options for choosing which announcements to send via telegram
    # 1 -> sends only the ones released today
    #
    now = datetime.now()
    month = now.strftime("%m")
    day = now.strftime("%d")

    for each in _list:
        check_date = each.date.split(" ")
        # if param == 1 and course_filter == 0 and month == months[check_date[2]] and day == check_date[1]:
        if True:
            for x in chars:
                each.title = each.title.replace(x[0], x[1])
                each.course = each.course.replace(x[0], x[1])
                each.body = each.body.replace(x[0], x[1])
                each.date = each.date.replace(x[0], x[1])
                print(each.course)
            bot = telegram.Bot(token=token)
            bot.send_message(chat_id=chat_id, parse_mode='MarkdownV2',
                             text=f'__*Τίτλος*__:\n{each.title} \n\n__*Μάθημα*__:\n{each.course} \n\n'
                                  f'__*Ανακοίνωση*__: \n{each.body}\n\n__*Ημερομηνία*__:\n{each.date}\n\n')


def main():
    recv = get(URL, USR, PASS, PATH_TO_DRIVER)
    send(recv, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, 1, 0)

    # bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    # temp = bot.get_updates()
    # for i in temp:
    #     print(i)


if __name__ == "__main__":
    main()