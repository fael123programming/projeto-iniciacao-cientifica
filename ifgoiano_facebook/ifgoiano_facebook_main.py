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
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType 
from time import sleep
from datetime import datetime, timedelta
from random import randint
from enum import Enum
import pandas
import os
import pickle
import re
from abc import ABC


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
FACEBOOK_URL = 'https://www.facebook.com/'
COOKIE_PATH = PROJECT_PATH + '/cookies.pkl'
CSVS_PATH = PROJECT_PATH + '/datasets/main/'


def get_children_of(ele):
    return ele.find_elements(By.XPATH, './*')


def get_first_child_of(ele):
    return ele.find_element(By.XPATH, './*')


def get_parent_of(ele):
    return ele.find_element(By.XPATH, '..')


def get_inner_text_of(ele):
    return ele.get_attribute('innerText')


def get_text_content_of(ele):
    return ele.get_attribute('textContent')


def get_outer_html_of(ele):
    return ele.get_attribute('outerHTML')


def clean_str(str_):
    cleaned_str = ''
    for i in str_.strip():
        if i in ('\n', '\t', '\r'):
            continue
        cleaned_str += i
    return cleaned_str                
        
        
def validate_datetime_str(datetime_str, regex_arr):
    for regex in regex_arr:
        if re.search(regex, datetime_str):
            return True
    return False


def validate_header_content(content):
    regex = '[\w\s\[\]()\.#*=+@$%ãáâàêéíóõúç!?<>:;/,&\-''""“]'
    return bool(re.search(regex, content))
    
    
def sleep_rand(min=3, max=15):
    return sleep(randint(min, max))
    
    
def read_cookie(path=COOKIE_PATH):
    return pickle.load(open(path, 'rb'))


def save_cookie(driver, path=COOKIE_PATH):
    cookies = driver.get_cookies()
    pickle.dump(cookies, open(COOKIE_PATH, 'wb'))


def get_month_number(month: str):
    month_lower = month.lower()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    for i in range(12):
        curr_month = months[i]
        if curr_month.startswith(month_lower):
            return i + 1


def convert_datetime_str(datetime_str):
    if not datetime_str:
        return None
    datetime_str = datetime_str.replace(' at ', ' ')
    split_data = datetime_str.split(', ')[-2:]
    month_day = split_data[0].split(' ')
    year_time = split_data[1].split(' ', 1)
    time = year_time[1].replace(' ', '')
    time_24hrs = datetime.strptime(time, '%I:%M%p').strftime('%H:%M')
    hours, minutes = time_24hrs.split(':')
    datetime_elements = dict()
    datetime_elements['day'] = int(month_day[1])
    datetime_elements['month'] = get_month_number(month_day[0])
    datetime_elements['year'] = int(year_time[0])
    datetime_elements['hour'] = int(hours)
    datetime_elements['minute'] = int(minutes)
    return datetime(datetime_elements['year'], datetime_elements['month'], datetime_elements['day'], datetime_elements['hour'], datetime_elements['minute'])
    
    
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


def get_day_period(timestamp):
    if not timestamp:
        return "desconhecido"
    hour = timestamp.hour
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
    valid_cols = [
        'titulo', 'descricao', 'data_hora', 'dia_semana',
        'periodo_dia', 'imagens', 'acessos', 'acessos_medio_hora',
        'tem_imagem_perfil'
    ]
    cols_to_drop = list()
    for col in cols:
        if col not in valid_cols:
            cols_to_drop.append(col)
    if len(cols_to_drop) > 0:
        df = df.drop(cols_to_drop, axis=1)
    return df


def get_anchor_that_matches_timestamp_pattern_of(pub, regex_arr):
    anchors = pub.find_elements(By.TAG_NAME, 'a')
    for anchor in anchors:
        anchor_txt = get_text_content_of(anchor)
        if validate_datetime_str(anchor_txt, regex_arr):
            return anchor


def get_header_content_div_of(pub):
    divs = pub.find_elements(By.TAG_NAME, 'div')     
    for div in divs:
        div_txt = get_text_content_of(div)
        if validate_header_content(div_txt):
            return div
              

def get_see_more_div_of(pub, see_more_regex):
    divs = pub.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
    for div in divs:
        div_txt = get_text_content_of(div)
        if re.search(see_more_regex, div_txt):
            return div
        
        
def get_div_that_matches(txt, pub):
    divs = pub.find_elements(By.TAG_NAME, 'div')
    for div in divs:
        div_txt = get_text_content_of(div)
        if div_txt == txt:
            return div
        
        
