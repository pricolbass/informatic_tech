# 1.2 Ветвление
## 1.	Плотность тела
```python
V1, m1, V2, m2 = int(input()), int(input()), int(input()), int(input())

p1 = m1 / V1
p2 = m2 / V2

if p1 > p2:
    print(1)
elif p1 < p2:
    print(2)
else:
    print('=')
```
## 2. Високосный год
```python
y = int(input())

if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
    print(29)
else:
    print(28)
```
## 3. Вася и работа
```python
n = int(input())

if ((n % 3 == 0) and (abs(n) % 10 != 3)) or ((n % 3 != 0) and (abs(n) % 10 == 3)):
    print(1)
else:
    print(0)
```
## 4. Области. Задача 7
```python
x, y = map(float, input().split())

if (0.5 <= y <= 1.5 and x <= 2) or (x >= 2):
    print('Yes')
else:
    print('No')
```
## 5. Улитка на координатной прямой
```python
x1, x2, x3 = map(int, input().split())

s1 = abs(x2 - x1)
s2 = abs(x3 - x1)

res = 0

if s1 <= s2:
    res += s1 + abs(x3 - x2)
else:
    res += s2 + abs(x3 - x2)
print(res)
```
## 6. Бассейн
```python
n, m, x, y = int(input()), int(input()), int(input()), int(input())

n, m = min(n, m), max(n, m)

if n > m:
    n, m = m, n

if x >= n / 2:
    x = n - x
if y >= m / 2:
    y = m - y

print(min(x, y))
```
## 7. Сундук с сокровищами
```python
a, b, c, d = int(input()), int(input()), int(input()), int(input()) ** 2

d1 = a ** 2 + b ** 2
d2 = a ** 2 + c ** 2
d3 = c ** 2 + b ** 2

if d1 <= d or d2 <= d or d3 <= d:
    print('Yes')
else:
    print('No')
```
## 8. Возраст
```python
k = int(input())

if 2 <= k % 10 <= 4 and not(12 <= k % 100 <= 14):
    print(f"Мне {k} года")
elif k % 10 == 1 and k % 100 != 11:
    print(f"Мне {k} год")
else:
    print(f"Мне {k} лет")
```
