import random


def print_board(board):
    for row in board:
        print(" ".join(row))


def generate_board(size):
    return [["O" for _ in range(size)] for _ in range(size)]


def place_ship(board, ship_size):
    direction = random.choice(["horizontal", "vertical"])
    row = random.randint(0, len(board) - 1)
    col = random.randint(0, len(board[0]) - 1)

    if direction == "horizontal" and col + ship_size <= len(board[0]):
        for i in range(ship_size):
            board[row][col + i] = "X"
    elif direction == "vertical" and row + ship_size <= len(board):
        for i in range(ship_size):
            board[row + i][col] = "X"
    else:
        place_ship(board, ship_size)


def is_valid_move(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])


def is_winner(board):
    return all(all(cell != "X" for cell in row) for row in board)


def main():
    board_size = 3
    num_ships = 3
    player_board = generate_board(board_size)
    computer_board = generate_board(board_size)

    for _ in range(num_ships):
        place_ship(player_board, 1)
        place_ship(computer_board, 1)

    while True:
        print("Ваше поле:")
        print_board(player_board)

        print("Поле компьютера:")
        print_board(computer_board)

        row = int(input("Введите номер строки: "))
        col = int(input("Введите номер столбца: "))

        if not is_valid_move(player_board, row, col):
            print("Некорректный ход. Попробуйте еще раз.")
            continue

        if computer_board[row][col] == "X":
            print("Вы попали!")
            computer_board[row][col] = "H"
            if is_winner(computer_board):
                print("Вы выиграли!")
                break
        else:
            print("Вы промахнулись!")
            computer_board[row][col] = "M"

        # Ход компьютера
        computer_row = random.randint(0, len(player_board) - 1)
        computer_col = random.randint(0, len(player_board[0]) - 1)

        print(f"Ход комьютера: {computer_row} {computer_col}")

        if player_board[computer_row][computer_col] == "X":
            print("Компьютер попал!")
            player_board[computer_row][computer_col] = "H"
            if is_winner(player_board):
                print("Вы проиграли!")
                break
        else:
            print("Компьютер промахнулся!")
            player_board[computer_row][computer_col] = "M"


if __name__ == "__main__":
    main()
