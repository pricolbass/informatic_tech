data_list = list(map(int, input('Задайте в одну строку через пробел список чисел: ').split()))


def actions(data: list, action_number: int):
    def even_elem():
        for i in range(len(data)):
            if data[i] % 2 == 0:
                data[i] *= 2
        print(f'Результат: {data}')

    def del_even_average():
        even_data = [elem for elem in data if elem % 2 == 0]
        even_average = sum(even_data) / len(even_data)
        for i in range(len(data) - 1, -1, -1):
            if data[i] < even_average:
                del data[i]
        print(f'Результат: {data}')

    def odd_right_elem():
        for i, (elem1, elem2) in enumerate(zip(data, data[1:])):
            if elem2 % 2 != 0:
                data[i] = 0
        print(f'Результат: {data}')

    def del_pairs():
        from collections import Counter
        element_count = Counter(data)

        for element in list(element_count):
            opposite = -element
            if opposite in element_count:
                min_count = min(element_count[element], element_count[opposite])
                element_count[element] -= min_count
                element_count[opposite] -= min_count

                if element_count[element] == 0:
                    del element_count[element]
                if element_count[opposite] == 0:
                    del element_count[opposite]

        new_lst = []
        for element, count in element_count.items():
            new_lst.extend([element] * count)
        data.clear()
        data.extend(new_lst)
        print(f'Результат: {data}')

    def even_odd():
        start_index = None
        for i in range(len(data)):
            if data[i] % 2 != 0:
                if start_index is None:
                    start_index = i
                else:
                    for j in range(start_index + 1, i):
                        data[j] /= 2
                    start_index = i
        print(f'Результат: {data}')

    def del_repeat():
        from collections import Counter
        element_count = Counter(data)

        for i in range(len(data) - 1, -1, -1):
            if element_count[data[i]] > 1:
                del data[i]
        print(f'Результат: {data}')

    def before_max_elem():
        max_elem = max(data)
        max_elem_ind = len(data) - data[::-1].index(max_elem)
        for i in range(max_elem_ind):
            if data[i] != max_elem:
                data[i] *= 3
        print(f'Результат: {data}')

    def next_min_elem():
        min_elem = min(data)
        min_elem_ind = data.index(min_elem)
        for i in range(len(data) - 1, min_elem_ind, -1):
            if data[i] != min_elem and data[i] % 2 != 0:
                del data[i]
        print(f'Результат: {data}')

    def next_max_elem():
        max_elem = max(data)
        max_elem_ind = data.index(max_elem)
        for i in range(max_elem_ind + 1, len(data)):
            if data[i] != max_elem and data[i] % 2 != 0:
                data[i] *= 10
        print(f'Результат: {data}')

    def min_max_elem():
        min_elem = min(data)
        max_elem = max(data)
        start = min(data.index(min_elem), data.index(max_elem))
        end = max(len(data) - data[::-1].index(min_elem), len(data) - data[::-1].index(max_elem))
        for i in range(start + 1, end):
            if data[i] % 2 == 0 and data[i] != max_elem and data[i] != min_elem:
                data[i] /= 2
        print(f'Результат: {data}')

    def next_positive():
        for i, (elem1, elem2) in enumerate(zip(data, data[1:])):
            if elem2 > 0:
                data[i] *= 3
        print(f'Результат: {data}')

    def del_2part():
        start = len(data) // 2
        for i in range(len(data) - 1, start - 1, -1):
            if data[i] % 5 == 0:
                del data[i]
        print(f'Результат: {data}')

    def before_negative():
        neg_elems = [elem for elem in data if elem < 0]
        if len(neg_elems):
            neg_max_ind = len(data) - data[::-1].index(neg_elems[-1])
            for i in range(neg_max_ind - 1, -1, -1):
                if data[i] > 0 and data[i] % 3 == 0:
                    data[i] += 9
        print(f'Результат: {data}')

    def del_min_div():
        min_elem = min(data)
        for i in range(len(data) - 1, -1, -1):
            if data[i] % min_elem == 0:
                del data[i]
        print(f'Результат: {data}')

    def next_max_even():
        max_elem = max(data)
        max_elem_ind = data.index(max_elem)
        for i in range(len(data) - 1, max_elem_ind, -1):
            if data[i] != max_elem and data[i] % 2 == 0:
                del data[i]
        print(f'Результат: {data}')

    def even_average():
        average = sum(data) / len(data)
        for i in range(len(data) - 1, -1, -1):
            if data[i] % 2 == 0 and data[i] > average:
                del data[i]
        print(f'Результат: {data}')

    def odd_elem_10():
        for i in range(len(data)):
            if data[i] % 2 != 0:
                data[i] += 10

    def next_max_average():
        average = sum(data) / len(data)
        max_elem = max(data)
        max_elem_ind = data.index(max_elem)
        for i in range(len(data) - 1, max_elem_ind, -1):
            if data[i] != max_elem and data[i] < average:
                del data[i]
        print(f'Результат: {data}')

    def next_even():
        for i, (elem1, elem2) in enumerate(zip(data, data[1:])):
            if elem2 % 2 == 0:
                data[i] -= 2
        print(f'Результат: {data}')

    def count_1():
        from collections import Counter
        element_count = Counter(data)

        for i in range(len(data) - 1, -1, -1):
            if element_count[data[i]] == 1:
                del data[i]
        print(f'Результат: {data}')

    def next_min_10():
        min_elem = min(data)
        min_elem_ind = data.index(min_elem)
        for i in range(len(data) - 1, min_elem_ind, -1):
            if data[i] != min_elem:
                data[i] -= 10
        print(f'Результат: {data}')

    def count_odd():
        from collections import Counter
        element_counter = Counter(data)

        for i in range(len(data) - 1, -1, -1):
            if data[i] % 2 != 0 and element_counter[data[i]] == 1:
                del data[i]

    def next_max_1():
        max_elem = max(data)
        max_elem_ind = data.index(max_elem)
        for i in range(len(data) - 1, max_elem_ind, -1):
            if data[i] != max_elem:
                data[i] -= 1
        print(f'Результат: {data}')

    def del_1part():
        end = len(data) // 2
        for i in range(end - 1, -1, -1):
            if data[i] % 3 == 0:
                del data[i]
        print(f'Результат: {data}')

    def before_min():
        min_elem = min(data)
        min_elem_ind = len(data) - data[::-1].index(min_elem)
        for i in range(min_elem_ind - 1):
            if data[i] != min_elem and data[i] % 2 == 0:
                data[i] -= 2
        print(f'Результат: {data}')

    def div_max():
        max_elem = max(data)
        for i in range(len(data) - 1, -1, -1):
            if max_elem % data[i] == 0:
                del data[i]
        print(f'Результат: {data}')

    def before_negative_5():
        for i, (elem1, elem2) in enumerate(zip(data, data[1:])):
            if elem1 < 0:
                data[i + 1] += 5
        print(f'Результат: {data}')

    def div_ind():
        for i in range(len(data) - 1, -1, -1):
            if data[i] % (i + 1) == 0:
                del data[i]
        print(f'Результат: {data}')

    def next_0():
        if 0 in data:
            ind_0 = data.index(0)
            for i in range(ind_0 + 1, len(data)):
                if data[i] != 0 and data[i] % 5 == 0:
                    data[i] *= 2
        print(f'Результат: {data}')

    def dig_1_elem():
        all_dig = set(str(data[0]))
        for i in range(len(data) - 1, -1, -1):
            if set(str(data[i])) == all_dig:
                del data[i]
        print(f'Результат: {data}')

    actions_dict = {
        1: even_elem,
        2: del_even_average,
        3: odd_right_elem,
        4: del_pairs,
        5: even_odd,
        6: del_repeat,
        7: before_max_elem,
        8: next_min_elem,
        9: next_max_elem,
        10: min_max_elem,
        11: next_positive,
        12: del_2part,
        13: before_negative,
        14: del_min_div,
        15: next_max_even,
        16: even_average,
        17: odd_elem_10,
        18: next_max_average,
        19: next_even,
        20: count_1,
        21: next_min_10,
        22: count_odd,
        23: next_max_1,
        24: del_1part,
        25: before_min,
        26: div_max,
        27: before_negative_5,
        28: div_ind,
        29: next_0,
        30: dig_1_elem
    }

    return actions_dict[action_number]()


