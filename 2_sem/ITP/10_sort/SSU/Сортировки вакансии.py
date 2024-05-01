import csv


def parser_hh(query: str, area: int):
    import requests
    import re
    import os

    if not os.path.exists('vacancies.csv'):
        session = requests.Session()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        session.headers.update(headers)

        params = {
            'text': query,
            'per_page': 100,
            'pages': 1,
            'page': 0,
            'only_with_salary': True,
            'area': area
        }

        response = session.get('https://api.hh.ru/vacancies', params=params)
        with open('vacancies.csv', mode='w', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['Компания', 'Должность', 'Зарплата', 'Опыт работы'])
            writer.writeheader()

            for item in response.json().get('items', []):
                try:
                    title = item['name']
                    company = item['employer']['name']
                    experience = item['experience']
                    if 'no' in experience['id']:
                        experience = 0
                    else:
                        experience = [elem.strip() for elem in
                                      re.split(r'between|and', experience['id'], flags=re.IGNORECASE)]
                        experience = (int(experience[1]) + int(experience[2])) // 2
                    salary = item['salary']
                    if salary['from'] is not None and salary['to'] is not None:
                        salary = (salary['from'] + salary['to']) // 2
                    elif salary['from'] is not None:
                        salary = salary['from']
                    elif salary['to'] is not None:
                        salary = salary['to']

                    writer.writerow({
                        'Компания': company,
                        'Должность': title,
                        'Зарплата': salary,
                        'Опыт работы': experience
                    })

                except Exception:
                    continue


parser_hh('Машинное обучение', 79)  # 79 - код Саратова


