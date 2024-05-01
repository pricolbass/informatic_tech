num_data = list(map(int, input('Введите числа через пробел: ').split()))


def actions(data: list, action_number: int, N=None, digit=None):
    def partition(arr, low, high, key):
        pivot = key(arr[high])
        i = low - 1
        for j in range(low, high):
            if key(arr[j]) <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort(arr, low, high, key=lambda x: x):
        if low < high:
            pi = partition(arr, low, high, key)
            quick_sort(arr, low, pi - 1, key)
            quick_sort(arr, pi + 1, high, key)
        return arr

    def pushdown(arr, n, i, key):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and key(arr[left]) > key(arr[largest]):
            largest = left
        if right < n and key(arr[right]) > key(arr[largest]):
            largest = right
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            pushdown(arr, n, largest, key)

    def heap_sort(arr, key=lambda x: x):
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            pushdown(arr, n, i, key)
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            pushdown(arr, i, 0, key)
        return arr

    def merge(arr, left, mid, right, key):
        n1 = mid - left + 1
        n2 = right - mid
        L = [arr[left + i] for i in range(n1)]
        R = [arr[mid + 1 + j] for j in range(n2)]

        i = j = 0
        k = left

        while i < n1 and j < n2:
            if key(L[i]) <= key(R[j]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    def merge_sort(arr, left, right, key=lambda x: x):
        if left < right:
            mid = (left + right) // 2
            merge_sort(arr, left, mid, key)
            merge_sort(arr, mid + 1, right, key)
            merge(arr, left, mid, right, key)
        return arr

    def mirror_number(x):
        is_negative = x < 0
        s = str(abs(x))
        reversed_number = int(s[::-1])
        return -reversed_number if is_negative else reversed_number

    def sum_digits_except_first_and_hundreds(x):
        x = abs(x)
        digits = list(map(int, str(x)))
        if len(digits) > 3:
            hundreds_digit = digits[-3]
        else:
            hundreds_digit = 0
        first_digit = digits[0]
        return sum(digits) - first_digit - hundreds_digit

    actions_dict = {
        1: (quick_sort(data.copy(), 0, len(data) - 1, key=abs), heap_sort(data.copy(), key=abs),
            merge_sort(data.copy(), 0, len(data) - 1, key=abs), sorted(data, key=abs)),
        2: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: -len(str(abs(x)))),
            heap_sort(data.copy(), key=lambda x: -len(str(abs(x)))),
            merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: -len(str(abs(x)))),
            sorted(data, key=lambda x: -len(str(abs(x))))),

        3: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: x % 11),
            heap_sort(data.copy(), key=lambda x: x % 11),
            merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: x % 11),
            sorted(data, key=lambda x: x % 11)),

        4: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: -(x % N)),
            heap_sort(data.copy(), key=lambda x: -(x % N)),
            merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: -(x % N)),
            sorted(data, key=lambda x: -(x % N))),

        5: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: int(str(abs(x))[-1])),
            heap_sort(data.copy(), key=lambda x: int(str(abs(x))[-1])),
            merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: int(str(abs(x))[-1])),
            sorted(data, key=lambda x: int(str(abs(x))[-1]))),

        6: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: -str(x).count('3')),
            heap_sort(data.copy(), key=lambda x: -str(x).count('3')),
            merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: -str(x).count('3')),
            sorted(data, key=lambda x: -str(x).count('3'))),

        7: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: str(x).count(str(digit))),
            heap_sort(data.copy(), key=lambda x: str(x).count(str(digit))),
            merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: str(x).count(str(digit))),
            sorted(data, key=lambda x: str(x).count(str(digit)))),

        8: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: -sum(map(int, str(abs(x))))),
            heap_sort(data.copy(), key=lambda x: -sum(map(int, str(abs(x))))),
            merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: -sum(map(int, str(abs(x))))),
            sorted(data, key=lambda x: -sum(map(int, str(abs(x)))))),

        9: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: max(map(int, str(abs(x))))),
            heap_sort(data.copy(), key=lambda x: max(map(int, str(abs(x))))),
            merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: max(map(int, str(abs(x))))),
            sorted(data, key=lambda x: max(map(int, str(abs(x)))))),

        10: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: -min(map(int, str(abs(x))))),
             heap_sort(data.copy(), key=lambda x: -min(map(int, str(abs(x))))),
             merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: -min(map(int, str(abs(x))))),
             sorted(data, key=lambda x: -min(map(int, str(abs(x)))))),
        11: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: int(str(abs(x))[:2])),
             heap_sort(data.copy(), key=lambda x: int(str(abs(x))[:2])),
             merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: int(str(abs(x))[:2])),
             sorted(data, key=lambda x: int(str(abs(x))[:2]))),

        12: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: -int(str(abs(x))[-2:])),
             heap_sort(data.copy(), key=lambda x: -int(str(abs(x))[-2:])),
             merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: -int(str(abs(x))[-2:])),
             sorted(data, key=lambda x: -int(str(abs(x))[-2:]))),

        13: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: int(str(abs(x))[1:-1]) if len(str(abs(x))) > 2 else 0),
             heap_sort(data.copy(), key=lambda x: int(str(abs(x))[1:-1]) if len(str(abs(x))) > 2 else 0),
             merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: int(str(abs(x))[1:-1]) if len(str(abs(x))) > 2 else 0),
             sorted(data, key=lambda x: int(str(abs(x))[1:-1]) if len(str(abs(x))) > 2 else 0)),

        14: (
            quick_sort(data.copy(), 0, len(data) - 1,
                       key=lambda x: -(max(map(int, str(abs(x)))) + min(map(int, str(abs(x)))))),
            heap_sort(data.copy(), key=lambda x: -(max(map(int, str(abs(x)))) + min(map(int, str(abs(x)))))),
            merge_sort(data.copy(), 0, len(data) - 1,
                       key=lambda x: -(max(map(int, str(abs(x)))) + min(map(int, str(abs(x)))))),
            sorted(data, key=lambda x: -(max(map(int, str(abs(x)))) + min(map(int, str(abs(x))))))),

        15: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: sum(map(int, str(abs(x)))) / len(str(abs(x)))),
             heap_sort(data.copy(), key=lambda x: sum(map(int, str(abs(x)))) / len(str(abs(x)))),
             merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: sum(map(int, str(abs(x)))) / len(str(abs(x)))),
             sorted(data, key=lambda x: sum(map(int, str(abs(x)))) / len(str(abs(x))))),

        16: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: -int(str(abs(x))[0])),
             heap_sort(data.copy(), key=lambda x: -int(str(abs(x))[0])),
             merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: -int(str(abs(x))[0])),
             sorted(data, key=lambda x: -int(str(abs(x))[0]))),

        17: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: (int(str(abs(x))[0]) + int(str(abs(x))[-1])) / 2.0),
             heap_sort(data.copy(), key=lambda x: (int(str(abs(x))[0]) + int(str(abs(x))[-1])) / 2.0),
             merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: (int(str(abs(x))[0]) + int(str(abs(x))[-1])) / 2.0),
             sorted(data, key=lambda x: (int(str(abs(x))[0]) + int(str(abs(x))[-1])) / 2.0)),

        18: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: -sum(map(int, str(abs(x))[:-1]))),
             heap_sort(data.copy(), key=lambda x: -sum(map(int, str(abs(x))[:-1]))),
             merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: -sum(map(int, str(abs(x))[:-1]))),
             sorted(data, key=lambda x: -sum(map(int, str(abs(x))[:-1])))),

        19: (quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: sum_digits_except_first_and_hundreds(x)),
             heap_sort(data.copy(), key=lambda x: sum_digits_except_first_and_hundreds(x)),
             merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: sum_digits_except_first_and_hundreds(x)),
             sorted(data, key=lambda x: sum_digits_except_first_and_hundreds(x))),

        20: (
            quick_sort(data.copy(), 0, len(data) - 1, key=lambda x: -mirror_number(x)),
            heap_sort(data.copy(), key=lambda x: -mirror_number(x)),
            merge_sort(data.copy(), 0, len(data) - 1, key=lambda x: -mirror_number(x)),
            sorted(data, key=lambda x: -mirror_number(x))
        )

    }

    res = actions_dict[action_number]
    print(f'Быстрая сортировка: {res[0]}\nПирамидальная сортировка: {res[1]}\nСортировка слиянием: {res[2]}'
          f'\nСортировка Python: {res[3]}')


