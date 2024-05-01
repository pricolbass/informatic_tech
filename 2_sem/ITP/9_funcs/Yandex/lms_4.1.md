# 4.1. Функции. Области видимости. Передача параметров в функции
## 1. Функциональное приветствие
```python
def print_hello(name):
    print(f'Hello, {name}!')
```
## 2. Функциональный НОД
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    result = a
    return result
```
## 3. Длина числа
```python
def number_length(n):
    n = str(n).lstrip('-')
    result = len(n)
    return result
```
## 4. Имя of the month
```python
MONTHS = {
    'en': ['January', 'February', 'March',
           'April', 'May', 'June',
           'July', 'August', 'September',
           'October', 'November', 'December'
           ],
    'ru': [
        'Январь', 'Февраль', 'Март',
        'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь',
        'Октябрь', 'Ноябрь', 'Декабрь'
    ]
}


def month(n: int, language: str) -> str:
    result = MONTHS[language][n - 1]
    return result
```
## 5. Числовая строка
```python
def split_numbers(s: str) -> tuple:
    result = tuple(int(n) for n in s.split())
    return result
```
## 6. Модернизация системы вывода
```python
output = set()


def modern_print(print_str: str):
    if print_str not in output:
        output.add(print_str)
        print(print_str)
```
## 7. Шахматный «обед»
```python
def can_eat(horse: tuple, shape: tuple) -> bool:
    return abs(horse[0] - shape[0]) + abs(horse[1] - shape[1]) == 3
```
## 8. А роза упала на лапу Азора 7.0
```python
def is_palindrome(s) -> bool:
    return str(s) == str(s)[::-1] if isinstance(s, int) else s == s[::-1]
```
## 9. Простая задача 5.0
```python
def is_prime(n: int) -> bool:
    for i in range(2, int(n ** .5) + 1):
        if n % i == 0:
            return False
    return n != 1
```
## 10. Слияние
```python
def merge(s1: tuple, s2: tuple) -> tuple:
    result = []
    index1, index2 = 0, 0

    while index1 < len(s1) and index2 < len(s2):
        if s1[index1] < s2[index2]:
            result.append(s1[index1])
            index1 += 1
        else:
            result.append(s2[index2])
            index2 += 1

    result.extend(s1[index1:])
    result.extend(s2[index2:])
    return tuple(result)
```
