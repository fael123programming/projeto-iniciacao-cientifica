from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_actions import PointerActions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType 
from time import sleep
import re
import pickle
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

def validate_datetime_str(datetime_str):
    # datetime_regex_array = [
    #     '^\d d$',  # E.g., 5 d
    #     '^\d\d? de [a-zç]{4,9}$',  # E.g., 12 de dezembro
    #     '^\d\d? de [a-zç]{4,9} de \d{4}$',  # E.g., 5 de janeiro de 2021
    #     '^\d\d? de [a-zç]{4,9} às \d\d:\d\d$',  # E.g., 18 de março às 11:30
    #     '^\d\d? de [a-zç]{4,9} de \d{4} às \d\d:\d\d$',  # E.g., 20 de junho de 2015 às 15:37
    #     '^[a-zA-Z-çá]{5,13}, \d\d? de [a-zç]{4,9} de \d{4} às \d\d:\d\d$'
    # ]
    datetime_regex_array = [
        '^\d\d?m$',
        '^\d\d?h$',
        '^\dd$',
        '^[A-Z][a-z]{2,9} \d\d? at \d\d?:\d\d (PM|AM)$',
        '^[A-Z][a-z]{5,9}, [A-Z][a-z]{2,9} \d\d?, \d{4} at \d\d?:\d\d (PM|AM)$',  # Thursday, April 13, 2023 at 6:56 PM
        '^[A-Z][a-z]{2,9} \d\d?$',
        '^[A-Z][a-z]{2,9} \d\d?, \d{4}$'
    ]
    for regex in datetime_regex_array:
        if re.search(regex, datetime_str):
            return True
    return False


def get_datetime_element_of(pub):
    anchors = pub.find_elements(By.TAG_NAME, 'a')
    for anchor in anchors:
        anchor_txt = anchor.get_attribute('innerText')
        if validate_datetime_str(anchor_txt):
            return anchor


def get_parent_of(ele):
    return ele.find_element(By.XPATH, '..')
    

def get_first_child_of(ele):
    return ele.find_element(By.XPATH, './*')
    

def get_text_content_of(ele):
    return ele.get_attribute('textContent')


def print_info_of(ele):
    print('textContent:', ele.get_attribute('textContent'))
    print('outerHTML:', ele.get_attribute('outerHTML'))
    print('innerHTML:', ele.get_attribute('innerHTML'))
    

def get_all_attribute_values_of(ele, driver):
    return driver.execute_script('''
        var values = []; 
        for (index = 0; index < arguments[0].attributes.length; index++) { 
            values.push(arguments[0].attributes[index].value);
        }
        return values;
    ''', ele)
    

def get_title_element(web_element):
    anchors = web_element.find_elements(By.TAG_NAME, 'a')
    for anchor in anchors:
        anchor_txt = get_text_content_of(anchor)
        if anchor_txt.lower() == 'if goiano':
            return anchor

    
def scroll_to_element(ele, driver, offset=150):
    x, y = ele.location['x'], ele.location['y'] - offset
    scroll_by_coord = f'window.scrollTo({x},{y});'
    driver.execute_script(scroll_by_coord)
    print(f'Scrolled to ({x},{y})')
        
        
def find_full_datetime(driver):
    regex = '^[A-Z][a-z]{5,9}, [A-Z][a-z]{2,9} \d\d?, \d{4} at \d\d?:\d\d (PM|AM)$'
    feed_div = WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
    )
    dt_ele = get_datetime_element_of(feed_div)
    dt_ele_children = dt_ele.find_elements(By.XPATH, './*')
    for dt_ele_child in dt_ele_children:
        dt_ele_child_attr_values = get_all_attribute_values_of(dt_ele_child, driver)
        for dt_ele_child_attr_value in dt_ele_child_attr_values:
            if re.search(regex, dt_ele_child_attr_value):
                return dt_ele_child_attr_value
        

def find_datetime_div(driver):
    # regex = '^[a-zA-Z-çá]{5,13}, \d\d? de [a-zç]{4,9} de \d{4} às \d\d:\d\d$'
    # regex = '^[A-Z][a-z]{5,9}, [A-Z][a-z]{2,9} \d\d?, \d{4} at \d\d?:\d\d (PM|AM)$'
    all_divs = driver.find_elements(By.TAG_NAME, 'div')
    resp = []
    for div in all_divs:
        div_txt = div.get_attribute('textContent')
        if validate_datetime_str(div_txt):
            resp.append(div_txt)
    return resp[0] if len(resp) == 1 else resp
    

def handle_cookies(driver, wait=30):
    selectors = [
        '//*[@id="facebook"]/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]',
        '//*[@id="facebook"]/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]'
    ]
    for selector in selectors:
        try:
            WebDriverWait(driver, wait).until(
                ec.element_to_be_clickable((By.XPATH, selector))
            ).click()
        except exceptions.TimeoutException:
            pass
        else:
            break

    
def get_posts(driver):
    feed_div = driver.find_element(By.CSS_SELECTOR, 'div[role="main"] div[role="main"] div')
    divs = feed_div.find_elements(By.XPATH, './*')
    return divs[:len(divs) - 3]  # There are 3 trash divs.

    
