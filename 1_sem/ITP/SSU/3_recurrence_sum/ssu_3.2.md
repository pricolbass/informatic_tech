# 3.2 Бесконечные суммы
## 1. Вложенные циклы. Задача 8.1
```python
h, e = map(float, input().split())

x = 0.2

while 1.8 + e > x:
    y = x
    y_sum = 0

    while e  < y:
        y_sum += y
        y = (1/13) * (x * y ** 2 + 2 * y)

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 2. Вложенные циклы. Задача 8.2
```python
h, e = map(float, input().split())

x = 0.1

while 0.7 + e > x:
    i1 = 3
    i2 = 2
    y = x / 2
    y_sum = 0

    while e < y:
        y_sum += y
        y = x ** i1 / 2 ** i2
        i1 += 2
        i2 += 1

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 3. Вложенные циклы. Задача 8.3
```python
h, e = map(float, input().split())

x = 0

while 0.9 + e > x:
    i = 1
    y = 1
    y_sum = 0

    while e < y:
        y_sum += y
        y = (x / 3) ** i
        i += 1

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 4. Вложенные циклы. Задача 8.4
```python
h, e = map(float, input().split())

eps = 1e-9

x = 0.2

while 0.6 + eps > x:
    i1 = 2
    i2 = 2
    y = 1
    y_sum = 0

    while e + eps < y:
        y_sum += y
        y = x ** i1 / (i2 * (i2 + 2))
        i1 += 1
        i2 += 2

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 5. Вложенные циклы. Задача 8.5
```python
h, e = map(float, input().split())

x = 0.05

while 0.95 + e > x:
    y = 1
    i = 0
    i1 = 1
    i2 = i1
    y_sum = 0

    while e < y:
        y_sum += (-1) ** i * y
        i += 1
        i2 += 2
        i1 *= i2
        y = x ** i / i1

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 6. Вложенные циклы. Задача 8.6
```python
h, e = map(float, input().split())

x = 0.02

while 0.80 + e > x:
    y0 = 1
    y1 = 0.2 + x
    y_sum = y0 + y1

    while e < y1:
        try:
            y0, y1 = y1, 0.5 * y1 ** 2 + y0 * x ** 2
            y_sum += y1
        except OverflowError:
            y_sum = 0
            break

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 7. Вложенные циклы. Задача 8.7
```python
h, e = map(float, input().split())

x = 0.1

while 3.0 + e > x:
    y0 = 0
    y1 = 0.5
    i = 1
    y_sum = y0 + y1

    while e < y1:
        try:
            y0, y1 = y1, ((y1 + y0) / i) + ((y0 ** 3 * x ** 2) / i)
            y_sum += y1
            i += 1
        except OverflowError:
            y_sum = 0
            break

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 8. Вложенные циклы. Задача 8.8
```python
h, e = map(float, input().split())

x = 0.6

while 1.0 + e > x:
    y0 = x
    y1 = x ** 2 / 10
    i = 1
    y_sum = y0 + y1

    while e < y1:
        try:
            y0, y1 = y1, 2 * x * y1 ** 2 - y0 ** 3 * x ** 4
            y_sum += y1
            i += 1
        except OverflowError:
            y_sum = 0
            break

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 9. Вложенные циклы. Задача 8.9
```python
h, e = map(float, input().split())

x = 0.0

while 0.99 + e > x:
    y = 1
    i1 = 1
    i2 = 0
    y_sum = 0

    while e < y:
        y_sum += y
        i1 += 2
        i2 += 1
        y = (x ** i1) / (i1 * (2 ** i2))

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 10. Вложенные циклы. Задача 8.10
```python
h, e = map(float, input().split())

x = 0.2

