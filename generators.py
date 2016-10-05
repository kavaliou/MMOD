from random import randint
import math

from primesieve import nth_prime


class GeneratorMixin(object):
    def __iter__(self):
        return self

    def next(self):
        return self.next_number()


class MiddleOfSquareGenerator(GeneratorMixin):
    def __init__(self, initial_number):
        self.initial_number = initial_number
        self.current_number = initial_number

    def next_number(self):
        self.current_number *= self.current_number
        self.current_number = int((str(self.current_number).ljust(8, '0'))[2:-2])
        return float(self.current_number) / 9999


class MultiCongGenerator(GeneratorMixin):
    def __init__(self, k, m, a0):
        self.k = k
        self.m = m
        self.a = a0

    def next_number(self):
        self.a = (self.k * self.a) % self.m
        return float(self.a) / self.m


class GaussGenerator(GeneratorMixin):
    def __init__(self, m, d, n=12):
        self.m = m
        self.d = d
        self.R = [
            MultiCongGenerator(
                nth_prime(randint(1000, 10000000)),
                63018038201,
                nth_prime(randint(10000, 100000))
            ) for _ in range(n)
        ]
        self.n = n

    def next_number(self):
        sum_r = sum(map(next, self.R))
        return self.m + (self.d * (12/self.n)**0.5 * (sum_r - self.n/2))


class UniformDistributionGenerator(GeneratorMixin):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.R = MultiCongGenerator(
            nth_prime(randint(1000, 10000000)),
            63018038201,
            nth_prime(randint(10000, 100000))
        )

    def next_number(self):
        return self.a + (self.b - self.a) * next(self.R)


class SimpsonDistributionGenerator(GeneratorMixin):
    def __init__(self, a, b):
        self.R = [UniformDistributionGenerator(a/2., b/2.) for _ in range(2)]

    def next_number(self):
        return sum(map(next, self.R))


class ExponentialDistributionGenerator(GeneratorMixin):
    def __init__(self, lamb):
        self.lamb = lamb
        self.R = UniformDistributionGenerator(0, 1)

    def next_number(self):
        return (-1./self.lamb) * math.log(next(self.R))


class TriangularDistributionGenerator(GeneratorMixin):
    def __init__(self, a, b, func):
        self.func = func
        self.a = a
        self.b = b
        self.R = [UniformDistributionGenerator(0, 1) for _ in xrange(2)]

    def next_number(self):
        return self.a + (self.b - self.a) * self.func(*map(next, self.R))
