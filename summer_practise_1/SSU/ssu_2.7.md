# 2.7 * Матрицы
## 1. Четные и нечетные числа столбца
```python
import numpy as np

N = int(input())
array = np.array([list(map(int, input().split())) for _ in range(N)])
even_counts = np.sum(array % 2 == 0, axis=0)
odd_counts = np.sum(array % 2 != 0, axis=0)
res = np.stack((even_counts, odd_counts), axis=1)
for column in res:
    print(column[0], column[1])
```
## 2. Линии из звездочек
```python
import numpy as np

n, m = map(int, input().split())
matrix = np.array([list(input()) for _ in range(n)])
print(np.sum(np.all(matrix == '*', axis=1)) + np.sum(np.all(matrix == '*', axis=0)))
```
## 3. Вакансии
```python
import numpy as np

n, m = map(int, input().split())
matrix = np.array([list(map(int, input().split())) for _ in range(n)])

sorted_indices = np.unravel_index(np.argsort(matrix, axis=None), matrix.shape)

vacancies_taken = np.zeros(n, dtype=bool)
candidates_taken = np.zeros(m, dtype=bool)

selected_cost = 0
for idx in range(len(sorted_indices[0])):
    i, j = sorted_indices[0][idx], sorted_indices[1][idx]
    if not vacancies_taken[i] and not candidates_taken[j]:
        vacancies_taken[i] = True
        candidates_taken[j] = True
        selected_cost += matrix[i, j]
    if vacancies_taken.all() or candidates_taken.all():
        break

total_cost = selected_cost

print(total_cost)
```
## 4. Фотографии бактерий
```python
import numpy as np


def read_matrix(lines):
    return np.array([list(line) for line in lines])


def extract_stars(matrix):
    rows = np.any(matrix == '*', axis=1)
    cols = np.any(matrix == '*', axis=0)
    return matrix[np.ix_(rows, cols)]


def rotate_matrix(matrix):
    return np.rot90(matrix)


def compare_matrices(mat1, mat2):
    for _ in range(4):
        if np.array_equal(mat1, mat2):
            return True
        mat1 = rotate_matrix(mat1)
    return False


na, ma = map(int, input().split())
matrix_a = np.array([list(input()) for _ in range(na)])

nb, mb = map(int, input().split())
matrix_b = np.array([list(input()) for _ in range(nb)])

stars_a = extract_stars(matrix_a)
stars_b = extract_stars(matrix_b)

if compare_matrices(stars_a, stars_b):
    print("YES")
else:
    print("NO")
```