while 0.8 + e > x:
    y0, y1 = 1, x
    i = 1
    y_sum = y0 + y1

    while e < y1:
        try:
            y0, y1 = y1, ((((x ** 2 - 2) * y1) / ((x ** 2 - 1) * i ** 2)) + (y0 ** 2 / i ** 2))
            y_sum += y1
            i += 1

        except OverflowError:
            y_sum = 0
            break

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 11. Вложенные циклы. Задача 8.11
```python
h, e = map(float, input().split())

x = 0.1

while 0.9 + e > x:
    i1 = 2
    y = x / 2
    y_sum = 0

    while e < y:
        y_sum += y
        y = x ** i1 / (2 ** i1 * (i1 + 1))
        i1 += 1

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 12. Вложенные циклы. Задача 8.12
```python
h, e = map(float, input().split())

x = 0.2

while 0.8 + e > x:
    y0, y1 = 1, x ** 2
    i = 1
    y_sum = y0 + y1

    while e < y1:
        try:
            y0, y1 = y1, 5 * x * y1 / i - y0 ** 2
            y_sum += y1
            i += 1

        except OverflowError:
            y_sum = 0
            break

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 13. Вложенные циклы. Задача 8.13
```python
h, e = map(float, input().split())

x = 0.1

while 0.9 + e > x:
    y = 1
    i = 1
    y_sum = 0

    while e < y:
        try:
            y_sum += y
            i += 1
            y = x ** i / 4 ** (i - 1)

        except OverflowError:
            y_sum = 0
            break

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 14. Вложенные циклы. Задача 8.14
```python
h, e = map(float, input().split())

x = 0.0

while 0.9 + e > x:
    y = 1
    i = 0
    y_sum = 0

    while e < y:
        try:
            y_sum += (-1) ** i * y
            i += 1
            y = x ** i / (2 ** i * 7 * i)

        except OverflowError:
            y_sum = 0
            break

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 15. Вложенные циклы. Задача 8.15
```python
h, e = map(float, input().split())

eps = 1e-9

x = 0.2

while 0.7 + e > x:
    y = 1
    i = 0
    i1 = 0
    y_sum = 0

    while e < y:
        y_sum += (-1) ** i * y
        i += 1
        i1 += 2
        y = x ** i1 / (i * (i + 2) * (i + 3))

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 16. Вложенные циклы. Задача 8.16
```python
h, e = map(float, input().split())

x = 0.1

while 0.9 + e > x:
    y = 1 + x / 4
    i = 0
    i1 = 1
    y_sum = 0

    while e < y:
        y_sum += (-1) ** i * y
        i += 1
        i1 += 1
        y = x ** i1 / (i1 * (i1 + 3))

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 17. Вложенные циклы. Задача 8.17
```python
h, e = map(float, input().split())

x = 0.0

while 0.8 + e > x:
    y = 1
    i = 0
    i1 = 1
    i2 = 3
    y_sum = 0

    while e < y:
        y_sum += (-1) ** i * y
        i += 1
        i1 += 2
        y = x ** i1 / (i2 * (i2 + 1) ** 2)
        i2 += 1

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 18. Вложенные циклы. Задача 8.18
```python
h, e = map(float, input().split())

x = 0.1

while 0.9 + e > x:
    y = 1
    i = 0
    y_sum = 0

    while e < y:
        y_sum += y
        i += 1
        y = x ** i / (2 ** (i + 1) * i)

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 19. Вложенные циклы. Задача 8.19
```python
h, e = map(float, input().split())

x = 0.2

while 0.6 + e > x:
    i1 = 1
    i2 = 6
    y = 1 / 4
    y_sum = 0

    while e < y:
        y_sum += y
        y = x ** (2 ** i1) / i2 ** 2
        i1 += 1
        i2 += 4

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
## 20. Вложенные циклы. Задача 8.20
```python
h, e = map(float, input().split())

x = 0.0

while 0.8 + e > x:
    y = 1/4
    i1 = 0
    i2 = -1
    y_sum = 0

    while e < y:
        y_sum += y
        i1 += 1
        i2 += 3
        y = i2 * x ** i1 / (i2 + 3) ** 2

    print(f'{x:.8f}', f'{y_sum:.8f}')
    x += h
```
