# 3.1. Строки, кортежи, списки
## 1. Азбука
```python
n = int(input())
for i in range(n):
    word = input()
    if word[0].lower() not in 'абв':
        print('NO')
        break
else:
    print('YES')
```
## 2. Кручу-верчу
```python
word = input()
for letter in word:
    print(letter)
```
## 3. Анонс новости
```python
L = int(input())

for i in range(int(input())):
    text = input()
    print(text[:L - 3] + '...') if len(text) > L else print(text)
```
## 4. Очистка данных
```python
while line := input():
    if not line.endswith('@@@'):
        if line.startswith('##'):
            print(line.lstrip('##'))
        else:
            print(line)
```
## 5. А роза упала на лапу Азора 4.0
```python
s = input()
print("YES") if s[::-1] == s else print("NO")
```
## 6. Зайка — 6
```python
res = 0
for _ in range(int(input())):
    res += input().lower().count('зайка')

print(res)
```
## 7. А и Б сидели на трубе
```python
n1, n2 = map(int, input().split())
print(n1 + n2)
```
## 8. Зайка — 7
```python
for _ in range(int(input())):
    index_ = input().find('зайка')
    if index_ >= 0:
        print(index_ + 1)
    else:
        print('Заек нет =(')
```
## 9. Без комментариев
```python
while s := input():
    if not s.startswith('#'):
        print(s[:s.index('#')] if '#' in s else s)
```
## 10. Частотный анализ на минималках
```python
from collections import Counter

text = ''
while (s := input()) != 'ФИНИШ':
    text += ''.join(s.lower().strip().split())

print(sorted(Counter(text).items(), key=lambda x: (-x[1], x[0]))[0][0])
```
## 11. Найдётся всё
```python
headers = []
for i in range(int(input())):
    headers.append(input())

search = input()

for header in headers:
    if search.lower() in header.lower():
        print(header)
```
## 12. Меню питания
```python
data = ['Манная', 'Гречневая', 'Пшённая', 'Овсяная', 'Рисовая']
n = int(input())

for i in range(n):
    print(data[i % len(data)])
```
## 13. Массовое возведение в степень
```python
n = int(input())

nums = [int(input()) for _ in range(n)]
p = int(input())
print('\n'.join(str(elem ** p) for elem in nums))
```
## 14. Массовое возведение в степень 2.0
```python
nums = list(map(int, input().split()))
p = int(input())
print(*[n ** p for n in nums])
```
## 15. НОД 3.0
```python
nums = list(map(int, input().split()))


def gcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b


res = nums[0]
for elem in nums[1:]:
    res = gcd(res, elem)

print(res)
```
## 16. Анонс новости 2.0
```python
L, N = int(input()), int(input())

while L > 3:
    s = input()
    print(s[:L - 3] + '...' if len(s) >= L - 3 else (s + '...' if L == 4 else s))
    L -= len(s)
```
## 17. А роза упала на лапу Азора 5.0
```python
s = ''.join(input().lower().split())
print('YES') if s == s[::-1] else print('NO')
```
## 18. RLE
```python
s = input()
elem_line, repeat = s[0], 1
for elem1, elem2 in zip(s, s[1:]):
    if elem1 == elem2:
        repeat += 1
    else:
        print(elem_line, repeat)
        elem_line, repeat = elem2, 1
print(elem_line, repeat)
```
## 19. Польский калькулятор
```python
s = input().split()
stack = []
for elem in s:
    if elem.isdigit():
        stack.append(elem)
    else:
        elem2 = stack.pop()
        elem1 = stack.pop()
        stack.append(eval(f'{elem1} {elem} {elem2}'))
print(stack[0])
```
## 20. Польский калькулятор — 2
```python
from math import factorial

s = input().split()
stack = []
for elem in s:
    if elem.isdigit():
        stack.append(elem)
    elif '+' == elem or '-' == elem or '*' == elem:
        dig_2 = stack.pop()
        dig_1 = stack.pop()
        stack.append(eval(f'{dig_1} {elem} {dig_2}'))
    elif '/' == elem:
        dig_2 = int(stack.pop())
        dig_1 = int(stack.pop())
        stack.append(str(dig_1 // dig_2))
    elif '~' == elem:
        stack[-1] = str(-int(stack[-1]))
    elif '!' == elem:
        stack[-1] = str(factorial(int(stack[-1])))
    elif '#' == elem:
        stack.append(stack[-1])
    elif '@' == elem:
        stack.append(stack.pop(-3))
print(stack[0])
```
