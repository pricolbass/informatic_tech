# 4.2. Позиционные и именованные аргументы. Функции высших порядков. Лямбда-функции
## 1. Генератор списков
```python
def make_list(length=0, value=0) -> list:
    return [value] * length
```
## 2. Генератор матриц
```python
def make_matrix(size, value=0) -> list:
    if type(size) is int:
        return [[value for _ in range(size)] for _ in range(size)]
    return [[value for _ in range(size[0])] for _ in range(size[1])]
```
## 3. Функциональный нод 2.0
```python
def gcd(*args) -> int:
    numbers = list(args)
    while len(numbers) > 1:
        while numbers[1]:
            numbers[0], numbers[1] = numbers[1], numbers[0] % numbers[1]
        numbers.pop(1)
    return numbers[0]
```
## 4. Имя of the month 2.0
```python
def month(num, language='ru') -> str:
    MONTH = {
        'en': [
            'January', 'February', 'March',
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

    return MONTH[language][num - 1]
```
## 5. Подготовка данных
```python
def to_string(*args, sep=' ', end='\n') -> str:
    return sep.join(map(str, list(args))) + end
```
## 6. Кофейня
```python
def order(*args) -> str:
    ingredients = in_stock
    ORDERS_INGR = {
        "Эспрессо": {"coffee": 1},
        "Капучино": {"coffee": 1,
                     "milk": 3},
        "Макиато": {"coffee": 2,
                    "milk": 1},
        "Кофе по-венски": {"coffee": 1,
                           "cream": 2},
        "Латте Макиато": {"coffee": 1,
                          "milk": 2,
                          "cream": 1},
        "Кон Панна": {"coffee": 1,
                      "cream": 1},
    }

    for ord_er in args:
        for ingredient in ORDERS_INGR[ord_er]:
            if ORDERS_INGR[ord_er].get(ingredient, 0) > in_stock[ingredient]:
                break
        else:
            for ingredient in ORDERS_INGR[ord_er]:
                in_stock[ingredient] -= ORDERS_INGR[ord_er][ingredient]
            return ord_er
    if in_stock == ingredients:
        return "К сожалению, не можем предложить Вам напиток"
```
## 7. В эфире рубрика «Эксперименты»
```python
numbers = []


def enter_results(*args):
    numbers.extend(list(args))


def get_sum():
    return round(sum(numbers[::2]), 2), round(sum(numbers[1::2]), 2)


def get_average():
    return round(2 * get_sum()[0] / len(numbers), 2), round(2 * get_sum()[1] / len(numbers), 2)
```
## 8. Длинная сортировка
```python
lambda x: (len(x), x.lower())
```
## 9. Чётная фильтрация
```python
lambda x: sum(map(int, str(x).lstrip('-'))) % 2 == 0
```
## 10. Ключевой секрет
```python
def secret_replace(text, **kwargs) -> str:
    result_string = ''
    symbols = {key: (value, 0) for key, value in kwargs.items()}
    print(symbols)
    for symbol in text:
        if symbol in symbols:
            result_string += symbols[symbol][0][symbols[symbol][1] % len(symbols[symbol][0])]
            symbols[symbol] = symbols[symbol][0], symbols[symbol][1] + 1
        else:
            result_string += symbol
    return result_string
```