def get_all_attributes_of(ele):
    return ele.get_property('attributes')


def get_all_attributes_of(ele, driver):
    return driver.execute_script('''
        var items = {}; 
        for (let index = 0; index < arguments[0].attributes.length; index++) { 
            items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value 
        }; 
        return items;
    ''', ele)
        
        
def get_first_parent(tag_name, element):
    '''
    Returns the first parent web element of `element` that is a `tag_name`.
    '''
    parent = get_parent_of(element)
    while parent.tag_name != tag_name:
        parent = get_parent_of(parent)
    return parent

       
def get_close_button(driver):
    try:
        divs = driver.find_elements(By.TAG_NAME, 'div')
    except exceptions.NoSuchElementException:
        return None
    else:
        for div in divs:
            attrs = get_all_attributes_of(div, driver)
            for value in attrs.values():
                value_lower = value.lower()
                if value_lower == 'close':
                    return div
        return None


class UnknownLanguageException(Exception):
    def __init__(self, lang):
        valid_langs = [l.value for l in Lang]
        super().__init__(f'Unknown language: \'{lang}\'. Pick one from {valid_langs}')
        
        
class UnparsableTitleException(Exception):
    def __init__(self, title):
        super().__init__(f'Could not infer a language from title: \'{title}\'')
        
        
class Bundle(ABC):
    
    def __init__(self, *, lang, regex, months, weekdays, day_periods, algorithms):
        valid_lang = False
        for l in Lang:
            if l == lang:
                valid_lang = True
                break
        if not valid_lang:
            raise UnknownLanguageException(lang)
        self._lang = lang
        self._resources = {
            'regex': regex,
            'months': months,
            'weekdays': weekdays,
            'day_period': day_periods,
            'algorithms': algorithms
        }
        
    @property
    def resources(self):
        return self._resources
    
    @property
    def lang(self):
        return self._lang
    

class EnglishBundle(Bundle):
    
    def __init__(self):
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        
        def convert_datetime_str(datetime_str) -> None | datetime:
            if not datetime_str:
                return None
            
            def get_month_number(month: str):
                month_lower = month.lower()
                for i in range(12):
                    curr_month = months[i]
                    if curr_month.startswith(month_lower):
                        return i + 1
                    
            datetime_str = datetime_str.replace(' at ', ' ')
            split_data = datetime_str.split(', ')[-2:]
            month_day = split_data[0].split(' ')
            year_time = split_data[1].split(' ', 1)
            time = year_time[1].replace(' ', '')
            time_24hrs = datetime.strptime(time, '%I:%M%p').strftime('%H:%M')
            hours, minutes = time_24hrs.split(':')
            datetime_elements = dict()
            datetime_elements['day'] = int(month_day[1])
            datetime_elements['month'] = get_month_number(month_day[0])
            datetime_elements['year'] = int(year_time[0])
            datetime_elements['hour'] = int(hours)
            datetime_elements['minute'] = int(minutes)
            return datetime(datetime_elements['year'], datetime_elements['month'], datetime_elements['day'], datetime_elements['hour'], datetime_elements['minute'])
        
        super().__init__(
            lang=Lang.EN,
            regex={
                'datetime': [
                    '^\d\d?m$',
                    '^\d\d?h$',
                    '^\dd$',
                    '^[A-Z][a-z]{2,9} \d\d? at \d\d?:\d\d (PM|AM)$',
                    '^[A-Z][a-z]{5,9}, [A-Z][a-z]{2,9} \d\d?, \d{4} at \d\d?:\d\d (PM|AM)$',
                    '^[A-Z][a-z]{2,9} \d\d?$',
                    '^[A-Z][a-z]{2,9} \d\d?, \d{4}$'
                ],
                'see_more': '^See more$',
                'shared_with_public': 'Shared with Public',
            },
            months=months,
            weekdays=['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'],
            day_periods=['morning', 'afternoon', 'night'],
            algorithms={
                'convert_datetime_str': convert_datetime_str
            }
        )
    
    
