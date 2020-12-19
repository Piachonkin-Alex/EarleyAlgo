# terminals - a-z
# non-terminals A-Z
# start - non-terminal S
# empty symbol is an empty string
class Rule:
    def __init__(self, left_side: str, right_side: str):
        self.lhs = left_side
        self.rhs = right_side


class Situation:
    def __init__(self, left_side: str, right_side: str, point_cord: int, offset: int):
        self.left_side = left_side
        self.ride_side = right_side
        self.point_cord = point_cord
        self.offset = offset

    def __hash__(self):
        return hash((self.left_side, self.ride_side, self.point_cord, self.offset))

    def __eq__(self, other):
        res = self.left_side == other.left_side and self.ride_side == other.ride_side
        return res and self.offset == other.offset and self.point_cord == other.point_cord


class EarleyParser:

    def __init__(self, rules: list):
        self.rules = []
        self.rules.append(Rule('#', 'S'))  # help rule
        self.rules += rules
        self.lists_of_situations = []
        self.word = ""

    def check(self, word: str):
        self.lists_of_situations = []
        self.word = word
        for _ in range(len(word) + 1):  # list of situation initialization
            self.lists_of_situations.append(set())
        self.lists_of_situations[0].add(Situation('#', 'S', 0, 0))  # first add
        for iteration in range(0, len(word) + 1):
            self.scan(iteration)
            sz = len(self.lists_of_situations[iteration])
            while True:
                self.complete(iteration)
                self.predict(iteration)
                if sz == len(self.lists_of_situations[iteration]):  # check changing
                    break
                else:
                    sz = len(self.lists_of_situations[iteration])
        if Situation('#', 'S', 1, 0) in self.lists_of_situations[-1]:  # finding result
            return True
        else:
            return False

    def scan(self, step):  # scan from j - 1 to j
        if step == 0:
            return
        for trans in self.lists_of_situations[step - 1]:
            if trans.point_cord < len(trans.ride_side) and trans.ride_side[trans.point_cord] == self.word[step - 1]:
                new_trans = Situation(trans.left_side, trans.ride_side, trans.point_cord + 1, trans.offset)
                self.lists_of_situations[step].add(new_trans)

    def predict(self, step):  # predict
        new = set()
        for trans in self.lists_of_situations[step]:
            if trans.point_cord == len(trans.ride_side):
                continue
            waiting_lhs = trans.ride_side[trans.point_cord]
            for rule in self.rules:
                if rule.lhs == waiting_lhs:
                    new_trans = Situation(rule.lhs, rule.rhs, 0, step)
                    new.add(new_trans)
        self.lists_of_situations[step].update(new)

    def complete(self, j):
        new = set()
        for trans in self.lists_of_situations[j]:
            if trans.point_cord < len(trans.ride_side):
                continue
            for wait_trans in self.lists_of_situations[trans.offset]:
                if wait_trans.point_cord < len(wait_trans.ride_side) and \
                        wait_trans.ride_side[wait_trans.point_cord] == trans.left_side:
                    new_trans = Situation(wait_trans.left_side, wait_trans.ride_side, wait_trans.point_cord + 1,
                                          wait_trans.offset)
                    new.add(new_trans)
        self.lists_of_situations[j].update(new)


if __name__ == '__main__':
    rules = []
    num = int(input())
    for _ in range(num):
        lhs = input()
        rhs = input()
        rules.append(Rule(lhs, rhs))
    word = input()
    print(EarleyParser(rules).check(word))
