class ProbabilityTableColumn(object):

    def __init__(self):
        pass

class ProbabilityTable(object):

    def __init__(self, parents = []):
        self.columns = len(parents)
        self.rows = 2 ** self.columns # 2^n
        self.true_prob = float(0)
        self.false_prob = float(0)

    def __repr__(self):
        # TODO: Create a table string represntation
        pass

