
def board():                             # печатаем разметку поля
    print()
    print("    | 0 | 1 | 2 |")
    print("________________")
    for i, line in enumerate(markup):
        line_str = f"  {i} | {' | '.join(line)} |"
        print(line_str)
        print("_________________")


def coord():                             #  вводим координаты и проверяем
    while True:
        cords = input("         Ваш ход: ").split()

        if len(cords) != 2:
            print(" Введите 2 координаты! ")
            continue
        x, y = cords
        if not (x.isdigit()) or not (y.isdigit()):
            print(" Введите числа! ")
            continue
        x, y = int(x), int(y)
        if 0 > x or x > 2 or 0 > y or y > 2:
            print(" Координаты вне диапазона! ")
            continue

        if markup[x][y] != " ":
            print(" Клетка занята! ")
            continue

        return x, y

def win():                                  # проверка на победителя
    win_cell = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for cord in win_cell:
        symbols = []
        for b in cord:
            symbols.append(markup[b[0]][b[1]])
        if symbols == ["X", "X", "X"]:
            print("Winner X!!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Winner 0!!!")
            return True
    return False

markup = [[" "]*3 for i in range(3)]
num = 0
while True:                         # проверяем чей ход
    num += 1

    board()

    if num % 2 == 1:
        print(" Ходит Х")
    else:
        print(" Ходит 0")

    x, y = coord()

    if num % 2 == 1:
         markup[x][y] = "X"
    else:
        markup[x][y] = "0"
    if num == 9:
        print("Ни кто не выиграл!!!")
