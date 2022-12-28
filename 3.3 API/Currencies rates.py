import requests
import xmltodict
import pandas as pd


def from_currency_to_rub(amount: int, value: float, nominal: float) -> float:
    """
    Переводит некоторое количество единиц заданной валюты в рубли.

    :param amount: Количество удельных единиц переводимой валюты.
    :param value: Значение value из выгрузки ЦБ РФ.
    :param nominal: Значение nominal из выгрузки ЦБ РФ.

    :returns: Сумму в рублях.
    """

    return amount * value / nominal


def get_date_range(file_name: str = "../vacancies_dif_currencies.csv") -> ((int, int), (int, int)):
    """
    Возвращает год и месяц для самой старой и новой вакансии из CSV-файла.

    :param file_name: Путь до CSV-файла. По умолчанию "../vacancies_dif_currencies.csv".

    :returns: 2 кортежа с числовыми значениями в формате (Year, Month) для старой и новой вакансии соответственно.
    """

    # data_frame = pd.read_csv(file_name)
    # earliest, latest = data_frame['published_at'].min(), data_frame['published_at'].max()
    # year_from, month_from = map(int, earliest[:7].split('-'))
    # year_to, month_to = map(int, latest[:7].split('-'))
    # Чтобы каждый раз не пересчитывать одно и то же значение
    return (2003, 1), (2022, 7)


def get_relevant_currencies(file_name: str = "../vacancies_dif_currencies.csv", threshold: int = 5000) -> list:
    """
    Возвращает список валют, количество вакансий с которыми в CSV-файле превосходит значение threshold.

    :param file_name: Путь до CSV-файла. По умолчанию "../vacancies_dif_currencies.csv".
    :param threshold: Пороговое значения. Валюта, количество появлений в файле больше этого значение, будет учитываться.

    :returns: Список кодовых значений валют.
    """

    # curr_count: {str, int} = {}
    # data_frame = pd.read_csv(file_name)
    # for curr in data_frame["salary_currency"]:
    #     if pd.isna(curr):
    #         continue
    #
    #     if curr in curr_count.keys():
    #         curr_count[curr] += 1
    #     else:
    #         curr_count[curr] = 1
    # result = [key for key, value in curr_count.items() if value > threshold and key not in ["RUR"]]
    return ['USD', 'EUR', 'KZT', 'UAH', 'BYR']


def get_exchange_coefficients(xml_dict: dict, rel_currencies: list) -> dict:
    """
    Возвращает словарь коэффициентов для кодов валют, представленных в rel_currencies.

    :param xml_dict: Словарь, полученный путём разбора xml-документа.
    :param rel_currencies: Список кодов валют, необходимых для подсчёта коэффициентов.

    :returns: Словарь в формате {код валюты: коэффициент}.
    """

    res = {}
    for currency in xml_dict["ValCurs"]["Valute"]:
        code = currency["CharCode"]
        if code not in rel_currencies:
            continue
        res[code] = from_currency_to_rub(1, float(currency["Value"].replace(',', '.')),
                                         float(currency["Nominal"].replace(',', '.')))
    return res


def get_xml_dict(url: str, payload: dict) -> dict:
    """
    Возвращает словарь разобранного xml-документа, полученного GET запросом по адресу url.

    :param url: Адрес для получения xml-документа.
    :param payload: Словарь параметров, передающихся в GET запрос.

    :returns: Словарь разобранного xml-документа.
    """

    response = requests.get(url, params=payload)
    xml = response.text
    return xmltodict.parse(xml)


def save_currencies_rates_csv(file_name: str, date_range: tuple, relevant_currencies: list) -> None:
    """
    Создаёт CSV-файл с именем file_name с коэффициентами для перевода из рублей в валюту из relevant-currencies.
    Коэффициенты представлены для первого числа каждого месяца в диапазоне date_range и высчитываются на основе данных,
    полученных с сайта ЦБ РФ.

    :param file_name: Путь до CSV-файла. По умолчанию "../vacancies_dif_currencies.csv".
    :param date_range: Диапазон в формате кортежа с числовыми значениями:
                       ((начальный год, начальный месяц), (конечный год, конечный месяц)).
    :param relevant_currencies: Список кодовых значений валют, по которым будет собрана статистика.

    :returns: Создаёт CSV-файл с ежемесячными коэффициентами для перевода из валюты в рубли.
    """

    (year_from, month_from), (year_to, month_to) = date_range
    df = pd.DataFrame(columns=["date", *relevant_currencies])

    for year in range(year_from, year_to + 1):
        start_month = month_from if year == year_from else 1
        end_month = month_to if year == year_to else 13

        for month in range(start_month, end_month):
            full_month = f"{'0' + str(month) if len(str(month)) == 1 else str(month)}"
            current_date = f"01/{full_month}/{year}"

            url = "http://www.cbr.ru/scripts/XML_daily.asp"
            payload = {"date_req": current_date, "d": 0}
            xml_dict = get_xml_dict(url, payload)

            new_data = get_exchange_coefficients(xml_dict, relevant_currencies)
            new_data["date"] = f"{year}-{full_month}"

            new_row = pd.Series(new_data)
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
    df.to_csv(file_name, index=False)


def main() -> None:
    save_currencies_rates_csv("../currencies_rates.csv", get_date_range(), get_relevant_currencies())


if __name__ == "__main__":
    main()
