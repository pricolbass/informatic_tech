# 5.1 Списки
## 1. Изменение элементов массива 1
```python
n = int(input())

a = [int(input()) for i in range(n)]
k = int(input())

print(*[elem * k for elem in a])
```
## 2. Одномерные массивы. Задача 3.3
```python
n = int(input())

a = list(map(int, input().split()))
m_a = max(a)
m_a_ind = a.index(m_a)
a[m_a_ind] = (-1) * a[m_a_ind]

print(*a)
```
## 3. ЕГЭ С2-2
```python
n, m, k = map(int, input().split())

a = list(map(int, input().split()))

res = 0
for number in a:
    if abs(number) % 10 == k and number % m != 0:
        res += number
print(res)
```
## 4. Палиндром
```python
import string

phrase = ''.join([elem for elem in input().strip() if elem not in string.punctuation and elem != ' ']).upper()

if phrase == phrase[::-1]:
    print('Yes')
else:
    print('No')
```
## 5. Цифровой корень
```python
n = int(input())

res = n

while len(str(res)) > 1:
    res = sum(int(number) for number in str(res))
print(res)
```
## 6. Слияние
```python
n, m = map(int, input().split())

a = list(map(int, input().split()))
b = list(map(int, input().split()))

i = j = 0
res = []

while i < n and j < m:
    if a[i] < b[j]:
        res += [a[i]]
        i += 1
    else:
        res += [b[j]]
        j += 1
if i < n:
    res += a[i:]
else:
    res += b[j:]
print(*res)
```
## 7. Расшифровка сдвигов
```python
n, p, q = map(int, input().split())

a = list(map(int, input().split()))
a = a[q:] + a[:q]

a1 = a[:len(a)//2]
a2 = a[len(a)//2:]

a1 = a1[p:] + a1[:p]
a2 = a2[p:] + a2[:p]

res = a1 + a2

print(*res)
```
## 8. Изменение порядка
```python
n = int(input())

a = list(map(int, input().split()))

min_a = a.index(min(a))
max_a = len(a) - a[::-1].index(max(a)) - 1

if min_a > max_a:
    max_a, min_a = min_a, max_a

res = a[:min_a] + a[min_a:max_a + 1][::-1] + a[max_a + 1:]
print(*res)
```
## 9. Гласные и согласные
```python
s = input().upper()

vowels = 'AEIOU'
consonants = 'BCDFGHJKLMNPQRSTVWXZ'
v_c = 'Y'

res = ''
for i, elem in enumerate(s):
    if elem == v_c:
        if i == 0 or res[-1] == 'C':
            res += 'V'
        else:
            res += 'C'
    elif elem in vowels:
        res += 'V'
    else:
        res += 'C'

print(res)
```
