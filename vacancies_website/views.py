from django.shortcuts import render

from vacancies_website.currency import create_currency_table
from vacancies_website.utility_demain import *
from vacancies_website.utility_georaphy import get_geograpgy_info


def home_page(request):
    create_currency_table()
    return render(request, 'home_page.html')


def demand_page(request):
    get_demain_info()
    return render(request, 'demand_page.html')


def geography_page(request):
    get_geograpgy_info()
    return render(request, 'geography_page.html')


def skills_page(request):
    return render(request, 'skills_page.html')


def vacancies_page(request):
    return render(request, 'vacancies_page.html')
