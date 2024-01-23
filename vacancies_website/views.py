import sqlite3

import requests
from django.shortcuts import render

from vacancies_website.currency import create_currency_table
from vacancies_website.utilities import *


# conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
# vacancies_table = 'vacancies'
#
# file_name = "C:/Users/eldo3/Downloads/vacancies.csv"
# vacancies = pd.read_csv(file_name, dtype={'name': str, 'key_skills': str, 'published_at': str})
# vacancies = vacancies.to_sql(vacancies_table, conn, if_exists='replace', index=False)
# vac_name = 'java'


def home_page(request):
    # create_currency_table()
    return render(request, 'home_page.html')


def demand_page(request):
    # Demain.get_demain_info()
    return render(request, 'demand_page.html')


def geography_page(request):
    # Gegraphy.get_geograpgy_info()
    return render(request, 'geography_page.html')


def skills_page(request):
    # Skills.get_top_skills_all_time(vacancies)
    Skills.get_top_skills(vacancies_table, vac_name)
    return render(request, 'skills_page.html')


def get_vacancies():
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": f"{vac_name}"
    }
    response = requests.get(url, params=params)
    vacancies = response.json()["items"][:10]

    for vacancy in vacancies:
        details_url = vacancy["url"]
        details_response = requests.get(details_url)
        details = details_response.json()
        vacancy["description"] = details["description"]
        vacancy['published_at'] = details["published_at"][:10]
        vacancy["key_skills"] = ", ".join([skill["name"] for skill in details["key_skills"]])

    return vacancies


def vacancies_page(request):
    vacancies = get_vacancies()
    return render(request, "vacancies_page.html", {"vacancies_page": vacancies})

