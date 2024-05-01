# 4.2 Файлы
## 1. Работа с текстовым файлом. Задача 3.1
```python
with open('input.txt', 'r') as input_file:
    c = input_file.readline().strip()
    res = sum([1 for line in input_file if line[0].strip() == c])

with open('output.txt', 'w') as output_file:
    output_file.write(str(res))
```
## 2. Работа с текстовым файлом. Задача 3.2
```python
res = 0
with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        if line and line[0] == line[-1]:
            res += 1

with open('output.txt', 'w') as output_file:
    output_file.write(str(res))
```
## 3. Работа с текстовым файлом. Задача 3.3
```python
res_len = 0
res_str = ''
with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        if len(line) > res_len:
            res_len = len(line)
            res_str = line

with open('output.txt', 'w') as output_file:
    output_file.write(f'{res_str}\n{res_len}')
```
## 4. Работа с текстовым файлом. Задача 3.4
```python
res_len = 10**9
res_str = ''
with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        if len(line) < res_len:
            res_len = len(line)
            res_str = line

with open('output.txt', 'w') as output_file:
    output_file.write(f'{res_str}\n{res_len}')
```
## 5. Работа с текстовым файлом. Задача 3.5
```python
len_ = 0
i = 0
res_i = 0
with open('input.txt', 'r') as input_file:
    for line in input_file:
        i += 1
        line = line.rstrip('\n')
        if len(line) > len_:
            len_ = len(line)
            res_i = i

with open('output.txt', 'w') as output_file:
    output_file.write(str(res_i))
```
## 6. Работа с текстовым файлом. Задача 3.6
```python
len_ = 10**8
i = 0
res_i = 0
with open('input.txt', 'r') as input_file:
    for line in input_file:
        i += 1
        line = line.rstrip('\n')
        if len(line) < len_:
            len_ = len(line)
            res_i = i

with open('output.txt', 'w') as output_file:
    output_file.write(str(res_i))
```
## 7. Работа с текстовым файлом. Задача 3.7
```python
res = ''

with open('input.txt', 'r') as input_file:
    a = input_file.readline().strip()
    for line in input_file:
        line = line.rstrip('\n')
        if line.startswith(a):
            res = line
            break

with open('output.txt', 'w') as output_file:
    output_file.write(res)
```
## 8. Работа с текстовым файлом. Задача 3.8
```python
res = ''

with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        if line:
            res += line[0]

with open('output.txt', 'w') as output_file:
    output_file.write(res)
```
## 9. Работа с текстовым файлом. Задача 3.9
```python
output_file = open('output.txt', 'w')

with open('input.txt', 'r') as input_file:
    k1, k2 = map(int, input_file.readline().split())
    for line in input_file:
        line = line.rstrip('\n')
        output_file.write(f"{line[k1-1:k2]}\n")
output_file.close()
```
## 10. Работа с текстовым файлом. Задача 3.10
```python
output_file = open('output.txt', 'w')
i = 0
with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        i += 1
        if i % 2 != 0:
            output_file.write(f"{line}\n")
output_file.close()
```
## 11. Работа с текстовым файлом. Задача 3.11
```python
output_file = open('output.txt', 'w')
i = 0
with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        if ' ' in line:
            output_file.write(f"{line}\n")
output_file.close()
```
## 12. Работа с текстовым файлом. Задача 3.12
```python
output_file = open('output.txt', 'w')
i = 0
with open('input.txt', 'r') as input_file:
    number = int(input_file.readline())
    for line in input_file:
        line = line.rstrip('\n')
        if len(line) == number:
            output_file.write(f"{line}\n")
output_file.close()
```
## 13. Работа с текстовым файлом. Задача 3.13
```python
output_file = open('output.txt', 'w')
i = 0
with open('input.txt', 'r') as input_file:
    number = int(input_file.readline())
    for line in input_file:
        line = line.rstrip('\n')
        if len(line) < number:
            output_file.write(f"{line}\n")
output_file.close()
```
## 14. Работа с текстовым файлом. Задача 3.14
```python
output_file = open('output.txt', 'w')
i = 0
with open('input.txt', 'r') as input_file:
    k1, k2 = map(int, input_file.readline().split())
    for line in input_file:
        line = line.rstrip('\n')
        i += 1
        if k1 <= i <= k2:
            output_file.write(f"{line}\n")
output_file.close()
```
## 15. Работа с текстовым файлом. Задача 3.15
```python
res = ''
with open('input.txt', 'r') as input_file:
    k = int(input_file.readline())
    for line in input_file:
        line = line.rstrip('\n')
        if len(line) >= k:
            res += line[k-1]


with open('output.txt', 'w') as output_file:
    output_file.write(res)
```
## 16. Работа с текстовым файлом. Задача 3.16
```python
i = 0
output_file = open('output.txt', 'w')
with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        i += 1
        output_file.write(f'{line} {i}\n')
```
## 17. Работа с текстовым файлом. Задача 3.17
```python
output_file = open('output.txt', 'w')
with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        output_file.write(f'{line} {len(line)}\n')
```
## 18. Работа с текстовым файлом. Задача 3.18
```python
output_file = open('output.txt', 'w')
with open('input.txt', 'r') as input_file:
    len_ = int(input_file.readline())
    for line in input_file:
        line = line.rstrip('\n')
        if len(line) > len_:
            output_file.write(f'{line}\n')
```
## 19. Работа с текстовым файлом. Задача 3.19
```python
output_file = open('output.txt', 'w')
with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        if len(line) % 2 == 0:
            output_file.write(f'{line}\n')
```
## 20. Работа с текстовым файлом. Задача 3.20
```python
output_file = open('output.txt', 'w')
with open('input.txt', 'r') as input_file:
    for line in input_file:
        line = line.rstrip('\n')
        output_file.write(f'{line[::2]}\n')
```
