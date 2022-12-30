import sqlite3
import pandas as pd


def multiply_currency(row: pd.Series):
    if row.salary_currency == "RUR":
        row.salary = int(row.salary)
        return row

    if pd.isna(row.salary_currency):
        row.salary = None
        return row
    currencies_con = sqlite3.connect("currencies_rates.db")
    currencies = pd.read_sql(f"""SELECT * FROM CURRENCIES WHERE DATE = '{row.published_at}'""", currencies_con)

    if row.salary_currency not in currencies.columns:
        row.salary = None
        return row

    try:
        coefficient = currencies[row.salary_currency][0]
    except IndexError:
        coefficient = pd.NA

    if pd.isna(coefficient):
        row.salary = None
        return row

    row.salary = int(row.salary * coefficient)
    return row


def main() -> None:
    df = pd.read_csv("../vacancies_dif_currencies.csv", dtype={"name": "str", "salary_from": "Float32",
                                                               "salary_to": "Float32", "salary_currency": "str",
                                                               "area_name": "str", "published_at": "str"},
                     verbose=True)

    clear_df = (df
                .assign(published_at=df["published_at"].apply(lambda date: date[:7]),
                        salary_from=df[["salary_from", "salary_to"]]
                        .mean(axis=1))
                .rename({"salary_from": "salary"}, axis="columns")
                .apply(multiply_currency, axis=1)
                .drop(columns=["salary_currency", "salary_to"])
                )

    vacancies_con = sqlite3.connect("vacancies_dif_currencies.db")
    (clear_df
     .to_sql("VACANCIES", vacancies_con, index=False, if_exists="replace"))


if __name__ == "__main__":
    # Чашкин Никита Андреевич АТ-35
    main()
