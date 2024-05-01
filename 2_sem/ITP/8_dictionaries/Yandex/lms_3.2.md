# 3.2. Множества, словари
## 7. Азбука Морзе
```python
morse = {'A': '.-', 'B': '-...', 'C': '-.-.',
         'D': '-..', 'E': '.', 'F': '..-.',
         'G': '--.', 'H': '....', 'I': '..',
         'J': '.---', 'K': '-.-', 'L': '.-..',
         'M': '--', 'N': '-.', 'O': '---',
         'P': '.--.', 'Q': '--.-', 'R': '.-.',
         'S': '...', 'T': '-', 'U': '..-',
         'V': '...-', 'W': '.--', 'X': '-..-',
         'Y': '-.--', 'Z': '--..',
         '0': '-----', '1': '.----', '2': '..---',
         '3': '...--', '4': '....-', '5': '.....',
         '6': '-....', '7': '--...', '8': '---..',
         '9': '----.'}

res = []
for symbol in input():
    if symbol != ' ':
        res.append(morse[symbol.upper()] + ' ')
    else:
        res.append('\n')
print(''.join(res))
```
## 8. Кашееды — 4
```python
n = int(input())
res = {}
for i in range(n):
    s = input().split()
    surname, porrs = s[0], s[1:]
    for porr in porrs:
        res.setdefault(porr, []).append(surname)
porridge_t = input()
if porridge_t in res:
    print('\n'.join(sorted(res[porridge_t])))
else:
    print('Таких нет')
```
## 9. Зайка — 9
```python
res = {}
s = input()
while s != '':
    for area in s.split():
        res.setdefault(area, 0)
        res[area] += 1
    s = input()
for key, value in res.items():
    print(key, value)
```
## 10. Транслитерация
```python
ru2la_alphabet = {
    "А": "A", "а": "a",
    "Б": "B", "б": "b",
    "В": "V", "в": "v",
    "Г": "G", "г": "g",
    "Д": "D", "д": "d",
    "Е": "E", "е": "e",
    "Ё": "E", "ё": "e",
    "Ж": "Zh", "ж": "zh",
    "З": "Z", "з": "z",
    "И": "I", "и": "i",
    "Й": "I", "й": "i",
    "К": "K", "к": "k",
    "Л": "L", "л": "l",
    "М": "M", "м": "m",
    "Н": "N", "н": "n",
    "О": "O", "о": "o",
    "П": "P", "п": "p",
    "Р": "R", "р": "r",
    "С": "S", "с": "s",
    "Т": "T", "т": "t",
    "У": "U", "у": "u",
    "Ф": "F", "ф": "f",
    "Х": "Kh", "х": "kh",
    "Ц": "Tc", "ц": "tc",
    "Ч": "Ch", "ч": "ch",
    "Ш": "Sh", "ш": "sh",
    "Щ": "Shch", "щ": "shch",
    "Ы": "Y", "ы": "y",
    "Э": "E", "э": "e",
    "Ю": "Iu", "ю": "iu",
    "Я": "Ia", "я": "ia"
}

s = input()
res = []
for letter in s:
    if letter in ru2la_alphabet:
        res.append(ru2la_alphabet[letter])
    elif letter in 'ъьЪЬ':
        continue
    elif letter.lower() == 'ё':
        res.append(ru2la_alphabet['е'])
    elif letter.lower() == 'й':
        res.append(ru2la_alphabet['и'])
    elif letter.lower() == 'Ё':
        res.append(ru2la_alphabet['E'])
    elif letter.lower() == 'Й':
        res.append(ru2la_alphabet['И'])
    else:
        res.append(letter)
print(''.join(res))
```
## 11. Однофамильцы
```python
n = int(input())

d = {}
for i in range(n):
    last_name = input()
    if last_name not in d:
        d[last_name] = 0
    d[last_name] += 1
print(sum(value for key, value in d.items() if value > 1))
```
## 12. Однофамильцы — 2
```python
n = int(input())

d = {}
for i in range(n):
    last_name = input()
    if last_name not in d:
        d[last_name] = 0
    d[last_name] += 1
d = {key: value for key, value in sorted(d.items()) if value > 1}
if d:
    for key, value in d.items():
        print(f'{key} - {value}')
else:
    print('Однофамильцев нет')
```
## 15. Двоичная статистика!
```python
print([{'digits': len(n), 'units': n.count('1'), 'zeros': n.count('0')} for n in
       list(map(lambda x: bin(x)[2:], list(map(int, input().split()))))])
```
## 17. Друзья друзей
```python
d = dict()

while s := input().split():
    if s[0] not in d:
        d[s[0]] = {s[1]}
    else:
        d[s[0]].add(s[1])

    if s[1] not in d:
        d[s[1]] = {s[0]}
    else:
        d[s[1]].add(s[0])

d1 = dict().fromkeys(d, set())
for key, value in d.items():
    for name in value:
        d1[key] = d1[key].union(d[name])
    d1[key].remove(key)
    for name in value:
        d1[key].discard(name)

for key, value in sorted(d1.items()):
    print(f'{key}: {", ".join(sorted(value))}')
```
## 18. Карта сокровищ
```python
d = {}
for _ in range(int(input())):
    x, y = map(str, input().split())

    if not (z := f'{x[:-1]} {y[:-1]}') in d:
        d[z] = 1
    else:
        d[z] += 1

print(max(d.values()))
```
## 19. Частная собственность
```python
from collections import defaultdict

d = defaultdict(list)
for _ in range(int(input())):
    s = input().split(': ')
    for toy in set(s[1].split(', ')):
        d[toy] += [s[0]]


print('\n'.join(sorted(key for key, value in d.items() if len(value) == 1)))
```
## 20. Простая задача 4.0
```python
from collections import defaultdict

data = sorted(map(int, input().split('; ')))
result = defaultdict(set)

for i in data:
    for j in data:
        a, b = i, j
        while b:
            a, b = b, a % b
        if a == 1:
            result[i].add(j)

for number in result:
    print(f'{number} - {", ".join(map(str, sorted( result[number])))}')
```
