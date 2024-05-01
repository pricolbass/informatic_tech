a = list(map(int, input('Введите целые числа через запятую:\n').split(',')))


# является ли число num степенью числа k
def is_power_(num, k):
    res = num
    while res % k == 0:
        res /= k

    return res == 1


# проверка на простоту
def is_prime(num):
    d = 2
    while d * d <= num and num % d != 0:
        d += 1
    return d * d > num > 1


# проверка на число Фибоначчи
def is_fib(num):
    f1, f2 = 0, 1
    while f1 < num:
        f1, f2 = f2, f1 + f2
    return num == f1


# проверка на одинаковые цифры в числе num
def not_same_nums(num):
    num_str = str(num)
    for i in range(len(num_str) - 1):
        if num_str[i] == num_str[i + 1]:
            return False
    return True


# являются ли цифры числа num строго возрастающими
def is_ascending(num):
    num_str = str(num)
    for i in range(len(num_str) - 1):
        if num_str[i] >= num_str[i + 1]:
            return False
    return True


# являются ли цифры числа num невозрастающими
def not_ascending(num):
    num_str = str(num)
    for i in range(len(num_str) - 1):
        if num_str[i] < num_str[i + 1]:
            return False
    return True


# являются ли цифры числа num строго убывающими
def is_decreasing(num):
    num_str = str(num)
    for i in range(len(num_str) - 1):
        if num_str[i] <= num_str[i + 1]:
            return False
    return True


# являются ли цифры числа num неубывающими
def not_decreasing(num):
    num_str = str(num)
    for i in range(len(num_str) - 1):
        if num_str[i] > num_str[i + 1]:
            return False
    return True


# произведение цифр числа num
def multiply_nums(num):
    num_str = str(num)
    res_ = 1
    for i in num_str:
        res_ *= int(i)
    return res_


# произведение ненулевых цифр числа num
def multiply_nums_not_0(num):
    num_str = str(num)
    res_ = 1
    for i in num_str:
        if i != '0':
            res_ *= int(i)
    return res_


