# 3.3. Списочные выражения. Модель памяти для типов языка Python
## 1. Список квадратов
```python
[i ** 2 for i in range(a, b + 1)]
```
## 2. Таблица умножения 2.0
```python
[[i * j for j in range(1, n + 1)] for i in range(1, n + 1)]
```
## 3. Длины всех слов
```python
[len(word) for word in sentence.split()]
```
## 4. Множество нечетных чисел
```python
{number for number in numbers if number % 2 != 0}
```
## 5. Множество всех полных квадратов
```python
{number for number in numbers if number in [i ** 2 for i in range(1, int(max(numbers) ** .5) + 1)]}
```
## 6. Буквенная статистика
```python
{symbol: text.lower().count(symbol) for symbol in text.lower() if symbol.isalpha()}
```
## 7. Делители
```python
{number: [d for d in range(1, number + 1) if number % d == 0] for number in numbers}
```
## 8. Аббревиатура
```python
''.join([word[0] for word in string.split()]).upper()
```
## 9. Преобразование в строку
```python
' - '.join(str(elem) for elem in sorted(set(numbers)))
```
## 10. RLE наоборот
```python
''.join(elem1 * elem2 for elem1, elem2 in rle)
```
