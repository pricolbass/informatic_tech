# 3.4. Встроенные возможности по работе с коллекциями
## 1. Автоматизация списка
```python
for i, elem in enumerate(map(str, input().split()), start=1):
    print(f'{i}. {elem}')
```
## 2. Сборы на прогулку
```python
for row1, row2 in zip(input().split(', '), input().split(', ')):
    print(f'{row1} - {row2}')
```
## 3. Рациональная считалочка
```python
from itertools import count

start, end, step = map(float, input().split())
for value in count(start, step):
    if value <= end:
        print(f'{value:.2f}')
    else:
        break
```
## 4. Словарная ёлка
```python
from itertools import accumulate

print('\n'.join(word for word in accumulate(map(lambda x: x + ' ', input().split()))))
```
## 5. Список покупок
```python
foods = set()
for _ in range(3):
    foods = foods.union({food for food in input().split(', ')})

for i, food in enumerate(sorted(foods), start=1):
    print(f'{i}. {food}')
```
## 6. Колода карт
```python
from itertools import product

values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'валет', 'дама', 'король', 'туз']
suits = ['пик', 'треф', 'бубен', 'червей']

cars_suit = input()
suits.remove(cars_suit)

for card in product(values, suits):
    print(card[0], card[1])
```
## 7. Игровая сетка
```python
from itertools import product

players = [input() for _ in range(int(input()))]
res = []
for player in product(players, players):
    if player[1] != player[0] and player[::-1] not in res:
        res.append(player)
print('\n'.join(map(lambda x: f'{x[0]} - {x[1]}', res)))
```
## 8. Меню питания 2.0
```python
from itertools import islice, cycle

m = int(input())
porridge_s = [input() for _ in range(m)]
n = int(input())
if n <= m:
    for porridge in islice(porridge_s, n):
        print(porridge)
else:
    i = 0
    for porridge in cycle(porridge_s):
        if i < n:
            print(porridge)
            i += 1
        else:
            break
```
## 9. Таблица умножения 3.0
```python
from itertools import product

for i in (n := range(1, int(input()) + 1)):
    print(' '.join(map(lambda x: str(x[0] * x[1]), product(n, [i]))))
```
## 10. Мы делили апельсин 2.0
```python
from itertools import product

n = int(input())
print('А Б В')
for oranges in product(range(1, n + 1), repeat=3):
    if oranges[0] + oranges[1] + oranges[2] == n:
        print(' '.join(str(orange) for orange in oranges))
```
## 11. Числовой прямоугольник 3.0
```python
from itertools import cycle

n, m = int(input()), int(input())

numbers = cycle(range(1, n * m + 1))
rectangle = [[next(numbers) for _ in range(m)] for _ in range(n)]
max_width = len(str(max(max(rectangle, key=max))))

print("\n".join(' '.join(f"{num:>{max_width}}" for num in row) for row in rectangle))
```
## 12. Список покупок 2.0
```python
products = []

for _ in range(int(input())):
    products.extend(input().split(', '))

for i, elem in enumerate(sorted(products), start=1):
    print(f'{i}. {elem}')
```
## 13. Расстановка спортсменов
```python
from itertools import permutations

s_people = [input() for _ in range(int(input()))]

for s_mens in sorted(permutations(s_people)):
    print(', '.join(s_mens))
```
## 14. Спортивные гадания
```python
from itertools import permutations

s_people = [input() for _ in range(int(input()))]

for s_mens in sorted(permutations(s_people, r=3)):
    print(', '.join(s_mens))
```
## 15. Список покупок 3.0
```python
from itertools import permutations

products = set()

for _ in range(int(input())):
    products.update(input().split(', '))

for product in sorted(permutations(products, r=3)):
    print(' '.join(product))
```
## 16. Расклад таков...
```python
from itertools import combinations

suits = ["бубен", "пик", "треф", "червей"]
nominals = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "валет", "дама", "король", "туз"]
suit, nominal = input(), input()

best_suit = [f'{n} {s}' for s in suits for n in nominals if n != nominal]
res = [triple for triple in combinations(best_suit, 3) if any(suit[:3] in card for card in triple)]
sort_res = sorted(['{}, {}, {}'.format(*sorted(triple)) for triple in res])

print('\n'.join(sort_res[:10]))
```
## 17. А есть ещё варианты?
```python
from itertools import combinations

suits = ["бубен", "пик", "треф", "червей"]
nominals = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "валет", "дама", "король", "туз"]
suit, nominal, combination = input(), input(), input()

best_suit = [f'{n} {s}' for s in suits for n in nominals if n != nominal]
res = [triple for triple in combinations(best_suit, 3) if any(suit[:3] in card for card in triple)]
sort_res = sorted(['{}, {}, {}'.format(*sorted(triple)) for triple in res])
index_comb = sort_res.index(combination)

print(sort_res[index_comb + 1])
```
## 18. Таблица истинности
```python
from itertools import product

s = input()
print('a b c f')

for bins in product('01', repeat=3):
    a, b, c = map(int, bins)
    print(a, b, c, int(eval(s, {'a': a, 'b': b, 'c': c})))
```
## 19. Таблица истинности 2
```python
from itertools import product

s = input()
var_s = sorted({var for var in s if var.isupper()})
print(' '.join(var_s) + ' F')

for bins in product('01', repeat=len(var_s)):
    print(f'{" ".join(bins)} {int(eval(s, {var: int(bins[i]) for i, var in enumerate(var_s)}))}')
```
## 20. Таблицы истинности 3
```python
from itertools import product

OPERATORS = {
    'not': 'not',
    'and': 'and',
    'or': 'or',
    '^': '!=',
    '->': '<=',
    '~': '==',
}

PRIORITY = {
    'not': 0,
    'and': 1,
    'or': 2,
    '^': 3,
    '->': 4,
    '~': 5,
    '(': 6,
}


def get_postfix_expression(expression, variables):
    stack = []
    result = []
    expression_list = expression.split()
    for token in expression_list:
        if token in variables:
            result.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack[-1] != '(':
                result.append(OPERATORS[stack.pop()])
            stack.pop()
        elif token in OPERATORS.keys():
            while len(stack) and PRIORITY[token] >= PRIORITY[stack[-1]]:
                result.append(OPERATORS[stack.pop()])
            stack.append(token)
    for _ in range(len(stack)):
        result.append(OPERATORS[stack.pop()])
    return result


def evaluate_expression(postfix_expression, variables):
    stack = []
    for token in postfix_expression:
        if token in variables.keys():
            stack.append(variables[token])
        else:
            if token == 'not':
                stack.append(not stack.pop())
            else:
                var2, var1 = stack.pop(), stack.pop()
                stack.append(eval(f'{var1} {token} {var2}'))
    return int(stack.pop())


user_input = input()
all_variables = sorted(set(char for char in user_input if char.isupper()))
print(' '.join(all_variables), 'F')

user_input = user_input.replace('(', '( ').replace(')', ' )')
postfix_expression_result = get_postfix_expression(user_input, all_variables)

for row in product('01', repeat=len(all_variables)):
    variables = {var: int(value) for var, value in zip(all_variables, row)}
    print(' '.join(row), evaluate_expression(postfix_expression_result, variables))
```
