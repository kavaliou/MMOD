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
