numbers = input('Введите целые числа через пробел: ').split()


def actions(nums: list, num_action: int):
    if num_action == 1:
        nums = [num.strip('-') for num in nums]
        res = set(nums[0])
        for num in nums[1:]:
            res.intersection_update(set(num))
        return sorted(res)
    if num_action == 2:
        nums = [num.strip('-') for num in nums]
        res = {str(i) for i in range(0, 10)}
        for num in nums[1:]:
            res.difference_update(set(num))
        return sorted(res)
    if num_action == 3:
        nums = [num.strip('-') for num in nums]
        res = set()
        all_dig = set()
        for num in nums:
            if int(num) % 10 == 0:
                res.update(set(num))
            else:
                all_dig.update(set(num))
        return sorted(res.difference(all_dig))
    if num_action == 4:
        res = set()
        all_dig = set()
        for num in nums:
            if int(num) < 0:
                res.update(set(num))
            else:
                all_dig.update(set(num))
        return sorted({dig for dig in res.difference(all_dig) if dig.isdigit()})
    if num_action == 5:
        nums = [num.strip('-') for num in nums]
        res = set()
        all_dig = set()
        for num in nums:
            if 100 <= int(num) <= 999:
                res.update(set(num))
            else:
                all_dig.update(set(num))
        return sorted(res.difference(all_dig))
    if num_action == 6:
        nums = [num.strip('-') for num in nums]
        res = set()
        all_dig = set()
        for num in nums:
            if 10 <= int(num) <= 99:
                res.update(set(num))
            else:
                all_dig.update(set(num))
        return sorted(all_dig.difference(res))
    if num_action == 7:
        nums = [num.strip('-') for num in nums]
        res = set()
        dig_3 = set()
        for num in nums:
            if 10 <= int(num) <= 99:
                res.update(set(num))
            elif 100 <= int(num) <= 999:
                dig_3.update(set(num))
        return sorted(dig_3.difference(res))
    if num_action == 8:
        nums = [num.strip('-') for num in nums]
        res = set()
        dig_3 = set()
        for num in nums:
            if 10 <= int(num) <= 99:
                res.update(set(num))
            elif 100 <= int(num) <= 999:
                dig_3.update(set(num))
        return sorted(dig_3.intersection(res))
    if num_action == 9:
        nums = [num.strip('-') for num in nums]
        dig_2_3 = set()
        all_dig = set()
        for num in nums:
            if 10 <= int(num) <= 99 or 100 <= int(num) <= 999:
                dig_2_3.update(set(num))
            else:
                all_dig.update(set(num))
        return sorted(all_dig.difference(dig_2_3))
    if num_action == 10:
        nums = [num.strip('-') for num in nums]
        res = set(nums[0]) | set(nums[-1])
        all_dig = set()
        for i in range(1, len(nums) - 1):
            all_dig.update(set(nums[i]))
        return sorted(res.difference(all_dig))
    if num_action == 11:
        nums = [num.strip('-') for num in nums]
        res = []
        for i in range(len(nums)):
            odd_digs = set()
            for dig in nums[i]:
                if dig in odd_digs:
                    odd_digs.remove(dig)
                else:
                    odd_digs.add(dig)
            res.append(sorted({int(dig) for dig in odd_digs}))
        return res
    if num_action == 12:
        nums = [num.strip('-') for num in nums]
        res = []
        for i in range(len(nums)):
            odd_digs = set()
            for dig in nums[i]:
                if dig in odd_digs:
                    odd_digs.remove(dig)
                else:
                    odd_digs.add(dig)
            res.append(sorted({int(dig) for dig in set(nums[i]).difference(odd_digs)}))
        return res
    if num_action == 13:
        nums = [num.strip('-') for num in nums]
        res = []
        for num in nums:
            all_dig = {str(i) for i in range(0, 10)}
            res.append(sorted(int(dig) for dig in all_dig.difference(set(num))))
        return res
    if num_action == 14:
        nums = [num.strip('-') for num in nums]
        res = []
        digs = set()
        for num in nums:
            set_num = set(num)
            res.append(sorted(int(dig) for dig in set_num.difference(digs)))
            digs.update(set_num)
        return res
    if num_action == 15:
        nums = [num.strip('-') for num in nums]
        res = []
        for num1, num2 in zip(nums, nums[1:]):
            res.append([[int(num1), int(num2)], sorted(int(dig) for dig in set(num1).intersection(set(num2)))])
        return res
    if num_action == 16:
        nums = [num.strip('-') for num in nums]
        res = []
        all_digs = {str(i) for i in range(0, 10)}
        for num1, num2 in zip(nums, nums[1:]):
            res.append([[int(num1), int(num2)], sorted(int(dig) for dig in all_digs.difference(set(num1) | set(num2)))])
        return res
    if num_action == 17:
        nums = [num.strip('-') for num in nums]
        res = []
        all_digs = {str(i) for i in range(0, 10)}
        for num1, num2 in zip(nums, nums[1:]):
            res.append([[int(num1), int(num2)], sorted(int(dig) for dig in set(num1).intersection(all_digs.difference(set(num2))))])
        return res
    if num_action == 18:
        nums = [num.strip('-') for num in nums]
        res = []
        all_digs = {str(i) for i in range(0, 10)}
        for num1, num2 in zip(nums, nums[1:]):
            set1, set2 = set(num1), set(num2)
            res.append([[int(num1), int(num2)], [sorted(int(dig) for dig in set1.intersection(set2)),
                                                 sorted(int(dig) for dig in all_digs - set1 - set2)]])
        return res
    if num_action == 19:
        nums = [num.strip('-') for num in nums]
        res = []
        for num1, num2, num3 in zip(nums, nums[1:], nums[2:]):
            set1, set2, set3 = set(num1), set(num2), set(num3)
            union_set = set1.union(set2).union(set3)
            only_2_sets = [int(dig) for dig in union_set if sum(dig in s for s in [set1, set2, set3]) == 2]
            res.append([[int(num1), int(num2), int(num3)], sorted(only_2_sets)])
        return res
    if num_action == 20:
        nums = [num.strip('-') for num in nums]
        res = []
        for num1, num2, num3 in zip(nums, nums[1:], nums[2:]):
            set1, set2, set3 = set(num1), set(num2), set(num3)
            union_set = set1.union(set2).union(set3)
            intersection_set = set1.intersection(set2).intersection(set3)
            all_digs = {str(i) for i in range(0, 10)}
            res.append([[int(num1), int(num2), int(num3)], [sorted(int(dig) for dig in intersection_set),
                                                            sorted(int(dig) for dig in all_digs.difference(union_set))]])
        return res


