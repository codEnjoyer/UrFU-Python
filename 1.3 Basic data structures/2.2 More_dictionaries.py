import csv
import re


def parse_html(line: str) -> str:
    line = re.sub(re.compile('<.*?>'), '', line)
    line = line.replace("\r\n", ", ")
    return ' '.join(line.replace("\n", ", ").split())


with open('vacancies.csv', 'r', newline='', encoding='utf-8-sig') as file:
    data = csv.reader(file)
    title = next(data)
    rows = [row for row in data
            if len(list(filter(lambda word: word != '', row))) == len(title)]

column_vacancy_dictionaries = []
for vacancy in rows:
    dictionary = {}
    column_vacancy_dictionaries.append(dictionary)
    for i in range(len(title)):
        dictionary[title[i]] = parse_html(vacancy[i])
        print(f'{title[i]}: {dictionary[title[i]]}')
    print()