if __name__ == '__main__':
    options = ChromeOptions()
    prefs = {
        'profile.default_content_setting_values.cookies': 2,         # Disable cookies.
        'profile.block_third_party_cookies': True,
        # 'profile.managed_default_content_settings.images': 2,        # Disable images.
        'profile.default_content_setting_values.notifications': 2,   # Disable allow notification popup.
        'intl.accept_languages': 'en,en_US'                                # Set the browser default language.
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')  # Use disk instead of main memory.
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(10)
    # url = 'https://www.facebook.com/ifgoiano/photos/pcb.9048550578520398/9048550455187077/?__cft__[0]=AZV83tPsLIEE2eQbINpUAj7FAyX2r4Q78h7lxmnzFP6G-w4iWCn3akEqB1eiMGrmfgn6XjPb6La5pO7ym7kvyaigpSZoPqrvExGIfGYVTE-4ORuD3evmSCo1Yx9Kt4TcbZ6uOXE1VunXUQct4K_h6gm9XQNB7V4V24IacZggkSXF5WpwvGfKgJ8_NberC_JhbszhH_z93JzxDI7fNf9z0hHQ&__tn__=*bH-R'
    # url = 'https://www.facebook.com/ifgoiano/photos/pcb.9040275326014590/9040265212682268/?__cft__[0]=AZXBtbZEeAOH4UVNvt8o2vuz1OAMl72_p9MpEP1gpc-3julEbCrpK1NFAzWd21YjMqsMZRAPknI52pmcoJiJD24ClbAarGMXaXu6RqHvNYzCHVcDlux2WFBnJ2H-zvJOs-NJVR35NxCgHqK0Fq8hYK6pfNa6vikKH58AFDsWmNxuYnyqIU1Ehzd1KaTPqyJilaZSug004YDv4YIhovZmDleF&__tn__=*bH-R'
    # url = 'https://www.facebook.com/ifgoiano/photos/pcb.9005647646144025/9005643352811121/?__cft__[0]=AZXQj4wWSvsCAKMSE4l3kRqzgVlpvUSrgn2kRQe2apufddBcwdvcE9NGUYR-LSTS6nuzzFkzxyomrPMSsOnUhotbG6bJ2qrIaUAD-Zx9Ea-VWBrlCGiU5tdO0jeN81cTPcwB9in6M_ZnT3fYwlkTSp0iwA3e93IlKWm6UQZXlh_NCn-1wt7BJ2mNnqiyp_ojfAgotX_pMHMe-egBLeKCS7lG&__tn__=*bH-R'
    # url = 'https://www.facebook.com/ifgoiano/photos/pcb.8964896783552445/8964896700219120/?__cft__[0]=AZWO8W8KMWiagqWiKCv3gETR0jnBQkhuwQcNJ6dDsEUTMEBDdl-JvOhfZoRefGHOnotJw77_78Et-16c8F-948Wboy1w_X4CtajRbDOVxFS2rgIbPpaWnxxhsmjfcRd50E3xNvToej-D0OFbN9_JvRBw58K9nHA61NrJV9ceHNCrZg0CbmkffnQGrkjvG4zmJn-OaULvOoqgXWlJ4_nOzEmN&__tn__=*bH-R'
    # url = 'https://www.facebook.com/ifgoiano/photos/pcb.8958692300839560/8958692154172908/?__cft__[0]=AZUao74pvnfrHW8h4hx9cI3eH_xURvkWA_5dVtmBCIdUlfIq3YjowS9twowLkkQsT825Cx-NMU-tqkK42Z6nplpuZ_yv7srxfMLENne5kY0XGTC4-xQTm_sqe1QIqy86rzfMwotw_qZF7vYT7UizCddqUYg74cVPA4SP60VFmM0yaOPP98wi-5W3bkkCPCohNnKUadOhJy9Rr6lhdD8BQHDg&__tn__=*bH-R'
    url = 'https://www.facebook.com/ifgoiano/photos/pcb.8924061744302616/8924034117638712/?__cft__[0]=AZWmQWXj5GFTgjq2SzGS-N-3Ls763y3oX-0MhNEVHMeVR4yiBQEsYm8SxxpCyo3qTu-XEQuQyG5-6XCBET7zo8dUHa9DGT6eyhVQEplA2SXjjUr4guVyezeBElVY3xfFmsh5pKw6JRFmxp86hiw_wJSrp7hWJ-OxMV_rb3UfegFEuM3E5WoVS4k_GhvJqXn0KU-0XFiqLunGPl7MXVQLfltO&__tn__=*bH-R'
    driver.get(url)
    first_image_url = driver.current_url.removesuffix('/')
    handle_cookies(driver)
    image_counter = 0
    while True:
        body = driver.find_element(By.TAG_NAME, 'body')
        ActionChains(driver).move_to_element(body).click(body).perform()
        body.send_keys(Keys.ARROW_RIGHT)
        image_counter += 1
        if driver.current_url == first_image_url:
            driver.quit()
            print(f'There are {image_counter} image(s).')
            break
    driver.quit()
    