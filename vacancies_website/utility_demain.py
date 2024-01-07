import sqlite3

import pandas as pd
from matplotlib import pyplot as plt

from vacancies_website.currency import get_curent_salary


def get_demain_info():
	years = {key: 0 for key in range(2017, 2024)}
	file_name = "C:/Users/eldo3/Downloads/example_vacancies/vacancies_for_learn_demo.csv"
	vac_name = 'java'
	vacancies = pd.read_csv(file_name)
	pd.set_option('display.max_columns', None)

	vacancies['year'] = vacancies['published_at'].str[0:4]
	vacancies['salary'] = get_curent_salary(vacancies)

	vacancies_with_sum_count = vacancies.groupby(['year']).agg(['sum', 'count'])
	vacancies_with_sum_count = vacancies_with_sum_count['salary']

	year_salary = years.copy()
	for index, row in vacancies_with_sum_count.iterrows():
		s = row['sum']
		c = row['count']
		year_salary[int(index)] = int(s // c)

	year_count = years.copy()
	for index, row in vacancies_with_sum_count.iterrows():
		year_count[int(index)] = int(row['count'])

	sorted_vacancies = vacancies.loc[vacancies['name'].str.contains(vac_name, na=False, case=False)]
	sorted_vacancies_grouped_by_salary = sorted_vacancies.groupby('year').agg(['sum', 'count'])
	sorted_vacancies_grouped_by_salary = sorted_vacancies_grouped_by_salary['salary']

	year_salary_filtered = years.copy()
	for index, row in sorted_vacancies_grouped_by_salary.iterrows():
		year_salary_filtered[int(index)] = int(row['sum'] // row['count'])

	year_count_filtered = years.copy()
	for index, row in sorted_vacancies_grouped_by_salary.iterrows():
		year_count_filtered[int(index)] = int(row['count'])

	get_demain_graph(year_salary, year_count, year_salary_filtered, year_count_filtered)


def get_demain_graph(year_salary, year_count, year_salary_filtered, year_count_filtered):
	# Постройка графиков
	plt.figure(figsize=(10, 6))

	# График динамики уровня зарплат по годам
	plt.subplot(2, 2, 1)
	plt.plot(list(year_salary.keys()), list(year_salary.values()))
	plt.title('Динамика уровня средней зарплаты по годам')
	plt.xlabel('Год')
	plt.ylabel('Уровень зарплат')

	# График динамики количества вакансий по годам
	plt.subplot(2, 2, 2)
	plt.plot(list(year_count.keys()), list(year_count.values()))
	plt.title('Динамика количества вакансий по годам')
	plt.xlabel('Год')
	plt.ylabel('Количество вакансий')

	# График динамики уровня зарплат по годам для выбранной профессии
	plt.subplot(2, 2, 3)
	plt.plot(list(year_salary_filtered.keys()), list(year_salary_filtered.values()))
	plt.title('Динамика уровня средней зарплаты по годам\nдля профессии Java-разработчика')
	plt.xlabel('Год')
	plt.ylabel('Уровень зарплат')

	# График динамики количества вакансий по годам для выбранной профессии
	plt.subplot(2, 2, 4)
	plt.plot(list(year_count_filtered.keys()), list(year_count_filtered.values()))
	plt.title('Динамика количества вакансий по годам\nдля профессии Java-разработчика')
	plt.xlabel('Год')
	plt.ylabel('Количество вакансий')
	plt.tight_layout()

	plt.savefig('vacancies_website/static/images/plot')


def get_demain_table(year_salary, year_count, year_salary_filtered, year_count_filtered):
	year = [2017]
	i = 0
	while i in year and i < 2024:
		year.append(i+1)

	results = pd.DataFrame({
		# 'Год': year,
		'Динамика уровня зарплат по годам': year_salary,
		'Динамика количества вакансий по годам': year_count,
		'Динамика уровня зарплат по годам для выбранной профессии': year_salary_filtered,
		'Динамика количества вакансий по годам для выбранной профессии': year_count_filtered
	})

	results.to_csv('vacancies_website/static/demain_table.csv', encoding='utf-8-sig', index=False)


# def get_curent_salary(df):
# 	database_name = 'mydatabase.db'
# 	currency_table = 'mytable'
#
# 	conn = sqlite3.connect(database_name)
#
# 	salaries = df['salary_from'].copy()
#
# 	for index, row in df.iterrows():
# 		salary = 0
# 		date = str(row['published_at'][:7])
# 		currency = 1
#
# 		if str(row['salary_currency']) != 'nan' and str(row['salary_currency']) != 'RUR':
# 			sql_query = f"SELECT {str(row['salary_currency'])} FROM {currency_table} WHERE date = '{date}' "
# 			cursor = conn.cursor()
# 			cursor = cursor.execute(sql_query)
#
# 			currency = cursor.fetchall()[0][0]
#
# 		if pd.isna(row['salary_from']) and pd.isna(row['salary_to']) or currency is None:
# 			salary = 0
# 		elif pd.isna(row['salary_from']):
# 			salary = int(row['salary_to'] / currency)
# 		elif pd.isna(row['salary_to']):
# 			salary = int(row['salary_from'] / currency)
# 		else:
# 			salary = int(((row['salary_from'] / currency) + (row['salary_to'] / currency)) // 2)
#
# 		salaries[int(index)] = salary
#
# 	return salaries


# get_demain_info()

