from modules import input_tools, parsing, xlsx

def get_and_save_data(start_dt, end_dt, xlsx_name):
    data = parsing.get_temperatures_in_range(start_dt, end_dt)
    xlsx.save_to_xlsx(data, xlsx_name)

def main():
    start_dt, end_dt = input_tools.input_data()
    xlsx_name = input_tools.input_xlsx_name()
    print('-'*40)
    get_and_save_data(start_dt, end_dt, xlsx_name)
    print('Данные сохранены в таблицу')

if __name__ == '__main__':
    main()
