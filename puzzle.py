class Puzzle:
    def __init__(self, width, height, blocks, objective):
        self.width = width
        self.height = height
        self.blocks = blocks
        self.objective = objective

p = Puzzle(4, 5, {
    (1, 1): (2, 2),
    (3, 1): (2, 1),
    (3, 2): (2, 1),
    (1, 3): (2, 1),
    (3, 4): (2, 1),
    (3, 3): (1, 1),
    (4, 3): (1, 1),
    (3, 5): (1, 1),
    (4, 5): (1, 1)
}, (1, 1, 2, 4))

print(p.blocks)
