from datetime import datetime

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


if __name__ == '__main__':
    print(convert_datetime_str('Domingo, 24 de JUNHO de 2023 às 2:30'))
