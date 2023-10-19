import json
import time

# получаем текущий год исходя из системного времени
def get_current_year():
    current_time = time.localtime(None)
    return current_time.tm_year

# используется для .sort(), чтобы провести сортировку данных по
# ВВП
def get_gdp_key_from_row(row):
    return row['GDP']

# используется для filter(), чтобы выкинуть все сущности, где не
# указан текущий год
def is_current_year_in_row(row):
    return (row['Year'] == get_current_year())

class Database:
    # получаем максимально возможное значение у IndicatorID исходя из
    # существующих данных
    def get_max_id(self):
        result_max = 0

        for row in self.data:
            current_max = row["IndicatorID"]

            if current_max > result_max:
                result_max = current_max

        return result_max

    def __init__(self):
        self.data = []

    def load_data(self, filename):
        # Загрузка данных из файла
        f = open(filename, 'r', encoding="utf-8")
        to_load = f.read()
        self.data = json.loads(to_load)
        f.close()

    def save_data(self, filename):
        f = open(filename, 'w', encoding="utf-8")
        to_write = json.dumps(self.data)
        f.write(to_write)
        f.flush()
        f.close()
        # Сохранение данных в файл

    def add_entity(self, entity):
        self.data.append(entity)

    def remove_entity(self, entity):
        for i in range(len(self.data)):
            if self.data[i]["IndicatorID"] == entity:
                del self.data[i]
                return

    def update_entity(self, user_id, entity):
        for i in range(len(self.data)):
            if self.data[i]["IndicatorID"] == user_id:
                self.data[i] = entity
                self.data[i]["IndicatorID"] = user_id

    def get_column_lengths(self, data):
        column_lengths = [0] * len(data[0])

        for row in data:
            for i, value in enumerate(row):
                column_lengths[i] = max(column_lengths[i], len(str(row[value])))


        return column_lengths


    def print_header(self, column_lengths):
        head_len = 0
        for i in column_lengths:
            head_len = head_len + i + 3
        print('='*head_len)

    # получаем данные по указанной стране за последние 5 лет (отсчитывая от текущего
    # системного года)
    def get_country_specific_indicators(self, name):
        current_year = get_current_year()
        filtered_data = []

        for row in self.data:
            if row['Country'] == name and row['Year'] >= (current_year - 5) \
               and row['Year'] <= current_year:
                filtered_data.append(row)

        return filtered_data

    # получаем данные по странам, у которых инфляция >= limit
    def get_countries_with_limited_inflation(self, limit):
        filtered_data = []

        for row in self.data:
            if row['Inflation'] >= limit:
                filtered_data.append(row)

        return filtered_data

    # получаем данные по странам, у которых топовое ВВП за последний год, в порядке
    # убывания
    def get_top_gdp_countries(self):
        filtered_data = list(filter(is_current_year_in_row, self.data))
        filtered_data.sort(key=get_gdp_key_from_row, reverse=True)

        return filtered_data

    def display_entities(self, to_display=None):
        # Вывод данных в виде таблицы
        output_data = self.data

        if to_display:
            output_data = to_display

        if not output_data:
            print("Нет данных")
            return

        # # Определение максимальной длины для каждого столбца

        column_lengths = self.get_column_lengths(output_data)

        # Вывод данных
        self.print_header(column_lengths)
        for row in output_data:
            self._print_row(row, column_lengths)
        self.print_header(column_lengths)

    def _print_row(self, row, column_lengths):
        print('|',end='')
        i = 0
        for attr, value in row.items():
            print(str(value).ljust(column_lengths[i],' '),end='')
            print(' | ',end='')
            i += 1
        print('')

def make_user_input_entity():
    print("Введите страну")
    user_country = input()

    print("Введите год")
    user_year = int(input())

    print("Введите ВВП")
    user_GDP = float(input())

    print("Введите процент инфляции")
    user_inf = float(input())

    user_input = {'IndicatorID': 0, 'Country': user_country, 'Year': user_year, 'GDP': user_GDP, 'Inflation': user_inf}
    return user_input

def obtain_user_id(db):
    user_id = int(input())

    if user_id >= db.get_max_id() or user_id < 0:
        print("Вы ввели неверный порядковый номер")
        exit(1)

    return user_id

def menu(db):
    while True:
        print("=== Консольное меню ===")
        print("1. Отобразить таблицу")
        print("2. Добавить сущность")
        print("3. Удалить сущность")
        print("4. Обновить сущность")
        print("5. Отобразить показатели страны за последние 5 лет")
        print("6. Отобразить страны, соответствующие указанному ограничению по инфляции")
        print("7. Отобразить страны с наилучшим ВВП за последний год")
        print("8. Завершение работы")

        choice = int(input("Введите номер пункта меню: "))

        if choice == 1:
            print("Содержимое таблицы:")
            # Код для выполнения действий меню 1
            db.display_entities()

        elif choice == 2:
            # Код для выполнения действий меню 2
            user_input = make_user_input_entity()

            max_id = db.get_max_id()
            user_input["IndicatorID"] = max_id + 1

            db.add_entity(user_input)
            print("Успех", max_id)

        elif choice == 3:
            print("Введите порядковый номер сущности, которую вы желаете удалить")

            # Код для выполнения действий меню 3
            user_id = obtain_user_id(db)
            db.remove_entity(user_id)
        elif choice == 4:
            print("Введите порядковый номер сущности, которую вы желаете обновить")
            # Код для выполнения действий меню 4

            user_id = obtain_user_id(db)
            user_input = make_user_input_entity()

            db.update_entity(user_id, user_input)

        elif choice == 5:
            print("Введите страну")
            user_country = input()

            db.display_entities(db.get_country_specific_indicators(user_country))

        elif choice == 6:
            print("Введите ограничение по инфляции")
            user_inf = float(input())

            db.display_entities(db.get_countries_with_limited_inflation(user_inf))

        elif choice == 7:
            db.display_entities(db.get_top_gdp_countries())

        elif choice == 8:
            print("Выход из программы")
            break

        else:
            print("Неверный выбор. Пожалуйста, введите номер пункта меню.")

# Запуск меню
db = Database()
db.load_data('economic_indicators.json')
menu(db)
