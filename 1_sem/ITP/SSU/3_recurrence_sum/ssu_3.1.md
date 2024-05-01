# 3.1 Рекуррентность и суммы
## 1. Числа Фибоначчи
```python
k = int(input())

f1, f2 = 1, 1

res = 0

for i in range(2, k):
    f1, f2 = f2 , f1 + f2

print(f2)
```
## 2. Винни Пух
```python
n = int(input())

f1, f2 = 0.1, 0.1

for i in range(2, n):
    f1, f2 = f2, f1 + f2
print(round(f2, 1))
```
## 3. Богатый дядюшка
```python
n = int(input())

f1 = 1
res = 1

for i in range(2, n + 1):
    f1 = f1 * 2 + i
    res += f1
print(res)
```
## 4. Рекуррентные соотношения 1
```python
n = int(input())

f1, f2 = 1, 3

i = 2

while f2 <= n:
    f1, f2 = f2, (f1 + f2) // 2 + 2
    i += 1

print(i - 1)
```
## 5. Рекуррентные соотношения 2
```python
A, N = map(int, input().split())

girls = A // 2
boys = A

if boys == 1 and N > 1:
    print(0, boys, girls)
else:
    res_g, res_b = girls, boys
    d = 1

    while res_g + res_b < N:
        d += 1
        boys, girls = int(boys * 0.9), int(girls * 1.15)
        res_g, res_b = res_g + girls, res_b + boys

    print(d, res_b, res_g)
```
## 6. Рекуррентные соотношения 6
```python
A, M = map(int, input().split())

c = A
v = c * 1.3
d = 1

res_v = v
res_c = c

while res_c + res_v <= M:
    c += 6
    v = c * 1.3
    res_v += v
    res_c += c
    d += 1

print(d, res_c)
```
## 7. Рекуррентные соотношения 7
```python
A, B = map(int, input().split())
d = 1

res = A

while A < B:
    A *= 3
    res += A
    d += 1

print(d, end=' ')
while res < 1_000_000:
    A *= 3
    res += A
    d += 1

print(d)
```
## 8. Рекуррентные соотношения 11
```python
S, K, M = map(int, input().split())

R = K - M
res = 0

while S >= K:
    S -= R
    res += 1
print(res)
```