def main(b: list, n: int):
    if n == 1:
        A = int(input('Введите начало отрезка для подсчёта количества: '))
        B = int(input('Введите конец отрезка для подсчёта количества: '))
        start = int(input('Введите номер с которого надо посчитать сумму: '))
        stop = int(input('Введите номер до которого надо посчитать сумму: '))

        return sum(1 for elem in b if A <= elem <= B and elem >= 0 and elem ** .5 == int(elem ** .5)), sum(
            elem for elem in b[start - 1:stop] if is_power_(elem, 3))

    if n == 2:
        start = int(input('Введите номер с которого надо посчитать количество: '))
        stop = int(input('Введите номер до которого надо посчитать количество: '))
        A = int(input('Введите начало отрезка для подсчёта суммы: '))
        B = int(input('Введите конец отрезка для подсчёта суммы: '))

        return sum(1 for elem in b[start - 1:stop] if is_prime(elem)), sum(
            elem for elem in b if A <= elem <= B if is_power_(elem, 2))

    if n == 3:
        A = int(input('Введите начало отрезка для подсчёта количества: '))
        B = int(input('Введите конец отрезка для подсчёта количества: '))
        start = int(input('Введите номер с которого надо посчитать сумму: '))
        stop = int(input('Введите номер до которого надо посчитать сумму: '))

        return sum(1 for elem in b if A <= elem <= B and elem % int(str(abs(elem))[0]) == 0), sum(
            elem for elem in b[start - 1:stop] if elem >= 0 and elem ** .5 == int(elem ** .5))

    if n == 4:
        start = int(input('Введите номер с которого надо посчитать количество: '))
        stop = int(input('Введите номер до которого надо посчитать количество: '))
        A = int(input('Введите начало отрезка для подсчёта суммы: '))
        B = int(input('Введите конец отрезка для подсчёта суммы: '))

        return sum(1 for elem in b[start - 1:stop] if elem % int(str(abs(elem))[0]) != 0), sum(
            elem for elem in b if A <= elem <= B and elem >= 4 and not is_prime(elem))

    if n == 5:
        A = int(input('Введите начало отрезка для подсчёта количества: '))
        B = int(input('Введите конец отрезка для подсчёта количества: '))
        start = int(input('Введите номер с которого надо посчитать сумму: '))
        stop = int(input('Введите номер до которого надо посчитать сумму: '))

        return sum(1 for elem in b if A <= abs(elem) <= B and is_prime(abs(elem))), sum(
            elem for elem in b[start - 1:stop] if is_power_(elem, 3))

    if n == 6:
        start = int(input('Введите номер с которого надо посчитать количество: '))
        stop = int(input('Введите номер до которого надо посчитать количество: '))
        A = int(input('Введите начало отрезка для подсчёта суммы: '))
        B = int(input('Введите конец отрезка для подсчёта суммы: '))

        return sum(1 for elem in b[start:stop:2] if is_power_(elem, 2)), sum(
            elem for elem in b if A <= abs(elem) <= B and abs(elem) ** .5 == int(abs(elem) ** .5))

    if n == 7:
        A = int(input('Введите начало отрезка для подсчёта количества: '))
        B = int(input('Введите конец отрезка для подсчёта количества: '))
        start = int(input('Введите номер с которого надо посчитать сумму: '))
        stop = int(input('Введите номер до которого надо посчитать сумму: '))

        return sum(1 for elem in b if A <= elem <= B and elem % int(str(abs(elem))[0]) != 0), sum(
            elem for elem in b[start:stop:2] if is_power_(abs(elem), 2))

    if n == 8:
        start = int(input('Введите номер с которого надо посчитать количество: '))
        stop = int(input('Введите номер до которого надо посчитать количество: '))
        A = int(input('Введите начало отрезка для подсчёта суммы: '))
        B = int(input('Введите конец отрезка для подсчёта суммы: '))

        return sum(1 for elem in b[start - 1:stop:2] if is_power_(abs(elem), 3)), sum(
            elem for elem in b if not (A <= elem <= B) and elem % int(str(abs(elem))[0]) == 0)

    if n == 9:
        start = int(input('Введите номер с которого надо посчитать количество: '))
        stop = int(input('Введите номер до которого надо посчитать количество: '))

        return sum(1 for elem in b if is_fib(elem)), sum(
            elem for elem in b[start - 1:stop:2] if elem >= 4 and not is_prime(elem))

    if n == 10:
        start = int(input('Введите номер с которого надо посчитать количество: '))
        A = int(input('Введите начало отрезка для подсчёта суммы: '))
        B = int(input('Введите конец отрезка для подсчёта суммы: '))

        return sum(1 for elem in b[start - 1:] if is_fib(abs(elem))), sum(
            elem for elem in b if not (A <= elem <= B) and elem >= 0 and elem ** .5 == int(elem ** .5))

    if n == 11:
        stop = int(input('Введите номер до которого надо посчитать сумму: '))

        return sum(1 for elem in b if not_same_nums(elem)), sum(elem for elem in b[:stop] if is_prime(elem))

    if n == 12:
        start = int(input('Введите номер с которого надо посчитать количество: '))

        return sum(
            1 for i, elem in enumerate(b) if i % 2 != 0 and i >= start - 1 and elem >= 4 and not (is_prime(elem))), sum(
            elem for elem in b if is_ascending(elem))

    if n == 13:
        A = int(input('Введите начало отрезка для подсчёта количества: '))
        B = int(input('Введите конец отрезка для подсчёта количества: '))
        stop = int(input('Введите номер до которого надо посчитать сумму: '))

        return sum(1 for elem in b if not (A <= elem <= B) and is_power_(elem, 2)), sum(
            elem for elem in b[:stop:2] if not_ascending(elem))

    if n == 14:
        start = int(input('Введите номер с которого надо посчитать количество: '))
        stop = int(input('Введите номер до которого надо посчитать количество: '))

        return sum(1 for elem in b[start - 1:stop] if not_decreasing(elem)), sum(
            elem for elem in b if '3' in str(elem) and is_power_(elem, 3))

    if n == 15:
        A = int(input('Введите начало отрезка для подсчёта количества: '))
        B = int(input('Введите конец отрезка для подсчёта количества: '))
        start = int(input('Введите номер с которого надо посчитать сумму: '))
        stop = int(input('Введите номер до которого надо посчитать сумму: '))

        return sum(1 for elem in b if A <= elem <= B and elem >= 4 and not (is_prime(elem))), sum(
            elem for elem in b[start - 1:stop] if is_decreasing(elem))

    if n == 16:
        start = int(input('Введите номер с которого надо посчитать количество: '))
        stop = int(input('Введите номер до которого надо посчитать количество: '))
        A = int(input('Введите начало отрезка для подсчёта суммы: '))
        B = int(input('Введите конец отрезка для подсчёта суммы: '))

        return sum(1 for elem in b[start - 1:stop] if is_fib(elem)), sum(
            elem for elem in b if A <= elem <= B and elem ** .5 == int(elem ** .5))

    if n == 17:
        res = [elem for elem in b[2::3] if is_power_(sum(int(j) for j in str(elem)), 2)]

        if len(res) == 0:
            print(f'Таких элементов в списке введенных чисел {b} нет')
            return None
        else:
            return sum(res) / len(res)

    if n == 18:
        A = int(input('Введите начало отрезка для подсчёта среднего арифметического: '))
        B = int(input('Введите конец отрезка для подсчёта среднего арифметического: '))
        res = [elem for elem in b[2::3] if not (A <= multiply_nums(elem) <= B)]

        if len(res) == 0:
            print(f'Таких элементов в списке введенных чисел {b} нет')
            return None
        else:
            return sum(res) / len(res)

    if n == 19:
        res = [elem for i, elem in enumerate(b) if (i + 1) % 3 != 0 and is_prime(sum(abs(int(j)) for j in str(elem)))]

        if len(res) == 0:
            print(f'Таких элементов в списке введенных чисел {b} нет')
            return None
        else:
            return sum(res) / len(res)

    if n == 20:
        res = [elem for i, elem in enumerate(b) if
               (i + 1) % 3 != 0 and multiply_nums_not_0(elem) % sum(int(j) for j in str(elem)) == 0]

        if len(res) == 0:
            print(f'Таких элементов в списке введенных чисел {b} нет')
            return None
        else:
            return sum(res) / len(res)


