from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions as exc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType 
from time import sleep
from datetime import datetime, timedelta
import pandas
import os
import pickle
import re
from random import randint

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
FACEBOOK_URL = 'https://www.facebook.com/'
COOKIE_PATH = PROJECT_PATH + '/cookies.pkl'
CSVS_PATH = PROJECT_PATH + '/datasets/'
WAIT = 60


def datetime_regex(datetime_str):
    return re.search("^\d\d? de [a-z]{4,9} de \d{4}$", datetime_str)

    
def clean_str(str_):
    cleaned_str = ''
    for i in str_.strip():
        if i in ('\n', '\t', '\r'):
            continue
        cleaned_str += i
    return cleaned_str                
        
        
def sleep_rand(min=3, max=15):
    return sleep(randint(min, max))
    
    
def get_login_credentials():
    # return {'login': 'leafar.seara@gmail.com', 'passwd': '__sambetO90'}
    return {'login': 'rafaelfonseca1020@gmail.com', 'passwd': '$mesarA_67@'}
    # return {'login': '+55 (64) 99244-9140', 'passwd': 'fabianamaurilio61'}


def read_cookie(path=COOKIE_PATH):
    return pickle.load(open(path, 'rb'))


def save_cookie(driver, path=COOKIE_PATH):
    cookies = driver.get_cookies()
    pickle.dump(cookies, open(COOKIE_PATH, 'wb'))


def get_month_number(month: str):
    month_lower = month.lower()
    months = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    for i in range(12):
        curr_month = months[i]
        if curr_month.startswith(month_lower):
            return i + 1


def get_datetime_from(date_string, time_string):
    date_elements = date_string.split('/')
    year, month, day = int('20' + date_elements[2]), int(date_elements[1]), int(date_elements[0])
    time_elements = time_string.split('h')
    hour, minute = int(time_elements[0]), int(time_elements[1])
    return datetime(year, month, day, hour, minute)


def get_relevance_index(timestamp, accesses):
    if timestamp is None or accesses is None:
        return None
    else:
        time_since_publication = datetime.now() - timestamp
        hours_since_publication = time_since_publication.total_seconds() / 3600
        return round(accesses / hours_since_publication, 2)


def get_weekday(timestamp):
    if timestamp is None:
        return None
    weekday = timestamp.weekday()
    if weekday == 0:
        return "segunda"
    elif weekday == 1:
        return "terca"
    elif weekday == 2:
        return "quarta"
    elif weekday == 3:
        return "quinta"
    elif weekday == 4:
        return "sexta"
    elif weekday == 5:
        return "sabado"
    elif weekday == 6:
        return "domingo"
    else:
        return None


def get_day_period(timestamp):
    if timestamp is None:
        return None
    hour = timestamp.hour
    if hour == 0 and timestamp.minute == 0 and timestamp.second == 0 and timestamp.microsecond == 0:
        return None  # It's assumed that the timestamp does not have time information.
    if hour < 12:
        return "manha"
    elif hour < 18:
        return "tarde"
    else:
        return "noite"


def clean_dataframe(df):
    df = df[df['acessos'].notna()].reset_index()  # Drop the rows with 'acessos' equal to 'nan'.
    df = df.drop_duplicates(subset=['titulo', 'data_hora']).reset_index()  # Drop duplicates.
    cols = df.columns
    valid_cols = ['titulo', 'descricao', 'data_hora', 'dia_semana',
                  'periodo_dia', 'imagens', 'acessos', 'acessos_medio_hora',
                  'tem_imagem_perfil']
    cols_to_drop = list()
    for col in cols:
        if col not in valid_cols:
            cols_to_drop.append(col)
    if len(cols_to_drop) > 0:
        df = df.drop(cols_to_drop, axis=1)
    return df


