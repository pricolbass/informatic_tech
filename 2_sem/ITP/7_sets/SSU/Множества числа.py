import random

while True:
    with open('input.txt', 'r', encoding='utf-8') as file:
        if file.readlines():
            break
        else:
            question_head = input('Вы хотите сами записать числа (да/нет)? ')
            with open('input.txt', 'a', encoding='utf-8') as file:
                if question_head.lower() == 'да':
                    print('Если хотите прекратить ввод строк, то напишите "stop"')
                    nums = input('Введите числа через пробел (их должно быть от 0 до 100): ')
                    while nums != 'stop':
                        file.write(nums + '\n')
                        nums = input('Введите числа через пробел (их должно быть от 0 до 100): ')
                    break
                elif question_head.lower() == 'нет':
                    max_lines = int(input('Введите максимальное число строк, которое может быть: '))
                    max_num = int(input('Введите максимальное число, которое может быть в строке: '))
                    for _ in range(random.randint(1, max_lines)):
                        nums_count = random.randint(0, 100)
                        nums = [str(random.randint(0, max_num)) for _ in range(nums_count)]
                        file.write(" ".join(nums) + "\n")
                    break
                else:
                    print('Вы ввели что-то кроме "да" и "нет".')


def actions(lines: list, action_number: int):
    numbers_list = []
    for line in lines:
        if line.strip():
            numbers = [int(num) for num in line.split()]
            numbers_list.append(numbers)
        else:
            numbers_list.append([])

    def find_unique_in_line(index):
        target_line_set = set(numbers_list[index])
        other_lines_set = set().union(*[set(line) for i, line in enumerate(numbers_list) if i != index])
        return list(target_line_set - other_lines_set)

    def find_not_in_line_but_others(index):
        target_line_set = set(numbers_list[index])
        other_lines_set = set().union(*[set(line) for i, line in enumerate(numbers_list) if i != index])
        return list(other_lines_set - target_line_set)

    def find_in_all(target_lines):
        return list(set.intersection(*[set(line) for line in target_lines]))

    def find_unique_in_condition(condition_func):
        target_lines_set = set().union(*[set(line) for line in numbers_list if condition_func(line)])
        other_lines_set = set().union(*[set(line) for line in numbers_list if not condition_func(line)])
        return list(target_lines_set - other_lines_set)

    def find_in_pairs(func):
        results = []
        for a, b in zip(numbers_list, numbers_list[1:]):
            results.append(func(a, b))
        return results

    def unique_in_first_line():
        return sorted(find_unique_in_line(0))

    def unique_in_kth_line():
        k = int(input('Введите число "k": '))
        return sorted(find_unique_in_line(k - 1))

    def not_in_first_but_in_others():
        return sorted(find_not_in_line_but_others(0))

    def not_in_last_but_in_others():
        return sorted(find_not_in_line_but_others(len(numbers_list) - 1))

    def unique_in_first_half():
        half_index = len(numbers_list) // 2
        return sorted(list(set().union(find_in_all(numbers_list[:half_index])) - set().union(find_in_all(numbers_list[half_index:]))))

    def unique_in_even_lines():
        return sorted(find_unique_in_condition(lambda line: numbers_list.index(line) % 2 == 1))

    def unique_in_lines_starting_with_zero():
        return sorted(find_unique_in_condition(lambda line: line[0] == 0 if line else False))

    def not_in_short_but_in_others():
        k = int(input('Введите число "k": '))
        return sorted(find_unique_in_condition(lambda line: len(line) >= k))

    def in_all_lines():
        return sorted(find_in_all(numbers_list))

    def in_all_even_lines():
        even_lines = [line for i, line in enumerate(numbers_list) if i % 2 == 1]
        return sorted(find_in_all(even_lines))

    def find_unique_numbers_in_lines():
        distinct_numbers = []
        for line in numbers_list:
            unique_numbers = set()
            for num in line:
                if num in unique_numbers:
                    unique_numbers.remove(num)
                else:
                    unique_numbers.add(num)
            distinct_numbers.append(unique_numbers)
        return distinct_numbers

    def numbers_in_both_consecutive_lines():
        return find_in_pairs(lambda a, b: list(set(a).intersection(set(b))))

    def numbers_unique_in_consecutive_lines():
        return find_in_pairs(lambda a, b: list(set(a) ^ set(b)))

    def numbers_only_in_first_of_consecutive_lines():
        return find_in_pairs(lambda a, b: list(set(a) - set(b)))

    def numbers_in_both_once():
        return find_in_pairs(lambda a, b: [x for x in set(a).intersection(set(b)) if a.count(x) == 1 and b.count(x) == 1])

    def numbers_once_in_first_not_in_second():
        return find_in_pairs(lambda a, b: [x for x in set(a) if a.count(x) == 1 and x not in set(b)])

    def numbers_odd_in_second_not_in_first():
        return find_in_pairs(lambda a, b: [x for x in set(b) if b.count(x) % 2 != 0 and x not in set(a)])

    def numbers_even_in_both_lines():
        return find_in_pairs(lambda a, b: [x for x in set(a).intersection(set(b)) if a.count(x) % 2 == 0 and b.count(x) % 2 == 0])

    def numbers_not_in_first_even_in_second():
        return find_in_pairs(lambda a, b: [x for x in set(b) - set(a) if b.count(x) % 2 == 0])

    def numbers_in_both_once_reverse():
        result = []
        n = len(numbers_list)
        for i in range(n // 2):
            a, b = numbers_list[i], numbers_list[-(i + 1)]
            common_once = [x for x in set(a).intersection(set(b)) if a.count(x) == 1 and b.count(x) == 1]
            print(a, b)
            result.append(common_once)

        if n % 2 != 0:
            middle = numbers_list[n // 2]
            unique_in_middle = [x for x in set(middle) if middle.count(x) == 1]
            result.append(unique_in_middle)
        return result
    actions_dict = {
        1: unique_in_first_line,
        2: unique_in_kth_line,
        3: not_in_first_but_in_others,
        4: not_in_last_but_in_others,
        5: unique_in_first_half,
        6: unique_in_even_lines,
        7: unique_in_lines_starting_with_zero,
        8: not_in_short_but_in_others,
        9: in_all_lines,
        10: in_all_even_lines,
        11: find_unique_numbers_in_lines,
        12: numbers_in_both_consecutive_lines,
        13: numbers_unique_in_consecutive_lines,
        14: numbers_only_in_first_of_consecutive_lines,
        15: numbers_in_both_once,
        16: numbers_once_in_first_not_in_second,
        17: numbers_odd_in_second_not_in_first,
        18: numbers_even_in_both_lines,
        19: numbers_not_in_first_even_in_second,
        20: numbers_in_both_once_reverse,
    }

    return actions_dict[action_number]()


while True:
    print('''Список действий:
1.  Найти числа, которые встречаются только в первой строке.
2.  Найти числа, которые встречаются только в k-й строке.
3.  Найти числа, которые не встречаются в первой строке, но есть хотя бы в одной из остальных.
4.  Найти числа, которые не встречаются в последней строке, но есть хотя бы в одной из остальных.
5.  Найти числа, которые встречаются только в первой половине строк.
6.  Найти числа, которые встречаются только в чётных строках.
7.  Найти числа, которые встречаются только в строках, начинающихся с нуля.
8.  Найти числа, которые не встречаются в строках, в которых менее k чисел, но встречаются в других.
9.  Найти числа, которые встречаются во всех строках.
10. Найти числа, которые встречаются во всех чётных строках.
11. Для каждой строки найти все различные числа в ней.
12. Для каждой пары подряд идущих строк найти числа, которые встречаются в обеих.
13. Для каждой пары подряд идущих строк найти числа, которые встречаются только в одной.
14. Для каждой пары подряд идущих строк найти числа, которые встречаются только в первой, но не встречаются во второй.
15. Для каждой пары подряд идущих строк найти числа, которые встречаются в обеих ровно по одному разу.
16. Для каждой пары подряд идущих строк найти числа, которые встречаются в первой ровно один раз и не встречаются во второй.
17. Для каждой пары подряд идущих строк найти числа, которые встречаются во второй нечётное число раз и не встречаются в первой.
18. Для каждой пары подряд идущих строк найти числа, которые встречаются в обеих строках чётное число раз.
19. Для каждой пары подряд идущих строк найти числа, которые не встречаются в первой строке, а во второй встречаются чётное число раз.
20. Для каждой пары из i-й с конца и i-й c начала строки найти числа, которые встречаются в обеих ровно по одному разу.
21. Завершить работу.''')

    action = int(input('Выберите действие (1-21): '))
    if 1 <= action <= 20:
        with open('input.txt', 'r', encoding='utf-8') as file:
            all_numbers = [line for line in file.readlines()]
        print(*actions(all_numbers, action))
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

with open("input.txt", "w") as file:
    file.write("")
