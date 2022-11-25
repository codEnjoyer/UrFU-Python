import numpy as np
import matplotlib.pyplot as plt

# years_salary_dic = {2007: 38916, 2008: 43646, 2009: 42492, 2010: 43846, 2011: 47451, 2012: 48243, 2013: 51510,
#                     2014: 50658, 2015: 52696, 2016: 62675, 2017: 60935, 2018: 58335, 2019: 69467, 2020: 73431,
#                     2021: 82690, 2022: 91795}
# years_count_dic = {2007: 2196, 2008: 17549, 2009: 17709, 2010: 29093, 2011: 36700, 2012: 44153, 2013: 59954,
#                    2014: 66837, 2015: 70039, 2016: 75145, 2017: 82823, 2018: 131701, 2019: 115086, 2020: 102243,
#                    2021: 57623, 2022: 18294}
# years_salary_vac_dic = {2007: 43770, 2008: 50412, 2009: 46699, 2010: 50570, 2011: 55770, 2012: 57960, 2013: 58804,
#                         2014: 62384, 2015: 62322, 2016: 66817, 2017: 72460, 2018: 76879, 2019: 85300, 2020: 89791,
#                         2021: 100987, 2022: 116651}
# years_count_vac_dic = {2007: 317, 2008: 2460, 2009: 2066, 2010: 3614, 2011: 4422, 2012: 4966, 2013: 5990, 2014: 5492,
#                        2015: 5375, 2016: 7219, 2017: 8105, 2018: 10062, 2019: 9016, 2020: 7113, 2021: 3466, 2022: 1115}
# area_salary_dic = {'Москва': 76970, 'Санкт-Петербург': 65286, 'Новосибирск': 62254, 'Екатеринбург': 60962,
#                    'Казань': 52580, 'Краснодар': 51644, 'Челябинск': 51265, 'Самара': 50994, 'Пермь': 48089,
#                    'Нижний Новгород': 47662}
# area_count_dic = {'Москва': 0.3246, 'Санкт-Петербург': 0.1197, 'Новосибирск': 0.0271, 'Казань': 0.0237,
#                   'Нижний Новгород': 0.0232, 'Ростов-на-Дону': 0.0209, 'Екатеринбург': 0.0207, 'Краснодар': 0.0185,
#                   'Самара': 0.0143, 'Воронеж': 0.0141}

years_salary_dic = {2007: 38916, 2008: 43646, 2009: 42492, 2010: 43846, 2011: 47451, 2012: 48243, 2013: 51510,
                    2014: 50658}
years_count_dic = {2007: 2196, 2008: 17549, 2009: 17709, 2010: 29093, 2011: 36700, 2012: 44153, 2013: 59954,
                   2014: 66837}
years_salary_vac_dic = {2007: 43770, 2008: 50412, 2009: 46699, 2010: 50570, 2011: 55770, 2012: 57960, 2013: 58804,
                        2014: 62384}
years_count_vac_dic = {2007: 317, 2008: 2460, 2009: 2066, 2010: 3614, 2011: 4422, 2012: 4966, 2013: 5990, 2014: 5492}
area_salary_dic = {'Москва': 57354, 'Санкт-Петербург': 46291, 'Новосибирск': 41580, 'Екатеринбург': 41091,
                   'Казань': 37587, 'Самара': 34091, 'Нижний Новгород': 33637, 'Ярославль': 32744, 'Краснодар': 32542,
                   'Воронеж': 29725}
area_count_dic = {'Москва': 0.4581, 'Санкт-Петербург': 0.1415, 'Нижний Новгород': 0.0269, 'Казань': 0.0266,
                  'Ростов-на-Дону': 0.0234, 'Новосибирск': 0.0202, 'Екатеринбург': 0.0143, 'Воронеж': 0.014,
                  'Самара': 0.0133, 'Краснодар': 0.0131}

print("Динамика уровня зарплат по годам: " + str(years_salary_dic))
print("Динамика количества вакансий по годам: " + str(years_count_dic))
print("Динамика уровня зарплат по годам для выбранной профессии: " + str(years_salary_vac_dic))
print("Динамика количества вакансий по годам для выбранной профессии: " + str(years_count_vac_dic))
print("Уровень зарплат по городам (в порядке убывания): " + str(area_salary_dic))
print("Доля вакансий по городам (в порядке убывания): " + str(area_count_dic))

fig, ax = plt.subplots(2, 2)
bar_width = 0.5

X_axis = np.arange(len(years_salary_dic.keys()))
ax[0, 0].bar(X_axis - bar_width / 2, years_salary_dic.values(), width=bar_width, label='средняя з/п')
ax[0, 0].bar(X_axis + bar_width / 2, years_salary_vac_dic.values(), width=bar_width, label='з/п программист')
ax[0, 0].set_xticks(X_axis, years_salary_dic.keys())
ax[0, 0].set_xticklabels(years_salary_dic.keys(), rotation='vertical', va='top', ha='center')
ax[0, 0].set_title('Уровень зарплат по годам')
ax[0, 0].grid(True, axis='y')
ax[0, 0].tick_params(axis='both', labelsize=8)
ax[0, 0].legend(fontsize=8)

ax[0, 1].bar(X_axis - bar_width / 2, years_count_dic.values(), width=bar_width, label='Количество вакансий')
ax[0, 1].bar(X_axis + bar_width / 2, years_count_vac_dic.values(), width=bar_width, label='Количество вакансий\nпрограммист')
ax[0, 1].set_xticks(X_axis, years_count_dic.keys())
ax[0, 1].set_xticklabels(years_count_dic.keys(), rotation='vertical', va='top', ha='center')
ax[0, 1].set_title('Количество вакансий по годам')
ax[0, 1].grid(True, axis='y')
ax[0, 1].tick_params(axis='both', labelsize=8)
ax[0, 1].legend(fontsize=8)

ax[1, 0].set_title("Уровень зарплат по городам")
ax[1, 0].invert_yaxis()
data = area_salary_dic
courses = list(data.keys())
courses = [label.replace(' ', '\n').replace('-', '-\n') for label in courses]
values = list(data.values())
ax[1, 0].tick_params(axis='both', labelsize=8)
ax[1, 0].set_yticklabels(courses, fontsize=6, va='center', ha='right')
ax[1, 0].barh(courses, values)
ax[1, 0].grid(True, axis='x')

other = 1 - sum((list(area_count_dic.values())))
new_dic = {'Другие': other}
new_dic.update(area_count_dic)
area_count_dic = new_dic
labels = list(area_count_dic.keys())
sizes = list(area_count_dic.values())
ax[1, 1].pie(sizes, labels=labels, textprops={'fontsize': 6})
ax[1, 1].axis('scaled')
ax[1, 1].set_title("Доля вакансий по городам")
plt.tight_layout()
# plt.savefig('graph.png', dpi=300)
plt.show()
