
class Backtrack(object):
    def __init__(self):
        self.finished = False

    def is_a_solution(self, a, k, inp):
        pass

    def process_solution(self, a, k, inp):
        pass

    def construct_candidates(self, a, k, inp):
        pass

    def make_move(self, a, k, inp):
        pass
    
    def unmake_move(self, a, k, inp):
        pass
    
    def backtrack(self, a, k, inp):
        if self.is_a_solution(a, k, inp):
            self.process_solution(a, k, inp)
        else:
            k += 1
            candidates = self.construct_candidates(a, k, inp)
            a.append(None)
            for c in candidates:
                a[k - 1] = c
                self.make_move(a, k, inp)
                self.backtrack(a, k, inp)
                self.unmake_move(a, k, inp)
                if self.finished:
                    return


class Subsets(Backtrack):
    def __init__(self, n):
        self.finished = False
        self.n = n
        self.solutions = []
        self.backtrack([], 0, n)

    def is_a_solution(self, a, k, n):
        return k == self.n

    def construct_candidates(self, a, k, n):
        return [True, False]

    def process_solution(self, a, k, n):
        self.solutions.append(list(a[:k]))


class Permutations(Backtrack):
    def __init__(self, n):
        self.finished = False
        self.n = n
        self.solutions = []
        self.backtrack([], 0, n)

    def is_a_solution(self, a, k, n):
        return k == self.n

    def process_solution(self, a, k, n):
        self.solutions.append(list(a[:k]))

    def construct_candidates(self, a, k, n):
        return [i for i in range(n) if i not in a[:k - 1]]


class SudokuBoard(object):
    def __init__(self, dim=9, data=None):
        self.dim = dim
        # 0 not normally part of the game, will assume it means unfilled
        self.m = [[0 for i in range(dim)] for j in range(dim)]
        self.free = dim*dim
        if data:
            for r, c, v in zip(*data):
                self.m[r][c] = v
                self.free -= 1
        self.moves = [[None, None] for i in range(self.free)]
    
    def show(self):
        s = ''
        for i in range(self.dim):
            for j in range(self.dim):
                if self.m[i][j]:
                    s += str(self.m[i][j])
                else:
                    s += ' '
                s += '  '
            s += '\n'
        print(s)


class Sudoku(Backtrack):
    def __init__(self, dim=9, next_sq='constrained', poss_val='look_ahead',
                 maxsteps=None, data=None):
        self.board = SudokuBoard(dim, data)
        self.finished = False

        self.next_square = {'constrained': self.most_constrained,
                            'arbitrary': self.arbitrary_selection}[next_sq]
        self.possible_values = {'look_ahead': self.look_ahead,
                                'local_count': self.localcount}[poss_val]
        self.nsteps = 0
        self.maxsteps = maxsteps or int(1e7)
        #self.backtrack([], 0, self.board)
        self.debug = False

    def iprint(self, str):
        if self.debug:
            print(str)

    def is_a_solution(self, a, k, board):
        return board.free == 0

    def process_solution(self, a, k, board):
        self.finished = True

    def make_move(self, a, k, board):
        if self.finished:
            return
        self.nsteps += 1
        board.free -= 1
        if self.nsteps > self.maxsteps:
            self.finished = True
        x, y = board.moves[k - 1]
        board.m[y][x] = a[k - 1]

    def unmake_move(self, a, k, board):
        if self.finished:
            return
        board.free += 1
        x, y = board.moves[k - 1]
        board.m[y][x] = 0

    def most_constrained(self, a, k, board):
        rowc = [0 for i in range(board.dim)]
        colc = list(rowc)
        maxr, maxc = 0, 0
        for i in range(board.dim):
            for j in range(board.dim):
                if board.m[i][j]:
                    rowc[i] += 1
                    colc[j] += 1
        rowsort = sorted(range(board.dim), key=lambda i: rowc[i])
        colsort = sorted(range(board.dim), key=lambda i: colc[i])
        for y in rowsort[::-1]:
            for x in colsort[::-1]:
                if not board.m[y][x]:
                    return x, y 

    def arbitrary_selection(self, a, k, board):
        for i in range(board.dim):
            for j in range(board.dim):
                if not board.m[i][j]:
                    return j, i  # return first empty

    def look_ahead(self, a, k, board):
        """ First check to make sure there are no unplayable spots """
        for i in range(board.dim):
            for j in range(board.dim):
                if not board.m[i][j]:
                    if not self.localcount(a, k, board, pos=(j, i)):
                        return []
        return self.localcount(a, k, board)

    def localcount(self, a, k, board, pos=None):
        poss = [False] + [True for i in range(1, board.dim+1)]
        x, y = pos if pos else board.moves[k-1]
        # Check row
        for i in range(board.dim):
            if board.m[y][i]:
                poss[board.m[y][i]] = False
            if board.m[i][x]:
                poss[board.m[i][x]] = False
        # Check sector
        sx, sy = (x//3)*3, (y//3)*3
        for xx in range(sx, sx + 3):
            for yy in range(sy, sy + 3):
                if board.m[yy][xx]:
                    poss[board.m[yy][xx]] = False

        return [i for i, p in enumerate(poss) if p]

    def construct_candidates(self, a, k, board):
        x, y = self.next_square(a, k, board)
        if x < 0 and y < 0:
            return []  # no solutions possible
        board.moves[k - 1] = [x, y]

        self.iprint("Next move at ({}, {})".format(x, y))
        if self.debug:
            board.show()
            p = self.possible_values(a, k, board)
            self.iprint("{}: At ({}, {}) possible {}".format(k, x, y, p))

        return self.possible_values(a, k, board)

        
if __name__=='__main__':
    row = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 6, 7, 7, 8, 8]
    col = [7, 8, 4, 5, 3, 7, 0, 6, 3, 6, 0, 3, 4, 2, 7, 1, 6]
    val = [1, 2, 3, 5, 6, 7, 7, 3, 4, 8, 1, 1, 2, 7, 4, 5, 6]

    # make easier
    row += [0, 1, 2, 3, 4, 5]  # , 3, 4, 5, 7, 8]
    col += [0, 1, 2, 2, 1, 2]  # , 8, 5, 8, 5, 8]
    val += [6, 1, 5, 8, 2, 4]  # , 4, 3, 7, 6, 8]

    s = Sudoku(data=(row, col, val))
    s.board.show()
    #s.debug=True
