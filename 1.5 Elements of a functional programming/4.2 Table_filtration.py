from csv import reader as csv_reader
from re import sub
from enum import Enum
from prettytable import PrettyTable, ALL


def custom_quit(msg: str) -> None:
    print(msg)
    quit()


class Translate(Enum):
    name: str = 'Название'
    description: str = 'Описание'
    key_skills: str = 'Навыки'
    experience_id: str = 'Опыт работы'
    premium: str = 'Премиум-вакансия'
    employer_name: str = 'Компания'
    salary_from: str = 'Нижняя граница вилки оклада'
    salary_to: str = 'Верхняя граница вилки оклада'
    salary_gross: str = 'Оклад указан до вычета налогов'
    salary_currency: str = 'Идентификатор валюты оклада'
    salary: str = 'Оклад'
    area_name: str = 'Название региона'
    published_at: str = 'Дата публикации вакансии'
    AZN: str = "Манаты"
    BYR: str = "Белорусские рубли"
    EUR: str = "Евро"
    GEL: str = "Грузинский лари"
    KGS: str = "Киргизский сом"
    KZT: str = "Тенге"
    RUR: str = "Рубли"
    UAH: str = "Гривны"
    USD: str = "Доллары"
    UZS: str = "Узбекский сум"
    noExperience: str = "Нет опыта"
    between1And3: str = "От 1 года до 3 лет"
    between3And6: str = "От 3 до 6 лет"
    moreThan6: str = "Более 6 лет"
    dict_naming_reverse: {str, str} = {'Название': 'name',
                                       'Описание': 'description',
                                       'Навыки': 'key_skills',
                                       'Опыт работы': 'experience_id',
                                       'Премиум-вакансия': 'premium',
                                       'Компания': 'employer_name',
                                       'Нижняя граница вилки оклада': 'salary_from',
                                       'Верхняя граница вилки оклада': 'salary_to',
                                       'Оклад указан до вычета налогов': 'salary_gross',
                                       'Идентификатор валюты оклада': 'salary_currency',
                                       'Оклад': 'salary',
                                       'Название региона': 'area_name',
                                       'Дата публикации вакансии': 'published_at'}

    @classmethod
    def translate_list_to_rus(cls, data: list) -> list:
        return [cls.__getitem__(name).value for name in data]

    @classmethod
    def translate_list_to_en(cls, data: list, dict_naming: dict) -> list:
        return [dict_naming[name] for name in data]


class UserInput:
    def __init__(self):
        self.file_name = '../vacancies_medium.csv'  # input('Введите название файла: ')  #
        self.filter_parameter = UserInput.process_filter_parameter(input('Введите параметр фильтрации: '))
        self.rows = input('Введите диапазон вывода: ').split()
        self.fields = input('Введите требуемые столбцы: ').split(', ')

    @staticmethod
    def process_filter_parameter(row_filter: str) -> str:
        valid_keys = ["Название", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
                      "Идентификатор валюты оклада", "Название региона", "Дата публикации вакансии"]

        if row_filter != "" and ": " not in row_filter:
            custom_quit("Формат ввода некорректен")

        if row_filter != "" and row_filter.split(": ")[0] not in valid_keys:
            custom_quit("Параметр поиска некорректен")

        return row_filter


class CSV:
    data: csv_reader
    title: list
    rows: list

    def __init__(self, file_name: str):
        with open(file_name, 'r', newline='', encoding='utf-8-sig') as file:
            self.data = csv_reader(file)
            try:
                self.title = next(self.data)
            except StopIteration:
                custom_quit('Пустой файл')

            self.rows = [row for row in self.data
                         if len(list(filter(lambda word: word != '', row))) == len(self.title)]

            if len(self.rows) == 0:
                custom_quit('Нет данных')


