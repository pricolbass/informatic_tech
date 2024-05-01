# 3.2. Множества, словари
## 1. Символическая выжимка
```python
print(''.join(set(input())))
```
## 2. Символическая разница
```python
print(''.join(set(input()).intersection(set(input()))))
```
## 3. Зайка — 8
```python
n = int(input())
res = set()
for i in range(n):
    res.update(set(input().split()))
print('\n'.join(res))
```
## 4. Кашееды
```python
n, m = int(input()), int(input())
set1, set2 = set(), set()
for i in range(n + m):
    if i < n:
        set1.add(input())
    elif i < n + m:
        set2.add(input())
res = set1.intersection(set2)
if len(res) == 0:
    print('Таких нет')
else:
    print(len(res))
```
## 5. Кашееды — 2
```python
n, m = int(input()), int(input())
res = set()
for i in range(n + m):
    s = input()
    if s not in res:
        res.add(s)
    else:
        res.remove(s)

if len(res) > 0:
    print(len(res))
else:
    print('Таких нет')
```
## 6. Кашееды — 3
```python
n, m = int(input()), int(input())
res = set()
for i in range(n + m):
    s = input()
    if s not in res:
        res.add(s)
    else:
        res.remove(s)

if len(res) > 0:
    print('\n'.join(sorted(res)))
else:
    print('Таких нет')
```
## 13. Дайте чего-нибудь новенького!
```python
n = int(input())
food = set()
for i in range(n):
    food.add(input())
m = int(input())
food_days = set()
for i in range(m):
    num = int(input())
    for j in range(num):
        food_days.add(input())
res = food.difference(food_days)
if len(res) > 0:
    print('\n'.join(sorted(res)))
else:
    print('Готовить нечего')
```
## 14. Это будет шедевр!
```python
n = int(input())
food = set()
for i in range(n):
    food.add(input())
m = int(input())
res = set()
for i in range(m):
    name = input()
    receipt = set()
    n_ingredients = int(input())
    for j in range(n_ingredients):
        receipt.add(input())
    if len(receipt.difference(food)) == 0:
        res.add(name)
if len(res) == 0:
    print('Готовить нечего')
else:
    print('\n'.join(sorted(res)))
```
## 16. Зайка — 10
```python
res = set()
while s := input().split():
    for i, elem in enumerate(s):
        if elem == 'зайка' and i not in (0, len(s) - 1):
            res.add(s[i - 1])
            res.add(s[i + 1])
        elif elem == 'зайка' and not i:
            res.add(s[i + 1])
        elif elem == 'зайка' and i == len(s) - 1:
            res.add(s[i - 1])

for elem in res:
    print(elem)
```