class PortugueseBundle(Bundle):
    
    def __init__(self):
        months = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

        def convert_datetime_str(datetime_str):
            if not datetime_str:
                return None
            
            def get_month_number(month: str):
                month_lower = month.lower()
                for i in range(12):
                    curr_month = months[i]
                    if curr_month.startswith(month_lower):
                        return i + 1
                    
            datetime_str = datetime_str.replace(' de ', ' ').replace(' às ', ' ').split(', ')[-1]
            split_data = datetime_str.split(' ')
            day = int(split_data[0])
            month = int(get_month_number(split_data[1]))
            year = int(split_data[2])
            hours, minutes = split_data[3].split(':')
            return datetime(year, month, day, int(hours), int(minutes))
        
        super().__init__(
            lang=Lang.PT,
            regex={
                'datetime': [
                    '^\d d$',  # E.g., 5 d
                    '^\d\d? de [a-zç]{4,9}$',  # E.g., 12 de dezembro
                    '^\d\d? de [a-zç]{4,9} de \d{4}$',  # E.g., 5 de janeiro de 2021
                    '^\d\d? de [a-zç]{4,9} às \d\d:\d\d$',  # E.g., 18 de março às 11:30
                    '^\d\d? de [a-zç]{4,9} de \d{4} às \d\d:\d\d$',  # E.g., 20 de junho de 2015 às 15:37
                    '^[a-zA-Z-çá]{5,13}, \d\d? de [a-zç]{4,9} de \d{4} às \d\d:\d\d$'
                ],
                'see_more': '^Ver mais$',
                'shared_with_public': 'Conteúdo partilhado com: Público',
            },
            months=months,
            weekdays=['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'],
            day_periods=['manhã', 'tarde', 'noite'],
            algorithms={
                'convert_datetime_str': convert_datetime_str
            }
        )
    
    
class Lang(Enum):
    EN = 'en'
    PT = 'pt'
    UNKNOWN = None


def get_bundle(lang):
    bundles = {
        'en': EnglishBundle(),
        'pt': PortugueseBundle()
    }
    return bundles[lang.value]

    
