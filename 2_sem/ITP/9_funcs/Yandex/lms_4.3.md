# 4.3. Рекурсия. Декораторы. Генераторы
## 1. Рекурсивный сумматор
```python
def recursive_sum(*args):
    if args:
        return args[0] + recursive_sum(*args[1:])
    else:
        return 0
```
## 2. Рекурсивный сумматор цифр
```python
def recursive_digit_sum(n: int) -> int:
    if n != 0:
        return n % 10 + recursive_digit_sum(n // 10)
    else:
        return 0
```
## 3. Многочлен N-ой степени
```python
def make_equation(*args) -> str:
    if len(args) > 1:
        return f'({make_equation(*args[:-1])}) * x {"- " if args[-1] < 0 else "+ "}{str(args[-1])}'
    else:
        return str(args[0])
```
## 4. Декор результата
```python
def answer(func):
    def wrapper(*args, **kwargs):
        return f'Результат функции: {func(*args, **kwargs)}'
    return wrapper
```
## 5. Накопление результата
```python
def result_accumulator(func):
    queue_list = []

    def wrapper(*args, method='accumulate'):
        queue_list.append(func(*args))
        if method == 'drop':
            temp = queue_list.copy()
            queue_list.clear()
            return temp

    return wrapper
```
## 6. Сортировка слиянием
```python
def merge_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr
    else:
        middle = int(n / 2)
        left = merge_sort(arr[:middle])
        right = merge_sort(arr[middle:])
        return merge(left, right)


def merge(left, right):
    sorted_list = []
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]:
            sorted_list.append(left[0])
            left = left[1:]
        else:
            sorted_list.append(right[0])
            right = right[1:]
    if len(left) > 0:
        sorted_list += left
    if len(right) > 0:
        sorted_list += right

    return sorted_list
```
## 7. Однотипность не порок
```python
def same_type(func):
    def wrapper(*args):
        if all(isinstance(arg, type(args[0])) for arg in args):
            return func(*args)
        else:
            print('Обнаружены различные типы данных')
            return False
    return wrapper
```
## 8. Генератор Фибоначчи
```python
def fibonacci(n: int):
    n1, n2 = 0, 1
    for i in range(n):
        yield n1
        n1, n2 = n2, n1 + n2
```
## 9. Циклический генератор
```python
def cycle(line):
    while line:
        for elem in line:
            yield elem
```
## 10. "Выпрямление" списка
```python
def make_linear(a: list) -> list:
    if not a:
        return a
    if isinstance(a[0], list):
        return make_linear(a[0]) + make_linear(a[1:])
    return a[:1] + make_linear(a[1:])
```
