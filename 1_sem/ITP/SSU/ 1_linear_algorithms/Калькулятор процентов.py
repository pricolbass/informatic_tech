number = int(input('Введите число: '))
actions = input('Выберите один из трех вариантов действия (только цифру):\n1. Найти процент от введённого числа\n2. '
                'Увеличить число на какой-то процент\n3. Уменьшить число на какой-то процент\n')
action = int(actions)
if action > 3:
    print('Извините, но такого действия не существует.')
else:
    percent = int(input('Введите значение процента: '))
    if percent >= 0:
        if action == 1:
            print(number * percent / 100)
        elif action == 2:
            print(number * (1 + percent / 100))
        elif action == 3:
            print(number * (1 - percent / 100))
    else:
        print('Процент не может быть отрицательным числом.')
