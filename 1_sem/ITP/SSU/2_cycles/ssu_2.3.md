# 2.3 Таблицы значений функций
## 1. Таблица значений функции 1
```python
a, b, h = map(float, input().split())

while a - b <= 1e-6:
    x = a
    if not (abs(1 + x) < 1e-6):
        y = 1/((1 + x) ** 2)
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 2. Таблица значений функции 2
```python
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if not (abs(x**2 - 1) < 1e-7):
        y = 1/(x**2 - 1)
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 3. Таблица значений функции 3
```python
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if - (x ** 2 - 1) < 1e-7:
        y = (x ** 2 - 1) ** .5
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 4. Таблица значений функции 4
```python
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if - (5 - x ** 3) < 1e-7:
        y = (5 - x ** 3) ** .5
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 5. Таблица значений функции 5
```python
import math

a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if (x - 1) > 1e-7:
        y = math.log((x - 1))
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 6. Таблица значений функции 6
```python
import math

a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if (4 - x ** 2) > 1e-7:
        y = math.log((4 - x ** 2))
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 7. Таблица значений функции 7
```python
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if 2*x - 1 > 1e-7:
        y = x/(2*x - 1) ** .5
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 8. Таблица значений функции 8
```python
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if x ** 2 + 2*x + 1 > 1e-7:
        y = (3*x + 4)/(x ** 2 + 2*x + 1) ** .5
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 9. Таблица значений функции 9
```python
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if abs(x - 1) > 1e-7 and abs(1 - 4 * x) > 1e-7:
        y = 1/(x - 1) + 2/(1 - 4*x)
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 10. Таблица значений функции 10
```python
import math
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if abs(x - 2) > 1e-7:
        y = math.log(abs(x - 2))
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 11. Таблица значений функции 11
```python
import math
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if not (abs(x - 2) < 1e-6) and x/(x - 2) > 1e-7 :
        y = math.log(x/(x - 2))
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 12. Таблица значений функции 12
```python
import math
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if x ** 4 - 1 > 1e-7 and 1 + x > 1e-7:
        y = math.log(x ** 4 - 1) * math.log(1 + x)
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 13. Таблица значений функции 13
```python
import math
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if x - 2 > 1e-7 and 5*x + 1 > 1e-7:
        y = math.log(x - 2)/((5*x + 1) ** .5)
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 14. Таблица значений функции 14
```python
import math
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if x ** 2 - 2*x + 1 > -1e-7 and 4 - 2*x > 1e-7:
        y = ((x ** 2 - 2*x + 1) ** .5)/math.log(4 - 2*x)
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 15. Таблица значений функции 15
```python
import math
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if not (abs(3 * x) < 1e-7) and (2 * x ** 5 - 1) > 1e-7:
        y = math.log(abs(3 * x)) * (2 * x ** 5 - 1) ** .5
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 16. Таблица значений функции 16
```python
a, b, h = map(float, input().split())

while a - b < 1e-7:
    x = a
    if abs(x ** 3 + 8) > 1e-7:
        y = 3 / abs(x ** 3 + 8)
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 17. Таблица значений функции 17
```python
a, b, h = map(float, input().split())

while a - b < 1e-7:
    x = a
    if abs(x ** 2 - 2) > 1e-7 and (x ** 3 - 1) > -1e-7:
        y = (x + 4) / (x ** 2 - 2) + (x ** 3 - 1) ** .5
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 18. Таблица значений функции 18
```python
a, b, h = map(float, input().split())

while a - b < 1e-7:
    x = a
    if (x ** 2 + 5) > -1e-7 and (x ** 2 + 1) > -1e-7:
        y = (x ** 2 + 1) ** .5 - (x ** 2 + 5) ** .5
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 19. Таблица значений функции 19
```python
a, b, h = map(float, input().split())

while a - b <= 1e-7:
    x = a
    if x ** 2 - 1 > 1e-7 and 2 * x ** 5 - 1 > 1e-7:
        y = (x ** 3 - 1) ** .5 / (x ** 2 - 1) ** .5
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
## 20. Таблица значений функции 20
```python
import math
a, b, h = map(float, input().split())

while a - b < 1e-7:
    x = a
    if abs(x + 7) > 1e-7 and 1e-7 < 1 - abs(x):
        y = 1 / (x + 7) + math.log(1 - abs(x))
        print(f'{x:.6f}', f'{y:.6f}')
    else:
        print(f'{x:.6f}', 'undefined')
    a += h
```
