from csv import reader
from re import sub
from enum import Enum
from prettytable import PrettyTable, ALL


class Translate(Enum):
    name = 'Название'
    description = 'Описание'
    key_skills = 'Навыки'
    experience_id = 'Опыт работы'
    premium = 'Премиум-вакансия'
    employer_name = 'Компания'
    salary_from = 'Нижняя граница вилки оклада'
    salary_to = 'Верхняя граница вилки оклада'
    salary_gross = 'Оклад указан до вычета налогов'
    salary_currency = 'Идентификатор валюты оклада'
    salary = 'Оклад'
    area_name = 'Название региона'
    published_at = 'Дата публикации вакансии'
    AZN = "Манаты"
    BYR = "Белорусские рубли"
    EUR = "Евро"
    GEL = "Грузинский лари"
    KGS = "Киргизский сом"
    KZT = "Тенге"
    RUR = "Рубли"
    UAH = "Гривны"
    USD = "Доллары"
    UZS = "Узбекский сум"
    noExperience = "Нет опыта"
    between1And3 = "От 1 года до 3 лет"
    between3And6 = "От 3 до 6 лет"
    moreThan6 = "Более 6 лет"

    @classmethod
    def translate_to_rus(cls, data: list):
        return [cls.__getitem__(name).value for name in data]

    @classmethod
    def translate_to_en(cls, data: list, dict_naming: dict):
        return [dict_naming[name] for name in data]


def csv_reader(file_name: str) -> (list, list):
    with open(file_name, 'r', newline='', encoding='utf-8-sig') as file:
        data = reader(file)
        try:
            header = next(data)
        except StopIteration:
            print("Пустой файл")
            quit()

        rows = [row for row in data
                if len(list(filter(lambda word: word != '', row))) == len(header)]
        if len(rows) == 0:
            print("Нет данных")
            quit()

    return header, rows


def parse_row_vacancy(row_vacs: list) -> dict:
    temp_dict = {}
    for index, value in enumerate(title):
        temp_dict[value] = parse_html(row_vacs[index])
    return temp_dict


def parse_html(line: str) -> str:
    line = sub('<.*?>', '', line)
    line = line.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in line.split('\n')]
    return res[0] if len(res) == 1 else res  # Спасибо Яндекс.Контесту за еще один костыль!


def format_vacancy_field(key: str, value: str or list) -> str:
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


class Vacancy:
    def __init__(self, fields: dict):
        self.name = None
        self.description = None
        self.key_skills = None
        self.experience_id = None
        self.premium = None
        self.employer_name = None
        self.salary_from = None
        self.salary_to = None
        self.salary_gross = None
        self.salary_currency = None
        self.area_name = None
        self.published_at = None
        self.salary = None

        for key, value in fields.items():
            self.__setattr__(key, format_vacancy_field(key, value))

        self.set_salary()

    def set_salary(self):
        s_gross = 'Без вычета налогов' if self.salary_gross == 'Да' else 'С вычетом налогов'
        self.salary = f'{self.salary_from} - {self.salary_to} ({self.salary_currency}) ({s_gross})'


def configure_rus_field_names(tab: PrettyTable, fields: list, skip: list) -> None:
    res = ['№']
    for field in fields:
        if field in skip:
            continue
        if field == 'salary_currency':
            field = 'salary'
        res.append(Translate.__getitem__(field).value)
    tab.field_names = res


def configure_table(tab: PrettyTable, fields: list) -> None:
    configure_rus_field_names(tab, fields, skip=['salary_from', 'salary_to', 'salary_gross'])
    tab.max_width = 20
    tab.custom_format = (lambda f, v: f"{v}"[:100] + '...' if len(str(v)) > 100 else f"{v}"[:100])


def fill_table(tab: PrettyTable, vacs: list):
    dict_naming_reverse: (str, str) = {'Название': 'name',
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
    for index, vac in enumerate(vacs):
        res = [index + 1]
        for t in tab.field_names[1:]:
            res.append(vac.__dict__[dict_naming_reverse[t]])
        tab.add_row(res)


def print_vacancies(vacs: list, rows_slice: list, user_fields: list) -> None:
    start = int(rows_slice[0]) - 1 if len(rows_slice) >= 1 else 0
    end = int(rows_slice[1]) - 1 if len(rows_slice) >= 2 else len(vacs)
    fields = ['№', *user_fields] if '' not in user_fields else ''

    table = PrettyTable(hrules=ALL, align='l')
    configure_table(table, title)
    fill_table(table, vacs)

    print(table.get_string(start=start, end=end, fields=fields))


user_input = {'file_name': '../vacancies_medium.csv', 'rows': input().split(), 'fields': input().split(', ')}

(title, row_vacancies) = csv_reader(user_input['file_name'])
vacancies = [Vacancy(parse_row_vacancy(row_vacancy)) for row_vacancy in row_vacancies]
print_vacancies(vacancies, rows_slice=user_input['rows'], user_fields=user_input['fields'])
