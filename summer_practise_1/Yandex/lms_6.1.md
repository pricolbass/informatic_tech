# 6.1. Модули math и numpy
## 1. Математика — круто, но это не точно
```python
import math

x = float(input())
print(math.log(x ** (3 / 16), 32) + x ** (math.cos((math.pi * x) / (2 * math.e))) - (math.sin(x / math.pi)) ** 2)
```
## 2. Потоковый НОД
```python
import math
from sys import stdin

for line in stdin:
    numbers = list(map(int, line.split()))
    print(math.gcd(*numbers))
```
## 3. Есть варианты?
```python
import math

N, M = map(int, input().split())
if M > N:
    favorable = math.comb(N, N)
    total = favorable
else:
    favorable = math.comb(N - 1, M - 1)
    total = math.comb(N, M)

print(favorable, total)
```
## 4. Среднее не арифметическое
```python
import math

numbers = list(map(float, input().split()))
print(math.prod(numbers) ** (1 / len(numbers)))
```
## 5. Шаг навстречу
```python
import math

x, y = map(float, input().split())
p, f = map(float, input().split())
x1 = p * math.cos(f)
x2 = p * math.sin(f)

print(math.dist((x, y), (x1, x2)))
```
## 6. Матрица умножения
```python
import numpy as np


def multiplication_matrix(n):
    matrix = np.arange(1, n + 1)
    return matrix * matrix[:, None]
```
## 7. Шахматная подготовка
```python
import numpy as np


def make_board(n):
    matrix = np.indices((n, n)).sum(axis=0) % 2
    return np.array(np.rot90(matrix), dtype='int8')
```
## 8. Числовая змейка 3.0
```python
import numpy as np


def snake(m, n, direction='H'):
    matrix = np.arange(1, m * n + 1, dtype='int16')

    if direction == 'H':
        matrix = matrix.reshape(n, m)
        odd_rows = np.arange(n) % 2 != 0
        matrix[odd_rows] = matrix[odd_rows, ::-1]
    elif direction == 'V':
        matrix = matrix.reshape(m, n).transpose()
        odd_columns = np.arange(m) % 2 != 0
        matrix[:, odd_columns] = matrix[::-1, odd_columns]
    return matrix
```
## 9. Вращение
```python
import numpy as np


def rotate(matrix, angle):
    return np.rot90(matrix, (360 - angle) // 90)
```
## 10. Лесенка
```python
import numpy as np


def stairs(vector):
    n = len(vector)
    indices = np.arange(n)
    return vector[(indices[:, None] - indices) % n].transpose()
```
