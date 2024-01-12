import requests
from django.shortcuts import render


def get_vacancies():
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "Java",  # Замените на профессию, которую вы ищете
        "per_page": 10,
        "order_by": "publication_time",
    }
    response = requests.get(url, params=params)
    vacancies = response.json()["items"][:10]

    for vacancy in vacancies:
        details_url = vacancy["url"]
        details_response = requests.get(details_url)
        details = details_response.json()
        vacancy["description"] = details["description"]
        vacancy["key_skills"] = ", ".join([skill["name"] for skill in details["key_skills"]])

    return vacancies


# def vacancies(request):
#     vacancies = get_vacancies()
#     return render(request, "vacancies.html", {"vacancies": vacancies})
