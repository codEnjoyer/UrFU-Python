from csv import reader as csv_reader
from re import sub
from prettytable import PrettyTable, ALL
from datetime import datetime


def custom_quit(msg: str) -> None:
    print(msg)
    quit()


class Translator:
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
    ru_to_en: {str, str} = {'Название': 'name',
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
    currency_to_rub: {str, float} = {
        "Манаты": 35.68,
        "Белорусские рубли": 23.91,
        "Евро": 59.90,
        "Грузинский лари": 21.74,
        "Киргизский сом": 0.76,
        "Тенге": 0.13,
        "Рубли": 1,
        "Гривны": 1.64,
        "Доллары": 60.66,
        "Узбекский сум": 0.0055,
    }

    def translate(self, key: str, dict_name: str = None) -> str:
        if dict_name is not None:
            return self.__getattribute__(dict_name)[key]
        return self.__getattribute__(key)

    def translate_currency_to_rub(self, currency: str) -> int or float:
        return self.currency_to_rub[currency]


class UserInterface:
    valid_filter_keys = ["Название", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
                         "Идентификатор валюты оклада", "Название региона", "Дата публикации вакансии"]

    valid_titles = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия",
                    "Компания", "Оклад", "Название региона", "Дата публикации вакансии"]
    file_name: str
    filter_parameter: str
    sort_parameter: str
    is_reverse_sort: str or bool
    rows: list
    fields: list

    def __init__(self):
        self.file_name = '../vacancies_medium.csv'  # input('Введите название файла: ')  #
        self.filter_parameter = input('Введите параметр фильтрации: ')
        self.sort_parameter = input('Введите параметр сортировки: ')
        self.is_reverse_sort = input('Обратный порядок сортировки (Да / Нет): ')
        self.rows = input('Введите диапазон вывода: ').split()
        self.fields = input('Введите требуемые столбцы: ').split(', ')

        self.validate_input()

    def validate_input(self):
        self.filter_parameter = self.process_filter_parameter(self.filter_parameter)
        self.sort_parameter = self.process_sort_parameter(self.sort_parameter)
        self.is_reverse_sort = self.process_reverse_sort_parameter(self.is_reverse_sort)

    def process_filter_parameter(self, row_filter: str) -> str:
        if row_filter != "" and ": " not in row_filter:
            custom_quit("Формат ввода некорректен")

        if row_filter != "" and row_filter.split(": ")[0] not in self.valid_filter_keys:
            custom_quit("Параметр поиска некорректен")

        return row_filter

    def process_sort_parameter(self, row_sort: str) -> str:
        if row_sort != "" and row_sort not in self.valid_titles:
            custom_quit("Параметр сортировки некорректен")

        return row_sort

    @staticmethod
    def process_reverse_sort_parameter(row_reverse: str) -> bool:
        if row_reverse not in ["Да", "Нет", ""]:
            custom_quit("Порядок сортировки задан некорректно")
        return row_reverse == "Да"

    @staticmethod
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


class Salary:
    salary_from: str
    salary_to: str
    salary_gross: str
    salary_currency: str

    def set_field(self, key: str, value: str):
        if key == 'salary_currency':
            value = translator.translate(value)
        if key in ['salary_from', 'salary_to']:
            value = f"{int(float(value)):,}".replace(',', ' ')
        self.__setattr__(key, value)

    def get_average_in_rur(self) -> float:
        return translator.translate_currency_to_rub(self.salary_currency) * (float(self.salary_from.replace(' ', '')) +
                                                                             float(self.salary_to.replace(' ', '')))\
               // 2
    def get_string(self) -> str:
        self.salary_gross = self.salary_gross.replace('False', 'Нет').replace('True', 'Да')
        s_gross = 'Без вычета налогов' if self.salary_gross == 'Да' else 'С вычетом налогов'
        return f'{self.salary_from} - {self.salary_to} ({self.salary_currency}) ({s_gross})'


class Vacancy:
    name: str
    description: str
    key_skills: str or list
    experience_id: str
    premium: str
    employer_name: str
    salary: Salary
    area_name: str
    date_time_published_at: datetime
    published_at: str

    def __init__(self, fields: dict):
        for key, value in fields.items():
            if not self.check_salary(key, value):
                self.__setattr__(key, self.get_correct_field(key, value))

    def get_field(self, field: str):
        if field in 'salary':
            return self.salary.get_string()
        return self.__getattribute__(field)

    def check_salary(self, key: str, value: str) -> bool:
        is_salary = False
        if key in ['salary_from', 'salary_to', 'salary_gross', 'salary_currency']:
            if not hasattr(self, 'salary'):
                self.salary = Salary()
            self.salary.set_field(key, value)
            is_salary = True
        return is_salary

    def get_correct_field(self, key: str, value: str or list) -> str:
        if key == 'key_skills' and type(value) == list:
            return "\n".join(value)
        elif value in ['True', 'False']:
            return value.replace('True', 'Да').replace('False', 'Нет')
        elif key == 'experience_id':
            return translator.translate(value)
        elif key == 'published_at':
            # ms = value[-4:]
            big, small = value[:19].split('T')
            year, month, day = big.split('-')
            hours, minutes, seconds = small.split(':')
            self.date_time_published_at = datetime(int(year), int(month), int(day),
                                                   int(hours), int(minutes), int(seconds))
            return '.'.join([day, month, year])
        else:
            return value

    def pass_filtering(self, filter_parameter: str) -> bool:
        if filter_parameter == '':
            return True

        f_key, f_value = filter_parameter.split(': ')
        if f_key == 'Оклад':
            return float(self.salary.salary_from.replace(' ', '')) <= float(f_value) <= \
                   float(self.salary.salary_to.replace(' ', ''))
        elif f_key == 'Идентификатор валюты оклада':
            return self.salary.salary_currency == f_value
        elif f_key == 'Навыки':
            for skill in f_value.split(", "):
                if skill not in self.key_skills.split("\n"):
                    return False
            return True
        else:
            return self.get_field(translator.translate(f_key, 'ru_to_en')) == f_value


