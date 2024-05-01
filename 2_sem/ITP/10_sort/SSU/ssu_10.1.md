# 10.1 Сортировки
## 1. Сортировки. Записи. Задача 2
```python
import random

n = int(input())


def quicksort(nums, fst, lst):
    if fst >= lst: return

    i, j = fst, lst
    pivot = nums[random.randint(fst, lst)]

    while i <= j:
        while nums[i] < pivot: i += 1
        while nums[j] > pivot: j -= 1
        if i <= j:
            nums[i], nums[j] = nums[j], nums[i]
            i, j = i + 1, j - 1
    quicksort(nums, fst, j)
    quicksort(nums, i, lst)
    return nums


students = {}
for _ in range(n):
    student = list(map(str, input().split()))
    marks = list(map(int, student[4:]))
    average_marks = sum(marks) / len(marks)
    students[average_marks] = students.get(average_marks, []) + [student]

sorted_average_marks = quicksort(list(students.keys()), 0, len(students.keys()) - 1)
for average_marks in sorted_average_marks:
    print('\n'.join([' '.join(student) for student in students[average_marks]]))
```
## 2. Сортировки. Записи. Задача 1
```python
n = int(input())

students = []

for _ in range(n):
    data = input().split()
    surname, name, patronymic, year = data[:4]
    marks = list(map(int, data[4:]))
    average_marks = sum(marks) / len(marks)
    students.append((average_marks, surname, name, patronymic, year, *marks))

students.sort(key=lambda x: x[0], reverse=True)

for student in students:
    print(' '.join(map(str, student[1:])))
```
## 3. Сортировки. Записи. Задача 5
```python
n = int(input())

students = []

for _ in range(n):
    data = input().split()
    surname, name, patronymic = data[:3]
    year = int(data[3])
    marks = list(map(int, data[4:]))
    students.append((surname, name, patronymic, year, *marks))

students.sort(key=lambda x: (x[0], -x[3]))

for student in students:
    print(' '.join(map(str, student)))
```
## 4. Сортировки. Матрицы. Задача 1
```python
n = int(input())

for _ in range(n):
    print(' '.join([str(elem) for elem in sorted(map(int, input().split()), reverse=True)]))
```
## 5. Сортировки. Матрицы. Задача 2
```python
n = int(input())
matrix = []

for _ in range(n):
    matrix.append(list(map(int, input().split())))

for col in range(n):
    column_values = [matrix[row][col] for row in range(n)]
    column_values.sort()
    for row in range(n):
        matrix[row][col] = column_values[row]

for row in matrix:
    print(" ".join(map(str, row)))
```
## 6. Сортировки. Матрицы. Задача 5
```python
n = int(input())
matrix = []

for _ in range(n):
    matrix.append(list(map(int, input().split())))

for col in range(n):
    column_values = [matrix[row][col] for row in range(n)]
    if col % 2 == 0:
        column_values.sort()
    else:
        column_values.sort(reverse=True)
    for row in range(n):
        matrix[row][col] = column_values[row]

for row in matrix:
    print(" ".join(map(str, row)))
```
## 7. Сортировки. Структуры. Задача 8
```python
n = int(input())

products = []
for _ in range(n):
    s = input().split()
    name, company = s[:2]
    num = int(s[2])
    products.append((name, company, num))

diff = input()
products = sorted([elem for elem in products if elem[1] != diff], key=lambda x: (x[0], -x[2]))
print('\n'.join([' '.join([str(item) for item in elem]) for elem in products[:10]]))
```
## 8. Сортировки. Структуры. Задача 10
```python
n = int(input())
cards = {}
for _ in range(n):
    rank, suit = input().split()
    rank = int(rank)
    if suit not in cards:
        cards[suit] = []
    cards[suit].append(rank)

order = input().strip()

for suit in order:
    if suit in cards:
        cards[suit].sort()

for suit in order:
    if suit in cards:
        print(suit + ':', ' '.join(map(str, cards[suit])))
    else:
        print(suit + ':')
```
## 9. ЕГЭ. Задача 19
```python
from collections import Counter

print(''.join([elem[0] for elem in sorted(Counter(input()[:-1]).items(), key=lambda x: (-x[1], x[0]))]))
```
## 10. ЕГЭ 2012-1
```python
countries = {}
for _ in range(int(input())):
    country = input()
    countries[country] = countries.get(country, 0) + 1

print('\n'.join([' '.join(map(str, elem)) for elem in sorted(countries.items(), key=lambda x: (-x[1], x[0]))]))
```
## 11. ЕГЭ 2012-6
```python
N = int(input())

accounts = {}

for _ in range(N):
    name, amount = input().split(',')
    amount = int(amount)
    if name not in accounts:
        accounts[name] = [0, 0]
    accounts[name][0] += amount
    accounts[name][1] += amount

sorted_accounts = sorted(accounts.items(), key=lambda x: (-x[1][0], x[0]))

for name, (balance, commission) in sorted_accounts:
    print(f"{name} {balance * 0.95:.2f} {commission * 0.05:.2f}")
```
