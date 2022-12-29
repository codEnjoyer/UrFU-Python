import pandas as pd
from numpy import nan
from collections import namedtuple


def get_processed_salary(row: namedtuple, currencies: pd.DataFrame) -> int or nan:
    """
    Проверяет аргументы на NaN, если имеется достаточно данных - возвращает зарплату в рублях, иначе NaN.

    :param row: Строка вакансии из DataFrame. Должна иметь поля salary_from, salary_to, salary_currency, published_at.
    :param currencies: Значения коэффициентов для перевода из валюты в рубли за некоторый период.

    :returns: Если нет коэффициента перевода в рубли за месяц, указанный в вакансии, то во NaN. Если и salary_from, и
    salary_to равны NaN, то NaN. Среднюю зарплату, если ни salary_from, ни salary_to не равны NaN. Если только один из
    них не равен NaN, то возвращает его.
    """

    if pd.isna(row.salary_currency) or pd.isna(row.salary_from) and pd.isna(row.salary_to):
        return nan

    currencies = currencies.set_index('date')
    date = row.published_at[:7]

    try:
        coefficient = 1 if row.salary_currency == "RUR" else currencies[row.salary_currency][date]
    except KeyError:
        return nan

    if pd.isna(coefficient):
        return nan

    if not pd.isna(row.salary_from) and not pd.isna(row.salary_to):
        return int(coefficient * (row.salary_from + row.salary_to) // 2)
    else:
        return int(coefficient * row.salary_from) if pd.isna(row.salary_to) else int(coefficient * row.salary_to)


def count_salary(df: pd.DataFrame) -> list:
    """
    Обрабатывает столбцы 'salary_from', 'salary_to', 'salary_currency' DataFrame и возвращает на их основе новый столбец
    'salary' с подсчитанным значением для каждой вакансии.

    :param df: DataFrame для обработки. Должен иметь поля 'salary_from', 'salary_to' и 'salary_currency'.

    :returns: Список вида [salary1, salary2, salary3, ...], где salaryN float or nan.
    """

    res = []
    currencies = pd.read_csv("../currencies_rates.csv", verbose=True)
    for row in df.itertuples(index=False, name="Vacancy"):

        # print(row.salary_from)
        salary = get_processed_salary(row, currencies)
        # print(salary)

        res.append(salary)
    return res


def join_salary_columns(df: pd.DataFrame, salary_values: list) -> pd.DataFrame:
    """
    Добавляет новый столбец salary на место столбца salary_from, удаляет столбцы salary_to и salary_currency.

    :param df: Выборка вакансий.
    :param salary_values: Список значений зарплат в рублях для каждой вакансии.

    :returns: Обновлённую выборку вакансий со столбцом salary.
    """

    df["salary_from"] = salary_values
    df = df.drop(columns=["salary_to", "salary_currency"])
    df.rename({"salary_from": "salary"}, axis=1, inplace=True)
    return df


def main() -> None:
    df = pd.read_csv("../vacancies_by_year.csv", verbose=True)
    salary_values = count_salary(df)
    df = join_salary_columns(df, salary_values)
    df.to_csv("../vacancies_by_year_joined_salary.csv", index=False)


if __name__ == "__main__":
    main()
