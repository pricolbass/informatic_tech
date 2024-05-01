a = list(map(int, input('Введите через пробел числа:\n').split()))


# проверка всех цифр числа num на чётность
def all_even(num):
    for digit in str(abs(num)):
        if int(digit) % 2 != 0:
            return False
    return True


# проверка цифр числа num на нечётность
def all_not_even(num):
    for digit in str(abs(num)):
        if int(digit) % 2 == 0:
            return False
    return True


def main(b: list, n: int) -> list:
    if n == 1:
        max_elem = max(b)
        while max_elem in b:
            b.remove(max_elem)
        return b

    if n == 2:
        min_elem = min(b)
        while min_elem in b:
            b.remove(min_elem)
        return b

    if n == 3:
        max_elem, min_elem = max(b), min(b)
        if abs(max_elem) < abs(min_elem):
            max_elem = min_elem
        elif abs(max_elem) == abs(min_elem):
            while min_elem in b:
                b.remove(min_elem)

        while max_elem in b:
            b.remove(max_elem)
        return b

    if n == 4:
        min_elem = float('inf')
        for elem in b:
            if abs(elem) < min_elem:
                min_elem = elem

        if -min_elem in b:
            while -min_elem in b:
                b.remove(-min_elem)

        while min_elem in b:
            b.remove(min_elem)
        return b

    if n == 5:
        i = 0
        while i < len(b):
            if 10 <= b[i] <= 99:
                b.pop(i)
            else:
                i += 1
        return b

    if n == 6:
        i = 0
        while i < len(b):
            if abs(b[i]) < 50:
                b.pop(i)
            else:
                i += 1
        return b

    if n == 7:
        i = 0
        while i < len(b):
            if b[i] < 0 or b[i] % 2 == 0:
                b.pop(i)
            else:
                i += 1
        return b

    if n == 8:
        i = 0
        while i < len(b):
            if b[i] < 0 and b[i] % 2 != 0:
                b.pop(i)
            else:
                i += 1
        return b

    if n == 9:
        i = 0
        while i < len(b):
            if 100 <= b[i] <= 999 and b[i] % 2 == 0:
                b.pop(i)
            else:
                i += 1
        return b

    if n == 10:
        i = 0
        while i < len(b):
            if 100 <= b[i] <= 999 or b[i] % 2 != 0:
                b.pop(i)
            else:
                i += 1
        return b

    if n == 11:
        i = 0
        while i < len(b):
            if b[i] < 0 and abs(b[i]) % 10 == 9:
                b.pop(i)
            else:
                i += 1
        return b

    if n == 12:
        i = 0
        while i < len(b):
            if b[i] < 0 and str(b[i])[1] == '1':
                b.pop(i)
            else:
                i += 1
        return b

    if n == 13:
        i = 0
        while i < len(b):
            if 50 <= abs(b[i]) <= 150:
                b.pop(i)
            else:
                i += 1
        return b

    if n == 14:
        i = 0
        while i < len(b):
            if '2' in str(b[i]):
                b.pop(i)
            else:
                i += 1
        return b

    if n == 15:
        i = 0
        while i < len(b):
            if '5' not in str(b[i]):
                b.pop(i)
            else:
                i += 1
        return b

    if n == 16:
        max_elem1, max_elem2 = float('-inf'), float('-inf')
        for elem in b:
            if elem > max_elem1:
                max_elem1, max_elem2 = elem, max_elem1
            elif elem > max_elem2:
                max_elem2 = elem

        while max_elem1 in b:
            b.remove(max_elem1)
        while max_elem2 in b:
            b.remove(max_elem2)
        return b

    if n == 17:
        min_elem1, min_elem2 = float('inf'), float('inf')
        for elem in b:
            if elem < min_elem1:
                min_elem1, min_elem2 = elem, min_elem1
            elif elem < min_elem2:
                min_elem2 = elem

        while min_elem1 in b:
            b.remove(min_elem1)
        while min_elem2 in b:
            b.remove(min_elem2)
        return b

    if n == 18:
        max_elem1, max_elem2 = float('-inf'), float('-inf')
        for elem in b:
            if (max_elem1 != float('-inf') and abs(elem) > abs(max_elem1)) or (abs(elem) > max_elem1):
                max_elem1, max_elem2 = elem, max_elem1
            elif max_elem2 != float('-inf') and abs(elem) > abs(max_elem2) or abs(elem) > max_elem2:
                max_elem2 = elem

        while max_elem1 in b:
            b.remove(max_elem1)
        while max_elem2 in b:
            b.remove(max_elem2)

        if -max_elem1 in b:
            while -max_elem1 in b:
                b.remove(-max_elem1)
        if -max_elem2 in b:
            while -max_elem2 in b:
                b.remove(-max_elem2)
        return b

    if n == 19:
        i = 0
        while i < len(b):
            if all_even(b[i]):
                b.pop(i)
            else:
                i += 1
        return b

    if n == 20:
        i = 0
        while i < len(b):
            if all_not_even(b[i]):
                b.pop(i)
            else:
                i += 1
        return b


while True:
    print('''
Список действий:
1.  максимальные элементы.
2.  минимальные элементы.
3.  максимальные по модулю элементы.
4.  минимальные по модулю элементы.
5.  двузначные элементы.
6.  элементы, которые по модулю меньше 50.
7.  все отрицательные и все чётные элементы.
8.  нечётные и при этом отрицательные элементы.
9.  трёхзначные и при этом чётные элементы.
10. все трёхзначные и все нечётные элементы.
11. отрицательные элементы, заканчивающие на 9.
12. отрицательные элементы с 1 в качестве старшей цифры.
13. элементы, модуль которых в диапазоне от 50 до 150.
14. элементы, в записи которых есть цифра 2.
15. элементы, в записи которых нет цифры 5.
16. два наибольших значения со всеми повторами.
17. два наименьших значения со всеми повторами.
18. два наибольших по модулю значения со всеми повторами.
19. элементы, в записи которых все цифры чётные.
20. элементы, в записи которых нет чётных цифр.
21. остановить работу.
''')
    action = int(input('Выберите одно из действий (1-21): '))

    if 1 <= action <= 20:
        print(f'Введенные числа:', end=' ')
        print(*a)
        a = main(a, action)
        print('Результат: ', end='')
        print(*a)
    elif action == 21:
        break
    else:
        print('Такого действия нет.')