class Bot:
    def __init__(self):
        options = ChromeOptions()
        prefs = {
            'profile.managed_default_content_settings.images': 2,        # Disable images.
            'profile.default_content_setting_values.notifications': 2,   # Disable allow notification popup.
            'intl.accept_languages': 'pt'                                # Set the browser default language.
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')  # Use disk instead of main memory.
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        self._driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager(
                    chrome_type=ChromeType.CHROMIUM
                ).install()
            ),
            options=options
        )
        self._driver.implicitly_wait(5)
        self._post_counter = 0
        self._data_dict = dict(
            # cabecalho=list(),
            # data_hora=list(),
            # periodo_dia=list(),
            # dia_semana=list()
            # imagens=list(),
            # qtd_curtidas=list(),
            # qtd_amei=list(),
            # qtd_forca=list(),
            # qtd_haha=list(),
            # qtd_uau=list(),
            # qtd_triste=list(),
            # qtd_grr=list(),
            # encaminhamentos=list(),
            # comentarios=list()
        )
        self._curr_scroll_pos = 0 
        self._tot_posts_extracted = 0
        self._curr_post_pos = 0
        self._curr_year = -1
        self._start_date_time = datetime.now()
    
    def _get_date_time(self, date_str):
        if date_str is None:
            return None
        date_str = date_str.replace('"', '')
        split_data = date_str.split(', ')[-1]
        clear_split_data = split_data.replace(' de ', ' ').replace(' às', '')
        date_elements = clear_split_data.split(' ')
        date = dict()
        date['day'] = int(date_elements[0])
        date['month'] = get_month_number(date_elements[1])
        if len(date_elements) >= 3:  # Year is provided.   
            date['year'] = int(date_elements[2])
        else:  # Get the current year from the bot object itself.
            date['year'] = self._curr_year
        if len(date_elements) == 4:  # Time is provided.
            time = date_elements[-1].split(':')
            date['hour'] = int(time[0])
            date['minute'] = int(time[1])
        else:
            date['hour'] = 0
            date['minute'] = 0
        return datetime(date['year'], date['month'], date['day'], date['hour'], date['minute'])

    def _show_post_info(self):
        self._post_counter += 1
        post_title = self._data_dict['titulo'][len(self._data_dict['titulo']) - 1]
        print(f'({self._post_counter}) - {post_title}')

    def _reset_values(self):
        for key in self._data_dict.keys():
            self._data_dict[key].clear()
        self._post_counter = 0

    def _get_current_scroll_pos(self):
        return self._driver.execute_script('return document.documentElement.scrollTop || document.body.scrollTop;')
    
    def _get_max_scroll_pos(self):
        return self._driver.execute_script('return document.body.scrollHeight;')
    
    def _log_in(self):
        # Check if there's a login cookie to be reused.
        try:
            self._driver.get(FACEBOOK_URL)
            cookies = read_cookie()
            for cookie in cookies:
                self._driver.add_cookie(cookie)
            self._driver.refresh()
            sleep_rand()
            print('> Logged in')
        except FileNotFoundError as e:
            print('No cookie file found')
            sleep_rand()
            login_credentials = get_login_credentials()
            user_cred_input = self._driver.find_element(By.ID, 'email')
            passwd_input = self._driver.find_element(By.ID, 'pass')
            login_btn = self._driver.find_element(By.CSS_SELECTOR, 'button[data-testid="royal_login_button"]')
            user_cred_input.send_keys(login_credentials['login'])
            sleep_rand()
            passwd_input.send_keys(login_credentials['passwd'])
            sleep_rand()
            login_btn.submit()
            print('> Logged in')
            sleep_rand()
            save_cookie(self._driver)
    
    def _go_to_user(self, user):
        self._driver.get(FACEBOOK_URL + user)
        print(f'> Reached user \'{user}\'')
        sleep_rand()
        self._simulate_scrolling()
    
    def _go_to_filter_page(self):
        search_btn = self._driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Pesquisar"]') 
        search_btn.click()
        sleep_rand()
        search_box = self._driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Pesquisar esta Página"]')
        search_box.send_keys('a')
        sleep_rand()
        search_box.send_keys(Keys.ENTER)
        print('> Filter page')
        sleep_rand()
        
    def _apply_filter_most_recent(self):
        most_rc_filt = self._driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Mais recentes"]')
        most_rc_filt.click()
        print('> Filter \'most recent\' applied')
        sleep_rand()
    
    def _apply_year(self, y):
        self._curr_year = y
        list_item_divs = self._driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]') 
        pub_year_list_item = list_item_divs[3]
        pub_year_ele = pub_year_list_item.find_element(By.CSS_SELECTOR, 'div[aria-label^="Filtrar"]')
        pub_year_ele.click()
        sleep_rand()
        base_y = 2004
        for i in range(self._curr_year - base_y + 1):
            pub_year_ele.send_keys(Keys.ARROW_UP)
            sleep(.5)
        pub_year_ele.send_keys(Keys.ENTER)
        print(f'> Year \'{self._curr_year}\' applied')
        
    def _apply_next_year(self):
        list_item_divs = self._driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]') 
        pub_year_list_item = list_item_divs[3]
        pub_year_ele = pub_year_list_item.find_element(By.CSS_SELECTOR, 'div[aria-label^="Filtrar"]')
        pub_year_ele.click()
        sleep_rand()
        pub_year_ele.send_keys(Keys.ARROW_UP)
        pub_year_ele.send_keys(Keys.ENTER)
        self._curr_year += 1
        print(f'> Year \'{self._curr_year}\' applied')
        sleep_rand()
        
    def _extract_posts(self):
        print('>> Extracting posts')
        while True:
            self._extract_data()      # Extract the data of the visible posts.
            self._scroll_page()       # Scroll the page down.
            self._wait_loading()      # Wait for the page to load more posts if any.
            if self._page_is_done():  # If there's no post left.
                print('-' * 165)
                posts_extracted = self._get_posts_qtd()
                print(f'>> {posts_extracted} posts extracted')
                self._tot_posts_extracted += posts_extracted 
                self._curr_post_pos = 0
                break
        sleep_rand()
                
    def _extract_header_common_post(self):
        # Click to see more header.
        post = self._get_current_post()
        see_more_divs = post.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
        for sm_div in see_more_divs:
            if 'Ver mais' in sm_div.get_attribute('innerText'):
                for i in range(5):  # Try at most 5 times to click at 'Ver mais'.
                    try:
                        action_builder = ActionChains(self._driver)
                        action_builder.move_to_element(sm_div).click(sm_div).perform()
                        break
                    except exc.ElementNotInteractableException as e:
                        sleep_rand()
                break
        # Get the whole header message.
        try:
            message_divs = WebDriverWait(post, WAIT).until(
                ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-ad-comet-preview="message"]'))
            )
            msg = ''
            for msg_div in message_divs:
                msg += msg_div.get_attribute('innerText').strip()
            return msg
        except exc.TimeoutException as e:
            return None
    
    def _extract_header_reels(self):
        # Click to see more header.
        post = self._get_current_post()
        for i in range(5):
            try:
                see_more_obj = WebDriverWait(post, WAIT).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'object[type="nested/pressable"]'))
                )
                action_builder = ActionChains(self._driver)
                action_builder.move_to_element(see_more_obj).click(see_more_obj).perform()
                break
            except exc.ElementNotInteractableException as e:
                sleep_rand()
        # Get the whole header message.
        try:
            reels_anchor = WebDriverWait(post, WAIT).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label^="Abrir reel"]'))
            )
            return reels_anchor.get_attribute('innerText').strip()
        except exc.TimeoutException:
            return None

    def _extract_date_time_common_post(self):
        post = self._get_current_post()
        while True:
            try:
                date_time_span = post.find_element(By.CSS_SELECTOR, 'span[id^="jsc"]')
                date_time_link = date_time_span.find_element(By.CSS_SELECTOR, 'a[role="link"]')
                return date_time_link.get_attribute('innerText').strip()
            except exc.NoSuchElementException:
                pass
        # action_builder = ActionChains(self._driver)
        # action_builder.move_to_element(date_time_link).perform()  # Object tree has one of this elements updated with a new attribute.
        # try:
        #     post = self._get_current_post()  # That's why we're getting the post again.
        #     span_aria = post.find_element(By.CSS_SELECTOR, 'span[aria-describedby^="jsc_"]')
        #     aria_describedby = span_aria.get_attribute('aria-describedby')
        #     target_date_time_element = post.find_element(By.ID, aria_describedby)
        #     return target_date_time_element.get_attribute('innerText').strip()
        # except exc.NoSuchElementException:
        #     return date_time_link.get_attribute('innerText').strip()
            
    def _extract_date_time_reels(self):
        return None
        # reels_span = None
        # while not reels_span:
        #     post = self._get_current_post()
        #     spans = post.find_elements(By.TAG_NAME, 'span')
        #     for span in spans:
        #         if 'Reels' in span.get_attribute('innerText'):
        #             reels_span = span
        #             break
        # while True:
        #     try:
        #         span_child_1 = reels_span.find_element(By.TAG_NAME, 'span')
        #         span_child_2 = span_child_1.find_element(By.TAG_NAME, 'span')
        #         date_time_span = span_child_2.find_elements(By.XPATH, './*')[2]
        #         return date_time_span.get_attribute('innerText').strip()
        #     except exc.NoSuchElementException:
        #         pass
        # action_builder = ActionChains(self._driver)
        # action_builder.move_to_element(date_time_span).perform()
        # return self._driver.find_element(By.CSS_SELECTOR, 'span[role="tooltip"]').get_attribute('innerText')
        # try:
        #     post = self._get_current_post()
        #     spans = post.find_elements(By.TAG_NAME, 'span')
        #     reels_span = None
        #     for span in spans:
        #         if 'Reels' in span.get_attribute('innerText'):
        #             reels_span = span
        #             break
        #     span_aria = reels_span.find_element(By.CSS_SELECTOR, 'span[aria-describedby^="jsc_"]')
        #     aria_describedby = span_aria.get_attribute('aria-describedby')
        #     date_time_ele = post.find_element(By.ID, aria_describedby)
        #     return date_time_ele.get_attribute('innerText').strip()
        # except exc.NoSuchElementException:
        #     return date_time_span.get_attribute('innerText').strip()
    
    def _post_is_reels(self):
        post = self._get_current_post()
        spans = post.find_elements(By.TAG_NAME, 'span')
        reels_span = None
        for span in spans:
            if 'Reels' in span.get_attribute('innerText'):
                reels_span = span
                break
        return reels_span is not None
    
    def _count_images(self, pub):
        pass
    
    def _extract_likes_count(self, pub):
        pass
    
    def _extract_qtd_love(self, pub):
        pass
    
    def _extract_qtd_care(self, pub):
        pass
    
    def _extract_qtd_haha(self, pub):
        pass
    
    def _extract_qtd_wow(self, pub):
        pass
    
    def _extract_qtd_sad(self, pub):
        pass
    
    def _extract_qtd_angry(self, pub):
        pass
    
    def _extract_forwardings(self, pub):
        pass
    
    def _get_current_post(self):
        while True:
            try:
                ign_excs = (exc.NoSuchElementException, exc.StaleElementReferenceException,)
                # feed_div = self._driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
                feed_div = WebDriverWait(self._driver, WAIT, ignored_exceptions=ign_excs).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
                )
                # feed_div_children = feed_div.find_elements(By.XPATH, './*')
                feed_div_children = WebDriverWait(feed_div, WAIT, ignored_exceptions=ign_excs).until(
                    ec.presence_of_all_elements_located((By.XPATH, './*'))
                )
                if self._curr_post_pos < 0 or self._curr_post_pos >= len(feed_div_children):
                    return None
                return feed_div_children[self._curr_post_pos]
            except exc.TimeoutException:
                pass
    
    def _get_posts_qtd(self):
        while True:
            try:
                ign_excs = (exc.NoSuchElementException, exc.StaleElementReferenceException,)
                feed_div = WebDriverWait(self._driver, WAIT, ignored_exceptions=ign_excs).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
                )
                # feed_div_children = feed_div.find_elements(By.XPATH, './*')
                feed_div_children = WebDriverWait(feed_div, WAIT, ignored_exceptions=ign_excs).until(
                    ec.presence_of_all_elements_located((By.XPATH, './*'))
                )
                return len(feed_div_children)
            except exc.TimeoutException:
                pass
                
    def _extract_data(self):
        posts_qtd = self._get_posts_qtd()
        for i in range(self._curr_post_pos, posts_qtd - 1):
            if self._post_is_reels():
                header = self._extract_header_reels()
                date_time_str = self._extract_date_time_reels()
            else:
                header = self._extract_header_common_post()
                date_time_str = self._extract_date_time_common_post()
            print('-' * 165)
            print(header)
            print(date_time_str)
            # print(f'{self._curr_post_pos} - {header} - {date_time_str}')
            # date_time = self._get_date_time(date_time_str)
            # day_period = get_day_period(date_time)
            # weekday = get_weekday(date_time)
            # self._data_dict['cabecalho'].append(header)
            # self._data_dict['data_hora'].append(date_time)
            # self._data_dict['periodo_dia'].append(day_period)
            # self._data_dict['dia_semana'].append(weekday)
            # self._data_dict['imagens'].append(self._count_images(curr_post))
            # self._data_dict['qtd_curtidas'].append(self._extract_likes_count(curr_post))
            # self._data_dict['qtd_amei'].append(self._extract_qtd_love(curr_post))
            # self._data_dict['qtd_forca'].append(self._extract_qtd_care(curr_post))
            # self._data_dict['qtd_haha'].append(self._extract_qtd_haha(curr_post))
            # self._data_dict['qtd_uau'].append(self._extract_qtd_wow(curr_post))
            # self._data_dict['qtd_triste'].append(self._extract_qtd_sad(curr_post))
            # self._data_dict['qtd_grr'].append(self._extract_qtd_angry(curr_post))
            # self._data_dict['encaminhamentos'].append(self._extract_forwardings(curr_post))
            # self._data_dict['comentarios'].append(self._extract_comments(curr_post))
            self._curr_post_pos += 1
        sleep_rand()
    
    def _scroll_page(self, percentage=.7):
        self._curr_scroll_pos = self._get_current_scroll_pos()
        max_scroll_pos = self._get_max_scroll_pos()
        new_scroll_pos = self._curr_scroll_pos + (max_scroll_pos - self._curr_scroll_pos) * percentage
        self._driver.execute_script(f'window.scrollTo(0, {new_scroll_pos});')
            
    def _wait_loading(self):
        while True:
            feed_div = WebDriverWait(self._driver, WAIT).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
            )
            feed_div_children = feed_div.find_elements(By.XPATH, './*')
            try:
                if not feed_div_children[-1].get_attribute('role') == 'article':  # If this conditional is false, the page is still loading more posts.
                    return
            except exc.StaleElementReferenceException:
                return
    
    def _page_is_done(self):
        return self._get_current_scroll_pos() == self._curr_scroll_pos
    
    def _simulate_scrolling(self, scrollings=5):
        for i in range(scrollings):    
            rand_scroll = randint(0, self._get_max_scroll_pos())
            self._driver.execute_script(f'window.scrollTo(0, {rand_scroll});')
            sleep_rand()
    
    def _export_data_to_csv(self):
        print('> Exporting data to csv')
        exec_end = datetime.now()
        print('-' * 100)
        print('|', f'Bot started on {self._start_date_time}'.center(98), '|', sep='')
        print('|', f'Bot finished on {exec_end}'.center(98), '|', sep='')
        print('|', f'Time spent: {exec_end - self._start_date_time}'.center(98), '|', sep='')
        print('|', f'Total of posts extracted: {self._tot_posts_extracted}'.center(98), '|', sep='')
        print('-' * 100)
        if not os.path.exists(CSVS_PATH):
            os.makedirs(CSVS_PATH)
        dataframe = pandas.DataFrame(data=self._data_dict)
        exec_start_str = self._start_date_time.__str__().split('.')[0].replace(' ', '_').replace('-', '_').\
            replace(':', '_').replace('.', '_')
        csv_file_name = 'fb_data_' + exec_start_str + '_' + (exec_end - self._start_date_time).__str__().split('.')[0].\
            replace(':', '_') + '.csv'
        # dataframe = clean_dataframe(dataframe)
        dataframe.to_csv(CSVS_PATH + csv_file_name, index=False)
    
    def get_posts(self, *, year_range=[2013, 2023]):
        print('> Bot is running <')
        self._log_in()
        self._go_to_user('ifgoiano')
        self._go_to_filter_page()
        self._apply_filter_most_recent()
        self._apply_year(year_range[0])
        while True:
            self._extract_posts()
            if year_range[0] < year_range[-1]:
                year_range[0] += 1
                self._apply_next_year()
            else:
                break
        # self._export_data_to_csv()
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()
        print('> Bot execution finished <')
        

if __name__ == '__main__':
    with Bot() as bot:
        bot.get_posts(year_range=[2020, 2023])
 