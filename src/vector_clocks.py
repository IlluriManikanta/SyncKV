class VectorClock:
    def __init__(self, node_id):
        self.clock = {}
        self.node_id = node_id

    def increment(self):
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1

    def update(self, other):
        for node, time in other.items():
            self.clock[node] = max(self.clock.get(node, 0), time)

    def is_concurrent(self, other):
        greater = lesser = False
        for node in set(self.clock) | set(other):
            a = self.clock.get(node, 0)
            b = other.get(node, 0)
            if a < b:
                lesser = True
            elif a > b:
                greater = True
        return greater and lesser

    def get(self):
        return dict(self.clock)

    def set(self, new_clock):
        self.clock = dict(new_clock)
