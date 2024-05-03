# 4.4. КР «Функции и их особенности в Python»
## 1. Ветряный вывод
```python
def print_weather(wind, temperature):
    print(f'За окном дует ветер со скоростью {wind} м/с. Температура воздуха {temperature}°C.')
```
## 2. Глобальное произведение
```python
s = []


def add_number(number):
    s.append(number)

    
def get_prod():
    proizv = 1
    for i in s:
        proizv *= i
    return f"{' * '.join([str(x) for x in s])} = {proizv}"
```
## 3. Кратный подсчёт
```python
def count_pairs(*numbers, div=10):
    c = 0
    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            if (numbers[i] + numbers[j]) % div == 0:
                c += 1
    return c
```
## 4. Генератор индексов
```python
def index(text):
    a = []
    for symbol in sorted(set(text)):
        if symbol not in a and symbol.isalpha():
            yield symbol, text.index(symbol)
```
## 5. Путешествие зайки
```python
def bunny(start, finish, length):
    ans = []

    def search_pos(position, path, jump):
        if position == finish: 
            if jump == 0:
                ans.append(path)
            else:
                return
        for i in [position + 1, position - 1, position + 3, position - 3]:
            if i >= 1 and jump >= 1:
                search_pos(i, path + [i], jump - 1)
    
    search_pos(start, [start], length)
    return ans
```
