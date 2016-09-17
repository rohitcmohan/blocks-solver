class Puzzle:
    def __init__(self, width, height, blocks, objective):
        self.width = width
        self.height = height
        self.blocks = blocks
        self.objective = objective

    def is_blocked(self, x, y):
        for (x0, y0), (width, height) in self.blocks:
            if x0 <= x <= x0 + width - 1 and y0 <= y <= y0 + height - 1:
                return (x0, y0)

        return None

    def is_free(self, x, y):
        return not self.is_blocked(x, y)

    def is_solved(self):
        return self.blocks[self.objective[0]][0] == self.objective[1]

    def __repr__(self):
        result = ('   ' * self.width + '\n' + ' _ ' * self.width + '\n' + '   ' * self.width + '\n') * self.height
        brushes = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        i = 0

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

                    if 0 == width - 1:
                        pic = pic[:index - 1] + '+-+' + pic[index + 2:]
                    elif i == 0:
                        pic = pic[:index - 1] + '+--' + pic[index + 2:]
                    elif i == width - 1:
                        pic = pic[:index - 1] + '--+' + pic[index + 2:]
                    else:
                        pic = pic[:index - 1] + '---' + pic[index + 2:]

            for j in range(height):
                for k, i in enumerate([0, width - 1]):
                    index = pos2index(x + i, y + j)

                    if k == 0:
                        index -= 1
                    else:
                        index += 1

                    pic = pic[:index] + '|' + pic[index + 1:]

                    if j != height - 1:
                        index += self.width * 3 + 1
                        pic = pic[:index] + '|' + pic[index + 1:]

                        index += self.width * 3 + 1
                        pic = pic[:index] + '|' + pic[index + 1:]

            return pic

        for position, size in self.blocks:
            result = draw_block(result, position, size, brushes[i])
            i += 1

        return result

p = Puzzle(4, 5, [
    ((1, 1), (2, 2)),
    ((3, 1), (2, 1)),
    ((3, 2), (2, 1)),
    ((1, 3), (2, 1)),
    ((3, 4), (2, 1)),
    ((3, 3), (1, 1)),
    ((4, 3), (1, 1)),
    ((3, 5), (1, 1)),
    ((4, 5), (1, 1)),
    ((1, 4), (1, 2))
], (0, (2, 4)))

print(p)
print(p.is_blocked(2, 4))
print(p.is_blocked(3, 4))
print(p.is_solved())
