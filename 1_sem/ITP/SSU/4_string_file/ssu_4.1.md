# 4.1 Строки
## 1. Добавь звёзды!
```python
s = input()

s_z = '*' * len(s)
print(s_z + s + s_z)
```
## 2. Слово в столбик в обратном порядке
```python
s = input()

for i in s[::-1]:
    print(i)
```
## 3. Буквы на четных местах в обратном порядке
```python
s1 = input()

s2 = ''

for i in range(1, len(s1), 2):
    s2 += s1[i]

print(s2[::-1])
```
## 4. Строки. Задача 19
```python
s = input()

if s == s[::-1]:
    print(1)
else:
    print(0)
```
## 5. Строки. Задача 3
```python
s = input()

l = len(s)

if l % 2 == 0:
    print(s[:l // 2 - 1] + s[l // 2 + 1:])
else:
    print(s[:l // 2] + s[l // 2 + 1:])
```
## 6. Сумма цифр
```python
s = input()

res = 0

for i in s:
    if i.isdigit():
        res += int(i)
print(res)
```
## 7. Строки. Задача 4
```python
c = input()
s = input()

print(s.replace(c, c*2))
```
## 8. Лишние пробелы
```python
s = input()

res = ' '.join(s.strip().split())

print(res)
```
## 9. Количество адресов электронной почты
```python
n = int(input())

s = []
res = 0

for i in range(n):
    s = input()
    if '..' not in s and s.count('@') == 1 and not s.startswith('@') and not s.endswith('@') :
        res += 1

print(res)
```
