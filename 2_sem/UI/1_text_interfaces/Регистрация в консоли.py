from string import punctuation, ascii_letters
import json
import hashlib
import re


def hash_password(password):
    """Генерирует хеш пароля."""
    return hashlib.sha256(password.encode()).hexdigest()


def user_exists(login, email, phone):
    """Проверяет, существует ли уже пользователь с таким же логином, email или телефоном."""
    try:
        with open('database.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
            for user in users:
                if user['login'] == login or user['email'] == email or user['phone'] == phone:
                    return True
    except FileNotFoundError:
        return False
    return False


def save_user(user_data):
    """Сохраняет данные пользователя в файл."""
    try:
        with open('database.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    users.append(user_data)
    with open('database.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)


def login_user():
    while True:
        login = input('Введите логин (не менее чем из 5 символов от A-Z и 0-9): ')
        if len(login) < 5:
            print('Извините, длина логина слишком короткая (не менее 5 символов), попробуйте еще раз.')
            continue
        elif not all(char in ascii_letters + '0123456789' for char in login):
            print('Извините, вы использовали недопустимые символы, попробуйте еще раз.')
            continue
        elif user_exists(login, None, None):
            print('Пользователь с таким логином уже существует, попробуйте другой.')
            continue
        else:
            break
    return login


def password_user():
    while True:
        password = input(
            'Введите пароль (не менее 8 символов, включая большие и маленькие буквы, цифры и спецсимволы): ')
        if len(password) < 8:
            print('Пароль слишком короткий, попробуйте еще раз.')
            continue
        elif not any(char.isdigit() for char in password):
            print('Пароль должен содержать хотя бы одну цифру.')
            continue
        elif not any(char.isupper() for char in password):
            print('Пароль должен содержать хотя бы одну заглавную букву.')
            continue
        elif not any(char.islower() for char in password):
            print('Пароль должен содержать хотя бы одну строчную букву.')
            continue
        elif not any(char in punctuation for char in password):
            print('Пароль должен содержать хотя бы один специальный символ.')
            continue
        else:
            break
    return repeat_password_user(password)


def repeat_password_user(password):
    сount_repeat = 0
    while True:
        repeat_password = input('Повторите пароль: ')
        if repeat_password != password:
            сount_repeat += 1
            if сount_repeat == 2:
                print('Пароли не совпадают. Необходимо создать пароль заново.')
                return password_user()
            else:
                print('Пароли не совпадают, попробуйте еще раз.')
        else:
            break
    return password


def email_user():
    while True:
        email = input('Введите почту: ')
        if '@' not in email or email.count('@') > 1 or email.startswith('@') or email.endswith('@'):
            print('Некорректный формат email, попробуйте еще раз.')
            continue
        elif user_exists(None, email, None):
            print('Пользователь с таким email уже существует, попробуйте другой.')
            continue
        else:
            break
    return email


def phone_user():
    while True:
        phone = input('Введите номер телефона (+7/8): ')
        if phone.startswith('+7'):
            phone = phone[2:]
        elif phone.startswith('8'):
            phone = phone[1:]
        phone = ''.join(re.split(r'\W+', phone))
        if len(phone) != 10 or not phone.isdigit():
            print('Номер телефона должен состоять из 10 цифр, попробуйте еще раз.')
            continue
        elif user_exists(None, None, phone):
            print('Пользователь с таким номером телефона уже существует, попробуйте другой.')
            continue
        else:
            break
    return phone


def register_user():
    """Регистрирует нового пользователя, сохраняя его данные в файл."""
    print('Регистрация')
    login = login_user()
    password = password_user()
    email = email_user()
    phone = phone_user()

    password_hash = hash_password(password)
    user_data = {
        'login': login,
        'password': password_hash,
        'email': email,
        'phone': phone
    }

    additional_info = input('Хотите ли вы добавить дополнительную информацию? (да/нет): ').lower()
    if additional_info == 'да':
        full_name = input('Введите ваше ФИО: ')
        city = input('Введите город, в котором вы живете: ')
        about = input('Введите некоторую информацию о себе: ')

        user_data['full_name'] = full_name
        user_data['city'] = city
        user_data['about'] = about

    save_user(user_data)
    print('Вы успешно зарегистрированы!')


def authenticate_user():
    """Авторизует пользователя, проверяя его логин и пароль."""
    print('Авторизация')
    login = input('Введите логин: ')
    password = input('Введите пароль: ')
    password_hash = hash_password(password)

    try:
        with open('database.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
            for user in users:
                if user['login'] == login and user['password'] == password_hash:
                    print('Авторизация успешна. Добро пожаловать!')
                    return True
    except FileNotFoundError:
        print('Файл с данными пользователя не найден.')
    except json.JSONDecodeError:
        print('Ошибка чтения файла с данными пользователя.')

    print('Логин или пароль неверны.')
    return False


if __name__ == "__main__":
    action = input("Вы хотите зарегистрироваться или войти? (регистрация/вход): ").lower()
    if action == "регистрация":
        register_user()
    elif action == "вход":
        authenticate_user()
    else:
        print("Неверная команда, программа завершена.")
