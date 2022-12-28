import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side
from openpyxl.styles.numbers import FORMAT_PERCENTAGE_00
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Environment, FileSystemLoader
import pdfkit
import datetime as dt


class UserInput:
    file_name: str
    profession_name: str

    def __init__(self, file_name: str = None, profession_name: str = None):
        if file_name is not None:
            self.file_name = file_name
        else:
            self.file_name = self._get_correct_input("Введите название файла: ", 'str')

        if profession_name is not None:
            self.profession_name = profession_name
        else:
            self.profession_name = self._get_correct_input("Введите название профессии: ", 'str')

    def _get_correct_input(self, question: str, input_type: str,
                           error_msg: str = "Данные некорректны, повторите ввод.") -> str:
        user_input = input(question)
        while not self._is_correct_input(user_input, input_type):
            print(error_msg)
            user_input = input(question)
        return user_input

    @staticmethod
    def _is_correct_input(user_input: str, input_type: str) -> bool:
        if user_input == "" or input_type == "":
            return False
        elif input_type == 'bool':
            return user_input.lower() in ['да', 'нет']
        elif input_type == 'int':
            return user_input.isdigit()
        return True


def get_data_by_years(df: pd.DataFrame, profession_name: str) -> dict:
    pass


def generate_pdf(df: pd.DataFrame, profession_name: str) -> None:
    pass


def main() -> None:
    ui = UserInput("../3.3 API/hh_ru_joined_salary.csv", "Программист")
    df = pd.read_csv(ui.file_name, dtype={"name": "str", "salary": "Int32", "area_name": "str"}, verbose=True)
    df = df.assign(published_at=df['published_at'].apply(lambda s: dt.datetime.fromisoformat(s).year).astype("int32"))
    print(df["published_at"].dtype)
    data = get_data_by_years(df, ui.profession_name)
    generate_pdf(df, ui.profession_name)


if __name__ == "__main__":
    main()
