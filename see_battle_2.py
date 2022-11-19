from random import randint

# Внутренняя ЛОГИКА ИГРЫ

class Point:  # создаем класс точка
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class FieldException(Exception):  # класс исключений
    pass


class FieldOutException(FieldException):  # класс исключений
    def __str__(self):
        return "Вне Зоны поражения!"


class FieldUsedException(FieldException):  # класс исключений
    def __str__(self):
        return "Точка уже поражена"


class FieldWrongShipException(FieldException):  # класс исключений
    pass


class Ship:  # создаем класс корабль
    def __init__(self, direct, ld, o):
        self.dir = direct
        self.ld = ld
        self.o = o
        self.lives = ld

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.ld):
            cur_x = self.dir.x
            cur_y = self.dir.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Point(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

 # ВНЕШНЯЯ ЛОГИКА ИГРЫ


class Field:  # создаем класс поле
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["O"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):  # раставляем корабли на  поле

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise FieldWrongShipException()  # выбрасываем исключение
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Point(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise FieldOutException()

        if d in self.busy:
            raise FieldUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "Z"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль на дне!!!")
                    return False
                else:
                    print("Есть попадание!")
                    return True

        self.field[d.x][d.y] = "."
        print("Промах!")
        return False

    def begin(self):
        self.busy = []


class Player:  # Создаем клас игрок
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except FieldException as e:
                print(e)


class AI(Player):  # Создаем класс АИ
    def ask(self):
        d = Point(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):  # создаем класс Живого игрока
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:  # проверка на координаты
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):  # проверяем ввел ли пользлватель число?
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Point(x - 1, y - 1)


class Game:  # Создаем класс игрового контроллера
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1]
        board = Field(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Point(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except FieldWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("         ИГРА      ")
        print("       морской бой    ")
        print("Корабли генерируются автоматически")
        print("------------------------")
        print("  формат ввода: x y ")
        print("  x - номер строки  ")
        print("  y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
