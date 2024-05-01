# 6.1 Двумерные матрицы
## 1. Двумерные массивы. Задача 1.3
```python
n, m = map(int, input().split())
A, B = map(int, input().split())

a = []

for _ in range(n):
    b = list(map(int, input().split()))
    if any(A <= x <= B for x in b):
        b = [0 if A <= num <= B else num for num in b]
    a.append(b)

for b in a:
    print(*b)
```
## 2. Двумерные массивы. Задача 1.6
```python
n, m = map(int, input().split())

sum_ = 0
len_ = 0

for _ in range(n):
    b = list(map(int, input().split()))
    sum_ += sum(b)
    len_ += len(b)

print(sum_ / len_)
```
## 3. Двумерные массивы. Задача 1.13
```python
n, m = map(int, input().split())
k = int(input())

res = []
for i in range(n):
    b = list(map(int, input().split()))
    if any(num > k for num in b):
        for j in range(len(b)):
            if b[j] > k:
                res.append([i + 1, j + 1])

for b_ind in res:
    print(b_ind[0], b_ind[1])
```
## 4. Двумерные массивы. Задача 2.1
```python
n = int(input())

sum_, len_ = 0, 0
for i in range(n):
    b = list(map(int, input().split()))
    if any(b[j] % 2 != 0 for j in range(i + 1, len(b))):
        for j in range(i + 1, len(b)):
            if b[j] % 2 != 0:
                sum_ += b[j]
                len_ += 1
if len_ == 0:
    print('No')
else:
    print(f'{(sum_ / len_):.6f}')
```
## 5. Двумерные массивы. Задача 2.5
```python
n = int(input())

sum_, len_ = 0, 0

for i in range(n):
    b = list(map(int, input().split()))
    s = b[-(i+1):][1:]
    sum_ += sum(s)
    len_ += len(s)

if len_ == 0:
    print('No')
else:
    print(f'{(sum_ / len_):.6f}')
```
## 6. Двумерные массивы. Задача 2.10
```python
n, m = map(int, input().split())

a = [list(map(int, input().split())) for i in range(n)]

print(*[min(column) for column in list(zip(*a))])
```
## 7. Двумерные массивы. Задача 2.11
```python
n, m = map(int, input().split())

a = [list(map(int, input().split()))[::-1] for i in range(n)]

for rows in a:
    print(*rows)
```
## 8. Двумерные массивы. Задача 2.12
```python
n, m = map(int, input().split())

a = [list(map(int, input().split())) for i in range(n)]
if n % 2 != 0:
    a[0], a[n//2] = a[n//2], a[0]
else:
    a[n//2 - 1], a[n//2] = a[n//2], a[n//2 - 1]

for rows in a:
    print(*rows)
```
## 9. Двумерные массивы. Задача 2.14
```python
n, m = map(int, input().split())

a = [list(map(int, input().split())) for i in range(n)]
if n % 2 == 0:
    a = [rows for elem in zip(a[1::2], a[::2]) for rows in elem]

for rows in a:
    print(*rows)
```