while True:
    print('''С помощью быстрой сортировки (qsort), пирамидальной сортировки (heapsort), сортировки слиянием (mergesort)
и встроенной сортировки Питона (функции sorted или метода списков sort) — расположить набор чисел в порядке:
1. возрастания модулей чисел
2. убывания количества цифр в числах
3. возрастания остатков от деления чисел на 11
4. убывания остатков от деления чисел на N
5. возрастания младших (последних) цифр чисел
6. убывания количества троек в записи чисел
7. возрастания количества вхождений заданной цифры digit в записи чисел
8. убывания суммы цифр чисел
9. возрастания максимальной цифры в числах
10. убывания минимальной цифры в числах
11. возрастания чисел, образованных двумя первыми цифрами данных чисел
12. убывания чисел, образованных последними двумя цифрами данных чисел
13. возрастания чисел, получающихся отбрасыванием у данных чисел их первой и последней цифры
14. убывания суммы максимальной и минимальной цифр чисел
15. возрастания среднего арифметического цифр чисел
16. убывания старших (первых) цифр чисел
17. возрастания среднего арифметического первой и последней цифр чисел
18. убывания суммы цифр чисел, кроме разряда единиц
19. возрастания суммы цифр чисел, кроме старшего разряда и разряда сотен
20. убывания зеркальных отражений данных чисел
21. завершить работу.''')
    action = int(input('Выберите действие (1-21): '))
    if 1 <= action <= 20:
        print(f'Исходный список чисел: {num_data}')
        N, digit = -1, -1
        if action == 4:
            N = int(input('Введите N: '))
        elif action == 7:
            digit = int(input('Введите digit: '))
        actions(num_data, action, N, digit)
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
