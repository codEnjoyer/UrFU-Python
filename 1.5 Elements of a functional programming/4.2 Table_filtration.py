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

    @classmethod
    def translate_to_rus(cls, data: list) -> list:
        return [cls.__getitem__(name).value for name in data]

    @classmethod
    def translate_to_en(cls, data: list, dict_naming: dict) -> list:
        return [dict_naming[name] for name in data]


def process_filter_parameter(row_filter: str) -> str:
    if row_filter == "":
        return row_filter

    acceptable = ["Название", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
                  "Идентификатор валюты оклада", "Название региона", "Дата публикации вакансии"]

    if ": " not in row_filter:
        print("Формат ввода некорректен")
        quit()

    if row_filter.split(": ")[0] not in acceptable:
        print("Параметр поиска некорректен")
        quit()

    return row_filter


def process_user_input() -> dict:
    file_name = input('Введите название файла: ')  # '../vacancies_medium.csv'  #
    filter_parameter = process_filter_parameter(input('Введите параметр фильтрации: '))
    rows = input('Введите диапазон вывода: ').split()
    fields = input('Введите требуемые столбцы: ').split(', ')
    return {'file_name': file_name,
            'filter_parameter': filter_parameter,
            'rows': rows,
            'fields': fields}


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
    for index, vac in enumerate(vacs):
        res = [index + 1]
        for t in tab.field_names[1:]:
            res.append(vac.__dict__[Translate.__getitem__('dict_naming_reverse').value[t]])
        tab.add_row(res)


def print_vacancies(vacs: list, rows_slice: list, user_fields: list) -> None:
    if len(vacs) == 0:
        print('Ничего не найдено')
        quit()

    start = int(rows_slice[0]) - 1 if len(rows_slice) >= 1 else 0
    end = int(rows_slice[1]) - 1 if len(rows_slice) >= 2 else len(vacs)
    fields = ['№', *user_fields] if '' not in user_fields else ''

    table = PrettyTable(hrules=ALL, align='l')
    configure_table(table, title)
    fill_table(table, vacs)

    print(table.get_string(start=start, end=end, fields=fields))


user_input = process_user_input()
(title, row_vacancies) = csv_reader(user_input['file_name'])

vacancies = []
for row_vacancy in row_vacancies:
    parsed_vac = Vacancy(parse_row_vacancy(row_vacancy))
    if parsed_vac.pass_filtering(user_input['filter_parameter']):
        vacancies.append(parsed_vac)

print_vacancies(vacancies, user_input['rows'], user_input['fields'])
