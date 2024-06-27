from airflow import DAG
from airflow.operators.python import PythonOperator

IFGOIANO_HOME = 'https://ifgoiano.edu.br/home/index.php'
IFGOIANO_PUBS_PAGE = \
    'https://www.ifgoiano.edu.br/home/index.php/component/content/category/160-noticias-anteriores.html'
DEFAULT_WAIT_SECS = 25


def get_month_number(month: str) -> int:
    month_lower = month.lower()
    if month_lower == 'janeiro':
        return 1
    elif month_lower == 'fevereiro':
        return 2
    elif month_lower == 'março':
        return 3
    elif month_lower == 'abril':
        return 4
    elif month_lower == 'maio':
        return 5
    elif month_lower == 'junho':
        return 6
    elif month_lower == 'julho':
        return 7
    elif month_lower == 'agosto':
        return 8
    elif month_lower == 'setembro':
        return 9
    elif month_lower == 'outubro':
        return 10
    elif month_lower == 'novembro':
        return 11
    elif month_lower == 'dezembro':
        return 12
    else:
        return -1


def get_datetime(date_str):
    from datetime import datetime
    
    if date_str is None:
        return None
    split_data = date_str.replace(',', '').replace(':', '').replace(' de', '').split(' ')
    date = dict()
    for i in split_data:
        if i.isdigit():
            i_int = int(i)
            if i_int <= 31:
                attr = 'day'
            else:
                attr = 'year'
            date[attr] = i_int
        else:
            month_number = get_month_number(i)
            if month_number != -1:
                date['month'] = month_number
            else:
                hour = ''
                minute = ''
                h_found = False
                for j in i:
                    if j == 'h':
                        h_found = True
                        continue
                    if h_found:
                        minute += j
                    else:
                        hour += j
                if hour.isdigit():
                    date['hour'] = int(hour)
                if minute.isdigit():
                    date['minute'] = int(minute)
    return datetime(date['year'], date['month'], date['day'], date['hour'], date['minute'])


def get_datetime_from(date_string, time_string):
    from datetime import datetime
    
    date_elements = date_string.split('/')
    year, month, day = int('20' + date_elements[2]), int(date_elements[1]), int(date_elements[0])
    time_elements = time_string.split('h')
    hour, minute = int(time_elements[0]), int(time_elements[1])
    return datetime(year, month, day, hour, minute)


def get_relevance_index(timestamp, accesses):
    from datetime import datetime
    
    if timestamp is None or accesses is None:
        return None
    else:
        time_since_publication = datetime.now() - timestamp
        hours_since_publication = time_since_publication.total_seconds() / 3600
        return round(accesses / hours_since_publication, 2)


def get_weekday(timestamp):
    if timestamp is None:
        return "desconhecido"
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
        return "desconhecido"


