import pandas as pd
from matplotlib import pyplot as plt

from vacancies_website.currency import get_curent_salary


def get_geograpgy_info():
	file_name = "C:/Users/eldo3/Downloads/example_vacancies/vacancies_for_learn_demo.csv"
	vac_name = 'java'
	vacancies = pd.read_csv(file_name)
	pd.set_option('display.max_columns', None)

	vacancies['year'] = vacancies['published_at'].str[0:4]
	vacancies['salary'] = get_curent_salary(vacancies)
	sl = vacancies['salary']

	area_percent_all = {}
	area_salary_all = {}

	all_vacancies_grouped_by_area = vacancies.groupby('area_name').agg(['sum', 'count'])['salary']

	for index, row in all_vacancies_grouped_by_area.iterrows():
		if row['count'] / len(all_vacancies_grouped_by_area) >= 0.1:
			area_salary_all[index] = int((row['sum'] // row['count']))
			area_percent_all[index] = row['count'] / len(all_vacancies_grouped_by_area)

	area_salary_all = list(sorted(area_salary_all.items(), key=lambda x: x[1], reverse=True))
	area_percent_all = list(sorted(area_percent_all.items(), key=lambda x: x[1], reverse=True))

	sorted_vacancies = vacancies.loc[vacancies['name'].str.contains(vac_name, na=False, case=False)]
	vacancies_grouped_by_area = sorted_vacancies.groupby('area_name').agg(['sum', 'count'])['salary']

	area_percent = {}
	area_salary = {}

	for index, row in vacancies_grouped_by_area.iterrows():
		if row['count'] / len(sorted_vacancies) >= 0.01:
			area_salary[index] = int((row['sum'] // row['count']))
			area_percent[index] = row['count'] / len(sorted_vacancies)

	area_salary = list(sorted(area_salary.items(), key=lambda x: x[1], reverse=True))
	area_percent = list(sorted(area_percent.items(), key=lambda x: x[1], reverse=True))

	get_geography_graph(area_salary_all, area_percent_all, area_salary, area_percent)


def get_geography_graph(area_salary_all, area_percent_all, area_salary, area_percent):
	plt.figure(figsize=(10, 25))
	plt.subplots_adjust(hspace=0.7)

	# График зарплат
	plt.subplot(4, 1, 1)
	plt.xticks(rotation=60)
	area_names = [item[0] for item in area_salary_all]
	salaries = [item[1] for item in area_salary_all]
	plt.bar(area_names, salaries)
	plt.xlabel('Город')
	plt.ylabel('Уровень зарплат')
	plt.title('Уровень зарплат по всем городам (в порядке убывания)')

	# График процентов
	plt.subplot(4, 1, 2)
	plt.xticks(rotation=60)
	area_names = [item[0] for item in area_percent_all]
	percents = [item[1] for item in area_percent_all]
	plt.bar(area_names, percents)
	plt.xlabel('Город')
	plt.ylabel('Доля вакансий')
	plt.title('Доля вакансий по всем городам (в порядке убывания)')

	# График зарплат
	plt.subplot(4, 1, 3)
	plt.xticks(rotation=60)
	area_names = [item[0] for item in area_salary]
	salaries = [item[1] for item in area_salary]
	plt.bar(area_names, salaries)
	plt.xlabel('Город')
	plt.ylabel('Уровень зарплат')
	plt.title('Уровень зарплат по городам (в порядке убывания)')

	# График процентов
	plt.subplot(4, 1, 4)
	plt.xticks(rotation=60)
	area_names = [item[0] for item in area_percent]
	percents = [item[1] for item in area_percent]
	plt.bar(area_names, percents)
	plt.xlabel('Город')
	plt.ylabel('Доля вакансий')
	plt.title('Доля вакансий по городам (в порядке убывания)')

	plt.savefig('vacancies_website/static/images/plot_geo')


get_geograpgy_info()
