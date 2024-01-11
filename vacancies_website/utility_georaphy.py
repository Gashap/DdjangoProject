import pandas as pd
from matplotlib import pyplot as plt

from vacancies_website.currency import get_curent_salary


def get_geograpgy_info(vacancies, vac_name):
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
	get_geography_table(area_salary_all, area_percent_all, area_salary, area_percent)


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
	plt.title('Уровень зарплат по городам (в порядке убывания)')

	# График процентов
	plt.subplot(4, 1, 2)
	plt.xticks(rotation=60)
	area_names = [item[0] for item in area_percent_all]
	percents = [item[1] for item in area_percent_all]
	plt.bar(area_names, percents)
	plt.xlabel('Город')
	plt.ylabel('Доля вакансий')
	plt.title('Доля вакансий по городам (в порядке убывания)')

	# График зарплат
	plt.subplot(4, 1, 3)
	plt.xticks(rotation=60)
	area_names = [item[0] for item in area_salary]
	salaries = [item[1] for item in area_salary]
	plt.bar(area_names, salaries)
	plt.xlabel('Город')
	plt.ylabel('Уровень зарплат')
	plt.title('Уровень зарплат Java-разработчика по городам (в порядке убывания)')

	# График процентов
	plt.subplot(4, 1, 4)
	plt.xticks(rotation=60)
	area_names = [item[0] for item in area_percent]
	percents = [item[1] for item in area_percent]
	plt.bar(area_names, percents)
	plt.xlabel('Город')
	plt.ylabel('Доля вакансий')
	plt.title('Доля вакансий Java-разработчика по городам (в порядке убывания)')

	plt.savefig('vacancies_website/static/images/plot_geo')


def get_geography_table(area_salary_all, area_percent_all, area_salary, area_percent):
	df_salary_all = pd.DataFrame(area_salary_all, columns=['Город', 'Уровень зарплат'])
	df_percent_all = pd.DataFrame(area_percent_all, columns=['Город', 'Доля вакансий'])
	df_salary = pd.DataFrame(area_salary, columns=['Город', 'Уровень зарплат'])
	df_percent = pd.DataFrame(area_percent, columns=['Город', 'Доля вакансий'])

	df_all = pd.merge(df_salary_all, df_percent_all, on='Город', suffixes=('_salary_all', '_percent_all'))
	df = pd.merge(df_salary, df_percent, on='Город', suffixes=('_salary', '_percent'))

	df_final = pd.merge(df_all, df, on='Город')

	df_final.to_html('templates/georaphy_table.html', encoding='utf-8', index=False)


# get_geograpgy_info()
