# 2.2. Условный оператор
## 1. Просто здравствуй, просто как дела
```python
name = input('Как Вас зовут?\n')
print(f'Здравствуйте, {name}!')
mood = input('Как дела?\n')
if mood == 'хорошо':
    print('Я за вас рада!')
else:
    print('Всё наладится!')
```
## 2. Кто быстрее?
```python
p, v = int(input()), int(input())

if p > v:
    print('Петя')
else:
    print('Вася')
```
## 3. Кто быстрее на этот раз?
```python
p, v, t = int(input()), int(input()), int(input())

max_speed = max(p, v, t)

if max_speed == p:
    print('Петя')
elif max_speed == v:
    print('Вася')
else:
    print('Толя')
```
## 4. Список победителей
```python
p, v, t = int(input()), int(input()), int(input())

max_speed = max(p, v, t)
min_speed = min(p, v, t)
if max_speed == p and min_speed == t:
    print(f'1. Петя\n2. Вася\n3. Толя')
elif max_speed == p and min_speed == v:
    print(f'1. Петя\n2. Толя\n3. Вася')
elif max_speed == v and min_speed == p:
    print(f'1. Вася\n2. Толя\n3. Петя')
elif max_speed == v and min_speed == t:
    print(f'1. Вася\n2. Петя\n3. Толя')
elif max_speed == t and min_speed == v:
    print(f'1. Толя\n2. Петя\n3. Вася')
else:
    print(f'1. Толя\n2. Вася\n3. Петя')
```
## 5. Яблоки
```python
n, m = int(input()), int(input())

p, v = 6 + n, 12 + m
if p > v:
    print('Петя')
else:
    print('Вася')
```
## 6. Сила прокрастинации
```python
year = int(input())

if (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0):
    print('YES')
else:
    print('NO')
```
## 7. А роза упала на лапу Азора
```python
n = input()

if n == n[::-1]:
    print('YES')
else:
    print('NO')
```
## 8. Зайка — 1
```python
s = list(input().lower().split())

if 'зайка' in s:
    print('YES')
else:
    print('NO')
```
## 9. Первому игроку приготовиться
```python
name1, name2, name3 = input(), input(), input()
print(min(name1, name2, name3))
```
## 10. Лучшая защита — шифрование
```python
n = int(input())

res = sorted([n % 10 + n // 10 % 10, n // 10 % 10 + n // 100], reverse=True)
print(f'{res[0]}{res[1]}')
```
## 11. Красота спасёт мир
```python
n = sorted(input())

print('YES') if (int(n[0]) + int(n[2])) == int(n[1]) * 2 else print('NO')
```
## 12. Музыкальный инструмент
```python
a, b, c = int(input()), int(input()), int(input())

print('YES') if a + b > c and a + c > b and b + c > a else print('NO')
```
## 13. Властелин Чисел: Братство общей цифры
```python
elf, gnome, human = input(), input(), input()

print(''.join(a for a, b, c in zip(elf, gnome, human) if a == b == c))
```
## 14. Властелин Чисел: Две Башни
```python
n = sorted(input())

if '0' not in n:
    print(n[0] + n[1], n[2] + n[1])
else:
    print(n[1] + n[0], n[2] + n[1])
```
## 15. Властелин Чисел: Возвращение Цезаря
```python
n = sorted(input() + input())

print(f'{n[-1]}{sum(int(elem) for elem in n[1:-1]) % 10}{n[0]}')
```
## 16. Легенды велогонок возвращаются: кто быстрее?
```python
p, v, t = int(input()), int(input()), int(input())


def table(f: str, s: str, t: str):
    print(f"""          {f}          
  {s}  
                  {t}  
   II      I      III   """)


max_speed = max(p, v, t)
min_speed = min(p, v, t)
if max_speed == p and min_speed == t:
    table('Петя', 'Вася', 'Толя')
elif max_speed == p and min_speed == v:
    table('Петя', 'Толя', 'Вася')
elif max_speed == v and min_speed == p:
    table('Вася', 'Толя', 'Петя')
elif max_speed == v and min_speed == t:
    table('Вася', 'Петя', 'Толя')
elif max_speed == t and min_speed == v:
    table('Толя', 'Петя', 'Вася')
else:
    table('Толя', 'Вася', 'Петя')
```
## 17. Корень зла
```python
a, b, c = float(input()), float(input()), float(input())

D = b ** 2 - 4 * a * c

if a == 0 and c == 0 and b == 0:
    print('Infinite solutions')
elif a == 0 and b != 0:
    print(f'{-c / b:.2f}')
elif D > 0 and a != 0:
    x1, x2 = (- b - D ** .5) / (2 * a), (- b + D ** .5) / (2 * a)
    print(f'{min(x1, x2):.2f} {max(x1, x2):.2f}')
elif D == 0 and a != 0:
    print(f'{-b / (2 * a):.2f}')
else:
    print('No solution')
```
## 18. Территория зла
```python
a, b, c = int(input()), int(input()), int(input())

c1, a1 = max(a, b, c), min(a, b, c)
b1 = a + c + b - a1 - c1

c1 **= 2
a1 **= 2
b1 **= 2

if a1 + b1 > c1:
    print('крайне мала')
elif a1 + b1 < c1:
    print('велика')
else:
    print('100%')
```
## 19. Автоматизация безопасности
```python
x, y = float(input()), float(input())

y1 = (x ** 2 + y ** 2) ** .5
y2 = .25 * x ** 2 + .5 * x + 8.25

if y1 > 10 and x != 0 and y != 0:
    print('Вы вышли в море и рискуете быть съеденным акулой!')
elif ((x >= 0 and y >= 0 and y1 <= 5) or ((x <= 0 <= y) and y <= 5 and y <= (5 * x + 35) / 3)
      or (((x >= 0 >= y) or (x <= 0 and y <= 0)) and y < y2) or (x == 0 and y == 0)):
    print('Опасность! Покиньте зону как можно скорее!')
else:
    print('Зона безопасна. Продолжайте работу.')
```
## 20. Зайка — 2
```python
s1, s2, s3 = input(), input(), input()

res = min([s for s in [s1, s2, s3] if 'зайка' in s])

print(res, len(res))
```
