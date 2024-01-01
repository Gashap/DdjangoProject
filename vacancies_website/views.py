from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from matplotlib import pyplot as plt


def home_page(request):
    return render(request, 'home_page.html')


def demand_page(request):
    x = [1, 2, 3, 4, 5]
    y = [25, 32, 34, 20, 25]

    plt.plot(x, y, color='green', marker='o', markersize=7)
    plt.xlabel('Ось х')  # Подпись для оси х
    plt.ylabel('Ось y')  # Подпись для оси y
    plt.title('Первый график')  # Название
    plt.savefig('vacancies_website/static/images/plot')
    return render(request, 'demand_page.html')


def geography_page(request):
    return render(request, 'geography_page.html')


def skills_page(request):
    return render(request, 'skills_page.html')


def vacancies_page(request):
    return render(request, 'vacancies_page.html')