while True:
    print('''
Список действий:
1.  Подсчитать количество чисел из этого набора, принадлежащих отрезку [A, B] и являющихся полными квадратами. А также сумму элементов с номерами от start до stop, которые представляют собой степени тройки.
2.  Подсчитать количество элементов с номерами от start до stop, являющихся простыми числами. А также сумму чисел из этого набора, принадлежащих заданному отрезку [A, B] и представляющих собой степени двойки.
3.  Подсчитать количество чисел из этого набора, которые принадлежат заданному отрезку [A, B] и делятся нацело на свою старшую цифру. А также сумму элементов с номерами от start до stop, являющихся полными квадратами.
4.  Подсчитать количество элементов с номерами от start до stop, которые не делятся на свою старшую цифру. А также сумму составных чисел среди элементов этого набора, принадлежащих заданному отрезку [A, B].
5.  Подсчитать количество чисел из этого набора, модули которых принадлежат отрезку [A, B] и являются простыми числами. А также сумму элементов с номерами от start до stop, представляющих собой степени тройки.
6.  Подсчитать количество элементов с чётными номерами от start до stop, представляющих собой степени двойки. А также сумму чисел из этого набора, модули которых принадлежат отрезку [A, B] и являются полными квадратами.
7.  Подсчитать количество чисел из этого набора, которые принадлежат заданному отрезку [A, B] и не делятся на свою старшую цифру. А также сумму элементов с чётными номерами от start до stop, модули которых являются степенями двойки.
8.  Подсчитать количество элементов с нечётными номерами от start до stop, модули которых являются степенями тройки. А также сумму чисел из этого набора, которые кратны своим старшим цифрам и не принадлежат отрезку [A, B].
9.  Подсчитать количество чисел Фибоначчи в данном наборе. А также сумму составных чисел среди элементов с нечётными номерами от start до stop.
10. Подсчитать количество чисел Фибоначчи и противоположных им среди элементов с номерами не меньше start. А также сумму чисел из этого набора, которые являются полными квадратами и не принадлежат заданному отрезку [A, B].
11. Подсчитать количество чисел из этого набора, в записи которых нет подряд идущих одинаковых цифр. А также сумму простых чисел среди элементов с номерами меньшими stop.
12. Подсчитать количество составных чисел среди элементов с чётными номерами, начиная со start. А также сумму чисел из этого набора, цифры в записи которых расположены строго по возрастанию.
13. Подсчитать количество степеней двойки среди чисел из этого набора, не принадлежащих отрезку [A, B]. А также сумму элементов с нечётными номерами до stop, цифры в записи которых расположены в порядке невозрастания.
14. Подсчитать количество элементов с номерами от start до stop, цифры в записи которых расположены в порядке неубывания. А также сумму степеней тройки среди чисел этого набора, в записи которых есть цифра три.
15. Подсчитать количество составных чисел из заданного отрезка [A, B] и сумму элементов с номерами от start до stop, цифры в записи которых расположены строго по убыванию.
16. Подсчитать количество чисел с номерами от start до stop, являющихся числами Фибоначчи. А также сумму элементов из заданного отрезка [A, B], представляющих собой полные квадраты.
17. Подсчитать среднее арифметическое элементов с кратными трём номерами, сумма цифр которых является степенью двойки.
18. Подсчитать среднее арифметическое элементов с кратными трём номерами, произведение цифр которых не принадлежит заданному отрезку [A, B].
19. Подсчитать среднее арифметическое элементов с не кратными трём номерами, сумма цифр которых является простым числом.
20. Подсчитать среднее арифметическое элементов с не кратными трём номерами, произведение ненулевых цифр которых кратно их же сумме цифр.
21. Остановить работу.
''')
    action = int(input('Выберите одно из действий (1-21): '))

    if 1 <= action <= 20:
        print(f'Введенные числа и номера соответствующих им номеров:\n{a}\n{[j+1 for j in range(len(a))]}')
        res_main = main(a, action)
        if type(res_main) == tuple:
            print(res_main[0], res_main[1])
        else:
            print(res_main)
    elif action == 21:
        break
    else:
        print('Такого действия нет.')
