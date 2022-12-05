from Testing import Translator, Salary, Vacancy, UserInterface
from unittest import TestCase


class TranslatorTests(TestCase):
    def test_translator_type(self):
        self.assertEqual(type(Translator()).__name__, 'Translator')

    def test_translator_field_translate(self):
        self.assertEqual(Translator().AZN, 'Манаты')

    def test_translator_method_translate(self):
        self.assertEqual(Translator().translate('USD'), 'Доллары')


class SalaryTests(TestCase):
    def test_salary_type(self):
        self.assertEqual(type(Salary(10, 20, 'RUR')).__name__, 'Salary')

    def test_salary_from(self):
        self.assertEqual(Salary(10, 20, 'Рубли').salary_from, 10)

    def test_salary_to(self):
        self.assertEqual(Salary(10, 20, 'Рубли').salary_to, 20)

    def test_salary_currency(self):
        self.assertEqual(Salary(10, 20, 'Рубли').salary_currency, 'Рубли')

    def test_salary_average(self):
        self.assertEqual(Salary(10, 20, 'Рубли').get_average_in_rur(), 15)

    def test_int_type_get_salary(self):
        self.assertEqual(type(Salary(10, 20, 'Рубли').get_average_in_rur()).__name__, 'int')

    def test_float_salary(self):
        self.assertEqual(Salary(10.5, 20.4, 'Рубли').get_average_in_rur(), 15.0)

    def test_currency_in_average_salary(self):
        self.assertEqual(Salary(10, 30, 'Евро').get_average_in_rur(), 1198)


class VacancyTests(TestCase):
    def test_vacancy_type(self):
        self.assertEqual(type(Vacancy({})).__name__, 'Vacancy')

    def test_vacancy_correct_name_field(self):
        self.assertEqual(Vacancy({'name': 'Программист'}).get_field('name'), 'Программист')

    def test_vacancy_salary_initialization(self):
        self.assertEqual(hasattr(Vacancy({'salary_from': '100'}), 'salary'), True)

    def test_vacancy_average_salary(self):
        self.assertEqual(Vacancy({'salary_from': '100',
                                  'salary_to': '150',
                                  'salary_currency': 'RUR'}).salary.get_average_in_rur(), 125)

    def test_vacancy_published_at(self):
        self.assertEqual(Vacancy({'published_at': '2000-01-01T10:00:00+00'}).get_field('published_at'), 2000)


class UserInterfaceTests(TestCase):
    def test_user_interface_type(self):
        self.assertEqual(type(UserInterface()).__name__, 'UserInterface')

    def test_user_interface_default_profession_name(self):
        self.assertEqual(UserInterface().profession_name, 'Программист')

    def test_user_interface_profession_name(self):
        self.assertEqual(UserInterface(profession_name='Аналитик').profession_name, 'Аналитик')

    def test_user_interface_default_file_name(self):
        self.assertEqual(UserInterface().file_name, '../vacancies_medium.csv')

    def test_user_interface_file_name(self):
        self.assertEqual(UserInterface(file_name='../vacancies_by_year.csv').file_name, '../vacancies_by_year.csv')