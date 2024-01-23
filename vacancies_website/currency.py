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
		date = datetime(2003, 1, 1)
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


# def get_curent_salary(vacancies_table):
# 	database_name = 'mydatabase.db'
# 	currency_table = 'mytable'
#
# 	conn = sqlite3.connect(database_name)
# 	cursor = conn.cursor()
#
# 	sql_query = f"SELECT published_at, salary_from, salary_to, salary_currency FROM {vacancies_table};"
# 	vacancies_salary = conn.execute(sql_query)
# 	vacancies_salary = vacancies_salary.fetchall()
#
# 	for row in vacancies_salary:
# 		date, salary_from, salary_to, salary_currency = row
# 		y_m = date[:7]
# 		currency = 1
#
# 		if salary_currency is not None and salary_currency != 'RUR':
# 			sql_query = f"SELECT {salary_currency} FROM {currency_table} WHERE date = '{y_m}';"
# 			cursor = conn.cursor()
# 			currency = cursor.execute(sql_query)
# 			currency = currency.fetchall()[0][0]
#
# 		if pd.isna(salary_from) and pd.isna(salary_to) or currency is None:
# 			salary = 0
# 		elif pd.isna(salary_from):
# 			salary = int(salary_to * currency)
# 		elif pd.isna(salary_to):
# 			salary = int(salary_from * currency)
# 		else:
# 			salary = int(((salary_from * currency) + (salary_to * currency)) // 2)
#
# 		sql_q = f"UPDATE {vacancies_table} SET salary = ? WHERE published_at = ?;"
# 		conn.execute(sql_q, (salary, date))
# 		conn.commit()
#
# 		cursor.close()
# 	conn.close()

# get_curent_salary(pd.read_csv("C:/Users/eldo3/Downloads/example_vacancies/vacancies_for_learn_demo.csv"))
