import pandas as pd
from matplotlib import pyplot as plt
from pandas import Series

from vacancies_website.currency import get_curent_salary


class Demain:
	@staticmethod
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

		Demain.get_demain_graph(year_salary, year_count, year_salary_filtered, year_count_filtered)
		Demain.get_demain_table(year_salary, year_count, year_salary_filtered, year_count_filtered)

	@staticmethod
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

	@staticmethod
	def get_demain_table(year_salary, year_count, year_salary_filtered, year_count_filtered):
		results = pd.DataFrame({
			'Год': list(year_salary.keys()),
			'Динамика уровня средней зарплаты по годам': list(year_salary.values()),
			'Динамика количества вакансий по годам': list(year_count.values()),
			'Динамика уровня средней зарплаты по годам\nдля профессии Java-разработчика': list(
				year_salary_filtered.values()),
			'Динамика количества вакансий по годам\nдля профессии Java-разработчика': list(year_count_filtered.values())
		})

		results.to_html('templates/demain_table.html', encoding='utf-8', index=False)


class Gegraphy:
	@staticmethod
	def get_geograpgy_info(vacancies, vac_name):
		pd.set_option('display.max_columns', None)

		vacancies['year'] = vacancies['published_at'].str[0:4]
		vacancies['salary'] = get_curent_salary(vacancies)

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

		Gegraphy.get_geography_graph(area_salary_all, area_percent_all, area_salary, area_percent)
		Gegraphy.get_geography_table(area_salary_all, area_percent_all, area_salary, area_percent)

	@staticmethod
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

	@staticmethod
	def get_geography_table(area_salary_all, area_percent_all, area_salary, area_percent):
		df_salary_all = pd.DataFrame(area_salary_all, columns=['Город', 'Уровень зарплат'])
		df_percent_all = pd.DataFrame(area_percent_all, columns=['Город', 'Доля вакансий'])
		df_salary = pd.DataFrame(area_salary, columns=['Город', 'Уровень зарплат'])
		df_percent = pd.DataFrame(area_percent, columns=['Город', 'Доля вакансий'])

		df_all = pd.merge(df_salary_all, df_percent_all, on='Город', suffixes=('_salary_all', '_percent_all'))
		df = pd.merge(df_salary, df_percent, on='Город', suffixes=('_salary', '_percent'))

		df_final = pd.merge(df_all, df, on='Город')

		df_final.to_html('templates/geography_table.html', encoding='utf-8', index=False)


class Skills:
	@staticmethod
	def get_top_skills_all_time(vacancies):
		pd.set_option('display.max_columns', None)

		skills_list = []
		for skill in vacancies['key_skills']:
			skills_list += skill.split('\n')

		vacancies_skills = Series(skills_list, name='vacancies_skills').value_counts()
		top_skills = vacancies_skills[0:20].to_dict()

		results = pd.DataFrame({
			'Навыки': list(top_skills.keys()),
			'Количество упоминаний': list(top_skills.values())
		})

		results.to_html('templates/skills_table.html', encoding='utf-8', index=False)

	@staticmethod
	def get_top_skills(vacancies, vac_name):
		pd.set_option('display.max_columns', None)

		vacancies['year'] = vacancies['published_at'].str[0:4]
		skills_by_year = vacancies.groupby(['year']).agg(['sum'])
		skills_by_year = skills_by_year['key_skills']

		for index, skills_list in skills_by_year.iterrows():
			skills = str(skills_list['sum']).split('\n')
			Skills.get_skills_graph(skills, index, False)

		sorted_vacancies = vacancies.loc[vacancies['name'].str.contains(vac_name, na=False, case=False)]
		sorted_skills_by_year = sorted_vacancies.groupby(['year']).agg(['sum'])
		sorted_skills_by_year = sorted_skills_by_year['key_skills']

		for index, skills_list in sorted_skills_by_year.iterrows():
			skills = str(skills_list['sum']).split('\n')
			Skills.get_skills_graph(skills, index, True)

	@staticmethod
	def get_skills_graph(skills, index, bool_sort):
		slice = 16
		for index_of_skill, skill in enumerate(skills):
			if len(skills[index_of_skill]) > slice:
				skills[index_of_skill] = f'{skill[:slice]}\n{skill[slice:slice * 2]}\n'

		vacancies_skills = Series(skills, name='vacancies_skills').value_counts()
		top_skills = vacancies_skills[0:20]

		plt.figure(figsize=(18, 13))
		plt.barh(list(top_skills.keys()), list(top_skills.values))
		plt.title(f'ТОП-20 навыков в профессии Java-разработчика в {index} году')
		plt.xlabel('Количество упомининйи')
		plt.ylabel('Навыки')

		if bool_sort:
			plt.savefig(f'vacancies_website/static/images/sorted_skill_plot/sorted_skill_plot{index}')
		else:
			plt.savefig(f'vacancies_website/static/images/skill_plot/skill_plot{index}')
