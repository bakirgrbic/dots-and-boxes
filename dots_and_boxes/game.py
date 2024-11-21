BOX_MASK = 0b0000_0000_1111_0000

PLAYER_ONE = 9
PLAYER_TWO = 8

LEFT = 3
TOP = 2
RIGHT = 1
BOTTOM = 0


class GameInfo:
    def __init__(self):
        self.score = [0, 0]
        self.turn = PLAYER_ONE
        self.finished = False

    def get_points(self):
        return self.score[PLAYER_ONE - self.turn]

    def get_player_one_points(self):
        return self.score[0]

    def get_player_two_points(self):
        return self.score[1]


class Board:
    def __init__(self):
        self.layout = [
            204, 68, 68, 68, 68, 68, 68, 68, 68, 102, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 136, 0,
            0, 0, 0, 0, 0, 0, 0, 34, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 136, 0, 0, 0, 0, 0, 0, 0,
            0, 34, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 136, 0, 0,
            0, 0, 0, 0, 0, 0, 34, 136, 0, 0, 0, 0, 0, 0, 0, 0, 34, 153, 17, 17, 17, 17, 17, 17,
            17, 17, 51,
        ]

    def set_bit(self, row, column, shift):
        self.layout[row * 10 + column] |= 1 << shift

    def get_bit(self, row, column, shift):
        return (self.layout[row * 10 + column] & (1 << shift)) > 0


class DotsAndBoxesGame:
    def __init__(self):
        self.board = Board()
        self.game_info = GameInfo()
        self.legal_moves = set(filter(lambda line: self.is_possible(line), range(200)))

    def get_line(self, num, player):
        box_num = num // 2
        row = box_num // 10
        col = box_num % 10
        side = num % 2
        return self._get_line_by(row, col, side, player)

    def _get_line_by(self, row, column, side, player):
        return self.board.get_bit(row, column, side + (4 * (player % 2)))

    def set_line(self, num, player):
        box_num = num // 2
        row = box_num // 10
        col = box_num % 10
        side = num % 2
        self.legal_moves.remove(num)
        self._set_line_by(row, col, side, player)

    def _set_line_by(self, row, column, side, player):
        self.board.set_bit(row, column, side + (4 * (player % 2)))
        self.check_box(row, column, player)

        horizontal = 1 - side % 2
        h_amount = -1 * side + 1
        vertical = side % 2
        v_amount = -1 * side + 2

        extra_row = row + (horizontal * h_amount)
        extra_column = column + (vertical * v_amount)
        extra_side = side + (horizontal * (2 * h_amount) + (vertical * (2 * v_amount)))

        self.board.set_bit(extra_row, extra_column, extra_side + (4 * (player % 2)))
        self.check_box(extra_row, extra_column, player)

        self.game_info.turn = 9 - (self.game_info.turn % PLAYER_TWO)

    def check_box(self, row, column, player):
        if (self.board.layout[10 * row + column] & BOX_MASK) | \
           ((self.board.layout[10 * row + column] << 4) & BOX_MASK) == BOX_MASK:
            self.board.set_bit(row, column, player)
            self.game_info.score[PLAYER_ONE - player] += 1
            self.game_info.turn = 9 - (player % PLAYER_TWO)

    def is_possible(self, line):
        return not (self.get_line(line, PLAYER_ONE) or self.get_line(line, PLAYER_TWO))
    