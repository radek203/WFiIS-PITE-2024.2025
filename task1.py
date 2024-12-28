class Matrix:
    mat = []

    def __init__(self, *args):
        self.mat = args

    def __add__(self, other):
        values = [(self.mat[i] + other.mat[i]) for i in range(0, 4)]
        return Matrix(*values)

    def __mul__(self, other):
        values = [(self.mat[i] * other.mat[i]) for i in range(0, 4)]
        return Matrix(*values)

    def __sub__(self, other):
        values = [(self.mat[i] - other.mat[i]) for i in range(0, 4)]
        return Matrix(*values)

    def __matmul__(self, other):
        return Matrix(
            self.mat[0] * other.mat[0] + self.mat[1] * other.mat[2],
            self.mat[0] * other.mat[1] + self.mat[1] * other.mat[3],
            self.mat[2] * other.mat[0] + self.mat[3] * other.mat[2],
            self.mat[2] * other.mat[1] + self.mat[3] * other.mat[3]
        )

    def __str__(self):
        return f"""|{self.mat[0]} {self.mat[1]}|\n|{self.mat[2]} {self.mat[3]}|"""

    def inverse(self):
        values = [self.mat[3], -self.mat[1], -self.mat[2], self.mat[0]]
        inverted = map(lambda x: (x / (self.mat[0] * self.mat[3] - self.mat[1] * self.mat[2])), values)
        return Matrix(*inverted)

    def print(self):
        print(self)
