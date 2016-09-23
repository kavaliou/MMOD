import matplotlib.pyplot as plt

from generator import MiddleOfSquareGenerator, MultiCongGenerator


def build_hist(title, numbers, n, m):
    plt.subplot(1, 1, 1)
    plt.title(title)
    numbers = [next(numbers) for _ in xrange(n)]
    plt.hist(numbers, m)
    plt.show()


def calculate_ter_ver_values(numbers, n):
    sum_z, sum_z_square = 0, 0

    for _ in xrange(n):
        that_number = next(numbers)
        sum_z += that_number
        sum_z_square += that_number ** 2

    m_o = float(sum_z) / n
    d = (float(sum_z_square) / n) - m_o**2
    return m_o, d


def calculate_r(numbers, n, s):
    numbers = [next(numbers) for _ in xrange(n)]
    sum = 0
    for i in xrange(n - s):
        sum += (numbers[i] * numbers[i + s])
    return (float(sum) * 12 / (n - s)) - 3


# MiddleOfSquareGenerator 123 1123 3123
if __name__ == '__main__':
    for i in xrange(123, 4000, 1000):
        print calculate_ter_ver_values(MiddleOfSquareGenerator(i).get_generator(), 10000)
        print calculate_r(MiddleOfSquareGenerator(i).get_generator(), 10000, 15)
        build_hist('Middle square method', MiddleOfSquareGenerator(i).get_generator(), 10000, 20)

    for i in (9929, 9059, 7873, 6949, 5791, 4547, 2287):
        print calculate_ter_ver_values(MultiCongGenerator(i, 63018038201, 123).get_generator(), 63010)
        print calculate_r(MultiCongGenerator(i, 63018038201, 123).get_generator(), 63010, 15)
        build_hist(
            'Multiplicative congruent method',
            MultiCongGenerator(i, 63018038201, 123).get_generator(),
            63010,
            20
        )
