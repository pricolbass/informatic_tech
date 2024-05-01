# 2.3. Циклы
## 1. Раз, два, три! Ёлочка, гори!
```python
s = input()
while s != 'Три!':
    print('Режим ожидания...')
    s = input()
print('Ёлочка, гори!')
```
## 2. Зайка — 3
```python
s = input()

res = 0
while s != 'Приехали!':
    if 'зайка' in s:
        res += 1
    s = input()

print(res)
```
## 3. Считалочка
```python
n1, n2 = int(input()), int(input())

for n in range(n1, n2 + 1):
    print(n, end=' ')
```
## 4. Считалочка 2.0
```python
n1, n2 = int(input()), int(input())

if n2 > n1:
    for n in range(n1, n2 + 1):
        print(n, end=' ')
else:
    for n in range(n1, n2 - 1, -1):
        print(n, end=' ')
```
## 5. Внимание! Акция!
```python
price = float(input())

res = 0
while price != 0:
    if price >= 500:
        res += price * 0.9
    else:
        res += price
    price = float(input())

print(res)
```
## 6. НОД
```python
n1, n2 = int(input()), int(input())

while n1 != n2:
    if n1 > n2:
        n1 -= n2
    else:
        n2 -= n1

print(n1)
```
## 7. НОК
```python
n1, n2 = int(input()), int(input())
a, b = n1, n2

while n1 != n2:
    if n1 > n2:
        n1 -= n2
    else:
        n2 -= n1

print(int(a / n1 * b))
```
## 8. Излишняя автоматизация 2.0
```python
s, n = input(), int(input())

for _ in range(n):
    print(s)
```
## 9. Факториал
```python
n = int(input())

res = 1
for i in range(2, n + 1):
    res *= i

print(res)
```
## 10. Маршрут построен
```python
direction = input()

res1, res2 = 0, 0
while direction != 'СТОП':
    steps = int(input())
    if direction == 'СЕВЕР':
        res1 += steps
    elif direction == 'ЮГ':
        res1 -= steps
    elif direction == 'ВОСТОК':
        res2 += steps
    else:
        res2 -= steps
    direction = input()

print(res1, res2, sep='\n')
```
## 11. Цифровая сумма
```python
print(sum(int(num) for num in input()))
```
## 12. Сильная цифра
```python
print(max(int(num) for num in input()))
```
## 13. Первому игроку приготовиться 2.0
```python
n = int(input())

res = input()
for _ in range(n - 1):
    name = input()
    if name < res:
        res = name

print(res)
```
## 14. Простая задача
```python
def prime(n):
    if n > 1:
        d = 2
        while d * d <= n and n % d != 0:
            d += 1
        return d * d > n
    return False


is_prime = prime(int(input()))
print('YES') if is_prime else print('NO')
```
## 15. Зайка - 4
```python
n = int(input())

res = 0
for _ in range(n):
    s = input()
    if 'зайка' in s:
        res += 1

print(res)
```
## 16. А роза упала на лапу Азора 2.0
```python
s = input()

is_pall = all(s[i] == s[-i - 1]for i in range(len(s) // 2))
print('YES') if is_pall else print('NO')
```
## 17. Чётная чистота
```python
s = input()

for num in s:
    if int(num) % 2 != 0:
        print(num, end='')
```
## 18. Простая задача 2.0
```python
n = int(input())

d = 2
while d < n:
    if n % d == 0:
        print(d, end=' * ')
        n //= d
    else:
        d += 1
print(d)
```
## 19. Игра в «Угадайку»
```python
begin, end = 0, 1001

print((begin + end) // 2)
while (x := input()) != 'Угадал!':
    if x == 'Меньше':
        if end == (begin + end) // 2:
            print(1)
        else:
            end = (begin + end) // 2
            print((begin + end) // 2)
    elif x == 'Больше':
        if begin == (begin + end) // 2:
            print(1000)
        else:
            begin = (begin + end) // 2
            print((begin + end) // 2)
```
## 20. Хайпанём немножечко!
```python
res, hn0 = -1, 0

for i in range(int(input())):
    bn = int(input())
    hn, rn, mn = bn % 256, (bn // 256) % 256, bn // 256 ** 2
    hn1 = ((mn + rn + hn0) * 37) % 256
    if hn1 != hn or hn > 99:
        res = i
        break
    hn0 = hn

print(res)
```
