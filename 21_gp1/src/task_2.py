import json

class Database:
    def __init__(self):
        self.data = []

    def load_data(self, filename):
        # Загрузка данных из файла
        with open(filename,encoding="utf-8") as f:
            self.data = json.load(f)

    def save_data(self, filename):
        # Сохранение данных в файл
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)

    def add_entity(self, entity):
        self.data.append(entity)

    def remove_entity(self, entity):
        self.data.remove(entity)

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

    def display_entities(self):
        # Вывод данных в виде таблицы
        if not self.data:
            print("Нет данных")
            return

        # # Определение максимальной длины для каждого столбца

        column_lengths = self.get_column_lengths(self.data)

        # Вывод данных
        self.print_header(column_lengths)
        for row in self.data:
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



# Пример использования
db = Database()
db.load_data('economic_indicators.json')
# print(db.data)

# Вывод данных
db.display_entities()
exit()

# Добавление новой сущности
new_entity = ['Value 1', 'Value 2', 'Value 3']
db.add_entity(new_entity)

# Вывод обновленных данных
db.display_entities()

# Удаление сущности
db.remove_entity(new_entity)

# Вывод обновленных данных
db.display_entities()

# Сохранение данных в файл
db.save_data('updated_data.csv')
