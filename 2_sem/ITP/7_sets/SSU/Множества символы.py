from string import ascii_letters, punctuation
n = int(input('Введите количество строк: '))
s = [input(f'Введите строку {i + 1}/{n}: ') for i in range(n)]


def actions(lines: list, num_action: int):
    if num_action == 1:
        res = set(lines[0])
        for line in lines[1:]:
            res.intersection_update(set(line))
        return sorted(symbol for symbol in res if symbol.isalpha())
    if num_action == 2:
        res = set(ascii_letters)
        for line in lines:
            res.difference_update(set(line))
        return sorted(res)
    if num_action == 3:
        res = set()
        for line in lines:
            res.update(set(line))
        return sorted(symbol for symbol in res if symbol.isalpha() and symbol.isupper())
    if num_action == 4:
        res = set(lines[0])
        for line in lines[1:]:
            res.difference_update(set(line))
        return sorted(symbol for symbol in res if symbol.isalpha())
    if num_action == 5:
        lines = lines[::-1]
        res = set(lines[0])
        for line in lines[1:]:
            res.difference_update(set(line))
        return sorted(symbol for symbol in res if symbol.isalpha())
    if num_action == 6:
        res = set(lines[0])
        for line in lines:
            res.intersection_update(set(line))
        return sorted(symbol for symbol in res if symbol in punctuation)
    if num_action == 7:
        res = set()
        for line in lines[:-1]:
            res.update(set(line))
        return sorted(symbol for symbol in res.difference(set(lines[-1])) if symbol in punctuation)
    if num_action == 8:
        res = set(lines[0])
        for line in lines[1:]:
            res.difference_update(set(line))
        return sorted(symbol for symbol in res if symbol in punctuation)
    if num_action == 9:
        res = set(lines[0])
        for line in lines:
            res.intersection_update(set(line))
        return sorted(symbol for symbol in res if symbol.isdigit())
    if num_action == 10:
        res = set(lines[0])
        for line in lines:
            res.difference_update(set(line))
        return sorted(symbol for symbol in res if symbol.isdigit())
    if num_action == 11:
        res = []
        for line in lines:
            uppercase_l = set(char.lower() for char in line if char.isaplha() and char.isupper())
            lowercase_l = set(char for char in line if char.isaplha() and char.islower())
            res.append(sorted(uppercase_l.difference(lowercase_l)))
        return res
    if num_action == 12:
        res = []
        for line in lines:
            uppercase_l = set(char.lower() for char in line if char.isaplha() and char.isupper())
            lowercase_l = set(char for char in line if char.isaplha() and char.islower())
            res.append(sorted(uppercase_l.intersection(lowercase_l)))
    if num_action == 13:
        res = []
        for line in lines:
            res.append(sorted(set(ascii_letters).difference(set(line))))
        return res
    if num_action == 14:
        res = []
        for line in lines:
            set_symbol = set()
            for symbol in line:
                if symbol.isalpha() and symbol not in set_symbol:
                    set_symbol.update(symbol)
                elif symbol.isalpha() and symbol in set_symbol:
                    set_symbol.remove(symbol)
            res.append(sorted(set_symbol))
        return res
    if num_action == 15:
        res = []
        for line in lines:
            set_symbol = set()
            res_set_line = set()
            for symbol in line:
                if symbol.isalpha() and symbol not in set_symbol:
                    set_symbol.update(symbol)
                elif symbol.isalpha() and symbol in set_symbol:
                    set_symbol.remove(symbol)
                    res_set_line.update(symbol)
            res.append(sorted(res_set_line))
        return res
    if num_action == 16:
        res = []
        for line in lines:
            set_symbol = set()
            for symbol in line:
                if symbol in punctuation and symbol not in set_symbol:
                    set_symbol.update(symbol)
                elif symbol in punctuation and symbol in set_symbol:
                    set_symbol.remove(symbol)
            res.append(sorted(set_symbol))
        return res
    if num_action == 17:
        res = []
        for line in lines:
            set_symbol = set()
            res_set_line = set()
            for symbol in line:
                if symbol in punctuation and symbol not in set_symbol:
                    set_symbol.update(symbol)
                elif symbol in punctuation and symbol in set_symbol:
                    set_symbol.remove(symbol)
                    res_set_line.update(symbol)
            res.append(sorted(res_set_line))
        return res
    if num_action == 18:
        res = []
        for line in lines:
            set_symbol = set()
            for symbol in line:
                if symbol.isdigit() and symbol not in set_symbol:
                    set_symbol.update(symbol)
                elif symbol.isdigit() and symbol in set_symbol:
                    set_symbol.remove(symbol)
            res.append(sorted(set_symbol))
        return res
    if num_action == 19:
        res = []
        for line in lines:
            set_symbol = set()
            res_set_line = set()
            for symbol in line:
                if symbol.isdigit() and symbol not in set_symbol:
                    set_symbol.update(symbol)
                elif symbol.isdigit() and symbol in set_symbol:
                    set_symbol.remove(symbol)
                    res_set_line.update(symbol)
            res.append(sorted(res_set_line))
        return res
    if num_action == 20:
        res = []
        for line in lines:
            set_symbol = set()
            res_twice = set()
            set_more_twice = set()
            for symbol in line:
                if symbol in set_more_twice:
                    continue
                if symbol in res_twice:
                    res_twice.remove(symbol)
                    set_more_twice.update(symbol)
                elif symbol in set_symbol:
                    set_symbol.remove(symbol)
                    res_twice.update(symbol)
                else:
                    set_symbol.update(symbol)
            res.append(sorted(res_twice))
        return res


while True:
    print('''Список действий:
1.  Найти буквы, встречающиеся в каждой строке.
2.  Найти буквы, не встречающиеся ни в одной из строк.
3.  Найти буквы, встречающиеся только в прописном варианте.
4.  Найти буквы первой строки, не встречающиеся в остальных строках.
5.  Найти буквы последней строки, не встречающиеся в остальных строках.
6.  Найти знаки препинания, встречающиеся в каждой строке.
7.  Найти такие из знаков препинания, имеющихся в данных строках, которые не встречаются в последней строке.
8.  Найти такие знаки препинания, которые встречаются только в первой строке.
9.  Найти цифры, встречающиеся в каждой строке.
10. Найти цифры, встречающиеся только в первой строке.
11. Для каждой строки вывести те буквы, которые встречаются в виде прописных, но не встречаются в виде строчных.
12. Для каждой строки вывести те буквы, которые встречаются и в виде прописных, и в виде строчных.
13. Для каждой строки вывести буквы, которых в строке нет.
14. Для каждой строки вывести буквы, которые встречаются ровно один раз.
15. Для каждой строки вывести буквы, которые встречаются не менее двух раз.
16. Для каждой строки вывести знаки препинания, которые встречаются ровно один раз.
17. Для каждой строки вывести знаки препинания, которые встречаются не менее двух раз.
18. Для каждой строки вывести цифры, которые встречаются ровно один раз.
19. Для каждой строки вывести цифры, которые встречаются не менее двух раз.
20. Для каждой строки вывести все символы, которые встречаются ровно два раза.
21. Завершить работу.''')

    action = int(input('Выберите действие (1-21): '))
    if 1 <= action <= 20:
        print('Ваши строки: ')
        print('\n'.join(s))
        print('Результат действия: ', end='')
        result = actions(s, action)
        print(*result)
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
