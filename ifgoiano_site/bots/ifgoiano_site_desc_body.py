import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import pandas
import os


IFGOIANO_HOME = 'https://ifgoiano.edu.br/home/index.php'
IFGOIANO_PUBS_PAGE = 'https://www.ifgoiano.edu.br/home/index.php/component/content/category/160-noticias-anteriores.html'
DEFAULT_WAIT_SECS = 30
CSVS_PATH = os.path.dirname(os.path.abspath(__file__)) + '/datasets/'


def clean_dataframe(df):
    df = df[df['descricao'].notna()].reset_index()  # Drop the rows with 'descricao' equal to 'nan'.
    df = df[df['corpo'].notna()].reset_index()  # Drop the rows with 'corpo' equal to 'nan'.
    df = df.drop_duplicates(subset=['descricao', 'corpo']).reset_index()  # Drop duplicates.
    cols = df.columns
    valid_cols = ['descricao', 'corpo']
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
            'profile.managed_default_content_settings.images': 2,   # Disable images.
            'intl.accept_languages': 'en,en_US'
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--log-level=3')
        self._driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ),
            options=options
        )
        self._driver.implicitly_wait(5)
        self._post_counter = 0
        self._data_dict = dict(
            descricao=list(),
            corpo=list()
        )
        print('----- Bot is running -----')

    def _show_post_info(self):
        self._post_counter += 1
        post_data = self._data_dict['descricao'][len(self._data_dict['descricao']) - 1]
        print(f'({self._post_counter}) - {post_data}')

    def _extract_post_data(self):
        try:
            description = WebDriverWait(self._driver, DEFAULT_WAIT_SECS).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'description'))
            ).text.strip().replace('\n', ' ').replace(',', ' ')
        except (exceptions.NoSuchElementException, exceptions.TimeoutException):
            try:
                description = WebDriverWait(self._driver, DEFAULT_WAIT_SECS).until(
                    ec.presence_of_element_located((By.CLASS_NAME, 'subtitle'))
                ).text.strip().replace('\n', ' ').replace(',', ' ')
            except (exceptions.NoSuchElementException, exceptions.TimeoutException):
                description = None  # Post does not have description.
        content_panel = WebDriverWait(self._driver, DEFAULT_WAIT_SECS).until(
            ec.presence_of_element_located((By.ID, 'content'))
        )
        paragraphs = content_panel.find_elements(By.TAG_NAME, 'p')
        body = ''.join(
            [p.text for p in paragraphs]
        ).strip().replace('\n', ' ').replace(',', ' ')
        if description is not None:
            body = body.replace(description, '')
        self._data_dict['descricao'].append(description)
        self._data_dict['corpo'].append(body)

    def _reset_values(self):
        for key in self._data_dict.keys():
            self._data_dict[key].clear()
        self._post_counter = 0

    def export_data(self):
        self._driver.quit()
        exec_end = datetime.now()
        print('-' * 100)
        print('|', f'Bot started on {self._exec_start}'.center(98), '|', sep='')
        print('|', f'Bot finished on {exec_end}'.center(98), '|', sep='')
        print('|', f'Time spent: {exec_end - self._exec_start}'.center(98), '|', sep='')
        print('|', f'Total of posts extracted: {self._post_counter}'.center(98), '|', sep='')
        print('-' * 100)
        if not os.path.exists(CSVS_PATH):
            os.makedirs(CSVS_PATH)
        dataframe = pandas.DataFrame(data=self._data_dict)
        exec_start_str = self._exec_start.__str__().split('.')[0].replace(' ', '_').replace('-', '_').\
            replace(':', '_').replace('.', '_')
        csv_file_name = 'pubs_data_' + exec_start_str + '_' + (exec_end - self._exec_start).__str__().split('.')[0].\
            replace(':', '_') + '.csv'
        dataframe.to_csv(CSVS_PATH + csv_file_name, index=False)

    def get_posts(self):
        self._exec_start = datetime.now()
        try:
            self._driver.get(IFGOIANO_HOME)
            featured_post_box = self._driver.find_element(By.CLASS_NAME, 'manchete-texto-lateral')
            featured_post_url = featured_post_box.find_element(By.TAG_NAME, 'a').get_attribute('href').strip()
            self._driver.execute_script(f'window.open(\'{featured_post_url}\', \'new page\');')
            self._driver.switch_to.window(self._driver.window_handles[1])
            self._extract_post_data()
            self._driver.close()
            self._show_post_info()
            self._driver.switch_to.window(self._driver.window_handles[0])
            box_secondary_posts = self._driver.find_element(By.CLASS_NAME, 'chamadas-secundarias')
            secondary_posts = box_secondary_posts.find_elements(By.TAG_NAME, 'div')
            for secondary_post in secondary_posts:
                secondary_post_url = secondary_post.find_element(By.TAG_NAME, 'a').get_attribute('href').strip()
                self._driver.execute_script(f'window.open(\'{secondary_post_url}\', \'new page\');')
                self._driver.switch_to.window(self._driver.window_handles[1])
                self._extract_post_data()
                self._driver.close()
                self._driver.switch_to.window(self._driver.window_handles[0])
                self._show_post_info()
            self._driver.get(IFGOIANO_PUBS_PAGE)
            post_boxes = self._driver.find_elements(By.CLASS_NAME, 'tileItem')
            for post_box in post_boxes[:len(post_boxes) - 1]:  # Ignore the last post.
                post_title = post_box.find_element(By.CLASS_NAME, 'tileHeadline')
                post_url = post_title.find_element(By.TAG_NAME, 'a').get_attribute('href').strip()
                self._driver.execute_script(f'window.open(\'{post_url}\', \'new page\');')
                self._driver.switch_to.window(self._driver.window_handles[1])
                self._extract_post_data()
                self._driver.close()
                self._driver.switch_to.window(self._driver.window_handles[0])
                self._show_post_info()
                # if self._post_counter == 10:
                #     self.export_data()
            self.export_data()
        except KeyboardInterrupt:
            print('\n----- Bot execution interrupted -----')
        except Exception as e:
            print(f'----- Exception raised: {e.__class__.__name__} -----')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()
        print('----- Bot execution finished -----')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.propagate = False
    logger.disabled = True
    with Bot() as bot:
        bot.get_posts()
 