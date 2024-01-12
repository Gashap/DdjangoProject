import pandas as pd
from matplotlib import pyplot as plt

from vacancies_website.currency import get_curent_salary


def get_demain_info(vacancies, vac_name):
	years = {key: 0 for key in range(2017, 2024)}
	pd.set_option('display.max_columns', None)

	vacancies['year'] = vacancies['published_at'].str[0:4]
	vacancies['salary'] = get_curent_salary(vacancies)

	vacancies_with_sum_count = vacancies.groupby(['year']).agg(['sum', 'count'])
	vacancies_with_sum_count = vacancies_with_sum_count['salary']

	year_salary = years.copy()
	for index, row in vacancies_with_sum_count.iterrows():
		year_salary[int(index)] = int(row['sum'] // row['count'])

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
	get_demain_table(year_salary, year_count, year_salary_filtered, year_count_filtered)


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

	results = pd.DataFrame({
		'Год': list(year_salary.keys()),
		'Динамика уровня средней зарплаты по годам': list(year_salary.values()),
		'Динамика количества вакансий по годам': list(year_count.values()),
		'Динамика уровня средней зарплаты по годам\nдля профессии Java-разработчика': list(year_salary_filtered.values()),
		'Динамика количества вакансий по годам\nдля профессии Java-разработчика': list(year_count_filtered.values())
	})

	results.to_html('templates/demain_table.html', encoding='utf-8', index=False)


# get_demain_info()