class Vacancy:
    name: str
    description: str
    key_skills: str or list
    experience_id: str
    premium: str
    employer_name: str
    salary_from: int or float
    salary_to: int or float
    salary_gross: str
    salary_currency: str
    area_name: str
    published_at: str
    salary: str

    def __init__(self, fields: dict):
        for key, value in fields.items():
            self.__setattr__(key, Vacancy.get_correct_field(key, value))

        self.set_salary()

    @staticmethod
    def get_correct_field(key: str, value: str or list) -> str:
        if key == 'key_skills' and type(value) == list:
            return "\n".join(value)
        elif value in ['True', 'False']:
            return value.replace('True', 'Да').replace('False', 'Нет')
        elif key in ['experience_id', 'salary_currency']:
            return Translate.__getitem__(value).value
        elif key in ['salary_from', 'salary_to']:
            return f"{int(float(value)):,}".replace(',', ' ')
        elif key == 'published_at':
            return '.'.join(reversed(value[:10].split('-')))
        else:
            return value

    def set_salary(self):
        s_gross = 'Без вычета налогов' if self.salary_gross == 'Да' else 'С вычетом налогов'
        self.salary = f'{self.salary_from} - {self.salary_to} ({self.salary_currency}) ({s_gross})'

    def pass_filtering(self, filter_parameter: str) -> bool:
        if filter_parameter == '':
            return True

        f_key, f_value = filter_parameter.split(': ')
        if f_key == 'Оклад':
            return float(self.salary_from.replace(' ', '')) <= float(f_value) <= float(self.salary_to.replace(' ', ''))
        elif f_key == 'Идентификатор валюты оклада':
            return self.salary_currency == f_value
        elif f_key == 'Навыки':
            for skill in f_value.split(", "):
                if skill not in self.key_skills.split("\n"):
                    return False
            return True
        else:
            return self.__dict__[Translate.__getitem__('dict_naming_reverse').value[f_key]] == f_value


class Table:
    table: PrettyTable

    def __init__(self):
        self.table = PrettyTable(hrules=ALL, align='l')

    def set_rus_fields(self, fields: list, skip: list) -> None:
        res = ['№']
        for field in fields:
            if field in skip:
                continue
            if field == 'salary_currency':
                field = 'salary'
            res.append(Translate.__getitem__(field).value)
        self.table.field_names = res

    def configure(self, fields: list) -> None:
        self.set_rus_fields(fields, skip=['salary_from', 'salary_to', 'salary_gross'])
        self.table.max_width = 20
        self.table.custom_format = (lambda f, v: f"{v}"[:100] + '...' if len(str(v)) > 100 else f"{v}"[:100])

    def fill(self, vacs: list):
        for index, vac in enumerate(vacs):
            res = [index + 1]
            for t in self.table.field_names[1:]:
                res.append(vac.__dict__[Translate.__getitem__('dict_naming_reverse').value[t]])
            self.table.add_row(res)

    def print(self, start: int, end: int, fields: list, sort_by: str = ''):
        print(self.table.get_string(start=start, end=end, fields=fields, sort_by=sort_by))


def parse_html(line: str) -> str:
    line = sub('<.*?>', '', line)
    line = line.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in line.split('\n')]
    return res[0] if len(res) == 1 else res  # Спасибо Яндекс.Контесту за еще один костыль!


def parse_row_vacancy(row_vacs: list) -> dict:
    temp_dict = {}
    for index, value in enumerate(title):
        temp_dict[value] = parse_html(row_vacs[index])
    return temp_dict


def get_filtered_vacancies(row_vacs: list, filter_parameter: str) -> list:
    vacs = []
    for row_vac in row_vacs:
        parsed_vac = Vacancy(parse_row_vacancy(row_vac))
        if parsed_vac.pass_filtering(filter_parameter):
            vacs.append(parsed_vac)
    return vacs


def print_vacancies(vacs: list, rows_slice: list, user_fields: list) -> None:
    if len(vacs) == 0:
        custom_quit('Ничего не найдено')

    start = int(rows_slice[0]) - 1 if len(rows_slice) >= 1 else 0
    end = int(rows_slice[1]) - 1 if len(rows_slice) >= 2 else len(vacs)
    fields = ['№', *user_fields] if '' not in user_fields else ''

    table = Table()
    table.configure(title)
    table.fill(vacs)
    table.print(start=start, end=end, fields=fields)


u_i = UserInput()
csv = CSV(u_i.file_name)
(title, row_vacancies) = csv.title, csv.rows
vacancies = get_filtered_vacancies(row_vacancies, u_i.filter_parameter)
print_vacancies(vacancies, u_i.rows, u_i.fields)