def actions(data: list, action_number: int):
    def bubble_sort(array: list) -> list:
        n = len(array)
        for i in range(n):
            for j in range(n - i - 1):
                if array[j][0] >= array[j + 1][0]:
                    array[j], array[j + 1] = array[j + 1], array[j]
        return array

    def insertion_sort(array: list) -> list:
        n = len(array)
        for i in range(1, n):
            j = i
            while j > 0 and array[j][0] < array[j - 1][0]:
                array[j - 1], array[j] = array[j], array[j - 1]
                j -= 1
        return array

    def selection_sort(array: list) -> list:
        n = len(array)
        for i in range(n):
            low_index = i
            low_key = array[i][0]
            for j in range(i, n):
                if array[j][0] < low_key:
                    low_key = array[j][0]
                    low_index = j
            array[i], array[low_index] = array[low_index], array[i]
        return array

    def stable_selection_sort(array: list) -> list:
        n = len(array)
        for i in range(n):
            low_index = i
            for j in range(i + 1, n):
                if array[j][0] < array[low_index][0]:
                    low_index = j
            temp = array[low_index]
            while low_index > i:
                array[low_index] = array[low_index - 1]
                low_index -= 1
            array[i] = temp
        return array

    def prepare_data(data, criteria):
        prepared_data = []
        for job in data:
            key = []
            for crit in criteria:
                if callable(crit):
                    key.append(crit(job))
                else:
                    key.append(job[crit])
            prepared_data.append((tuple(key), job))
        return prepared_data

    def sort_vacancies(data, criteria, *sort_functions):
        prepared_data = prepare_data(data, criteria)
        results = []
        for sort_function in sort_functions:
            sorted_data = sort_function(prepared_data.copy())
            sorted_jobs = [item[1] for item in sorted_data]
            results.append(sorted_jobs)
        return results

    actions_dict = {
        1: sort_vacancies(data, ['Должность', 'Компания'], bubble_sort, insertion_sort, selection_sort,
                          stable_selection_sort),
        2: sort_vacancies(data, ['Должность', lambda job: int(job['Зарплата'])], bubble_sort, insertion_sort,
                          selection_sort,
                          stable_selection_sort),
        3: sort_vacancies(data, ['Должность', lambda job: -int(job['Зарплата'])], bubble_sort, insertion_sort,
                          selection_sort,
                          stable_selection_sort),
        4: sort_vacancies(data, ['Должность', lambda job: int(job['Опыт работы'])], bubble_sort, insertion_sort,
                          selection_sort,
                          stable_selection_sort),
        5: sort_vacancies(data, ['Должность', lambda job: -int(job['Опыт работы'])], bubble_sort, insertion_sort,
                          selection_sort,
                          stable_selection_sort),
        6: sort_vacancies(data, ['Должность', 'Компания', lambda job: int(job['Зарплата'])], bubble_sort,
                          insertion_sort, selection_sort, stable_selection_sort),
        7: sort_vacancies(data, ['Должность', 'Компания', lambda job: -int(job['Зарплата'])], bubble_sort,
                          insertion_sort, selection_sort, stable_selection_sort),
        8: sort_vacancies(data, ['Должность', 'Компания', lambda job: int(job['Опыт работы'])], bubble_sort,
                          insertion_sort, selection_sort, stable_selection_sort),
        9: sort_vacancies(data, ['Должность', 'Компания', lambda job: -int(job['Опыт работы'])], bubble_sort,
                          insertion_sort, selection_sort, stable_selection_sort),
        10: sort_vacancies(data, ['Компания', lambda job: int(job['Зарплата'])], bubble_sort, insertion_sort,
                           selection_sort, stable_selection_sort),
        11: sort_vacancies(data, ['Компания', lambda job: -int(job['Зарплата'])], bubble_sort, insertion_sort,
                           selection_sort, stable_selection_sort),
        12: sort_vacancies(data, ['Компания', 'Должность', lambda job: int(job['Зарплата'])], bubble_sort,
                           insertion_sort, selection_sort, stable_selection_sort),
        13: sort_vacancies(data, ['Компания', 'Должность', lambda job: -int(job['Зарплата'])], bubble_sort,
                           insertion_sort, selection_sort, stable_selection_sort),
        14: sort_vacancies(data, ['Компания', 'Должность', lambda job: int(job['Опыт работы'])], bubble_sort,
                           insertion_sort, selection_sort, stable_selection_sort),
        15: sort_vacancies(data, ['Компания', 'Должность', lambda job: -int(job['Опыт работы'])], bubble_sort,
                           insertion_sort, selection_sort, stable_selection_sort),
        16: sort_vacancies(data, ['Компания', lambda job: (int(job['Опыт работы']), int(job['Зарплата']))], bubble_sort,
                           insertion_sort, selection_sort, stable_selection_sort),
        17: sort_vacancies(data, ['Компания', lambda job: (int(job['Опыт работы']), -int(job['Зарплата']))],
                           bubble_sort, insertion_sort, selection_sort, stable_selection_sort),
        18: sort_vacancies(data, ['Должность', lambda job: (-int(job['Опыт работы']), int(job['Зарплата']))],
                           bubble_sort, insertion_sort, selection_sort, stable_selection_sort),
        19: sort_vacancies(data, [lambda job: (0, int(job['Зарплата'])) if int(job['Опыт работы']) == 0 else (
            1, job['Должность'], -int(job['Зарплата']))], bubble_sort, insertion_sort, selection_sort,
                           stable_selection_sort),
        20: sort_vacancies(data, [lambda job: (int(job['Опыт работы']) == 0,
                                               -int(job['Зарплата']) if int(job['Опыт работы']) == 0 else (
                                                   job['Должность'], int(job['Зарплата'])))
                                  ], bubble_sort, insertion_sort, selection_sort, stable_selection_sort)

    }

    res = actions_dict[action_number]

    for result, sort_name in zip(res,
                                 ["bubble_sort", "insertion_sort", "selection_sort", "stable_selection_sort"]):
        with open(f'vacancies_{sort_name}.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['Компания', 'Должность', 'Зарплата', 'Опыт работы'])
            writer.writeheader()
            writer.writerows(result)


while True:
    print('''Считать из файла информацию о вакансиях: фирма, должность, средняя зарплата, необходимый опыт работы.
Сортировать вакансии пузырьком, выбором (обычным образом и с добавлением устойчивости) и вставками:
1. по должности, при равенстве по фирме.
2. по должности, при равенстве по возрастанию зарплаты.
3. по должности, при равенстве по убыванию зарплаты.
4. по должности, при равенстве по возрастанию опыта работы.
5. по должности, при равенстве по убыванию опыта работы.
6. по должности, при равенстве по фирме, при равенстве по возрастанию зарплаты.
7. по должности, при равенстве по фирме, при равенстве по убыванию зарплаты.
8. по должности, при равенстве по фирме, при равенстве по возрастанию опыта работы.
9. по должности, при равенстве по фирме, при равенстве по убыванию опыта работы.
10. по фирме, при равенстве по возрастанию зарплаты.
11. по фирме, при равенстве по убыванию зарплаты.
12. по фирме, при равенстве по должности, при равенстве по возрастанию зарплаты.
13. по фирме, при равенстве по должности, при равенстве по убыванию зарплаты.
14. по фирме, при равенстве по должности, при равенстве по возрастанию опыта работы.
15. по фирме, при равенстве по должности, при равенстве по убыванию опыта работы.
16. по фирме, при равенстве по возрастанию опыта работы, при равенстве по возрастанию зарплаты.
17. по фирме, при равенстве по возрастанию опыта работы, при равенстве по убыванию зарплаты.
18. по должности, при равенстве по убыванию опыта работы, при равенстве по возрастанию зарплаты.
19. те вакансии, где не требуется опыт работы, по возрастанию зарплаты, остальные по должности, при равенстве по убыванию зарплаты.
20. те вакансии, где не требуется опыт работы, по убыванию зарплаты, остальные по должности, при равенстве по возрастанию зарплаты.
21. завершить работу.''')
    action = int(input('Выберите действие (1-21): '))
    if 1 <= action <= 20:
        with open('vacancies.csv', 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            data_list = [row for row in reader]
        actions(data_list, action)
        question = input('Хотите продолжить (да/нет)? ').lower().strip()
        if question == 'да':
            continue
        elif question == 'нет':
            break
        else:
            print('Извините, но вы ввели не "да" и не "нет".')
    elif action == 21:
        break
    else:
        print('Извините, но нет такого действия, попробуйте еще раз.')
