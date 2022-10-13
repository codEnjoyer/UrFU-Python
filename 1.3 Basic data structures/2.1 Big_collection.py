import csv

with open(input() if input() != '' else 'vacancies.csv', 'r', newline='', encoding='utf-8-sig') as file:
    data = csv.reader(file)
    title = next(data)
    rows = [row for row in data if len(list(filter(lambda word: word != '', row))) == len(title)]

print(title, rows, sep='\n')
