import sqlite3

import pandas as pd
from bs4 import BeautifulSoup


def create_currency_table():
	import requests
	import csv
	from datetime import datetime
	from sqlalchemy import create_engine

	url = "https://www.cbr.ru/scripts/XML_daily.asp"

	currencies = ["BYR", "USD", "EUR", "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]

	with open("vacancies_website/static/currency_table.csv", "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerow(["date"] + currencies)

		# Пройдите через каждый месяц с 01.01.2003 по 01.06.2023
		date = datetime(2017, 1, 1)
		end_date = datetime(2023, 12, 1)
		while date <= end_date:
			response = requests.get(url, params={"date_req": date.strftime("%d/%m/%Y")})

			soup = BeautifulSoup(response.content, 'xml')
			valutes = soup.find_all('Valute')

			rates = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
			for valute in range(len(valutes)):
				if valutes[valute].CharCode.text in currencies or valutes[valute].CharCode.text == "BYN":
					course = valutes[valute].Value.text.replace(',', '.')
					nominal = valutes[valute].Nominal.text
					value = round(float(course) / float(nominal), 8)

					if valutes[valute].CharCode.text == "BYN":
						rates[currencies.index('BYR')] = value
					else:
						rates[currencies.index(valutes[valute].CharCode.text)] = value

			writer.writerow([date.strftime("%Y-%m")] + rates)

			if date.month == 12:
				date = date.replace(year=date.year + 1, month=1)
			else:
				date = date.replace(month=date.month + 1)

	# Создайте движок SQLAlchemy
	engine = create_engine('sqlite:///mydatabase.db')
	# Загрузите данные из CSV-файла
	data = pd.read_csv('vacancies_website/static/currency_table.csv')
	# Запишите данные в таблицу SQL
	data.to_sql('mytable', engine, if_exists='replace', index=False)


def get_curent_salary(df):
	database_name = 'mydatabase.db'
	currency_table = 'mytable'

	conn = sqlite3.connect(database_name)

	salaries = df['salary_from'].copy()

	for index, row in df.iterrows():
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
			salary = int(row['salary_to'] * currency)
		elif pd.isna(row['salary_to']):
			salary = int(row['salary_from'] * currency)
		else:
			salary = int(((row['salary_from'] * currency) + (row['salary_to'] * currency)) // 2)

		salaries[int(index)] = salary

	return salaries


# get_curent_salary(pd.read_csv("C:/Users/eldo3/Downloads/example_vacancies/vacancies_for_learn_demo.csv"))
