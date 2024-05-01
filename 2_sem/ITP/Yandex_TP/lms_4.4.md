# 4.4. КР «Функции и их особенности в Python»
## 1. Метео-вывод
```python
def print_meteo(temperature, pressure):
    print(f'На улице {temperature}°C. Давление {pressure} мм. рт. ст.')
```
## 2. Глобальное сложение
```python
s = []


def add_number(number):
    s.append(number)


def get_sum():
    return f"{' + '.join([str(elem) for elem in s])} = {sum(s)}"

```
## 3. Кратный поиск
```python
from math import inf


def find_pair(*numbers, div=6):
    max_s = -inf
    b_p = None
    ind_j = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            current_sum = numbers[i] + numbers[j]
            if current_sum % div == 0:
                if current_sum > max_s:
                    max_s = current_sum
                    b_p = (numbers[i], numbers[j])
                    ind_j = j
                elif current_sum == max_s and j > ind_j:
                    max_s = current_sum
                    b_p = (numbers[i], numbers[j])
                    ind_j = j
    return b_p
```
## 4. Частотный генератор
```python
def counter(text: str):
    for symbol in sorted(set(text)):
        if symbol.isalpha():
            yield symbol, text.count(symbol)
```
## 5. Путешествие кузнечика
```python
def grasshopper(start, finish, length):
    def search(current, path, remaining_jumps):

        if current == finish:
            if remaining_jumps == 0:
                results.append(path)
            return
        next_positions = [current + 1, current + 2, current - 1, current - 2]
        for next_pos in next_positions:
            if next_pos >= 1 and (remaining_jumps > 1 or next_pos == finish):
                search(next_pos, path + [next_pos], remaining_jumps - 1)

    results = []
    search(start, [start], length)
    return results
```
