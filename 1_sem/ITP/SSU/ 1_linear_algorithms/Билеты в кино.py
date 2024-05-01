cinema = input('В каком кинотеатре хотите купить билеты? ')
film = input('На какой фильм хотите пойти? ')
session1, session2, session3 = '10:00', '15:00', '21:00'
session = input(f'Выберите один из сеансов:\n{session1}\n{session2}\n{session3}\n')

if session != session1 and session != session2 and session != session3:
    print('Извините, но сеанса на это время не существует.')
else:
    print(f'Вы успешно забронировали билеты в кинотеатр “{cinema}” на фильм “{film}”.\nСеанс начинается в {session}. '
          f'Приятного просмотра!')
