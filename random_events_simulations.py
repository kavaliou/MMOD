from sys import argv
from datetime import datetime

from generator import MultiCongGenerator


class RandomEvent(object):
    def __init__(self, p_a):
        self.p_a = p_a
        self.random_generator = MultiCongGenerator(datetime.now().microsecond % 63018038201, 63018038201, 123) \
            .get_generator()

    def occurred(self):
        return next(self.random_generator) <= self.p_a


class ComplexRandomEvent(object):
    def __init__(self, p_a, p_b):
        self.p_a = p_a
        self.p_b = p_b
        self.first_random_generator = MultiCongGenerator(datetime.now().microsecond % 63018038201, 63018038201, 123) \
            .get_generator()
        self.second_random_generator = MultiCongGenerator(datetime.now().microsecond % 63018038201, 63018038201, 123) \
            .get_generator()

    def occurred(self):
        return next(self.first_random_generator) <= self.p_a and next(self.second_random_generator) <= self.p_b


def gen_random_event(p_a=0.5, count=100000):
    random_event = RandomEvent(p_a)
    t = 0
    for i in xrange(count):
        t += int(random_event.occurred())
    return t


def gen_complex_random_event(p_a=0.5, p_b=0.5, count=100000):
    random_event = ComplexRandomEvent(p_a, p_b)
    t = 0
    for i in xrange(count):
        t += int(random_event.occurred())
    return t


if __name__ == '__main__':
    # print gen_random_event(*map(float, argv[1:]))
    print gen_complex_random_event(*map(float, argv[1:]))
