
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
        print(a[:k], k, [i for i in range(n) if i not in a[:k]])
        return [i for i in range(n) if i not in a[:k]]
