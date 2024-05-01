import re
s = input('Введите строку: ')

a = []


# функция для проверок
def main(b: list, n: int):
    if n == 1:
        return all(any(word.is_upper() for word in line.split()) for line in b)

    elif n == 2:
        return any(all(word.is_upper() for word in line.split()) for line in b)

    elif n == 3:
        return all(any(word.is_digit() for word in line.split()) for line in b)

    elif n == 4:
        return all(not any(word.is_digit() for word in line.split()) for line in b)

    elif n == 5:
        return all(any(len(word) == 1 for word in line.split()) for line in b)

    elif n == 6:
        return any(all(len(word) >= 3 for word in line.split()) for line in b)

    elif n == 7:
        return all(any(word.istitle() for word in line.split()) for line in b)

    elif n == 8:
        return any(not any(word.istitle() for word in line.split()) for line in b)

    elif n == 9:
        return any(all(word.istitle() for word in line.split()) for line in b)

    elif n == 10:
        k = int(input('Введите k - количество букв: '))
        return all(any(len(word) > k for word in line.split()) for line in b)

    elif n == 11:
        return any(line.split()[0] == line.split()[-1] for line in b)

    elif n == 12:
        return all(len(line.split()) % (i + 1) == 0 for i, line in enumerate(b))

    elif n == 13:
        return any(len(set(len(word) for word in line.split())) == 1 for line in b)

    elif n == 14:
        subs = input(f'Введите подстроку: ')
        return any(all(subs not in word for word in line.split()) for line in b)

    elif n == 15:
        symbol = input('Введите символ:')
        return all(line.count(symbol) >= 2 for line in b)

    elif n == 16:
        word = input('Введите слово:')
        return all(word in line for line in b)

    elif n == 17:
        word = input('Введите слово:')
        return all(line.count(word) <= 1 for line in b)

    elif n == 18:
        return any(all(word != word[::-1] for word in line.split()) for line in b)

    elif n == 19:
        return all(any(word == word[::-1] for word in line.split()) for line in b)

    elif n == 20:
        return any(all(word == word[::-1] for word in line.split()) for line in b)


while len(re.sub(r'[^a-zA-Z]', '', s)) > 0:
    a.append(s)
    s = input('Введите строку: ')

while True:
    print('''
Список проверок:
1.  Проверить, что во всех строках есть хотя бы одно слово, записанное полностью в верхнем регистре.
2.  Проверить, что хотя бы в одной строке все слова записаны полностью в верхнем регистре.
3.  Проверить, что во всех строках есть хотя бы одно целое число без знака (состоящее только из цифр).
4.  Проверить, что хотя бы в одной строке нет ни одного целого числа без знака (состоящего только из цифр).
5.  Проверить, что во всех строках есть слова из одной буквы.
6.  Проверить, что хотя бы в одной строке нет ни одного слова короче трёх символов.
7.  Проверить, что во всех строках есть слова, начинающиеся с прописной (заглавной) буквы.
8.  Проверить, что хотя бы в одной строке ни одно слово не начинается с прописной (заглавной) буквы.
9.  Проверить, что хотя бы в одной строке все слова начинаются с прописной (заглавной) буквы.
10. Проверить, что во всех строках есть хотя бы одно слово длиннее k букв.
11. Проверить, что хотя бы одна строка начинается и заканчивается одним и тем же словом. 
12. Проверить, что количество слов в каждой строке кратно её номеру.
13. Проверить, что хотя бы в одной строке все слова одинаковой длины.
14. Проверить, что хотя бы в одной строке ни одно слово не содержит заданную подстроку.
15. Проверить, что в каждой строке заданный символ встречается не менее чем в двух словах.
16. Проверить, что заданное слово встречается в каждой строке.
17. Проверить, что ни в одной строке заданное слово не встречается больше одного раза.
18. Проверить, что хотя бы в одной строке нет ни одного слова-палиндрома.
19. Проверить, что все строки содержат хотя бы по одному слову-палиндрому.
20. Проверить, что хотя бы в одной строке все слова — палиндромы.
21. Остановить работу.
    ''')

    check = int(input('Выберите одну из проверок (1-21): '))

    if 1 <= check <= 20:
        res = main(a, check)
        if res:
            print('Строки соответствуют условию проверки.')
        else:
            print('Строки не соответствуют условию проверки.')
    elif check == 21:
        break
    else:
        print('Такого действия нет.')
