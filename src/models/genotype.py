class Genotype:

    def __init__(self):
        self.gen_color: tuple[int, int, int, int] = (0, 0, 0, 0)
        self.gen_triangle: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] = ((0, 0), (0, 0), (0, 0))