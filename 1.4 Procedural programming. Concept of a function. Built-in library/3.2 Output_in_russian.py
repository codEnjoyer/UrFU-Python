from csv import reader
from re import sub


def csv_reader(file_name: str) -> (list, list):
    with open(file_name, 'r', newline='', encoding='utf-8-sig') as file:
        data = reader(file)
        header = next(data)
        rows = [row for row in data
                if len(list(filter(lambda word: word != '', row))) == len(header)]
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
        return ", ".join(value)
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


def print_vacancies(vacs: list) -> None:
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

    for vac in vacs:
        for key, value in vac.__dict__.items():
            if key in ['salary_from', 'salary_to', 'salary_gross', 'salary_currency']:
                if key == 'salary_currency':
                    print(f"{dict_naming['salary']}: {vac.salary}")
                continue
            if key == 'salary':
                continue
            print(f"{dict_naming[key]}: {value}")
        print()


(title, row_vacancies) = csv_reader('vacancies_medium.csv')
vacancies = [Vacancy(parse_row_vacancy(row_vacancy)) for row_vacancy in row_vacancies]
print_vacancies(vacancies)
