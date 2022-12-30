import pandas as pd
import sqlite3

connection = sqlite3.connect("vacancies_by_year.db")
all_years = range(2003, 2023)
p_name = "Программист"  # input("Введите название профессии: ")
font_dec = '\033[1m' + '\033[92m'
end_dec = '\033[0m'

df_prof = pd.read_sql(f"""
SELECT STRFTIME('%Y', published_at || '-01') AS year, ROUND(AVG(salary)) AS 'mean', COUNT(salary) AS 'count'
FROM VACANCIES
WHERE name LIKE '%{p_name}'
GROUP BY YEAR
""", connection, index_col='year')

for year in all_years:
    y = str(year)
    if y not in df_prof.index:
        df_prof.loc[y] = 0
df_prof = df_prof.sort_index()

print(font_dec + "Статистика по годам для профессии" + end_dec)
print(df_prof)

df_year = pd.read_sql("""
SELECT STRFTIME('%Y', published_at || '-01') AS year, ROUND(AVG(salary)) AS 'mean', COUNT(salary) AS 'count'
FROM VACANCIES
GROUP BY YEAR
""", connection, index_col='year')

print(font_dec + "Общая статистика по годам" + end_dec)
print(df_year)

df_city_count = pd.read_sql("""
SELECT area_name, CAST(ROUND(CAST(count as REAL) / (SELECT COUNT(*) FROM VACANCIES), 4) * 100 AS TEXT) ||
'%' as 'proc' FROM (SELECT area_name, COUNT(salary) as 'count'
FROM VACANCIES
GROUP BY area_name
ORDER BY count DESC)
LIMIT 10
""", connection, index_col='area_name')

print(font_dec + "Процент от всех вакансий по городам" + end_dec)
print(df_city_count)

# Чашкин Никита Андреевич
