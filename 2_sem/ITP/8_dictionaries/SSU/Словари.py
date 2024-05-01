from collections import defaultdict


def actions(data: list, action_number: int):
    def count_digit():
        d_counter = defaultdict(int)
        for elem in data:
            if elem.isdigit() or elem.lstrip("-").isdigit():
                d_counter[elem] = d_counter.get(elem, 0) + 1
        return d_counter

    def count_words():
        d_counter = defaultdict(int)
        for elem in data:
            if elem.isalpha():
                d_counter[elem] = d_counter.get(elem, 0) + 1
        return d_counter

    def k_count_max_words():
        k = int(input('Введите k: '))
        d_counter = count_words()
        return sorted(d_counter.items(), key=lambda x: (-x[1], x[0]))[:k]

    def k_count_min_words():
        k = int(input('Введите k: '))
        d_counter = count_words()
        return sorted(d_counter.items(), key=lambda x: (x[1], x[0]))[:k]

    def k_count_exactly_nums():
        k = int(input('Введите k: '))
        d_counter = count_digit()
        return sorted([(key, value) for key, value in d_counter.items() if value == k])

    def k_count_exactly_words():
        k = int(input('Введите k: '))
        d_counter = count_words()
        return sorted([(key, value) for key, value in d_counter.items() if value == k])

    def first_count_words():
        d_counter = count_words()
        count_first = 0
        for elem in data:
            if elem.isalpha():
                count_first = d_counter[elem]
                print(f'Первое слово: {data[0], count_first}')
                break
        else:
            print('Слов нет')
        return sorted([(key, value) for key, value in d_counter.items() if value == count_first])

    def first_count_nums():
        d_counter = count_digit()
        count_first = 0
        for elem in data:
            if elem.isdigit() or elem.lstrip("-").isdigit():
                count_first = d_counter[elem]
                print(f'Первое число: {data[0], count_first}')
                break
        else:
            print('Чисел нет')
        return sorted([(key, value) for key, value in d_counter.items() if value == count_first])

    def last_count_words():
        d_counter = count_words()
        count_last = 0
        for elem in data[::-1]:
            if elem.isalpha():
                count_last = d_counter[elem]
                print(f'Последнее слово: {data[0], count_last}')
                break
        else:
            print('Слов нет')
        return sorted([(key, value) for key, value in d_counter.items() if value == count_last])

    def last_count_nums():
        d_counter = count_digit()
        count_last = 0
        for elem in data[::-1]:
            if elem.isdigit() or elem.lstrip("-").isdigit():
                count_last = d_counter[elem]
                print(f'Последнее число: {data[0], count_last}')
                break
        else:
            print('Чисел нет')
        return sorted([(key, value) for key, value in d_counter.items() if value == count_last])

    def index_words_fl():
        d_index = defaultdict(set)
        for i, elem in enumerate(data):
            if elem.isalpha():
                d_index[elem].add(i)
        return [(key, (sorted(value)[0], sorted(value)[-1])) for key, value in d_index.items()]

    def index_nums_fl():
        d_index = defaultdict(set)
        for i, elem in enumerate(data):
            if elem.isdigit() or elem.lstrip("-").isdigit():
                d_index[elem].add(i)
        return [(key, (sorted(value)[0], sorted(value)[-1])) for key, value in d_index.items()]

    def index_words():
        d_index = defaultdict(set)
        for i, elem in enumerate(data):
            if elem.isalpha():
                d_index[elem].add(i)
        return [(key, sorted(value)) for key, value in d_index.items()]

    def index_nums():
        d_index = defaultdict(set)
        for i, elem in enumerate(data):
            if elem.isdigit() or elem.lstrip("-").isdigit():
                d_index[elem].add(i)
        return [(key, sorted(value)) for key, value in d_index.items()]

    def index_plus_minus():
        d_index = dict(index_nums())
        return [((key, '-' + key), (value, d_index['-' + key])) for key, value in d_index.items() if
                '-' + key in d_index]

    def palindrome_word():
        d_index = defaultdict(set)
        for i, elem in enumerate(data):
            if elem.isalpha() and elem == elem[::-1]:
                d_index[elem].add(i)
        return [(key, sorted(value)) for key, value in d_index.items()]

    def reverse_word():
        d_index = dict(index_words())
        res = defaultdict(list)
        for key in d_index:
            if key[::-1] in d_index and (key, key[::-1]) not in res:
                res[(key[::-1], key)] += d_index[key] + d_index[key[::-1]]
        return res

    def index_nums_f():
        d_index = defaultdict(set)
        for i, elem in enumerate(data):
            if (elem.isdigit() and elem not in d_index) or (elem.lstrip("-").isdigit() and '-' + elem not in d_index):
                d_index[elem].add(i)
        return [((key, '-' + key), (value, d_index['-' + key])) for key, value in d_index.items() if
                '-' + key in d_index]

    def index_nums_l():
        d_index = defaultdict(set)
        for i, elem in enumerate(data[::-1]):
            if (elem.isdigit() and elem not in d_index) or (elem.lstrip("-").isdigit() and '-' + elem not in d_index):
                d_index[elem].add(i)
        return [((key, '-' + key), (value, d_index['-' + key])) for key, value in d_index.items() if
                '-' + key in d_index]

    actions_dict = {
        1: count_digit,
        2: count_words,
        3: k_count_max_words,
        4: k_count_min_words,
        5: k_count_exactly_nums,
        6: k_count_exactly_words,
        7: first_count_words,
        8: first_count_nums,
        9: last_count_words,
        10: last_count_nums,
        11: index_words_fl,
        12: index_nums_fl,
        13: index_words,
        14: index_nums,
        15: index_plus_minus,
        16: palindrome_word,
        17: reverse_word,
        18: index_nums_f,
        19: index_nums_l,

    }

    return actions_dict[action_number]()


while True:
    print('''Во входном файле задан набор слов и целых чисел, разделённых пробелами.
1)  Подсчитать, сколько раз встречается каждое присутствующее в файле число.
2)  Для каждого слова, не являющегося числом, подсчитать количество его вхождений.
3)  Найти k слов, встречающихся чаще остальных.
4)  Найти k слов, встречающихся реже остальных.
5)  Найти числа, встречающиеся ровно k раз.
6)  Найти слова, не являющиеся числами, встречающиеся ровно k раз.
7)  Найти все слова, встречающиеся столько же раз, сколько первое слово.
8)  Найти все слова, встречающиеся столько же раз, сколько первое число.
9)  Найти все слова, встречающиеся столько же раз, сколько последнее слово.
10) Найти все слова, встречающиеся столько же раз, сколько последнее число.
11) Для каждого слова найти первое и последнее вхождение.
12) Для каждого числа найти первое и последнее вхождение.
13) Для каждого слова найти все номера его позиций.
14) Для каждого числа найти все номера его позиций.
15) Для каждого числа найти позиции всех вхождений его самого и противоположного ему.
16) Для каждого слова-палиндрома найти позиции всех его вхождений.
17) Для каждого слова найти позиции вхождения его самого и его перевёрнутого варианта.
18) Для каждого числа найти первое вхождение его самого и противоположного ему.
19) Для каждого числа найти последнее вхождение его самого и противоположного ему.
20) Для каждого слова, не являющегося числом, найти все такие его позиции, которые кратны длине слова.
21) Завершить работу.''')
    action = int(input('Выберите действие (1-21): '))
    if 1 <= action <= 20:
        with open('input.txt', 'r', encoding='utf-8') as file:
            all_text = ' '.join([line.strip('\n') for line in file.readlines()]).split()
        print(actions(all_text, action))
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
