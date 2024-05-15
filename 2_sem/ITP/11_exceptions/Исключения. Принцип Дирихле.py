import argparse
import csv
import os
import re


def get_env_variable(names, prompt, default=None):
    values = [os.getenv(name, default) for name in names]
    if all(value in (None, 0) for value in values):
        value = input(f"{prompt} (default: {default}): ") or default
        if value is None:
            raise ValueError(f"Переменная среды {names[0]} не установлена и значение не указано.")
        return value
    value = [value for value in values if value not in (None, 0)][-1]
    return value


def parse_arguments():
    pattern = re.compile(r'''[,;](?=(?:[^"]*"[^"]*")*[^"]*$)''')

    parser = argparse.ArgumentParser(description="Принцип Дирихле")
    parser.add_argument("--file", "-f", default='input.csv', help="Имя csv файла.")
    parser.add_argument("--number", "-n", type=int, default=None, help="Количество ящиков.")
    parser.add_argument("--rows", type=int, default=None, help="Количество непустых строк.")
    parser.add_argument("--cols", type=int, default=None, help="Количество непустых колонок.")
    parser.add_argument("--pigeons", "-m", type=int, default=None, help="Количество предметов.")
    parser.add_argument("items", nargs='*', default=None, help="Список предметов через , или ;.")

    args = parser.parse_args()

    args.file = get_env_variable(["FILE", 'F'], "Введите имя файла", "input.csv") or args.file

    try:
        args.number = args.number or int(get_env_variable(["NUMBER", "N"], "Введите количество ящиков", None))
        args.rows = args.rows or int(get_env_variable(["ROWS"], "Введите количество непустых строк", None))
        args.cols = args.cols or int(get_env_variable(["COLS"], "Введите количество непустых колонок", None))
        args.pigeons = args.pigeons or int(get_env_variable(["PIGEONS", "M"], "Введите количество предметов", None))
    except ValueError:
        raise ValueError('number (n), pigeons (m), rows, cols - должны быть целыми числами.')

    if not args.items:
        items_str = get_env_variable(["ITEMS"], f"Введите список {args.pigeons} предметов через , или ;: ")
        args.items = [elem.strip() for elem in pattern.split(items_str)]
    if len(args.items) != args.pigeons:
        raise ValueError(
            f'Количество предметов ({len(args.items)}) не соответствует указанному количеству ({args.pigeons}).')

    return args


def create_csv(filename):
    pattern = re.compile(r'''[,;](?=(?:[^"]*"[^"]*")*[^"]*$)''')

    while n_cols := input('Введите количество столбцов: '):
        if n_cols.isdigit() and int(n_cols) > 0:
            break
        else:
            print('Вы ввели не целое положительно число.')

    while n_rows := input('Введите количество строк: '):
        if n_rows.isdigit() and int(n_rows) > 0:
            break
        else:
            print('Вы ввели не целое положительно число.')

    file_items = []

    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        n_rows, n_cols = int(n_rows), int(n_cols)
        for i in range(n_rows):
            while row_csv := input(f'Введите список {n_cols} предметов через , или ;: '):
                items_ = [elem.strip() for elem in pattern.split(row_csv)]
                if n_cols != len(items_):
                    print(f'Количество предметов ({len(items_)}) не соответствует указанному количеству ({n_cols}).')
                else:
                    writer.writerow(items_)
                    file_items += [items_]
                    break
    print(f'Файл {filename} успешно создан.')
    return file_items


def read_csv(filename):
    try:
        with open(filename, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            return list(reader)
    except FileNotFoundError:
        while question := input(f'Файл {filename} не найден. Вы хотите его создать (Да/Нет)? ').lower().strip():
            if question == 'да':
                return create_csv(filename)
            elif question == 'нет':
                raise FileNotFoundError(f'Файл {filename} не найден.')
            else:
                print('Вы ввели, что-то кроме да и нет.')
    except Exception as e:
        raise Exception(f'Ошибка чтения файла {filename}: {e}')


def validate_data(args, csv_data):
    n = args.number
    m = args.pigeons
    rows = args.rows
    cols = args.cols

    if rows and sum(1 for row in csv_data if any(row)) > rows:
        raise ValueError(f'Число непустых строк в файле {args.file} больше {rows}')

    if cols and sum(1 for col in zip(*csv_data) if any(col)) > cols:
        raise ValueError(f'Число непустых колонок в файле {args.file} больше {cols}')

    return n, m


def dirichle_principle(n, m):
    if m > n:
        return f'Если в {n} ящиках лежит {m} предметов, то хотя бы в одном ящике лежит не менее {m // n + 1} предметов.'
    elif m < n:
        return f'Если в {n} ящиках лежит {m} предметов, то пустых ящиков как минимум {n - m}.'
    else:
        return f'Если в {n} ящиках лежит {m} предметов, то каждый ящик содержит ровно один предмет.'  # ответ на вопрос


def main():
    args = parse_arguments()
    csv_data = read_csv(args.file)

    try:
        n, m = validate_data(args, csv_data)
        result = dirichle_principle(n, m)
        print(result)
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
