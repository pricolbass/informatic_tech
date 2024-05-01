from keyword import kwlist, iskeyword
from string import punctuation


def show_string(s: str) -> None:
    if s:
        print(f'"{current_string}" ({len(current_string)})')
    else:
        print("Строка пуста")


def modify_string(s: str) -> str:
    print('''Cписок действий:
1)  перевести текст в верхний регистр и дописать в конец строки её первую букву
2)  перевести текст в нижний регистр и дописать в начало строки её последнюю букву
3)  сделать первую букву текста заглавной, остальные строчными и дописать в начало и конец строки заданную букву
4)  сделать заглавной первую букву каждого слова, остальные строчными и убрать все вхождения подстроки 'не'
5)  инвертировать регистр всех букв и удвоить строку (записать её два раза подряд)
6)  убрать все вхождения заданной подстроки и записать все символы строки через подчёркивание
7)  заменить все вхождения 'да' на 'нет' и вставить пробел между каждой парой символов строки
8)  убрать все пробельные символы из начала строки и заменить все вхождения заданной подстроки звёздочками
9)  убрать все пробельные символы из конца строки и дописать восклицательный знак, если длина строки стала нечётной
10) заменить первое вхождение заданной подстроки на другую и дополнить строку спереди нулями до заданной длины
11) заменить первое вхождение заданной подстроки на другую и дополнить слева до заданной длины определённым символом
12) убрать первое вхождение заданной подстроки и выровнять строку посередине заданной длины, дополнив подчёркиваниями
13) повторить строку n раз и дополнить справа до заданной длины определённым символом
14) вставить '(!)' после каждого вхождения заданной подстроки и дописать в начало строки её предпоследнюю букву
15) вставить '?' перед каждым вхождением заданной подстроки и инвертировать регистр всех букв
16) взять в квадратные скобки все вхождения заданной подстроки и убрать все пробельные символы в начале и в конце строки
17) перевести текст в верхний регистр и убрать первое вхождение заданной подстроки
18) поменять местами первую и последнюю буквы строки и повторить строку n раз
19) сделать заглавной первую букву каждого слова, остальные строчными и взять в круглые скобки все вхождения заданной подстроки
20) заменить первое вхождение заданной подстроки на такое же количество звёздочек, а все остальные вхождения удалить, после этого инвертировать регистр всех букв''')

    choice_modif = int(input("Выберите действие (1-20): "))

    if choice_modif == 1:
        s = s.upper()
        return s + s[0]

    elif choice_modif == 2:
        s = s.lower()
        return s[-1] + s

    elif choice_modif == 3:
        a = input('Введите любую букву: ')
        return a + s.capitalize() + a

    elif choice_modif == 4:
        s = s.title()
        if 'не' in s:
            return ''.join(s.split('не')).strip()
        print(f'Подстроки "не" нет в строке "{s}"')
        return s

    elif choice_modif == 5:
        return s[::-1] * 2

    elif choice_modif == 6:
        a = input(f'Введите подстроку строки "{s}": ')
        if a in s:
            return '_'.join(list(''.join(s.split(a))))
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 7:
        if 'да' in s:
            s = s.replace('да', 'нет')
        else:
            print(f'Подстроки "да" нет в строке "{s}"')
        return ' '.join([s[i:i + 2] for i in range(0, len(s), 2)])

    elif choice_modif == 8:
        s = s.lstrip()
        a = input(f'Введите подстроку строки "{s}": ')
        if a in s:
            return s.replace(a, '*')
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 9:
        s = s.rstrip()
        if len(s) % 2 != 0:
            return s + '!'
        return s

    elif choice_modif == 10:
        a = input(f'Введите подстроку строки "{s}": ')
        if a in s:
            b = input(f'Введите строку на которую хотите заменить предыдущую подстроку "{a}" строки "{s}": ')
            s = s.replace(a, b, 1)
            l_s = int(input(f'Введите длину для будущей строки, длина текущей - {len(s)}: '))
            if len(s) < l_s:
                while len(s) < l_s:
                    s = '0' + s
                return s
            print(f'Длина, которую вы задали {l_s} меньше либо равна текущей длине {len(s)}')
            return s
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 11:
        a = input(f'Введите подстроку строки "{s}": ')
        if a in s:
            b = input(f'Введите строку на которую хотите заменить предыдущую подстроку "{a}" строки "{s}": ')
            l_s = int(input(f'Введите длину для будущей строки, длина текущей - {len(s)}: '))
            c = input('Введите символ: ')
            s = s.replace(a, b, 1)
            if len(s) < l_s:
                while len(s) < l_s:
                    s = c + s
                return s
            print(f'Длина, которую вы задали {l_s} меньше либо равна текущей длине {len(s)}')
            return s
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 12:
        a = input(f'Задайте подстроку строки "{s}": ')
        if a in s:
            s = ''.join(s.split(a, 1))
            l_s = int(input(f'Введите длину для будущей строки, длина текущей - {len(s)}: '))
            if len(s) < l_s:
                pad_length = l_s - len(s)
                pad_left = pad_length // 2
                pad_right = pad_length - pad_left
                return '_' * pad_left + s + '_' * pad_right
            print(f'Длина, которую вы задали {l_s} меньше либо равна текущей длине {len(s)}')
            return s
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 13:
        n = int(input(f'Сколько раз повторить строку "{s}": '))
        s *= n
        l_s = int(input(f'Введите длину для будущей строки, длина текущей - {len(s)}: '))
        a = input(f'Задайте подстроку строки "{s}": ')
        if len(s) < l_s:
            while len(s) < l_s:
                s += a
            return s
        print(f'Длина, которую вы задали {l_s} меньше либо равна текущей длине {len(s)}')
        return s

    elif choice_modif == 14:
        a = input(f'Задайте подстроку строки "{s}": ')
        if a in s:
            return s[-2] + s.replace(a, a + '(!)')
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 15:
        a = input(f'Задайте подстроку строки "{s}": ')
        if a in s:
            return s.replace(a, '?' + a)[::-1]
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 16:
        a = input(f'Задайте подстроку строки "{s}": ')
        s = s.strip()
        if a in s:
            return s.replace(a, '[' + a + ']')
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 17:
        s = s.upper()
        a = input(f'Задайте подстроку строки "{s}": ')
        if a in s:
            return ''.join(s.split(a, 1))
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 18:
        n = int(input(f'Сколько раз повторить строку "{s}": '))
        return (s[-1] + s[1:-1] + s[0]) * n

    elif choice_modif == 19:
        s = s.title()
        a = input(f'Задайте подстроку строки "{s}": ')
        if a in s:
            return s.replace(a, '(' + a + ')')
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    elif choice_modif == 20:
        a = input(f'Задайте подстроку строки "{s}": ')
        if a in s:
            return ''.join(s.replace(a, '*' * len(a), 1).split(a))[::-1]
        print(f'Подстроки "{a}" нет в строке "{s}"')
        return s

    else:
        print("Неверный выбор. Пожалуйста, выберите действие снова.")


