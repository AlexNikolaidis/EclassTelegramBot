import telegram
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date

TELEGRAM_BOT_TOKEN = '#'
TELEGRAM_CHAT_ID = '#'
***REMOVED***
URL = '#'
USR = '#'
PASS = '#'
PATH_TO_DRIVER = '#'

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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def print(self):
        print(f'Title:\n{self.title}')
        print(f'Course:\n{self.course}')
        print(f'Body:\n{self.body}')
        print(f'Date:\n{self.date}')


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
        temp_date = div.parent.parent.find_all('td')[1]
        tmp.date = temp_date.string
        for x in chars:
            tmp.title = tmp.title.replace(x[0], x[1])
            tmp.course = tmp.course.replace(x[0], x[1])
            tmp.body = tmp.body.replace(x[0], x[1])
            tmp.date = tmp.date.replace(x[0], x[1])
        _list.append(tmp)

    return _list


def send(_list, token, chat_id, param1, param2, course_filter):
    # param1 gives different options for choosing which announcements to send via telegram
    # 0 -> sends everything it finds
    # 1 -> sends only the ones released today
    # 2 -> sends only the ones released X days before where X is param2 (if not used set param2 to 0)
    #
    # course_filter takes the course name exactly as it appears in eclass
    # and only sends announcements for this course/courses
    #
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    d0 = date(int(year), int(month), int(day))

    if course_filter == 0:
        course_filter = []

    for each in _list:
        course_filter.append(each.course)
        if any(each.course in s for s in course_filter):
            if param1 == 0:
                bot = telegram.Bot(token=token)
                bot.send_message(chat_id=chat_id, parse_mode='MarkdownV2',
                                 text=f'__*Τίτλος*__:\n{each.title} \n\n__*Μάθημα*__:\n{each.course} \n\n'
                                      f'__*Ανακοίνωση*__: \n{each.body}\n\n__*Ημερομηνία*__:\n{each.date}\n\n')
            elif param1 == 1:
                check_date = each.date.split(" ")
                if month == months[check_date[2]] and day == check_date[1]:
                    bot = telegram.Bot(token=token)
                    bot.send_message(chat_id=chat_id, parse_mode='MarkdownV2',
                                     text=f'__*Τίτλος*__:\n{each.title} \n\n__*Μάθημα*__:\n{each.course} \n\n'
                                          f'__*Ανακοίνωση*__: \n{each.body}\n\n__*Ημερομηνία*__:\n{each.date}\n\n')
            elif param1 == 2:
                check_date = each.date.split(" ")
                d1 = date(int(check_date[3]), int(months[check_date[2]]), int(check_date[1]))
                # delta is how old is the announc. in days
                delta = (d0 - d1).days
                if delta <= param2:
                    bot = telegram.Bot(token=token)
                    bot.send_message(chat_id=chat_id, parse_mode='MarkdownV2',
                                     text=f'__*Τίτλος*__:\n{each.title} \n\n__*Μάθημα*__:\n{each.course} \n\n'
                                          f'__*Ανακοίνωση*__: \n{each.body}\n\n__*Ημερομηνία*__:\n{each.date}\n\n')


def send_single(announc, token, chat_id):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, parse_mode='MarkdownV2',
                     text=f'__*Τίτλος*__:\n{announc.title} \n\n__*Μάθημα*__:\n{announc.course} \n\n'
                          f'__*Ανακοίνωση*__: \n{announc.body}\n\n__*Ημερομηνία*__:\n{announc.date}\n\n')


def main():
    recv = get(URL, USR, PASS, PATH_TO_DRIVER)
    try:
        file = open('announc_history', 'rb')
        history = pickle.load(file)
        file.close()
        sent = 0
        for each in reversed(recv):
            if each not in history:
                send_single(each, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
                sent += 1
                history.insert(0, each)
        with open('announc_history', 'wb') as file:
            pickle.dump(recv, file)
        now = datetime.now()
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        if sent == 0 and int(hour) == 12 and 25 <= int(minute) <= 35:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            bot.send_message(disable_notification=True, chat_id=TELEGRAM_CHAT_ID, parse_mode='MarkdownV2',
                             text='*Καμία νέα ανακοίνωση* \U0001F4A9')
    except FileNotFoundError:
        send(recv, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, 0, 0, 0)
        with open('announc_history', 'wb') as history_pickle:
            pickle.dump(recv, history_pickle)


if __name__ == "__main__":
    main()
