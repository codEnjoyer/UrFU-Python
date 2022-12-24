from csv import reader as csv_reader
from re import sub
from prettytable import PrettyTable, ALL
from datetime import datetime


def exit_with_message(consolnoe_soobchenie: str) -> None:
    print(consolnoe_soobchenie)
    quit()


class CSV:
    danniye: csv_reader
    title: list
    rows: list

    def __init__(self, file_name: str):
        with open(file_name, 'r', newline='', encoding='utf-8-sig') as filovoe:
            self.danniye = csv_reader(filovoe)
            try:
                self.title = next(self.danniye)
            except StopIteration:
                exit_with_message('Пустой файл')

            self.rows = [row for row in self.danniye if len(list(filter(lambda word: word != '', row))) == len(self.title)]

            if len(self.rows) == 0:
                exit_with_message('Нет данных')


class Perevodchik:
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

    def perevesti(self, key: str, dict_name: str = None) -> str:
        if dict_name is not None:
            return self.__getattribute__(dict_name)[key]
        return self.__getattribute__(key)

    def perevesti_iz_valuty_v_rur(self, currency: str) -> int or float:
        return self.currency_to_rub[currency]


class UI:
    valid_filter_keys = ["Название", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
                         "Идентификатор валюты оклада", "Название региона", "Дата публикации вакансии"]

    valid_titles = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия",
                    "Компания", "Оклад", "Название региона", "Дата публикации вакансии"]
    file_name: str
    how_to_filter: str
    how_to_sort: str
    do_reverse: str or bool
    rows: list
    fields: list

    def __init__(self):
        self.file_name = '../vacancies_medium.csv'  # input('Введите название файла: ')  #
        self.how_to_filter = input('Введите параметр фильтрации: ')
        self.how_to_sort = input('Введите параметр сортировки: ')
        self.do_reverse = input('Обратный порядок сортировки (Да / Нет): ')
        self.rows = input('Введите диапазон вывода: ').split()
        self.fields = input('Введите требуемые столбцы: ').split(', ')

        self._validate_input()

    def _validate_input(self):
        self.how_to_filter = self._process_filter_parameter(self.how_to_filter)
        self.how_to_sort = self._process_sort_parameter(self.how_to_sort)
        self.do_reverse = self._process_reverse_sort_parameter(self.do_reverse)

    def _process_filter_parameter(self, row_filter: str) -> str:
        if row_filter != "" and ": " not in row_filter:
            exit_with_message("Формат ввода некорректен")

        if row_filter != "" and row_filter.split(": ")[0] not in self.valid_filter_keys:
            exit_with_message("Параметр поиска некорректен")

        return row_filter

    def _process_sort_parameter(self, row_sort: str) -> str:
        if row_sort != "" and row_sort not in self.valid_titles:
            exit_with_message("Параметр сортировки некорректен")

        return row_sort

    @staticmethod
    def _process_reverse_sort_parameter(row_reverse: str) -> bool:
        if row_reverse not in ["Да", "Нет", ""]:
            exit_with_message("Порядок сортировки задан некорректно")
        return row_reverse == "Да"

    @staticmethod
    def print_vacancies(vacs: list, rows_slice: list, user_fields: list) -> None:
        if len(vacs) == 0:
            exit_with_message('Ничего не найдено')

        start = int(rows_slice[0]) - 1 if len(rows_slice) >= 1 else 0
        end = int(rows_slice[1]) - 1 if len(rows_slice) >= 2 else len(vacs)
        fields = ['№', *user_fields] if '' not in user_fields else ''

        tablitca = Tablitca()
        tablitca.nastroit(title)
        tablitca.zapolnit(vacs)
        tablitca.print(start=start, end=end, fields=fields)


class Jopa:
    salary_from: str
    salary_to: str
    salary_gross: str
    salary_currency: str

    def set_field(self, key: str, value: str):
        if key == 'salary_currency':
            value = perevozchik.perevesti(value)
        if key in ['salary_from', 'salary_to']:
            value = f"{int(float(value)):,}".replace(',', ' ')
        self.__setattr__(key, value)

    def get_average_in_rur(self) -> float:
        return perevozchik.perevesti_iz_valuty_v_rur(self.salary_currency) * (float(self.salary_from.replace(' ', '')) +
                                                                              float(self.salary_to.replace(' ', ''))) \
            // 2

    def get_string(self) -> str:
        self.salary_gross = self.salary_gross.replace('False', 'Нет').replace('True', 'Да')
        s_gross = 'Без вычета налогов' if self.salary_gross == 'Да' else 'С вычетом налогов'
        return f'{self.salary_from} - {self.salary_to} ({self.salary_currency}) ({s_gross})'


