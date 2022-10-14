from csv import reader
from re import sub
from prettytable import PrettyTable, ALL


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
    d = {}
    for index, value in enumerate(title):
        d[value] = parse_html(row_vacs[index])
    return d


def parse_html(line: str) -> str:
    line = sub('<.*?>', '', line)
    line = line.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in line.split('\n')]
    return res[0] if len(res) == 1 else res  # Спасибо Яндекс.Контесту за еще один костыль!


def format_vacancy_field(key: str, value: str or list) -> str:
    dict_experience = {"noExperience": "Нет опыта",
                       "between1And3": "От 1 года до 3 лет",
                       "between3And6": "От 3 до 6 лет",
                       "moreThan6": "Более 6 лет"}
    dict_currency = {"AZN": "Манаты",
                     "BYR": "Белорусские рубли",
                     "EUR": "Евро",
                     "GEL": "Грузинский лари",
                     "KGS": "Киргизский сом",
                     "KZT": "Тенге",
                     "RUR": "Рубли",
                     "UAH": "Гривны",
                     "USD": "Доллары",
                     "UZS": "Узбекский сум"}

    if key == 'key_skills' and type(value) == list:
        return "\n".join(value)
    elif value in ['True', 'False']:
        return value.replace('True', 'Да').replace('False', 'Нет')
    elif key == 'experience_id':
        return dict_experience[value]
    elif key in ['salary_from', 'salary_to']:
        return f"{int(float(value)):,}".replace(',', ' ')
    elif key == 'salary_currency':
        return dict_currency[value]
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


def configure_field_names() -> list:
    dict_naming: (str, str) = {'name': 'Название',
                               'description': 'Описание',
                               'key_skills': 'Навыки',
                               'experience_id': 'Опыт работы',
                               'premium': 'Премиум-вакансия',
                               'employer_name': 'Компания',
                               'salary_from': 'Нижняя граница вилки оклада',
                               'salary_to': 'Верхняя граница вилки оклада',
                               'salary_gross': 'Оклад указан до вычета налогов',
                               'salary_currency': 'Идентификатор валюты оклада',
                               'salary': 'Оклад',
                               'area_name': 'Название региона',
                               'published_at': 'Дата публикации вакансии'}
    res = ['№']
    for t in title:
        if t in ['salary_from', 'salary_to', 'salary_gross']:
            continue
        if t == 'salary_currency':
            t = 'salary'
        res.append(dict_naming[t])
    return res


def configure_table(tab: PrettyTable) -> None:
    tab.field_names = configure_field_names()
    tab.hrules = ALL
    tab.align = 'l'
    tab.max_width = 20
    tab.custom_format = (lambda f, v: f"{v}"[:100] + '...' if len(str(v)) > 100 else f"{v}"[:100])


def print_vacancies(vacs: list) -> None:
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
    table = PrettyTable()
    configure_table(table)

    for index, vac in enumerate(vacs):
        res = [index + 1]
        for t in table.field_names[1:]:
            res.append(vac.__dict__[dict_naming_reverse[t]])
        table.add_row(res)
    print(table)


(title, row_vacancies) = csv_reader('vacancies_medium.csv')
vacancies = [Vacancy(parse_row_vacancy(row_vacancy)) for row_vacancy in row_vacancies]
print_vacancies(vacancies)
