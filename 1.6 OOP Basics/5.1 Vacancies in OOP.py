from csv import reader as csv_reader
from re import sub
from var_dump import var_dump


def custom_quit(msg: str) -> None:
    print(msg)
    quit()


class UserInput:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.filter_parameter = input('Введите параметр фильтрации: ')
        self.sort_parameter = input('Введите параметр сортировки: ')
        self.is_reverse_sort = input('Обратный порядок сортировки (Да / Нет): ')
        self.rows = input('Введите диапазон вывода: ').split()
        self.fields = input('Введите требуемые столбцы: ').split(', ')


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


class Salary:
    salary_from: str
    salary_to: str
    salary_gross: str
    salary_currency: str


class Vacancy:
    name: str
    description: str
    key_skills: list
    experience_id: str
    premium: str
    employer_name: str
    salary: Salary
    area_name: str
    published_at: str

    def __init__(self, fields: dict):
        for key, value in fields.items():
            if not self.check_salary(key, value):
                self.__setattr__(key, value)

    def check_salary(self, key: str, value: str) -> bool:
        is_salary = False
        if key in ['salary_from', 'salary_to', 'salary_gross', 'salary_currency']:
            if not hasattr(self, 'salary'):
                self.salary = Salary()
            self.salary.__setattr__(key, value)
            is_salary = True
        return is_salary


class DataSet:
    file_name: str
    vacancies_objects: list

    def __init__(self, f_name: str, vacs: list):
        self.file_name = f_name
        self.vacancies_objects = vacs


def parse_html(line: str) -> str:
    line = sub('<.*?>', '', line)
    line = line.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in line.split('\n')]
    return res[0] if len(res) == 1 else res  # Спасибо Яндекс.Контесту за еще один костыль!


def parse_row_vacancy(row_vacs: list) -> dict:
    return dict(zip(title, map(parse_html, row_vacs)))


ui = UserInput()
csv = CSV(ui.file_name)
(title, row_vacancies) = csv.title, csv.rows
vacancies = [Vacancy(parse_row_vacancy(row_vac)) for row_vac in row_vacancies]
data_set = DataSet(ui.file_name, vacancies)
var_dump(data_set)