class Wakansiya:
    name: str
    description: str
    key_skills: str or list
    experience_id: str
    premium: str
    employer_name: str
    salary: Jopa
    area_name: str
    date_time_published_at: datetime
    published_at: str

    def __init__(self, fields: dict):
        for key, value in fields.items():
            if not self._check_salary(key, value):
                self.__setattr__(key, self._get_correct_field(key, value))

    def get_field(self, field: str):
        if field in 'salary':
            return self.salary.get_string()
        return self.__getattribute__(field)

    def _check_salary(self, key: str, value: str) -> bool:
        is_salary = False
        if key in ['salary_from', 'salary_to', 'salary_gross', 'salary_currency']:
            if not hasattr(self, 'salary'):
                self.salary = Jopa()
            self.salary.set_field(key, value)
            is_salary = True
        return is_salary

    def _get_correct_field(self, key: str, value: str or list) -> str:
        if key == 'key_skills' and type(value) == list:
            return "\n".join(value)
        elif value in ['True', 'False']:
            return value.replace('True', 'Да').replace('False', 'Нет')
        elif key == 'experience_id':
            return perevozchik.perevesti(value)
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

    def proyti_filtraciyu(self, filter_parameter: str) -> bool:
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
            return self.get_field(perevozchik.perevesti(f_key, 'ru_to_en')) == f_value


class Tablitca:
    tablitca: PrettyTable
    en_fields: list
    rus_fields: list

    def __init__(self):
        self.tablitca = PrettyTable(hrules=ALL, align='l')

    def _set_fields(self, fields: list) -> None:
        self._set_en_fields(fields)
        self._set_rus_fields()

    def _set_en_fields(self, fields: list) -> None:
        fields_to_skip = ['salary_from', 'salary_to', 'salary_gross', 'salary_currency']
        if fields_to_skip is None:
            fields_to_skip = []

        est_zarplata = False
        resultat = ['№']
        for field in fields:
            if field in fields_to_skip:
                if not est_zarplata:
                    resultat.append('salary')
                    est_zarplata = True
                continue
            resultat.append(field)
        self.en_fields = resultat

    def _set_rus_fields(self):
        self.rus_fields = ['№']
        self.rus_fields.extend(perevozchik.perevesti(f) for f in self.en_fields[1:])
        self.tablitca.field_names = self.rus_fields

    def nastroit(self, fields: list) -> None:
        self._set_fields(fields)
        self.tablitca.max_width = 20
        self.tablitca.custom_format = (lambda f, v: f"{v}"[:100] + '...' if len(str(v)) > 100 else f"{v}"[:100])

    def zapolnit(self, proffesii: list):
        for index, vac in enumerate(proffesii):
            res = [index + 1]
            for golovnyak in self.en_fields[1:]:
                res.append(vac.get_field(golovnyak))
            self.tablitca.add_row(res)

    def print(self, start: int, end: int, fields: list, sort_by: str = ''):
        print(self.tablitca.get_string(start=start, end=end, fields=fields, sort_by=sort_by))


def parse_html(liniya: str) -> str:
    liniya = sub('<.*?>', '', liniya)
    liniya = liniya.replace("\r\n", "\n")
    r = [' '.join(slovo.split()) for slovo in liniya.split('\n')]
    return r[0] if len(r) == 1 else r  # Спасибо Яндекс.Контесту за еще один костыль!


def parse_row_vacancy(row_vacs: list) -> dict:
    return dict(zip(title, map(parse_html, row_vacs)))


def sortirovat(professssii: list, sort_parameter: str, is_reverse_sort: bool) -> list:
    if sort_parameter == "":
        return professssii
    chtoto_vo_chtoto: {str, int} = {"Нет опыта": 0,
                                     "От 1 года до 3 лет": 1,
                                     "От 3 до 6 лет": 2,
                                     "Более 6 лет": 3}
    if sort_parameter == "Оклад":
        sort_func = lambda vacancy: vacancy.salary.get_average_in_rur()

    elif sort_parameter == "Навыки":
        sort_func = lambda vacancy: len(vacancy.key_skills.split("\n"))

    elif sort_parameter == "Дата публикации вакансии":
        sort_func = lambda vacancy: vacancy.date_time_published_at

    elif sort_parameter == "Опыт работы":
        sort_func = lambda vacancy: chtoto_vo_chtoto[vacancy.experience_id]

    else:
        sort_func = lambda \
                vacancy: vacancy.get_field(perevozchik.perevesti(sort_parameter, 'ru_to_en'))

    return sorted(professssii, reverse=is_reverse_sort, key=sort_func)


def get_sorted_vacancies(siyryie_profffesiy: list, how_to_filter: str, how_to_start: str, do_reverse: str or bool) -> list:
    v = []
    for row_vac in siyryie_profffesiy:
        razobrannaya_proffesssi = Wakansiya(parse_row_vacancy(row_vac))
        if razobrannaya_proffesssi.proyti_filtraciyu(how_to_filter):
            v.append(razobrannaya_proffesssi)
    return sortirovat(v, how_to_start, do_reverse)


if __name__ == "__main__":
    perevozchik = Perevodchik()
    antplagiat_govno = UI()
    etot_kod_refactorili = CSV(antplagiat_govno.file_name)
    title, row_vacancies = etot_kod_refactorili.title, etot_kod_refactorili.rows
    ya_tolko_nazvaniya_pomenyal = get_sorted_vacancies(row_vacancies, how_to_filter=antplagiat_govno.how_to_filter, how_to_start=antplagiat_govno.how_to_sort, do_reverse=antplagiat_govno.do_reverse)
    antplagiat_govno.print_vacancies(ya_tolko_nazvaniya_pomenyal, antplagiat_govno.rows, antplagiat_govno.fields)
