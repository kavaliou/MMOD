class GeneratorMixin(object):
    def get_generator(self):
        while True:
            yield self.next_number()


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
            MultiCongGenerator(num, 63018038201, 3018038 + i).get_generator()
            for i, num in enumerate([
                9929, 6301803820, 8038206301, 27751, 93563, 93277513,
                9921, 6303820, 88206301, 271, 9563, 937513
            ])
        ]
        self.n = n

    def next_number(self):
        sum_r = sum(map(next, self.R))
        return self.m + (self.d * (12/self.n)**0.5 * (sum_r - self.n/2))
