# 8.1 Словари
## 1. Римские цифры
```python
r_letters = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

letter = input()
if letter in r_letters:
    print(r_letters[letter])
else:
    print(0)
```
## 2. Выбор. Задача 4
```python
k = int(input())

cards = {14: 'Ace', 13: 'King', 12: 'Queen', 11: 'Jack', 10: 'ten', 9: 'nine', 8: 'eight', 7: 'seven', 6: 'six'}
print(cards[k])
```
## 3. Выбор. Задача 5
```python
m, k = map(int, input().split())

cards_dignity = {1: 'spades', 2: 'clubs', 3: 'diamonds', 4: 'hearts'}
cards_suit = {14: 'ace', 13: 'king', 12: 'queen', 11: 'jack', 10: 'ten', 9: 'nine', 8: 'eight', 7: 'seven', 6: 'six'}
print(f'the {cards_suit[k]} of {cards_dignity[m]}')
```
## 4. ЕГЭ. Задача 16
```python
import sys

res = {}
for line in sys.stdin:
    line = line.strip().lower()
    if line:
        for symbol in line:
            if symbol.isalpha():
                res[symbol] = res.get(symbol, 0) + 1
        if '.' in line:
            break
res = sorted(res.items(), key=lambda x: (-x[1], x[0]))
print(res[0][0], res[0][1])
```
## 5. Две строки 3
```python
from collections import Counter

line1 = Counter(input().strip())
line2 = Counter(input().strip())

f = False
for letter in line2:
    if line2[letter] > line1.get(letter, 0):
        f = False
        break
    else:
        f = True
        
print(f)
```
## 6. Расшифровка оценок
```python
grade_counts = {2: 0, 3: 0, 4: 0, 5: 0}

s = input()

i = 0
while i < len(s):
    if s[i] == '0':
        grade_counts[2] += 1
        i += 1
    elif i + 1 < len(s) and s[i:i + 2] == '11':
        grade_counts[5] += 1
        i += 2
    elif i + 2 < len(s) and s[i:i + 3] == '101':
        grade_counts[4] += 1
        i += 3
    elif i + 2 < len(s) and s[i:i + 3] == '100':
        grade_counts[3] += 1
        i += 3
    else:
        i += 1

max_grade = max(grade_counts, key=grade_counts.get)
print(max_grade)
```
