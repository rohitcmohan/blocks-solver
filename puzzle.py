class Puzzle:
    def __init__(self, width, height, blocks, objective):
        self.width = width
        self.height = height
        self.blocks = blocks
        self.objective = objective

    def has_point(self, x, y):
        return 1 <= x <= self.width and 1 <= y <= self.height

    def is_blocked(self, x, y):
        for k, ((x0, y0), (width, height)) in enumerate(self.blocks):
            if x0 <= x <= x0 + width - 1 and y0 <= y <= y0 + height - 1:
                return k

        return None

    def is_free(self, x, y):
        return not self.is_blocked(x, y)

    def is_solved(self):
        return self.blocks[self.objective[0]][0] == self.objective[1]

    def get_moves(self, block, visited = None):
        if visited is None: visited = [repr(self)]

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        result = []

        for dx, dy in directions:
            # Check if block can be moved in this direction

            ((x, y), (width, height)) = self.blocks[block]
            blocked = False

            for i in range(width):
                if blocked: continue

                for j in range(height):
                    pt = (x + dx + i, y + dy + j)

                    if not self.has_point(*pt) or self.is_blocked(*pt) not in [None, block]:
                        blocked = True
                        continue

            if not blocked:
                newblocks = self.blocks[:]
                newblocks[block] = ((x + dx, y + dy), (width, height))
                p = Puzzle(self.width, self.height, newblocks, self.objective)
                representation = repr(p)

                if representation not in visited:
                    result.append(p)
                    visited.append(representation)

                    # Get more moves with this block
                    result.extend(p.get_moves(block, visited))

        return result

    def get_all_moves(self):
        result = []

        for block in range(len(self.blocks)):
            result.extend(self.get_moves(block))

        return result

    def solve(self):
        def get_path(puzzle, visited):
            result = [puzzle]

            while True:
                representation = repr(puzzle)
                puzzle = visited[representation]

                if puzzle is not None:
                    result.insert(0, puzzle)
                else:
                    break

            return result

        # Use breadth-first-search to look for the solution

        queue = [self]
        visited = {repr(self): None}

        while len(queue) >= 1:
            puzzle = queue.pop()

            if puzzle.is_solved():
                return get_path(puzzle, visited)

            for p in puzzle.get_all_moves():
                representation = repr(p)

                if representation in visited:
                    continue

                visited[representation] = puzzle
                queue.insert(0, p)

        return None

    def __repr__(self):
        result = ('   ' * self.width + '\n' + ' _ ' * self.width + '\n' + '   ' * self.width + '\n') * self.height

        def pos2index(x, y):
            width = self.width * 9 + 3
            return self.width * 3 + (y - 1) * width + 3 * x - 1

        def draw_point(pic, x, y, brush):
            index = pos2index(x, y)
            return pic[:index] + brush + pic[index + 1:]

        def draw_block(pic, position, size, brush = 'X'):
            (x, y) = position
            (width, height) = size

            for i in range(width):
                for j in range(height):
                    pic = draw_point(pic, x + i, y + j, brush)

            for i in range(width):
                for k, j in enumerate([0, height - 1]):
                    index = pos2index(x + i, y + j)

                    if k == 0:
                        index -= self.width * 3 + 1
                    else:
                        index += self.width * 3 + 1

                    line = '---'

                    if 0 == width - 1:
                        line = '+-+'
                    elif i == 0:
                        line = '+--'
                    elif i == width - 1:
                        line = '--+'

                    pic = pic[:index - 1] + line + pic[index + 2:]

            for j in range(height):
                for k, i in enumerate([0, width - 1]):
                    index = pos2index(x + i, y + j)

                    if k == 0:
                        index -= 1
                    else:
                        index += 1

                    pic = pic[:index] + '|' + pic[index + 1:]

                    if j != height - 1:
                        for _ in range(2):
                            index += self.width * 3 + 1
                            pic = pic[:index] + '|' + pic[index + 1:]

            return pic

        for k, (position, size) in enumerate(self.blocks):
            brush = ' '
            if k == self.objective[0]: brush = 'X'

            result = draw_block(result, position, size, brush)

        return result

# Add blocks in this form:
#   (position, size)
#
# Objective is given in:
#   (block_index, final_position)

p = Puzzle(4, 5, [
    ((2, 1), (2, 2)),
    ((1, 1), (1, 2)),
    ((4, 1), (1, 2)),
    ((1, 3), (1, 2)),
    ((4, 3), (1, 2)),
    ((2, 3), (2, 1)),
    ((2, 4), (1, 1)),
    ((3, 4), (1, 1)),
    ((1, 5), (1, 1)),
    ((4, 5), (1, 1))
], (0, (2, 4)))

solution = p.solve()

print('Moves: ' + str(len(solution) - 1))

for q in solution:
    print(q)
    input()