def check_string(s: str) -> bool:
    print('''Cписок проверок:
1)  заканчивается ли строка заданной подстрокой
2)  встречается ли заданная подстрока в строке
3)  встречается ли заданная подстрока в строке без учёта регистра
4)  чётна ли длина строки
5)  совпадают ли первая и предпоследняя буквы строки
6)  совпадают ли вторая и последняя буквы строки
7)  совпадают ли первая и последняя буквы строки без учёта регистра
8)  встречается ли одна подстрока раньше другой
9)  встречается ли заданная подстрока больше одного раза
10) встречается ли заданная подстрока чётное количество раз
11) начинается ли строка с заданной подстроки
12) может ли строка быть логином: состоит только из букв и длина от 3 до 20
13) может ли строка быть логином: состоит только из букв и цифр и длина от 4 до 16
14) может ли строка быть паролем: длина не меньше введённого значения
15) может ли строка быть ID: состоит только из цифр и представляет собой шестизначное число
16) является ли строка ключевым словом Питона
17) может ли строка быть номером сотового телефона: 11 цифр, возможно, разделённых пробелами
18) может ли строка быть номером сотового телефона: 11 цифр, в начале может быть или не быть плюс
19) может ли строка быть адресом электронной почты: символ ‘@’ встречается ровно один раз, причём не в начале и не в конце строки
20) может ли строка быть адресом сайта: есть хотя бы одна точка, нет подряд идущих точек, начинается и заканчивается не точкой''')

    choice_check = int(input("Выберите действие (1-20): "))

    if choice_check == 1:
        a = input(f'Задайте подстроку строки "{s}": ')
        return s.endswith(a)

    elif choice_check == 2:
        a = input(f'Задайте подстроку строки "{s}": ')
        return a in s

    elif choice_check == 3:
        a = input(f'Задайте подстроку строки "{s}": ')
        return a.lower() in s.lower()

    elif choice_check == 4:
        return len(s) % 2 == 0

    elif choice_check == 5:
        return len(s) >= 2 and s[-2] == s[0]

    elif choice_check == 6:
        return len(s) >= 2 and s[1] == s[-1]

    elif choice_check == 7:
        s_ = s.lower()
        return len(s_) >= 1 and s_[0] == s_[-1]

    elif choice_check == 8:
        a = input(f'Задайте подстроку строки "{s}": ')
        b = input(f'Задайте еще одну подстроку строки "{s}": ')
        if a in s and b in s:
            return s.find(a) < s.find(b)
        else:
            print(f'Либо "{a}" либо "{b}" нет в строке {s}')
            return False

    elif choice_check == 9:
        a = input(f'Задайте подстроку строки "{s}": ')
        return s.count(a) > 1

    elif choice_check == 10:
        a = input(f'Задайте подстроку строки "{s}": ')
        return s.count(a) % 2 == 0

    elif choice_check == 11:
        a = input(f'Задайте подстроку строки "{s}": ')
        return s.startswith(a)

    elif choice_check == 12:
        return 3 <= len(s) <= 20 and s.isalpha()

    elif choice_check == 13:
        return 4 <= len(s) <= 16 and s.isalnum()

    elif choice_check == 14:
        l_s = int(input(f'Введите длину для проверки: '))
        return len(s) >= l_s

    elif choice_check == 15:
        return s.isdigit() and len(s) == 6

    elif choice_check == 16:
        return iskeyword(s)

    elif choice_check == 17:
        return all(x.isspace() or x.isdigit() for x in s) and len(''.join(s.split())) == 11

    elif choice_check == 18:
        return (s[0] == '+' and s[1:].isdigit() and len(s) == 12) or (len(s) == 11 and s.digit())

    elif choice_check == 19:
        return s.count('@') == 1 and not s.endswith('@') and not s.startswith('@')

    elif choice_check == 20:
        return s.count('.') >= 1 and '..' not in s and not s.startswith('.') and not s.endswith('.')

    else:
        print("Неверный выбор. Пожалуйста, выберите проверку снова.")


