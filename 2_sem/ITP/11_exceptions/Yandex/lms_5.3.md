# 5.3. Модель исключений Python. Try, except, else, finally. Модули
## 1. Обработка ошибок
```python
try:
    func()
except Exception as e:
    print(type(e).__name__)
else:
    print('No Exceptions')
```
## 2. Ломать — не строить
```python
try:
    func('3', None)
except ValueError:
    print('Ура! Ошибка!')
```
## 3. Ломать — не строить 2
```python
class BrokeException:
    def __repr__(self):
        raise Exception


try:
    elem = BrokeException()
    func(elem)
except Exception:
    print('Ура! Ошибка!')
```
## 4. Контроль параметров
```python
def only_positive_even_sum(a, b):
    if not all(isinstance(elem, int) for elem in (a, b)):
        raise TypeError
    if not all(elem > 0 and elem % 2 == 0 for elem in (a, b)):
        raise ValueError
    return a + b
```
## 5. Слияние с проверкой
```python
from collections.abc import Iterable


def merge(a, b):
    if not all(isinstance(elem, Iterable) for elem in (a, b)):
        raise StopIteration
    if not (all(isinstance(elem, type(a[0])) for elem in a) and all(isinstance(elem, type(a[0])) for elem in b)):
        raise TypeError
    if list(a) != sorted(a) or list(b) != sorted(b):
        raise ValueError

    return tuple(sorted(list(a) + list(b)))
```
## 6. Корень зла 2
```python
class NoSolutionsError(Exception):
    pass


class InfiniteSolutionsError(Exception):
    pass


def find_roots(a, b, c):
    if not all(type(elem) in (int, float) for elem in (a, b, c)):
        raise TypeError
    if not a and not b and not c:
        raise InfiniteSolutionsError
    if (not a and not b and not c) or b ** 2 - 4 * a * c < 0:
        raise NoSolutionsError
    if a and b ** 2 - 4 * a * c == 0:
        return -b / (2 * a), -b / (2 * a)
    if b and not a:
        return -c / b
    if a:
        x_y = sorted([(-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a), (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)])
        return x_y[0], x_y[1]
    else:
        raise NoSolutionsError
```
## 7. Валидация имени
```python
class CyrillicError(Exception):
    pass


class CapitalError(Exception):
    pass


def name_validation(name):
    if not isinstance(name, str):
        raise TypeError
    if not all(symbol.lower() in 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя' for symbol in name):
        raise CyrillicError
    if name != name.lower().capitalize():
        raise CapitalError
    return name
```
## 8. Валидация имени пользователя
```python
from string import ascii_lowercase, digits


class BadCharacterError(Exception):
    pass


class StartsWithDigitError(Exception):
    pass


def username_validation(username):
    valid = ascii_lowercase + '_' + digits
    if not isinstance(username, str):
        raise TypeError
    if not all(symbol.lower() in valid for symbol in username):
        raise BadCharacterError
    if username[0].isdigit():
        raise StartsWithDigitError
    return username
```
## 9. Валидация пользователя
```python
from string import ascii_lowercase, digits


class CyrillicError(Exception):
    pass


class CapitalError(Exception):
    pass


class BadCharacterError(Exception):
    pass


class StartsWithDigitError(Exception):
    pass


def name_validation(name):
    if not isinstance(name, str):
        raise TypeError
    if not all(symbol.lower() in 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя' for symbol in name):
        raise CyrillicError
    if name != name.lower().capitalize():
        raise CapitalError
    return name


def username_validation(username):
    valid = ascii_lowercase + '_' + digits
    if not isinstance(username, str):
        raise TypeError
    if not all(symbol.lower() in valid for symbol in username):
        raise BadCharacterError
    if username[0].isdigit():
        raise StartsWithDigitError
    return username


def user_validation(**kwargs):
    if len(kwargs) != 3 or [elem for elem in kwargs] != ['last_name', 'first_name', 'username']:
        raise KeyError
    if not all(isinstance(elem, str) for key, elem in kwargs.items()):
        raise TypeError
    kwargs['last_name'] = name_validation(kwargs['last_name'])
    kwargs['first_name'] = name_validation(kwargs['first_name'])
    kwargs['username'] = username_validation(kwargs['username'])
    return kwargs
```
## 10. Валидация пароля
```python
import hashlib


class MinLengthError(Exception):
    pass


class PossibleCharError(Exception):
    pass


class NeedCharError(Exception):
    pass


class StartsWithDigitError(Exception):
    pass


def password_validation(password, min_length=8,
                        possible_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
                        at_least_one=str.isdigit):
    if not isinstance(password, str):
        raise TypeError
    if len(password) < min_length:
        raise MinLengthError
    if any(symbol not in possible_chars for symbol in password):
        raise PossibleCharError
    if not any(map(at_least_one, password)):
        raise NeedCharError
    return hashlib.sha256(password.encode()).hexdigest()
```
