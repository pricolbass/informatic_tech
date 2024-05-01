# 1.1 Линейные алгоритмы
## 1. 	A + B на разных строках
```python
a = int(input())
b = int(input())

print(a + b)
```
## 2. Линейные алгоритмы. Задача 2.1
```python
n = int(input())

n1 = n // 100
n2 = n // 10 % 10
n3 = n % 10

print(n1 + n2 + n3)
print(n1 * n2 * n3)
```
## 3. Линейные алгоритмы. Задача 2.5
```python
n = int(input())

n3 = n % 10 * 1000

print(n3 + n)
```
## 4. Часы и минуты
```python
k = int(input())

hours = k // 3600
minutes = k % 3600 // 60

print(f"It is {hours} hours {minutes} minutes.")
```
## 5. Путь улитки
```python
x1, x2, x3 = int(input()), int(input()), int(input())

s1 = x2 - x1
s2 = x3 - x2
s3 = x3 - x1

print(abs(s1) + abs(s2) + abs(s3))
```
## 6. Восстановление чисел по сумме и разности
```python
a, b = int(input()), int(input())

y = (a - b) // 2
x = a - y

print(x, y)
```
## 7. Максимальное число квадратов
```python
a, b, k = int(input()), int(input()), int(input())

print((a // k) * (b // k))
```
## 8. Амёбы
```python
n = int(input())

i = n // 3

print(2 ** i)
```
