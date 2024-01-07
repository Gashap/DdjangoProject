import sqlite3

import pandas as pd
from matplotlib import pyplot as plt


def create_currency_table():
	import requests
	import csv
	from datetime import datetime
	from sqlalchemy import create_engine

	# Определите URL API
	url = "https://www.cbr.ru/scripts/XML_daily.asp"

	# Определите валюты, которые вам нужны
	currencies = ["BYR", "USD", "EUR", "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]

	# Создайте файл CSV
	with open("vacancies_website/static/currency_table.csv", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerow(["date"] + currencies)

		# Пройдите через каждый месяц с 01.01.2003 по 01.06.2023
		date = datetime(2017, 1, 1)
		end_date = datetime(2023, 12, 1)
		while date <= end_date:
			# Получите данные с API
			response = requests.get(url, params={"date_req": date.strftime("%d/%m/%Y")})
			data = response.content.decode("windows-1251")

			# Извлеките курсы валют
			rates = []
			for currency in currencies:
				start = data.find("<CharCode>" + currency + "</CharCode>")
				if start != -1:
					start = data.find("<Value>", start) + 7
					end = data.find("</Value>", start)
					rate = data[start:end].replace(",", ".")
					rates.append(float(rate))
				elif currency == "BYR" and start == -1:
					start = data.find("<Value>", 887) + 7
					end = data.find("</Value>", 887)
					rate = data[start:end].replace(",", ".")
					rates.append(float(rate))
				else: rates.append("")

			# Запишите данные в CSV
			writer.writerow([date.strftime("%Y-%m")] + rates)

			# Перейдите к следующему месяцу
			if date.month == 12: date = date.replace(year=date.year + 1, month=1)
			else: date = date.replace(month=date.month + 1)

	# Создайте движок SQLAlchemy
	engine = create_engine('sqlite:///mydatabase.db')
	# Загрузите данные из CSV-файла
	data = pd.read_csv('vacancies_website/static/currency_table.csv')
	# Запишите данные в таблицу SQL
	data.to_sql('mytable', engine, if_exists='replace', index=False)


def get_demain_info():
	create_currency_table()

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


def get_curent_salary(df):
	database_name = 'mydatabase.db'
	currency_table = 'mytable'

	conn = sqlite3.connect(database_name)

	# currency_dict = {'date': 0, 'BYR': 1, 'USD': 2, 'EUR': 3,
	# 				'KZT': 4, 'UAH': 5, 'AZN': 6, 'KGS': 7, 'UZS': 8}

	salaries = df['salary_from'].copy()

	for index, row in df.iterrows():
		salary = 0
		date = str(row['published_at'][:7])
		currency = 1

		if str(row['salary_currency']) != 'nan' and str(row['salary_currency']) != 'RUR':
			sql_query = f"SELECT {str(row['salary_currency'])} FROM {currency_table} WHERE date = '{date}' "
			cursor = conn.cursor()
			cursor = cursor.execute(sql_query)

			currency = cursor.fetchall()[0][0]

		if pd.isna(row['salary_from']) and pd.isna(row['salary_to']) or currency is None:
			salary = 0
		elif pd.isna(row['salary_from']):
			salary = int(row['salary_to'] / currency)
		elif pd.isna(row['salary_to']):
			salary = int(row['salary_from'] / currency)
		else:
			salary = int(((row['salary_from'] / currency) + (row['salary_to'] / currency)) // 2)

		salaries[int(index)] = salary

	return salaries


# get_demain_info()

