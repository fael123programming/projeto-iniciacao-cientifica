from selenium import webdriver
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import os


def chat_gpt():
    start = datetime.now()
    print(f'Bot started at {start}')
    opts = webdriver.ChromeOptions()
    opts.add_argument(f'user-data-dir=C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opts
        )
        driver.implicitly_wait(5)
        # driver.get('https://chat.openai.com')
        driver.get('https://youtube.com')
        sleep(10)
    except Exception as exc:
        print('Exception raised:', exc.__class__.__name__)
        print(exc)
    finally:
        driver.close()


if __name__ == '__main__':
    chat_gpt()
