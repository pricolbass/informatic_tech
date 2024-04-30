# 2.1. Ввод и вывод данных. Операции с числами, строками. Форматирование
## 1. Привет, Яндекс!
```python
print('Привет, Яндекс!')
```
## 2. Привет, всем!
```python
name = input('Как Вас зовут?\n')
print(f'Привет, {name}')
```
## 3. Излишняя автоматизация
```python
print((input() + '\n') * 3)
```
## 4. Сдача
```python
nom = int(input())

print(int(nom - 2.5 * 38))
```
## 5. Магазин
```python
price, weight, money = int(input()), int(input()), int(input())

print(int(money - weight * price))
```
## 6. Чек
```python
name, price, weight, money = input(), int(input()), int(input()), int(input())

dep = int(weight * price)

print(f'''Чек
{name} - {weight}кг - {price}руб/кг
Итого: {dep}руб
Внесено: {money}руб
Сдача: {int(money - dep)}руб''')
```
## 7. Делу — время, потехе — час
```python
n = int(input())

print(n * 'Купи слона!\n')
```
## 8. Наказание
```python
n = int(input())
s = input()

print(n * f'Я больше никогда не буду писать "{s}"!\n')
```
## 9. Деловая колбаса
```python
n, m = int(input()), int(input())

speed = 2 / 2 / 2

print(int(n * m * speed))
```
## 10. Детский сад — штаны на лямках
```python
name, num = input(), int(input())

num = str(num)

print(f'''Группа №{num[0]}.  
{num[-1]}. {name}.  
Шкафчик: {num}.  
Кроватка: {num[1]}.
''')
```
## 11. Автоматизация игры
```python
num = int(input())

num = str(num)

print(int(num[1] + num[0] + num[3] + num[2]))
```
## 12. Интересное сложение
```python
n1 = int(input())
n2 = int(input())

res = 0

for i in range(3):
    n1, n1_ = n1 // 10, n1 % 10
    n2, n2_ = n2 // 10, n2 % 10

    res += (n1_ + n2_) % 10 * 10 ** i
    
print(res)
```
## 13. Дед Мороз и конфеты
```python
kids = int(input())
candies = int(input())

res1, res2 = candies // kids, candies % kids

print(res1, res2, sep='\n')
```
## 14. Шарики и ручки
```python
red, green, blue = int(input()), int(input()), int(input())

print(red + blue + 1)
```
## 15. В ожидании доставки
```python
n, m, t = int(input()), int(input()), int(input())

current_time = n * 60 + m + t
hours, minute = current_time // 60, current_time % 60
days, hour = hours // 24, hours % 24

print(f'{hour:02d}:{minute:02d}')
```
## 16. Доставка
```python
a, b, c = int(input()), int(input()), int(input())

print(f'{abs(b - a) / c:.2f}')
```
## 17. Ошибка кассового аппарата
```python
n, m = int(input()), input()

print(n + int(m, 2))
```
## 18. Сдача 10
```python
n, m = input(), int(input())

print(m - int(n, 2))
```
## 19. Украшение чека
```python
name, price, weight, money = input(), int(input()), int(input()), int(input())

price_line = f'{weight}кг * {price}руб/кг'

print('================Чек================')
print(f'Товар:{name.rjust(35 - 6)}')
print(f'Цена:{price_line.rjust(35 - 5)}')
print(f'Итого:{str(weight * price).rjust(35 - 9)}руб')
print(f'Внесено:{str(money).rjust(35 - 11)}руб')
print(f'Сдача:{str(money - (weight * price)).rjust(35 - 9)}руб')
print('===================================')
```
## 20. Мухи отдельно, котлеты отдельно
```python
n, m, k1, k2 = int(input()), int(input()), int(input()), int(input())

x = n * (k2 - m) / (k2 - k1)
y = n - x
print(int(x), int(y))
```
