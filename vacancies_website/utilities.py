import sqlite3

import pandas as pd
from matplotlib import pyplot as plt
from pandas import Series


conn = sqlite3.connect('mydatabase.db', check_same_thread=False)

vacancies_table = 'vacancies'
currency_table = 'mytable'

#file_name = "C:/Users/eldo3/Downloads/vacancies.csv"
#vacancies = pd.read_csv(file_name, dtype={'name': str, 'key_skills': str, 'published_at': str})
#vacancies = vacancies.to_sql(vacancies_table, conn, if_exists='replace', index=False)
vac_name = 'java'


class Demain:
	@staticmethod
	def get_demain_info():
		years = {key: 0 for key in range(2003, 2024)}
		cursor = conn.cursor()

		cursor.execute(f"ALTER TABLE {vacancies_table} ADD COLUMN year TEXT;")
		cursor.execute(f"ALTER TABLE {vacancies_table} ADD COLUMN salary INTEGER;")
		conn.commit()

		cursor.execute(f"UPDATE {vacancies_table} SET year = SUBSTRING(published_at, 1, 4);")
		conn.commit()

		cursor.execute(f"UPDATE {vacancies_table} SET salary_from = salary_to WHERE salary_from IS NULL AND salary_to IS NOT NULL;")
		cursor.execute(f"UPDATE {vacancies_table} SET salary_to = salary_from WHERE salary_to IS NULL AND salary_from IS NOT NULL;")
		conn.commit()

		currency_query = f"""UPDATE {vacancies_table} SET salary = 
							CASE 
								WHEN salary_from IS NULL AND salary_to IS NULL OR salary_currency IS NULL THEN 0
								ELSE ((salary_from + salary_to) / 2) * (
									CASE 
										WHEN salary_currency = 'BYR' THEN (SELECT BYR FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
										WHEN salary_currency = 'USD' THEN (SELECT USD FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
										WHEN salary_currency = 'EUR' THEN (SELECT EUR FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
										WHEN salary_currency = 'KZT' THEN (SELECT KZT FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
										WHEN salary_currency = 'UAH' THEN (SELECT UAH FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
										WHEN salary_currency = 'AZN' THEN (SELECT AZN FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
										WHEN salary_currency = 'KGS' THEN (SELECT KGS FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
										WHEN salary_currency = 'UZS' THEN (SELECT UZS FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
										WHEN salary_currency = 'GEL' THEN (SELECT GEL FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
										ELSE 1
									END)
							END"""
		cursor.execute(currency_query)
		conn.commit()

		cursor.execute(f"DELETE FROM {vacancies_table} WHERE salary > 10000000;")
		conn.commit()

		vacancies_all = f"SELECT year, SUM(salary) AS sum_salary, COUNT(*) AS count_vacancies FROM {vacancies_table} GROUP BY year;"
		vacancies_all = cursor.execute(vacancies_all)
		vacancies_all = vacancies_all.fetchall()

		year_salary = years.copy()
		for row in range(len(vacancies_all)):
			year, sum_salary, count_vacancies = vacancies_all[row]
			year_salary[int(year)] = sum_salary // count_vacancies

		year_count = years.copy()
		for row in range(len(vacancies_all)):
			year, sum_salary, count_vacancies = vacancies_all[row]
			year_count[int(year)] = int(count_vacancies)

		vacancies_group_by_year = f"""SELECT year, SUM(salary) AS sum_salary, COUNT(*) AS count_vacancies
								FROM {vacancies_table} WHERE LOWER(name) LIKE LOWER('%{vac_name}%') GROUP BY year;"""
		vacancies_group_by_year = conn.execute(vacancies_group_by_year)
		vacancies_group_by_year = vacancies_group_by_year.fetchall()

		year_salary_filtered = years.copy()
		for row in range(len(vacancies_group_by_year)):
			year, sum_salary, count_vacancies = vacancies_group_by_year[row]
			year_salary_filtered[int(year)] = sum_salary // count_vacancies

		year_count_filtered = years.copy()
		for row in range(len(vacancies_group_by_year)):
			year, sum_salary, count_vacancies = vacancies_group_by_year[row]
			year_count_filtered[int(year)] = count_vacancies

		Demain.get_demain_graph(year_salary, year_count, year_salary_filtered, year_count_filtered)
		Demain.get_demain_table(year_salary, year_count, year_salary_filtered, year_count_filtered)

		cursor.close()

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
			'Средняя зарплата': list(year_salary.values()),
			'Количество вакансий': list(year_count.values()),
			'Средняя зарплата\nJava-разработчика': list(
				year_salary_filtered.values()),
			'Количество вакансий\nJava-разработчика': list(year_count_filtered.values())
		})

		results.to_html('templates/demain_table.html', encoding='utf-8', index=False)


