from csv import reader
from re import sub


def parse_html(line: str) -> str:
    line = sub('<.*?>', '', line)
    line = line.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in line.split('\n')]
    return res[0] if len(res) == 1 else res  # Спасибо Яндекс.Контесту за еще один костыль!


def decline_word(count: int, word: str) -> str:
    rubles = ['рублей', 'рубля', 'рубль']
    years = ['лет', 'года', 'год']
    vacancies = ['вакансий', 'вакансии', 'вакансия']
    times = ['раза', 'раз']
    skills = ['скилла', 'скиллов']
    cities = ['города', 'городов']

    if word == 'рубли':
        current_word = rubles
    elif word == 'года':
        current_word = years
    elif word == 'вакансии':
        current_word = vacancies
    elif word == 'разы':
        current_word = times
    elif word == 'скиллы':
        current_word = skills
    elif word == 'города':
        current_word = cities
    else:
        current_word = None

    remainderHundred = count % 100
    remainderTen = count % 10
    if word in ['рубли', 'года', 'вакансии']:
        if remainderTen == 0 or 5 <= remainderTen <= 9 or 11 <= remainderHundred <= 19:
            return current_word[0]
        elif 2 <= remainderTen <= 4:
            return current_word[1]
        else:
            return current_word[2]
    elif word in ['скиллы', 'города']:
        if remainderTen == 1 and remainderHundred != 11:
            return current_word[0]
        else:
            return current_word[1]
    elif word in ['разы']:
        if 2 <= remainderTen <= 4 and remainderHundred not in [12, 13, 14]:
            return 'раза'
        else:
            return 'раз'
    else:
        return 'None'


class Vacancy:
    def __init__(self, fields: dict):
        for key, value in fields.items():
            self.__setattr__(key, value)

        if hasattr(self, 'salary_from') and hasattr(self, 'salary_to'):
            self.salary_to = int(float(self.salary_to))
            self.salary_from = int(float(self.salary_from))
            self.average_salary = (self.salary_from + self.salary_to) // 2


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


def print_vacancies(vacancies: list) -> None:
    for vacancy in vacancies:
        for key, value in vacancy.__dict__.items():
            print(f"{key}: {value}")
        print()


def print_salaries(vacancies: list, key: str) -> None:
    vacancies = sorted(vacancies, key=lambda vacancy: vacancy.average_salary, reverse=key == 'высокие')
    print(f'Самые {key} зарплаты:')
    for index, vac in enumerate(vacancies):
        if index == 10:
            break
        print(f'    {index + 1}) {vac.name} в компании "{vac.employer_name}"'
              f' - {vac.average_salary} {decline_word(vac.average_salary, "рубли")} (г. {vac.area_name})')
    print()


def count_skills(vacancies: list) -> dict:
    skill_count = {}
    for vacancy in vacancies:
        if type(vacancy.key_skills) == list:
            for skill in vacancy.key_skills:
                if skill in skill_count.keys():
                    skill_count[skill] += 1
                else:
                    skill_count[skill] = 1
        else:
            if vacancy.key_skills in skill_count:
                skill_count[vacancy.key_skills] += 1
            else:
                skill_count[vacancy.key_skills] = 1
    return skill_count


def print_skills(skill_count: dict) -> None:
    skill_count_array = sorted(skill_count.items(), key=lambda t: t if type(t) == str else t[1], reverse=True)
    print(f'Из {len(skill_count_array)} {decline_word(len(skill_count_array), "скиллы")}, самыми популярными являются:')
    for index, pair in enumerate(skill_count_array):
        if index == 10:
            break
        print(f'    {index + 1}) {pair[0]} - упоминается {pair[1]} {decline_word(pair[1], "разы")}')
    print()


def count_cities(vacancies: list) -> dict:
    cities = {}
    for vacancy in vacancies:
        if cities.get(vacancy.area_name, []):
            cities[vacancy.area_name][0] += vacancy.average_salary
            cities[vacancy.area_name][1] += 1
        else:
            cities[vacancy.area_name] = [vacancy.average_salary, 1]
    return cities


def print_cities(cities_list: dict) -> None:
    cities_list = sorted(cities_list.items(), key=lambda i: i[1][0] // i[1][1], reverse=True)
    print(f"Из {len(cities_list)} {decline_word(len(cities_list), 'города')}, самые высокие средние ЗП:")

    index = 0
    for item in cities_list:
        if index == 10:
            break
        current_city = item[0]
        current_city_total_salary = item[1][0]
        current_city_number_of_vacancies = item[1][1]
        current_city_average_salary = current_city_total_salary // current_city_number_of_vacancies
        if current_city_number_of_vacancies >= len(vacancies) // 100:
            print(f"    {index + 1}) {current_city} - средняя зарплата"
                  f" {current_city_average_salary} {decline_word(current_city_average_salary, 'рубли')}"
                  f" ({current_city_number_of_vacancies} {decline_word(current_city_number_of_vacancies, 'вакансии')})")
            index += 1


(title, row_vacancies) = csv_reader('vacancies_big.csv')
vacancies = [Vacancy(parse_row_vacancy(row_vacancy)) for row_vacancy in row_vacancies if 'RUR' in row_vacancy]

print_vacancies(vacancies)

print_salaries(vacancies, 'высокие')
print_salaries(vacancies, 'низкие')

skill_count_dict: (str, int) = count_skills(vacancies)
print_skills(skill_count_dict)

cities: (str, list) = count_cities(vacancies)
print_cities(cities)
