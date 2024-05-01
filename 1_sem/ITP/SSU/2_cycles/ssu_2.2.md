# 2.2 Вложенные циклы
## 1. Максимальное количество делителей
```python
a, b = map(int, input().split())


def count_del(x) -> int:
    c = 0
    for d in range(1, int(x ** .5) + 1):
        if x % d == 0:
            c += 1
            if x ** .5 != x // d:
                c += 1
    return c


res, s = 0, 0
for num in range(a, b + 1):
    c_d = count_del(num)
    if c_d >= s:
        res = num
        s = c_d

print(res)
```
## 2. Вложенные циклы. Задача 1.1
```python
a, b = map(int, input().split())


def is_prime(x) -> bool:
    for d in range(2, int(x ** .5) + 1):
        if x <= 1:
            return False
        elif x % d == 0:
            return False
    return True


for i in range(a, b + 1):
    if is_prime(i):
        print(i, end=' ')
```
## 3. Вложенные циклы. Задача 1.2
```python
n = int(input())

d = 2
c = 0

while d <= n:
    if n % d == 0:
        n //= d
        c += 1
    else:
        d += 1

if c == 2:
    print('Yes')
else:
    print('No')
```
## 4. Вложенные циклы. Задача 1.7
```python
n = int(input())


def is_prime(x) -> bool:
    for d in range(2, int(x ** .5) + 1):
        if x <= 1:
            return False
        if x % d == 0:
            return False
    return True


if is_prime(n):
    print(n)
else:
    l_p = n - 1
    u_p = n + 1

    while True:
        if is_prime(l_p):
            print(l_p)
            break
        if is_prime(u_p):
            print(u_p)
            break
        l_p -= 1
        u_p += 1
```
