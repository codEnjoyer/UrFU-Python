from csv import reader
from re import sub


def parse_html(line: str) -> str:
    line = sub('<.*?>', '', line)
    line = line.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in line.split('\n')]
    return res[0] if len(res) == 1 else res  # Спасибо Яндекс.Контесту за еще один костыль!


def reformat_field(key: str, value) -> str:
    if key == 'key_skills' and type(value) == list:
        return ", ".join(value)
    elif value in ['True', 'False']:
        return value.replace('True', 'Да').replace('False', 'Нет')
    else:
        return value


class Vacancy:
    def __init__(self, fields: dict):
        for key, value in fields.items():
            self.__setattr__(key, reformat_field(key, value))

        if hasattr(self, 'salary_from') and hasattr(self, 'salary_to'):
            self.salary_to = float(self.salary_to)
            self.salary_from = float(self.salary_from)


def csv_reader(file_name: str) -> (list, list):
    with open(file_name, 'r', newline='', encoding='utf-8-sig') as file:
        data = reader(file)
        title = next(data)
        rows = [row for row in data
                if len(list(filter(lambda word: word != '', row))) == len(title)]
    return title, rows


def parse_row_vacancy(row_vacs: list) -> dict:
    d = {}
    for index, value in enumerate(title):
        d[value] = parse_html(row_vacs[index])
    return d


def print_vacancies(vacancies: list, dict_naming: dict) -> None:
    for vacancy in vacancies:
        for key, value in vacancy.__dict__.items():
            print(f"{dict_naming[key]}: {value}")
        print()


(title, row_vacancies) = csv_reader('vacancies_medium.csv')
vacancies = [Vacancy(parse_row_vacancy(row_vacancy)) for row_vacancy in row_vacancies]
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
                           'area_name': 'Название региона',
                           'published_at': 'Дата и время публикации вакансии'}

print_vacancies(vacancies, dict_naming)
