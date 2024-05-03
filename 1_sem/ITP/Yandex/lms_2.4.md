# 2.4. Вложенные циклы
## 1. Таблица умножения
```python
n = int(input())

for i in range(1, n + 1):
    for j in range(1, n + 1):
        if j < n:
            print(i * j, end=' ')
        else:
            print(i * j)
```
## 2. Не таблица умножения
```python
n = int(input())

for i in range(1, n + 1):
    for j in range(1, n + 1):
        print(f'{j} * {i} = {i * j}')
```
## 3. Новогоднее настроение
```python
for d in range(1, x := int(input()) + 1):
    if d in (sum(range(i)) for i in range(x)):
        print(d)
    else:
        print(d, end=' ')
```
## 4. Суммарная сумма
```python
n = int(input())

res = 0
for _ in range(n):
    res += sum(int(elem) for elem in input())
print(res)
```
## 5. Зайка — 5
```python
res, temp = 0, 0
for _ in range(int(input())):
    while (s := input()) != 'ВСЁ':
        if 'зайка' == s:
            temp += 1
    if temp:
        res += 1
        temp = 0
print(res)
```
## 6. НОД 2.0
```python
n = int(input())

res = int(input())
for _ in range(n - 1):
    n1 = int(input())
    while res != 0 and n1 != 0:
        if res > n1:
            res %= n1
        else:
            n1 %= res
    res += n1
print(res)
```
## 7. На старт! Внимание! Марш!
```python
for i in range(int(input())):
    for j in range(3 + i, 0, -1):
        print(f'До старта {j} секунд(ы)')
    print(f'Старт {i + 1}!!!')
```
## 8. Максимальная сумма
```python
name, n = '', 0
for _ in range(int(input())):
    name_1 = input()
    n_1 = sum(int(elem) for elem in input())
    if n_1 >= n:
        n, name = n_1, name_1
print(name)
```
## 9. Большое число
```python
res = ''
for _ in range(int(input())):
    res += max(input())
print(res)
```
## 10. Мы делили апельсин
```python
n = int(input())
print('А Б В')
for i in range(1, n - 1):
    for j in range(1, n - i):
        print(f'{i} {j} {n - i - j}')
```
## 11. Простая задача 3.0
```python
def prime(n):
    for i in range(2, int(n ** .5) + 1):
        if n % i == 0:
            return False
    return n != 1


res = 0
for _ in range(int(input())):
    if prime(int(input())):
        res += 1
print(res)
```
## 12. Числовой прямоугольник
```python
n, m = int(input()), int(input())

n1, width = 0, len(str(n * m))
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if j < m:
            print(str(j + n1).rjust(width), end=' ')
        else:
            print(str(j + n1).rjust(width))
    n1 += m
```
## 13. Числовой прямоугольник 2.0
```python
n, m = int(input()), int(input())

width = len(str(n * m))
for i in range(1, n + 1):
    for j in range(i, i + n * (m - 1) + 1, n):
        if j == i + n * (m - 1):
            print(str(j).rjust(width))
        else:
            print(str(j).rjust(width), end=' ')
```
## 14. Числовая змейка
```python
n, m = int(input()), int(input())

n1, width = 0, len(str(n * m))
for i in range(1, n + 1):
    if i % 2:
        for j in range(m * (i - 1) + 1, m * i + 1):
            if j == m * i:
                print(str(j).rjust(width, ' '))
            else:
                print(str(j).rjust(width, ' '), end=' ')
    else:
        for j in range(m * i, m * (i - 1), -1):
            if j == m * (i - 1) + 1:
                print(str(j).rjust(width, ' '))
            else:
                print(str(j).rjust(width, ' '), end=' ')
```
## 15. Числовая змейка 2.0
```python
n, m = int(input()), int(input())

width = len(str(n * m))
for i in range(1, n + 1):
    for j in range(m):
        if not j % 2 and j != m - 1:
            print(str(i + 2 * n * (j // 2)).rjust(width, ' '), end=' ')
        elif not j % 2 and j == m - 1:
            print(str(i + 2 * n * (j // 2)).rjust(width, ' '))
        elif j % 2 and j != m - 1:
            print(str(2 * n * (j // 2 + 1) - (i - 1)).rjust(width, ' '), end=' ')
        else:
            print(str(2 * n * (j // 2 + 1) - (i - 1)).rjust(width, ' '))
```
## 16. Редизайн таблицы умножения
```python
n, m = int(input()), int(input())

for i in range(1, n + 1):
    for j in range(1, n + 1):
        if j != n:
            print(f'{(str(i * j) + " ").center(m)}|' if m % 2 else f'{(str(i * j)).center(m)}|', end='')
        else:
            print(f'{(str(i * j) + " ").center(m)}' if m % 2 else f'{str(i * j).center(m)}')
    if i != n:
        print(f'{"-" * ((m + 1) * n - 1)}')
```
## 17. А роза упала на лапу Азора 3.0
```python
n = int(input())

res = 0
for _ in range(n):
    s = input()
    if s == s[::-1]:
        res += 1
print(res)
```
## 18. Новогоднее настроение 2.0
```python
elem, lengths = '', [0]
for i in range(1, (n := int(input())) + 1):
    elem += str(i) + ' '
    if i in (sum(range(x)) for x in range(i + 2)):
        lengths.append(len(elem) - 1)
        elem = ''
lengths.append(len(elem) - 1)

d = 1
for i in range(1, n + 1):
    if i - 1 in (sum(range(x)) for x in range(i + 2)):
        print(f"{' ' * ((max(lengths) - lengths[d]) // 2)}{i}", end=' ' if i != 1 else '\n')
        d += 1
    else:
        print(i, end='\n' if i in (sum(range(i)) for i in range(i + 2)) else ' ')
```
## 19. Числовой квадрат
```python
for i in range(n := int(input())):
    for j in range(n):
        d = str(min(i, j, n - i - 1, n - j - 1) + 1)
        print(d.rjust(len(str((n + 1) // 2)), ' '), end=' ' if j < n - 1 else '\n')
```
## 20. Математическая выгода
```python
def convert_b2b(num, b1=10, b2=10):
    n = int(num, b1) if isinstance(num, str) else num
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res = ''
    while n > 0:
        n, m = divmod(n, b2)
        res += alphabet[m]
    return res[::-1]


number = input()
min_base, max_dig = 0, 0
for base in range(2, 11):
    sum_dig = sum(map(int, convert_b2b(number, 10, base)))
    if sum_dig > max_dig:
        max_dig = sum_dig
        min_base = base
    elif sum_dig == max_dig:
        min_base = min(min_base, base)
print(min_base)
```