class Table:
    table: PrettyTable
    # en_fields: list = ['№', 'name', 'description', 'key_skills', 'experience_id', 'premium',
    #                    'employer_name', 'salary', 'area_name', 'published_at']
    en_fields: list
    rus_fields: list

    def __init__(self):
        self.table = PrettyTable(hrules=ALL, align='l')

    def set_fields(self, fields: list) -> None:
        self.set_en_fields(fields)
        self.set_rus_fields()

    def set_en_fields(self, fields: list) -> None:
        skip = ['salary_from', 'salary_to', 'salary_gross', 'salary_currency']
        if skip is None:
            skip = []
        is_salary_set = False
        res = ['№']
        for field in fields:
            if field in skip:
                if not is_salary_set:
                    res.append('salary')
                    is_salary_set = True
                continue
            res.append(field)
        self.en_fields = res

    def set_rus_fields(self):
        self.rus_fields = ['№']
        self.rus_fields.extend(translator.translate(f) for f in self.en_fields[1:])
        self.table.field_names = self.rus_fields

    def configure(self, fields: list) -> None:
        self.set_fields(fields)
        self.table.max_width = 20
        self.table.custom_format = (lambda f, v: f"{v}"[:100] + '...' if len(str(v)) > 100 else f"{v}"[:100])

    def fill(self, vacs: list):
        for index, vac in enumerate(vacs):
            res = [index + 1]
            for header in self.en_fields[1:]:
                res.append(vac.get_field(header))
            self.table.add_row(res)

    def print(self, start: int, end: int, fields: list, sort_by: str = ''):
        print(self.table.get_string(start=start, end=end, fields=fields, sort_by=sort_by))


def parse_html(line: str) -> str:
    line = sub('<.*?>', '', line)
    line = line.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in line.split('\n')]
    return res[0] if len(res) == 1 else res  # Спасибо Яндекс.Контесту за еще один костыль!


def parse_row_vacancy(row_vacs: list) -> dict:
    return dict(zip(title, map(parse_html, row_vacs)))


def sort_vacancies(vacs: list, sort_parameter: str, is_reverse_sort: bool) -> list:
    if sort_parameter == "":
        return vacs
    experience_to_int: {str, int} = {"Нет опыта": 0,
                                     "От 1 года до 3 лет": 1,
                                     "От 3 до 6 лет": 2,
                                     "Более 6 лет": 3}
    sort_func = None
    if sort_parameter == "Оклад":
        sort_func = lambda vacancy: vacancy.salary.get_average_in_rur()

    elif sort_parameter == "Навыки":
        sort_func = lambda vacancy: len(vacancy.key_skills.split("\n"))

    elif sort_parameter == "Дата публикации вакансии":
        sort_func = lambda vacancy: vacancy.date_time_published_at

    elif sort_parameter == "Опыт работы":
        sort_func = lambda vacancy: experience_to_int[vacancy.experience_id]

    else:
        sort_func = lambda \
                vacancy: vacancy.get_field(translator.translate(sort_parameter, 'ru_to_en'))

    return sorted(vacs, reverse=is_reverse_sort, key=sort_func)


def get_sorted_vacancies(row_vacs: list, filter_parameter: str,
                         sort_parameter: str, is_reverse_sort: str or bool) -> list:
    vacs = []
    for row_vac in row_vacs:
        parsed_vac = Vacancy(parse_row_vacancy(row_vac))
        if parsed_vac.pass_filtering(filter_parameter):
            vacs.append(parsed_vac)
    return sort_vacancies(vacs, sort_parameter, is_reverse_sort)


if __name__ == "__main__":
    translator = Translator()
    ui = UserInterface()
    csv = CSV(ui.file_name)
    title, row_vacancies = csv.title, csv.rows
    vacancies = get_sorted_vacancies(row_vacancies, filter_parameter=ui.filter_parameter,
                                     sort_parameter=ui.sort_parameter, is_reverse_sort=ui.is_reverse_sort)
    ui.print_vacancies(vacancies, ui.rows, ui.fields)