while True:
    print('''Список заданий:
1.  Все четные элементы увеличить в 2 раза.
2.  Удалить элементы, имеющие значение меньше среднего арифметического четных элементов массива.
3.  Все элементы, правее которых стоит нечетное значение, заменить на 0.
4.  Удалить пары противоположных элементов.
5.  Все четные элементы, стоящие между нечетными, уменьшить в 2 раза.
6.  Удалить элементы, встречающиеся в массиве более одного раза.
7.  Все элементы, стоящие перед максимальным, увеличить в 3 раза.
8.  Удалить все нечетные элементы, стоящие после минимального.
9.  Все нечетные элементы, стоящие после максимального, увеличить в 10 раз.
10. Все четные элементы между минимальным и максимальным разделить на 2.
11. Все элементы, после которых стоит положительное число, увеличить в 3 раза.
12. Удалить кратные 5 элементы из второй половины списка.
13. Все элементы кратные 3, стоящие перед отрицательными, увеличить на 9.
14. Удалить элементы, которые делятся на минимальный элемент без остатка.
15. Удалить четные элементы, стоящие после максимального.
16. Удалить четные элементы, имеющие значение больше среднего арифметического всех элементов массива.
17. Все нечетные элементы увеличить на 10.
18. Удалить элементы, стоящие после максимального и имеющие значение меньше среднего арифметического всех элементов массива.
19. Все элементы, правее которых стоит четный элемент, уменьшить на 2.
20. Удалить элементы, встречающиеся в массиве только один раз.
21. Все элементы, стоящие после минимального, уменьшить на 10.
22. Удалить нечетные элементы, встречающиеся в массиве только один раз.
23. Все элементы, стоящие после максимального, уменьшить на 1.
24. Удалить кратные 3 элементы из первой половины списка.
25. Все четные элементы, стоящие левее минимального, уменьшить в 2 раза.
26. Удалить элементы, являющиеся делителями максимального.
27. Все элементы, перед которыми стоит отрицательное число, увеличить на 5.
28. Удалить элементы, которые делятся на свой индекс (нумерация с 1).
29. Все элементы кратные 5, стоящие после 0, увеличить в 2 раза.
30. Удалить элементы, которые содержат все цифры первого элемента.
31. Завершить работу.''')
    action = int(input('Выберите действие (1-31): '))
    if 1 <= action <= 30:
        print(f'Введённый список чисел: {data_list}')
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