while True:
    print('''Список действий:
1.  Найти все такие цифры, которые встречаются в записи каждого из чисел.
2.  Найти все такие цифры, которые не встречаются в записи этих чисел.
3.  Найти все такие цифры, которые встречаются только в кратных 10 числах.
4.  Найти все такие цифры, которые встречаются только в отрицательных числах.
5.  Найти все такие цифры, которые встречаются только в трёхзначных числах.
6.  Найти все такие цифры, которые не встречаются в двузначных числах.
7.  Найти все такие цифры, которые встречаются в двузначных, но не встречаются в трёхзначных числах.
8.  Найти все такие цифры, которые встречаются и в двузначных, и в трёхзначных числах.
9.  Найти все такие цифры, которые не встречаются ни в двузначных, ни в трёхзначных числах.
10. Найти все такие цифры, которые встречаются в первом и последнем числах, но не встречаются ни в одном из остальных.
11. Для каждого числа найти цифры, встречающиеся в его записи нечётное число раз (не используя прямой подсчёт и count).
12. Для каждого числа найти цифры, встречающиеся в его записи чётное число раз (не используя прямой подсчёт и count).
13. Для каждого числа найти цифры, не встречающиеся в его записи.
14. Для каждого числа найти такие его цифры, которые не встречаются в предыдущих числах.
15. Для каждой пары подряд идущих чисел найти общие цифры.
16. Для каждой пары подряд идущих чисел найти такие цифры, которые не встречаются ни в одном из них.
17. Для каждой пары подряд идущих чисел найти такие цифры, которые есть в первом числе, но отсутствуют во втором.
18. Для каждой пары подряд идущих чисел перечислить цифры, которые либо встречаются в обоих числах,  либо не встречаются ни в одном из них.
19. Для каждой тройки подряд идущих чисел определить цифры, которые встречаются ровно в двух из них.
20. Для каждой тройки подряд идущих чисел определить цифры, которые встречаются во всех трёх или не встречаются ни в одном их этих чисел.
21. Завершить работу.''')

    action = int(input('Выберите действие (1-21): '))
    if 1 <= action <= 20:
        print('Ваша последовательность чисел: ', end='')
        print(*numbers)
        print('Результат действия: ', end='')
        result = actions(numbers, action)
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
