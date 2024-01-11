from django.shortcuts import render

from vacancies_website.currency import create_currency_table
from vacancies_website.utility_demain import *
from vacancies_website.utility_georaphy import get_geograpgy_info
from vacancies_website.utility_skills import get_top_skills


file_name = "C:/Users/eldo3/Downloads/example_vacancies/vacancies_for_learn_demo.csv"
vacancies = pd.read_csv(file_name, dtype={'name': str, 'key_skills': str, 'published_at': str})
vac_name = 'java'


def home_page(request):
    create_currency_table()
    return render(request, 'home_page.html')


def demand_page(request):
    get_demain_info(vacancies, vac_name)
    return render(request, 'demand_page.html')


def geography_page(request):
    get_geograpgy_info(vacancies, vac_name)
    return render(request, 'geography_page.html')


def skills_page(request):
    get_top_skills(vacancies, vac_name)
    return render(request, 'skills_page.html')


def vacancies_page(request):
    return render(request, 'vacancies_page.html')


def demain_table(request):
    return render(request, 'demain_table.html')


def geography_table(request):
    return render(request, 'georaphy_table.html')
