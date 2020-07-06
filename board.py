import math
import random


class Board:
    def __init__(self, size_of_board):
        self.size = size_of_board
        self.board = self.create_board()
        self.win_indexes = self.winning_indexes()
        self.winner = None
        self.winner_coords = None
        self.player = "X"
        self.opponent = "O"
        self.player_on_turn = self.player
        self.board_cache = BoardCache(size_of_board)

    def create_board(self):
        return [["-" for row in range(self.size)] for coll in range(self.size)]

    def winning_indexes(self):
        indexes = []

        for row in range(self.size):
            indexes.append([(row, coll) for coll in range(self.size)])
            indexes.append([(coll, row) for coll in range(self.size)])

        indexes.append([(i, i) for i in range(self.size)])
        indexes.append([(i, self.size - i - 1) for i in range(self.size)])

        return indexes

    def check_win_conditions(self, player, opponent):  # ked tak zefektivnit

        for indexes in self.win_indexes:
            if all("X" == self.board[r][c] for r, c in indexes):
                return player, indexes
            elif all("O" == self.board[r][c] for r, c in indexes):
                return opponent, indexes

        return False, None

    def possible_moves(self):  # OK
        cells = []

        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                if cell == "-":
                    cells.append((x, y))

        return cells

    def victory(self, player, opponent):  # OK
        win = self.check_win_conditions(player, opponent)
        possible_moves = self.possible_moves()

        if win[0]:
            self.winner = win[0]
            self.winner_coords = win[1]
            return True

        elif not possible_moves:
            self.winner = "Tie"
            return True

        return False

    def set_cell_value(self, x, y, symbol):  # OK
        if self.board[x][y] == "-":
            self.board[x][y] = symbol
            return True

        return False

    def evaluate(self, player, opponent):
        for index in self.win_indexes:
            if len(set([self.board[r][c] for r, c in index])) == 1:
                first = index[0][0]
                snd = index[0][1]
                first_symbol = self.board[first][snd]
                if first_symbol == player:
                    return 100
                elif first_symbol == opponent:
                    return -100

        # Else if none of them have won then return 0
        return 0

    def minimax(self, maxturn, player, opponent, depth, alpha, beta, avail_moves):

        score = self.evaluate(player, opponent)

        if score == 100:
            return score - depth

        if score == -100:
            return score + depth

        if not avail_moves:
            return score

        if maxturn:
            best_val = -math.inf
            for order, move in enumerate(avail_moves):
                x_coord = move[0]
                y_coord = move[1]

                self.board[x_coord][y_coord] = player
                new_moves = [*avail_moves]
                new_moves.pop(order)
                hashed_val = self.board_cache.compute_hash(self.board)
                if hashed_val in self.board_cache.cache:
                    move = self.board_cache.cache[hashed_val]
                else:
                    move = self.minimax(False, player, opponent, depth + 1, alpha, beta, new_moves)
                    self.board_cache.cache[hashed_val] = move

                best_val = max(move, best_val)
                alpha = max(alpha, best_val)

                self.board[x_coord][y_coord] = "-"

                if alpha >= beta:
                    return best_val

            return best_val

        else:
            best_val = math.inf
            for order, move in enumerate(avail_moves):
                x_coord = move[0]
                y_coord = move[1]

                self.board[x_coord][y_coord] = opponent
                new_moves = [*avail_moves]
                new_moves.pop(order)
                hashed_val = self.board_cache.compute_hash(self.board)
                if hashed_val in self.board_cache.cache:
                    move = self.board_cache.cache[hashed_val]
                else:
                    move = self.minimax(True, player, opponent, depth + 1, alpha, beta, new_moves)
                    self.board_cache.cache[hashed_val] = move

                best_val = min(move, best_val)
                beta = min(best_val, beta)

                self.board[x_coord][y_coord] = "-"

                if alpha >= beta:
                    return best_val

            return best_val

    def play_optimal_move(self, player, opponent):

        best_val = -math.inf
        coord1 = None
        coord2 = None

        alpha = -math.inf
        beta = math.inf
        avail_moves = self.possible_moves()

        for order, move in enumerate(avail_moves):
            x_coord = move[0]
            y_coord = move[1]

            self.board[x_coord][y_coord] = player
            new_moves = [*avail_moves]
            new_moves.pop(order)

            move_val = self.minimax(False, player, opponent, 0, alpha, beta, new_moves)
            self.board[x_coord][y_coord] = "-"

            if move_val > best_val:
                best_val = move_val
                coord1 = x_coord
                coord2 = y_coord

            alpha = max(alpha, best_val)
            if alpha >= beta:
                break

        return coord1, coord2


class BoardCache:
    def __init__(self, size):
        self.cache = {}
        self.zobTable = [[[random.randint(1, 2 ** 32 - 1) for i in range(2)] for j in range(size)] for k in range(size)]

    @staticmethod
    def indexing(piece):
        if piece == "X":
            return 0
        if piece == "O":
            return 1
        else:
            return -1

    def compute_hash(self, board):
        hashed_val = 0

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != "-":
                    piece = self.indexing(board[i][j])
                    hashed_val ^= self.zobTable[i][j][piece]

        return hashed_val
