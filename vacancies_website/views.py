from django.shortcuts import render

from vacancies_website.utility import *


def home_page(request):
    return render(request, 'home_page.html')


def demand_page(request):
    get_demain_info()
    return render(request, 'demand_page.html')


def geography_page(request):
    return render(request, 'geography_page.html')


def skills_page(request):
    return render(request, 'skills_page.html')


def vacancies_page(request):
    return render(request, 'vacancies_page.html')
