import os

BASE_DIR = '/home/leafar/Documents/dev/projeto-iniciacao-cientifica/airflow/dags/'
TARGET_DIR = '/home/leafar/Documents/dev/projeto-iniciacao-cientifica/ifgoiano_site/dataset/'
        

if __name__ == '__main__':
	os.system(f'mv {BASE_DIR}/site_data*.csv {TARGET_DIR}')