def get_day_period(timestamp):
    if timestamp is None:
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
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        from webdriver_manager.core.utils import ChromeType
        
        options = ChromeOptions()
        prefs = {
            'profile.managed_default_content_settings.images': 2,   # Disable images.
            'intl.accept_languages': 'en,en_US'                     # Set English as browser default language.
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')  # Use disk instead of main memory.
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
            titulo=list(),
            descricao=list(),
            data_hora=list(),
            dia_semana=list(),
            periodo_dia=list(),
            imagens=list(),
            acessos=list(),
            acessos_medio_hora=list(),
            tem_imagem_perfil=list()
        )

    def _show_post_info(self):
        self._post_counter += 1
        post_title = self._data_dict['titulo'][len(self._data_dict['titulo']) - 1]
        print(f'({self._post_counter}) - {post_title}')

    def _extract_post_data(self, extract_timestamp=True):
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support import expected_conditions as ec
        from selenium.common import exceptions
        from selenium.webdriver.common.by import By
        
        content_panel = WebDriverWait(self._driver, DEFAULT_WAIT_SECS).until(
            ec.presence_of_element_located((By.ID, 'content'))
        )
        title = WebDriverWait(content_panel, DEFAULT_WAIT_SECS).until(
            ec.presence_of_element_located((By.TAG_NAME, 'h1'))
        ).text.strip()
        timestamp = None
        if extract_timestamp:
            try:
                timestamp_str = WebDriverWait(content_panel, DEFAULT_WAIT_SECS).until(
                    ec.presence_of_element_located((By.CLASS_NAME, 'documentPublished'))
                ).text.strip()
                timestamp = get_datetime(timestamp_str)
            except (exceptions.NoSuchElementException, exceptions.TimeoutException):
                pass
        try:
            accesses_str = WebDriverWait(content_panel, DEFAULT_WAIT_SECS).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'documentHits'))
            ).text.strip().split(' ')[1]
            accesses = int(accesses_str) - 1
        except (exceptions.NoSuchElementException, exceptions.TimeoutException):
            accesses = None
        try:
            description = WebDriverWait(self._driver, DEFAULT_WAIT_SECS).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'description'))
            ).text.strip()
        except (exceptions.NoSuchElementException, exceptions.TimeoutException):
            try:
                description = WebDriverWait(self._driver, DEFAULT_WAIT_SECS).until(
                    ec.presence_of_element_located((By.CLASS_NAME, 'subtitle'))
                ).text.strip()
            except (exceptions.NoSuchElementException, exceptions.TimeoutException):
                description = None  # Post does not have description.
        images_count = len(content_panel.find_elements(By.TAG_NAME, 'img'))
        if self._data_dict['tem_imagem_perfil'][-1]:  # Access the last element inside the list.
            images_count += 1
        self._data_dict['titulo'].append(title)
        self._data_dict['descricao'].append(description)
        if extract_timestamp:
            self._data_dict['data_hora'].append(timestamp)
            self._data_dict['dia_semana'].append(get_weekday(timestamp))
            self._data_dict['periodo_dia'].append(get_day_period(timestamp))
            self._data_dict['acessos_medio_hora'].append(get_relevance_index(timestamp, accesses))
        self._data_dict['imagens'].append(images_count)
        self._data_dict['acessos'].append(accesses)

    def _reset_values(self):
        for key in self._data_dict.keys():
            self._data_dict[key].clear()
        self._post_counter = 0

    def get_posts(self):
        from selenium.webdriver.common.by import By
        from datetime import datetime, timedelta
        from selenium.common import exceptions
        import pandas
        import os
        
        print('----- Bot is running -----')
        three_hours = timedelta(hours=3)
        exec_start = datetime.now() - three_hours
        try:
            while True:
                try:
                    self._driver.get(IFGOIANO_HOME)
                except exceptions.TimeoutException:
                    pass
                else:
                    print(f'> Accessed \'{IFGOIANO_HOME}\'')
                    break
            # Get the data of the featured post.
            featured_post_box = self._driver.find_element(By.CLASS_NAME, 'manchete-texto-lateral')
            featured_post_url = featured_post_box.find_element(By.TAG_NAME, 'a').get_attribute('href').strip()
            post_has_profile_image = len(featured_post_box.find_elements(By.TAG_NAME, 'img')) == 1
            self._driver.execute_script(f"window.open('{featured_post_url}', 'new page');")
            self._driver.switch_to.window(self._driver.window_handles[1])
            if post_has_profile_image:
                self._data_dict['tem_imagem_perfil'].append('sim')
            else:
                self._data_dict['tem_imagem_perfil'].append('nao')
            self._extract_post_data()
            self._driver.close()
            self._show_post_info()
            self._driver.switch_to.window(self._driver.window_handles[0])
            print(f'> Data of featured post extracted')
            # Get the data of the remaining posts at IFGOIANO_HOME.
            box_secondary_posts = self._driver.find_element(By.CLASS_NAME, 'chamadas-secundarias')
            secondary_posts = box_secondary_posts.find_elements(By.TAG_NAME, 'div')
            for secondary_post in secondary_posts:
                post_has_profile_image = len(secondary_post.find_elements(By.TAG_NAME, 'img')) == 1
                secondary_post_url = secondary_post.find_element(By.TAG_NAME, 'a').get_attribute('href').strip()
                self._driver.execute_script(f"window.open('{secondary_post_url}', 'new page');")
                self._driver.switch_to.window(self._driver.window_handles[1])
                if post_has_profile_image:
                    self._data_dict['tem_imagem_perfil'].append('sim')
                else:
                    self._data_dict['tem_imagem_perfil'].append('nao')
                self._extract_post_data()
                self._driver.close()
                self._driver.switch_to.window(self._driver.window_handles[0])
                self._show_post_info()
            print(f'> Data of the remaining posts at site home extracted')
            # Get the data of all posts at IFGOIANO_PUBS_PAGE.
            while True:
                try:
                    self._driver.get(IFGOIANO_PUBS_PAGE)
                except exceptions.TimeoutException:
                    pass
                else:
                    print(f'> Accessed \'{IFGOIANO_PUBS_PAGE}\'')
                    break
            post_boxes = self._driver.find_elements(By.CLASS_NAME, 'tileItem')
            for post_box in post_boxes[:len(post_boxes) - 1]:  # Ignore the last post.
                post_title = post_box.find_element(By.CLASS_NAME, 'tileHeadline')
                post_url = post_title.find_element(By.TAG_NAME, 'a').get_attribute('href').strip()
                post_has_profile_image = len(post_box.find_elements(By.TAG_NAME, 'img')) == 1
                post_box_side_info = post_box.find_elements(By.TAG_NAME, 'li')
                date_published = post_box_side_info[2].text
                time_published = post_box_side_info[3].text
                post_publication_timestamp = get_datetime_from(date_published, time_published)
                self._driver.execute_script(f"window.open('{post_url}', 'new page');")
                self._driver.switch_to.window(self._driver.window_handles[1])
                if post_has_profile_image:
                    self._data_dict['tem_imagem_perfil'].append('sim')
                else:
                    self._data_dict['tem_imagem_perfil'].append('nao')
                self._extract_post_data(extract_timestamp=False)
                self._data_dict['data_hora'].append(post_publication_timestamp)
                self._data_dict['dia_semana'].append(get_weekday(post_publication_timestamp))
                self._data_dict['periodo_dia'].append(get_day_period(post_publication_timestamp))
                self._data_dict['acessos_medio_hora'].append(get_relevance_index(post_publication_timestamp,
                                                                                 self._data_dict['acessos'][-1]))
                self._driver.close()
                self._driver.switch_to.window(self._driver.window_handles[0])
                self._show_post_info()
                if self._post_counter == 10:
                    break
            self._driver.quit()
            print('> Data of all remaining posts extracted')
            print('----- Bot execution finished -----')
            exec_end = datetime.now() - three_hours
            print('-' * 100)
            print('|', f'Bot started on {exec_start}'.center(98), '|', sep='')
            print('|', f'Bot finished on {exec_end}'.center(98), '|', sep='')
            print('|', f'Time spent: {exec_end - exec_start}'.center(98), '|', sep='')
            print('|', f'Total of posts extracted: {self._post_counter}'.center(98), '|', sep='')
            print('-' * 100)
            # if not os.path.exists(CSVS_PATH):
            #     os.makedirs(CSVS_PATH)
            dataframe = pandas.DataFrame(data=self._data_dict)
            exec_start_str = exec_start.__str__().split('.')[0].replace(' ', '_').replace('-', '_').\
                replace(':', '_').replace('.', '_')
            csv_file_name = '/site_data_' + exec_start_str + '_' + (exec_end - exec_start).__str__().split('.')[0].\
                replace(':', '_') + '.csv'
            dataframe = clean_dataframe(dataframe)
            dir = os.path.dirname(os.path.abspath(__file__))
            dataframe.to_csv(dir + csv_file_name, index=False)
            print(f'> Extracted data export to csv file \'{csv_file_name}\'')
        except KeyboardInterrupt:
            print('\n----- Bot execution interrupted -----')
        except Exception as e:
            print(f'----- Exception raised: {e.__class__.__name__} -----')
            raise
    
    
if __name__ == '__main__':
    from datetime import datetime, timedelta
    
    dag_args = {
        'owner': 'Rafael',
        'retries': 5,
        'retry_delay': timedelta(minutes=5)
    }
    start_date = datetime(2023, 2, 20)  # Change the starting date accordingly.
        
    with DAG(
        dag_id='ifgoiano_site_dag',
        description='DAG for getting and processing data of publications from www.ifgoiano.edu.br',
        default_args=dag_args,
        start_date=start_date,
        end_date=start_date + timedelta(days=30),
        schedule='0 21 * * *',  # timedelta(hours=18, minutes=0, seconds=0),
        catchup=False
    ) as dag:
        get_posts = PythonOperator(
            task_id='get_posts',
            python_callable=Bot().get_posts
        )
        get_posts
