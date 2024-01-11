import pandas as pd
from matplotlib import pyplot as plt
from pandas import Series


def get_top_skills(vacancies, vac_name):
	pd.set_option('display.max_columns', None)

	vacancies['year'] = vacancies['published_at'].str[0:4]
	skills_by_year = vacancies.groupby(['year']).agg(['sum'])
	skills_by_year = skills_by_year['key_skills']

	for index, skills_list in skills_by_year.iterrows():
		skills = str(skills_list['sum']).split('\n')
		get_skills_graph(skills, index, False)

	sorted_vacancies = vacancies.loc[vacancies['name'].str.contains(vac_name, na=False, case=False)]
	sorted_skills_by_year = sorted_vacancies.groupby(['year']).agg(['sum'])
	sorted_skills_by_year = sorted_skills_by_year['key_skills']

	for index, skills_list in sorted_skills_by_year.iterrows():
		skills = str(skills_list['sum']).split('\n')
		get_skills_graph(skills, index, True)


def get_skills_graph(skills, index, bool_sort):
	slice = 16
	for index_of_skill, skill in enumerate(skills):
		if len(skills[index_of_skill]) > slice:
			skills[index_of_skill] = f'{skill[:slice]}\n{skill[slice:slice * 2]}\n'

	vacancies_skills = Series(skills, name='vacancies_skills').value_counts()
	top_skills = vacancies_skills[0:20]

	plt.figure(figsize=(18, 13))
	plt.barh(list(top_skills.keys()), list(top_skills.values))
	plt.title(f'ТОП-20 навыков в профессии Java-разработчика в {index} году')
	plt.xlabel('Количество упомининйи')
	plt.ylabel('Навыки')

	# if bool_sort: plt.savefig(f'C:/Users/eldo3/Downloads/exercise/sorted_skill_plot{index}')
	# else: plt.savefig(f'C:/Users/eldo3/Downloads/exercise/skill_plot{index}')

	if bool_sort: plt.savefig(f'vacancies_website/static/images/sorted_skill_plot/sorted_skill_plot{index}')
	else: plt.savefig(f'vacancies_website/static/images/skill_plot/skill_plot{index}')


# get_top_skills()
