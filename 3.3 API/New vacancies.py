import time
import requests
import json
import pandas as pd
from math import ceil
import datetime


def get_page(params: dict) -> dict:
    """
    Получает ответ от api.hh.ru/vacancies с заданными параметрами params.

    :param params: Параметры для поиска вакансий.

    :returns: Словарь, полученный в результате обработки полученного JSON-объекта.
    """

    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    return json.loads(data)


def get_relevant_vacancy_fields(vacancy_data: dict) -> list:
    """
    Возвращает только те поля вакансии, которые были указаны в ТЗ (name, salary_from, salary_to, salary_currency,
    area_name, published_at).

    :param vacancy_data: Словарь с данными об одной вакансии.

    :returns: Список из полей вакансии вида [name, salary_from, salary_to, salary_currency, area_name, published_at].
    """

    name = vacancy_data["name"]
    area_name = vacancy_data["area"]["name"]
    published_at = vacancy_data["published_at"]

    salary = vacancy_data["salary"]
    if salary is not None:
        salary_from = salary["from"]
        salary_to = salary["to"]
        salary_currency = salary["currency"]
    else:
        salary_from, salary_to, salary_currency = None, None, None
    return [name, salary_from, salary_to, salary_currency, area_name, published_at]


def get_fields_from_vacancies_page(vac_data: dict) -> pd.DataFrame:
    """
    Обрабатывает словарь страницы с вакансиями.

    :param vac_data: Словарь страницы с вакансиями.

    :returns: DataFrame со столбцами ["name", "salary_from", "salary_to", "salary_currency", "area_name",
    "published_at"] из словаря с вакансиями.
    """

    parsed_relevant_vacancies_fields = [get_relevant_vacancy_fields(values) for values in vac_data["items"]]

    t = pd.DataFrame(parsed_relevant_vacancies_fields,
                     columns=["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"])
    return t


def get_vacancies_from_last_n_hours(n_hours: int, max_vacancies_count: int,
                                    per_page: int = 100, pages: int = 20) -> pd.DataFrame:
    """
    Получает вакансии с hh.ru за последние n_hours часов. Для правильного подсчёта необходимо указать максимально
    возможное количество получаемых вакансий. Per_page * pages не должно быть больше 2000.

    :param n_hours: Количество часов в период которых, начиная с текущего момента, будут получены вакансии.
    :param max_vacancies_count: Максимально возможное количество получаемых вакансий. Из-за ограничения на выгрузку
    более чем 2000 вакансий их получение организовано через некоторые периоды времени, величина которых зависит от этого
     параметра.
    :param per_page: Количество вакансий, получаемых на одной странице. Не может быть больше 100.
    :param pages: Количество страниц, получаемых за один период времени.

    :returns: DataFrame с полученными вакансиями за последние n_hours со столбцами ["name", "salary_from", "salary_to",
    "salary_currency", "area_name", "published_at"].
    """

    df = pd.DataFrame(columns=["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"])

    parsing_iterations: int = ceil(max_vacancies_count / (per_page * pages))
    time_period: int = ceil(n_hours / parsing_iterations)
    time_from: datetime = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(hours=n_hours)

    for iteration in range(parsing_iterations):
        time_to = time_from + datetime.timedelta(hours=time_period)
        for page in range(pages):
            params = {
                'text': 'IT',
                'per_page': per_page,
                'page': page,
                'specialization': 1,
                'date_from': time_from.isoformat(),
                'date_to': time_to.isoformat()
            }

            vacancies_page = get_page(params)
            if page == vacancies_page["pages"]:
                break

            t = get_fields_from_vacancies_page(vacancies_page)
            df = pd.concat([df, t], ignore_index=True)

            print(df.shape)
            time.sleep(0.1)

        time_from = time_to
    return df


def main() -> None:
    vacancies_period_in_hours = 48
    max_vacancies_count = 10_000

    df = get_vacancies_from_last_n_hours(vacancies_period_in_hours, max_vacancies_count)
    df.to_csv("hh_ru.csv", index=False)


if __name__ == "__main__":
    main()