def count_string(s: str) -> int:
    print('''Список для счёта количества:
1)  гласных русских букв в текущей строке
2)  согласных русских букв в текущей строке
3)  прописных (заглавных) букв в текущей строке
4)  строчных букв в текущей строке
5)  цифр в текущей строке
6)  чётных цифр в текущей строке
7)  нечётных цифр в текущей строке
8)  пробельных символов в текущей строке
9)  непробельных символов в текущей строке
10) знаков препинания в текущей строке
11) букв и цифр в текущей строке
12) непробельных символов, не являющихся ни буквами, ни цифрами в текущей строке 
13) символов из набора ‘0oO1Il’ в текущей строке
14) символов не из набора ‘0oO1Il’ в текущей строке
15) символов текущей строки, присутствующих во введённой строке
16) символов текущей строки, не встречающихся во введённой строке
17) символов текущей строки, присутствующих во введённой строке, без учёта регистра
18) символов текущей строки, не встречающихся во введённой строке, без учёта регистра
19) различных символов из введённой строки, встречающихся в текущей строке
20) различных символов из введённой строки, встречающихся в текущей строке без учёта регистра''')

    choice_count = int(input("Выберите действие (1-20): "))

    if choice_count == 1:
        vowels = 'аеёиоуыэюя'
        return sum(1 for i in s if i in vowels)

    elif choice_count == 2:
        consonants = 'бвгджзйклмнпрстфхцчшщ'
        return sum(1 for i in s if i in consonants)

    elif choice_count == 3:
        return sum(1 for i in s if i.isupper())

    elif choice_count == 4:
        return sum(1 for i in s if i.islower())

    elif choice_count == 5:
        return sum(1 for i in s if i.isdigit())

    elif choice_count == 6:
        return sum(1 for i in s if i.isdigit() and int(i) % 2 == 0)

    elif choice_count == 7:
        return sum(1 for i in s if i.isdigit() and int(i) % 2 == 1)

    elif choice_count == 8:
        return s.count(' ')

    elif choice_count == 9:
        return len(s) - s.count(" ")

    elif choice_count == 10:
        return sum([1 for i in s if i in punctuation])

    elif choice_count == 11:
        return sum([1 for i in s if i.isalnum()])

    elif choice_count == 12:
        return sum([1 for i in s if not i.isspace() and not i.isalnum()])

    elif choice_count == 13:
        return sum([1 for i in s if i in '0oO1Il'])

    elif choice_count == 14:
        return sum([1 for i in s if i not in '0oO1Il'])

    elif choice_count == 15:
        a = input(f'Введите строку: ')
        return sum([1 for i in s if i in a])

    elif choice_count == 16:
        a = input(f'Введите строку: ')
        return sum([1 for i in s if i not in a])

    elif choice_count == 17:
        a = input(f'Введите строку: ')
        return sum([1 for i in s.lower() if i in a.lower()])

    elif choice_count == 18:
        a = set(input(f'Введите строку: ').lower())
        s = set(s.lower())
        return len(s - a)

    elif choice_count == 19:
        a = set(input(f'Введите строку: '))
        s = set(s)
        return len(a.intersection(s))

    elif choice_count == 20:
        a = set(input(f'Введите строку: ').lower())
        s = set(s.lower())
        return len(a.intersection(s))

    else:
        print("Неверный выбор. Пожалуйста, выберите, что хотите посчитать, снова.")


current_string = input('Введите строку: ')
while True:
    print("Выберите действие:")
    print("1. Показать текущую строку в двойных кавычках и в скобках её длину")
    print("2. Заменить текущую строку, прочитав новую")
    print("3. Внести изменения в строку")
    print("4. Проверить строку")
    print("5. Подсчитать количество")
    print("6. Завершить работу")
    choice = int(input("Ваш выбор (1-6): "))
    if choice == 1:
        show_string(current_string)
    elif choice == 2:
        current_string = input('Введите новую строку, взамен предыдущей: ')
    elif choice == 3:
        new_string = modify_string(current_string)
        print(f'Было: "{current_string}"\nСтало: "{new_string}"')
        current_string = new_string
    elif choice == 4:
        check_answer = check_string(current_string)
        print(f'Проверяли строку "{current_string}"')
        if check_answer:
            print('Да')
        else:
            print('Нет')
    elif choice == 5:
        count_answer = count_string(current_string)
        print(f'Считали количество у строки "{current_string}"')
        print(f'Количество равно {count_answer}')
    elif choice == 6:
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите действие снова.")