class Gegraphy:
	@staticmethod
	def get_geograpgy_info():

		cursor = conn.cursor()
		cursor.execute(f"ALTER TABLE {vacancies_table} ADD COLUMN year TEXT;")
		cursor.execute(f"ALTER TABLE {vacancies_table} ADD COLUMN salary INTEGER;")
		conn.commit()

		cursor.execute(f"UPDATE {vacancies_table} SET year = SUBSTRING(published_at, 1, 4);")
		conn.commit()

		cursor.execute(f"UPDATE {vacancies_table} SET salary_from = salary_to WHERE salary_from IS NULL AND salary_to IS NOT NULL;")
		cursor.execute(f"UPDATE {vacancies_table} SET salary_to = salary_from WHERE salary_to IS NULL AND salary_from IS NOT NULL;")
		conn.commit()

		currency_query = f"""UPDATE {vacancies_table} SET salary = 
									CASE 
										WHEN salary_from IS NULL AND salary_to IS NULL OR salary_currency IS NULL THEN 0
										ELSE ((salary_from + salary_to) / 2) * (
											CASE 
												WHEN salary_currency = 'BYR' THEN (SELECT BYR FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
												WHEN salary_currency = 'USD' THEN (SELECT USD FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
												WHEN salary_currency = 'EUR' THEN (SELECT EUR FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
												WHEN salary_currency = 'KZT' THEN (SELECT KZT FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
												WHEN salary_currency = 'UAH' THEN (SELECT UAH FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
												WHEN salary_currency = 'AZN' THEN (SELECT AZN FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
												WHEN salary_currency = 'KGS' THEN (SELECT KGS FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
												WHEN salary_currency = 'UZS' THEN (SELECT UZS FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
												WHEN salary_currency = 'GEL' THEN (SELECT GEL FROM {currency_table} WHERE date = (SELECT SUBSTRING(published_at, 1, 7) FROM {vacancies_table}))
												ELSE 1
											END)
									END"""
		cursor.execute(currency_query)
		conn.commit()

		cursor.execute(f"DELETE FROM {vacancies_table} WHERE salary > 10000000;")
		conn.commit()

		area_salary_all = {}
		area_percent_all = {}

		sql_query = f"SELECT area_name, SUM(salary) AS sum_salary, COUNT(*) AS count_vacancies FROM {vacancies_table} GROUP BY area_name;"
		all_vacancies_grouped_by_area = cursor.execute(sql_query)
		all_vacancies_grouped_by_area = all_vacancies_grouped_by_area.fetchall()

		for row in range(len(all_vacancies_grouped_by_area)):
			area_name, sum_salary, count_vacancies = all_vacancies_grouped_by_area[row]
			if count_vacancies / len(all_vacancies_grouped_by_area) >= 0.1:
				area_salary_all[area_name] = int((sum_salary // count_vacancies))
				area_percent_all[area_name] = count_vacancies / len(all_vacancies_grouped_by_area)

		area_salary_all = list(sorted(area_salary_all.items(), key=lambda x: x[1], reverse=True))
		area_percent_all = list(sorted(area_percent_all.items(), key=lambda x: x[1], reverse=True))

		vacancies_grouped_by_area = f"""SELECT area_name, SUM(salary) AS sum_salary, COUNT(*) AS count_vacancies
						FROM vacancies WHERE LOWER(name) LIKE LOWER('%{vac_name}%') GROUP BY area_name;"""
		vacancies_grouped_by_area = cursor.execute(vacancies_grouped_by_area)
		vacancies_grouped_by_area = vacancies_grouped_by_area.fetchall()

		# sorted_vacancies = vacancies.loc[vacancies['name'].str.contains(vac_name, na=False, case=False)]
		# vacancies_grouped_by_area = sorted_vacancies.groupby('area_name').agg(['sum', 'count'])['salary']

		area_percent = {}
		area_salary = {}

		for row in range(len(vacancies_grouped_by_area)):
			area_name, sum_salary, count_vacancies = vacancies_grouped_by_area[row]
			if count_vacancies / len(vacancies_grouped_by_area) >= 0.01:
				area_salary[area_name] = int((sum_salary // count_vacancies))
				area_percent[area_name] = count_vacancies / len(vacancies_grouped_by_area)

		area_salary = list(sorted(area_salary.items(), key=lambda x: x[1], reverse=True))
		area_percent = list(sorted(area_percent.items(), key=lambda x: x[1], reverse=True))

		Gegraphy.get_geography_graph(area_salary_all[:10], area_percent_all[:10], area_salary[:10], area_percent[:10])
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
