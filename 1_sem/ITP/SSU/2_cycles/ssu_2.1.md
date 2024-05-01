# 2.1 Циклы
## 1. Грузовой автомобиль
```python
n = int(input())

s = 0

for i in range(n):
    x = int(input())
    s += x
m = int(input())

if m >= s:
    print('True')
else:
    print('False')
```
## 2. Циклы. Произведение
```python
res, x = 1, float(input())
while x >= 0:
    res *= x
    x = float(input())
print(f"{res:.6f}")
```
## 3. Циклы с параметром. Задача 3
```python
n = int(input())

res, c, j = 0, 0, 0

for i in range(n):
    x = abs(int(input()))
    j += 1
    if x >= c:
        res = j
        c = x

print(res)
```
## 4. ЕГЭ. Задача 6
```python
n = int(input())

y, res, j = 0, 1, 1

for i in range(n):
    x = int(input())
    if x == y:
        j += 1
        res = max(res, j)
    else:
        j = 1
    y = x
print(res)
```
## 5. Циклы. Задача 1.5
```python
n = int(input())


def is_prime(x) -> bool:
    if x <= 1:
        return False
    for i in range(2, int(x ** .5) + 1):
        if round(x) % i == 0:
            return False
    return True


for num in range(2, int(n ** .5) + 1):
    if is_prime(num) and num ** 3 == n:
        print('Yes')
        break
else:
    print('No')
```
## 6. Циклы. Задача 1.2
```python
n = int(input())

d = 2

while d <= n:
    if n % d == 0:
        print(d, end=' ')
        n //= d
    else:
        d += 1
```
## 7. Анализ последовательности чисел
```python
n = int(input())
x = int(input())

res = ''

while x > -2000000000:
    if x > n and (res == 'ASCENDING' or res == ''):
        res = 'ASCENDING'
    elif x == n and (res == 'CONSTANT' or res == ''):
        res = 'CONSTANT'
    elif x < n and (res == 'DESCENDING' or res == ''):
        res = 'DESCENDING'
    elif x >= n and (res == 'WEAKLY ASCENDING' or res == 'ASCENDING' or res == 'CONSTANT'):
        res = 'WEAKLY ASCENDING'
    elif x <= n and (res == 'WEAKLY DESCENDING' or res == 'DESCENDING' or res == 'CONSTANT'):
        res = 'WEAKLY DESCENDING'
    else:
        res = 'RANDOM'
    n = x
    x = int(input())
print(res)
```
## 8. Максимальный блок
```python
n = int(input())

m_s = -10**9
c_s = 0

for i in range(n):
    b = int(input())
    c_s = max(b, c_s + b)
    m_s = max(c_s, m_s)
print(m_s)
```
