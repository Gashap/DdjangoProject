import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from matplotlib import pyplot as plt


def home_page(request):
    return render(request, 'home_page.html')


def demand_page(request):
    years = {key: 0 for key in range(2017, 2024)}
    file_name = "C:/Users/eldo3/Downloads/example_vacancies/vacancies_for_learn_demo.csv"
    vac_name = 'java'
    vacancies = pd.read_csv(file_name)
    pd.set_option('display.max_columns', None)
    vacancies['year'] = vacancies['published_at'].str[0:4]
    vacancies['salary'] = (vacancies['salary_from'] + vacancies['salary_to']) / 2
    vacancies_with_sum_count = vacancies.groupby('year').agg(['sum', 'count'])
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

    vacancies_grouped_by_area = sorted_vacancies.groupby('area_name').agg(['sum', 'count'])['salary']
    area_percent = {}
    area_salary = {}
    for index, row in vacancies_grouped_by_area.iterrows():
        if row['count'] / len(sorted_vacancies) >= 0.01:
            area_salary[index] = int((row['sum'] // row['count']))
            area_percent[index] = row['count'] / len(sorted_vacancies)

    # Постройка графиков
    plt.figure(figsize=(10, 6))

    # График динамики уровня зарплат по годам
    plt.subplot(2, 2, 1)
    plt.plot(list(year_salary.keys()), list(year_salary.values()))
    plt.title('Динамика уровня зарплат по годам')
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
    plt.title('Динамика уровня зарплат по годам\nдля выбранной профессии')
    plt.xlabel('Год')
    plt.ylabel('Уровень зарплат')

    # График динамики количества вакансий по годам для выбранной профессии
    plt.subplot(2, 2, 4)
    plt.plot(list(year_count_filtered.keys()), list(year_count_filtered.values()))
    plt.title('Динамика количества вакансий по годам\nдля выбранной профессии')
    plt.xlabel('Год')
    plt.ylabel('Количество вакансий')

    plt.tight_layout()
    plt.savefig('vacancies_website/static/images/plot')
    return render(request, 'demand_page.html')


def geography_page(request):
    return render(request, 'geography_page.html')


def skills_page(request):
    return render(request, 'skills_page.html')


def vacancies_page(request):
    return render(request, 'vacancies_page.html')
