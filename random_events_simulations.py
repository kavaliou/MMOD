from generator import MultiCongGenerator


class RandomEvent(object):
    def __init__(self, p_a):
        self.p_a = p_a
        self.random_generator = MultiCongGenerator(9929, 63018038201, 123).get_generator()

    def occurred(self):
        return next(self.random_generator) <= self.p_a