class Bot:
    def __init__(self):
        options = ChromeOptions()
        prefs = {
            'profile.default_content_setting_values.cookies': 2,         # Disable cookies.
            'profile.block_third_party_cookies': True,
            'profile.managed_default_content_settings.images': 2,        # Disable images.
            'profile.default_content_setting_values.notifications': 2,   # Disable allow notification popup.
            # 'intl.accept_languages': 'en,en_US'
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--no-sandbox')
        # options.add_argument('--lang=en_US')  # Set language in headless mode.
        options.add_argument('--disable-dev-shm-usage')  # Use disk instead of main memory.
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        self._driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        self._driver.implicitly_wait(5)
        self._post_counter = 0
        self._data_dict = dict(
            header=list(),
            timestamp=list(),
            # images=list(),
            has_video=list(),
            # like=list(),
            # love=list(),
            # care=list(),
            # haha=list(),
            # wow=list(),
            # sad=list(),
            # angry=list(),
            # forwardings=list(),
            # comments=list()
        )
        self._curr_scroll_pos = 0  # A variable used later for keeping the current position of the page scrolling.
        self._curr_post_pos = 0
        self._start_date_time = datetime.now()
        self._lang = Lang.UNKNOWN
        self._bundle = None

    def get_posts(self):
        print('----- Bot is running -----')
        self._browse_to(FACEBOOK_URL + 'ifgoiano')
        self._set_lang()
        self._handle_cookies_popup_if_any()
        self._handle_login_popup_if_any()
        self._extract_posts()
        self._export_data_to_csv()
        
    def _browse_to(self, url):
        print(f'> Reaching \'{url}\'')
        self._driver.get(url)
        
    def _set_lang(self):
        page_lang = self._get_page_language()
        if 'en' in page_lang:
            self._lang = Lang.EN
        elif 'pt' in page_lang:
            self._lang = Lang.PT
        else:
            raise UnparsableTitleException(self._driver.title)
        self._bundle = get_bundle(self._lang)
        print(f'> Language set: {self._lang.value}')
        
    def _handle_cookies_popup_if_any(self):
        print('> Handling cookies popup if any')
        WAIT = 30
        selectors = [
            '//*[@id="facebook"]/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]',
            '//*[@id="facebook"]/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]'
        ]
        for selector in selectors:
            try:
                WebDriverWait(self._driver, WAIT).until(
                    ec.element_to_be_clickable((By.XPATH, selector))
                ).click()
            except exceptions.TimeoutException:
                pass
            else:
                return
    
    def _handle_login_popup_if_any(self):
        print('> Handling login popup if any')
        try:
            self._driver.find_element(By.TAG_NAME, 'form')
        except exceptions.NoSuchElementException:
            print('Form not found :<')
        else:
            ActionChains(self._driver).send_keys(Keys.BACK_SPACE).send_keys(Keys.ENTER).perform()
            
    def _extract_posts(self):
        print('> Extracting posts')
        while True:
            try:
                self._extract_data()
                self._scroll_page()
            except exceptions.WebDriverException as e:
                break
            
    def _export_data_to_csv(self):
        exec_end = datetime.now()
        print('-' * 100)
        print('|', f'Bot started on {self._start_date_time}'.center(98), '|', sep='')
        print('|', f'Bot finished on {exec_end}'.center(98), '|', sep='')
        print('|', f'Time spent: {exec_end - self._start_date_time}'.center(98), '|', sep='')
        print('|', f'Total of posts extracted: {self._curr_post_pos + 1}'.center(98), '|', sep='')
        print('-' * 100)
        if not os.path.exists(CSVS_PATH):
            os.makedirs(CSVS_PATH)
        print('> Exporting data to csv')
        dataframe = pandas.DataFrame(data=self._data_dict)
        exec_start_str = self._start_date_time.__str__().split('.')[0].replace(' ', '_').replace('-', '_').\
            replace(':', '_').replace('.', '_')
        csv_file_name = 'fb_data_' + exec_start_str + '_' + (exec_end - self._start_date_time).__str__().split('.')[0].\
            replace(':', '_') + '.csv'
        # dataframe = clean_dataframe(dataframe)
        dataframe.to_csv(CSVS_PATH + csv_file_name, index=False)
        
    def _extract_data(self):
        for post in self._get_web_elements_of_posts():
            self._data_dict['header'].append(self._extract_header(post))
            self._data_dict['timestamp'].append(
                self._bundle.resources['algorithms']['convert_datetime_str'](
                    self._extract_date_time(post, self._bundle.resources['regex']['datetime'])
                )
            )
            self._data_dict['has_video'].append(self._has_video(post))
            # if self._data_dict['has_video'][-1]:
            #     images = 0
            # else:
            #     images = self._count_images(post)
            # self._data_dict['images'].append(images)
            # self._fetch_reactions_and_populate(post)
            # self._data_dict['encaminhamentos'].append(self._extract_forwardings(curr_post))
            # self._data_dict['comentarios'].append(self._extract_comments(curr_post))
            self._show_post_info()
            self._curr_post_pos += 1
            # self._delete_element_from_page(post)
            
    def _scroll_page(self):
        self._curr_scroll_pos = self._get_current_scroll_pos()
        max_scroll_pos = self._get_max_scrollable_pos()
        # max_scroll_pos = self._get_max_scroll_pos()
        new_scroll_pos = int(self._curr_scroll_pos + (max_scroll_pos - self._curr_scroll_pos) * .8)
        self._driver.execute_script(f'window.scrollTo(0, {new_scroll_pos});')
        sleep_rand()
        if self._get_current_scroll_pos() == self._curr_scroll_pos:  # Page is taking too much to load.
            self._driver.execute_script(f'window.scrollTo(0, {int(self._curr_scroll_pos * .8)})')  # Scroll up 20%.
   
    def _show_post_info(self):
        post_data = {}
        for key in self._data_dict.keys():
            value = self._data_dict[key][-1]
            if value.__class__.__name__ == 'datetime':
                value = str(value)
            if len(str(value)) > 25:
                value = value[0:25] + '...'
            post_data[key] = value
        print(f'({self._curr_post_pos + 1}) - {post_data}')
        
    def _reset_values(self):
        for key in self._data_dict.keys():
            self._data_dict[key].clear()
        self._curr_post_pos = 0

    def _get_inner_text_of(self, ele):
        return self._driver.execute_script('return arguments[0].innerText;', ele)
        
    def _get_current_scroll_pos(self):
        return int(self._driver.execute_script('return document.documentElement.scrollTop || document.body.scrollTop;'))
    
    def _get_max_scrollable_pos(self):
        # For some reason, document.body.scrollHeight does not return the actual max scrollable height.
        self._curr_scroll_pos = self._get_current_scroll_pos()
        self._driver.execute_script(f'window.scrollTo(0, {self._get_max_scroll_pos()})')  # Try to scroll to the maximum pos.
        actual_max_scrollable_pos = self._get_current_scroll_pos()  # Get the actual maximum scrollable pos.
        self._driver.execute_script(f'window.scrollTo(0, {self._curr_scroll_pos})')  # Go back to the former value.
        return actual_max_scrollable_pos
        
    def _get_max_scroll_pos(self):
        return int(self._driver.execute_script('return document.body.scrollHeight;'))
    
    def _get_all_attribute_values_of(self, ele):
        return self._driver.execute_script('''
            var values = []; 
            for (index = 0; index < arguments[0].attributes.length; index++) { 
                values.push(arguments[0].attributes[index].value);
            }
            return values;
        ''', ele)
    
    def _open_new_tab(self, url):
        self._driver.execute_script(f'window.open("{url}", "new page");')
        self._driver.switch_to.window(self._driver.window_handles[-1])
    
    def _close_current_tab(self):
        self._driver.close()
        if len(self._driver.window_handles) == 0:
            self._driver.quit()
        else:
            self._driver.switch_to.window(self._driver.window_handles[-1])
    
    def _scroll_to_element(self, ele, offset=150):
        x, y = ele.location['x'], ele.location['y'] - offset
        scroll_by_coord = f'window.scrollTo({x},{y});'
        self._driver.execute_script(scroll_by_coord)
    
    def _extract_header(self, pub):
        def clean_header_content(content):
            shared_with_public_txt = self._bundle.resources['regex']['shared_with_public']
            i_s_w_p = content.index(shared_with_public_txt) + len(shared_with_public_txt)
            result = content[i_s_w_p : len(content)].replace('\n', ' ').strip()
            while shared_with_public_txt in result:
                result = result.replace(shared_with_public_txt, '')
            return result
        
        pub_txt = get_text_content_of(pub)
        see_more_txt = self._bundle.resources['regex']['see_more'][1:-1]
        while see_more_txt in pub_txt:
            see_more_div = get_see_more_div_of(pub, see_more_txt)
            if see_more_div:
                self._scroll_to_element(see_more_div)
                ActionChains(self._driver).move_to_element(see_more_div).click(see_more_div).perform()
            pub_txt = get_text_content_of(pub)
        return clean_header_content(get_text_content_of(pub))
    
    def _extract_date_time(self, pub, regex_arr):
        def swap_funcs(funcs):
            funcs.append(funcs[0])
            del funcs[0]
            
        get_text_funcs = [get_text_content_of, get_inner_text_of]
        while True:
            try:
                anchor = get_anchor_that_matches_timestamp_pattern_of(pub, regex_arr)
                while not anchor:
                    anchor = get_anchor_that_matches_timestamp_pattern_of(pub, regex_arr)
                self._scroll_to_element(anchor)
                ActionChains(self._driver).move_to_element(anchor).perform()
                try:    
                    # tooltip_span = WebDriverWait(self._driver, 30).until(
                    #     ec.presence_of_element_located((By.CSS_SELECTOR, 'span[role="tooltip"]'))
                    # )
                    # tooltip_span = self._driver.find_element(By.ID, aria_describedby)
                    tooltip_spans = WebDriverWait(self._driver, 30).until(
                        ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[role="tooltip"]'))
                    )
                except exceptions.TimeoutException:
                    return None
                else:
                    return get_text_content_of(tooltip_spans[-1])
            except exceptions.StaleElementReferenceException:
                swap_funcs(get_text_funcs)
        
    # def _count_images(self, pub):
    #     image_counter = 0
    #     possible_urls = ['https://scontent', 'https://external']
    #     for url in possible_urls:
    #         try:
    #             images = pub.find_elements(By.CSS_SELECTOR, f'img[src^="{url}"]')
    #         except exceptions.NoSuchElementException:
    #             pass
    #         else:
    #             image_counter += len(images)
    #     return image_counter
    
    def _count_images(self, pub):
        '''
        Counts how many images `pub` has. It is considered an image one that is `accessible through https`, `has a class` attribute and is `enclosed by an anchor`.
        '''
        try:
            images = pub.find_elements(By.CSS_SELECTOR, 'img[src^="https://"]')  # Get only images accessible through https. 
            filtered = []
            for image in images:
                if image.get_attribute('src').startswith('https://static'):
                    continue
                filtered.append(image)
        except exceptions.NoSuchElementException:
            return 0
        else:
            image_counter = 0
            for image in filtered:
                if image.get_attribute('class'):
                    fp_a = get_first_parent('a', image)
                    fp_a_href = fp_a.get_attribute('href')
                    if not fp_a_href.startswith('https://www.facebook.com'):
                        return len(filtered)
                    self._open_new_tab(fp_a_href)
                    first_image_url = self._driver.current_url.removesuffix('/')
                    if '/pcb.' in first_image_url:  # There are multiple images for the current post.
                        while True:
                            body = self._driver.find_element(By.TAG_NAME, 'body')
                            ActionChains(self._driver).move_to_element(body).click(body).perform()
                            body.send_keys(Keys.ARROW_RIGHT)
                            image_counter += 1
                            if self._driver.current_url == first_image_url:
                                self._close_current_tab()
                                return image_counter
                    else:
                        self._close_current_tab()
                        return len(filtered)
            return image_counter
                
    def _populate_reactions(self, reactions_data=dict()):
        keys = reactions_data.keys()
        reactions = ('like', 'love', 'care', 'haha', 'wow', 'sad', 'angry')
        for reaction in reactions:
            if reaction not in keys:
                reactions_data[reaction] = 0
        for key, value in reactions_data.items():
            self._data_dict[key].append(value)
        
    def _fetch_reactions_and_populate(self, pub):
        try:
            toolbar_span = pub.find_element(By.CSS_SELECTOR, 'span[role="toolbar"]')
            tb_s_child = get_first_child_of(toolbar_span)
            reactions = dict()
            for child in get_children_of(tb_s_child):
                while True:
                    self._scroll_to_element(child)
                    ActionChains(self._driver).move_to_element(child).perform()
                    try:
                        tooltip_span = WebDriverWait(self._driver, 30).until(
                            ec.presence_of_element_located((By.CSS_SELECTOR, 'span[role="tooltip"]'))
                        )
                    except exceptions.TimeoutException:
                        pass
                    else:
                        tt_s_split_inner_text = get_inner_text_of(tooltip_span).strip().split('\n')
                        reactions[tt_s_split_inner_text[0].lower()] = len(tt_s_split_inner_text[1:])
                        break
            self._populate_reactions(reactions)
        except exceptions.NoSuchElementException:
            self._populate_reactions()  # Post has no reactions at all!
    
    def _extract_forwardings(self, pub):
        pass
    
    def _has_video(self, pub):
        try:
            pub.find_element(By.TAG_NAME, 'video')
        except exceptions.NoSuchElementException:
            return False
        else:
            return True
        
    def _get_web_elements_of_posts(self):
        while True:
            try:
                role_main  = WebDriverWait(self._driver, 15).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"]'))
                )
                role_articles = WebDriverWait(role_main, 30).until(
                    ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="article"]'))
                )
            except exceptions.TimeoutException:
                print('Feed div not found')
            else:
                break
        return role_articles[self._curr_post_pos : -3]
        # feed_div_children = feed_div.find_elements(By.XPATH, './*')
        # return feed_div_children[self._curr_post_pos:-3]  # There are 3 trash divs.
            
    def _go_back(self):
        ActionChains(self._driver).send_keys(Keys.ALT).send_keys(Keys.ARROW_LEFT).perform()
        
    def _delete_element_from_page(self, ele):
        self._driver.execute_script('arguments[0].parentNode.removeChild(arguments[0]);', ele)
            
    def _wait_loading(self):
        sleep_rand()
        # self._driver.execute_script(f'window.scrollTo(0, {self._get_current_scroll_pos() * .9});')
        # WAIT_LIMIT = 60
        # now = datetime.now()
        # secs_timedelta = timedelta(seconds=WAIT_LIMIT)
        # while datetime.now() - now < secs_timedelta:  # Keep checking for WAIT_LIMIT seconds.
        # while True:
        #     feed_div = self._driver.find_element(By.CSS_SELECTOR, self._posts_div)
        #     feed_div_children = feed_div.find_elements(By.XPATH, './*')
        #     if len(feed_div_children) - 3 > self._curr_post_pos + 1:  # If more posts were loaded to the page.
        #         return
        #     self._driver.execute_script(f'window.scrollTo(0, {self._get_max_scroll_pos() * .9});')
            # sleep_rand()
                
    def _page_is_done(self):
        # return self._get_current_scroll_pos() == self._curr_scroll_pos
        return self._curr_post_pos == 999
    
    def _simulate_scrolling(self, times=5):
        print('> Simulating user scrolling')
        for i in range(times):    
            rand_scroll = randint(0, self._get_max_scroll_pos())
            self._driver.execute_script(f'window.scrollTo(0, {rand_scroll});')
            sleep_rand()
        self._driver.execute_script(f'window.scrollTo(0, 0);')
            
    def _get_page_language(self):
        return self._driver.execute_script('return document.documentElement.lang;')
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()
        print('----- Bot execution finished -----')
        

if __name__ == '__main__':
    with Bot() as bot:
        bot.get_posts()
 