import matplotlib.pyplot as plt

from generators import MiddleOfSquareGenerator, MultiCongGenerator, \
    GaussGenerator, UniformDistributionGenerator, SimpsonDistributionGenerator, \
    ExponentialDistributionGenerator, TriangularDistributionGenerator
from imitation_modeling.imitation_model import Model


def build_hist(title, numbers, m):
    plt.subplot(1, 1, 1)
    plt.title(title)
    plt.hist(numbers, m)
    plt.show()


def build_hist_from_generator(title, numbers, n, m):
    numbers = [next(numbers) for _ in xrange(n)]
    build_hist(title, numbers, m)


def calculate_ter_ver_values(numbers):
    sum_z, sum_z_square = 0, 0
    n = len(numbers)

    for that_number in numbers:
        sum_z += that_number
        sum_z_square += that_number ** 2

    m_o = float(sum_z) / n
    d = (float(sum_z_square) / n) - m_o**2
    return m_o, d


def calculate_ter_ver_values_from_generator(numbers, n):
    numbers = [next(numbers) for _ in xrange(n)]
    return calculate_ter_ver_values(numbers)


def calculate_r(numbers, n, s):
    numbers = [next(numbers) for _ in xrange(n)]
    sum = 0
    for i in xrange(n - s):
        sum += (numbers[i] * numbers[i + s])
    return (float(sum) * 12 / (n - s)) - 3


def test_discrete():
    def exponential(lamb, x):
        import math
        return (-1./lamb) * math.log(x)

    discrete(create_p(exponential), 10000)


def create_p(fun):
    my_lambda = 2
    x = 0.01
    d_x = 0.01
    current_fun = fun(my_lambda, x)

    pi = [(0.0, (0.0, current_fun))]
    while x <= 1.0:
        f = fun(my_lambda, x+d_x)
        pi.append((x, (current_fun, current_fun + f)))
        current_fun += f
        x += d_x

    maximum = pi[-1][-1][-1]
    return [(p[0], (p[1][0]/maximum, p[1][1]/maximum)) for p in pi]


def discrete(array, n):
    frequency = [0] * len(array)
    gen = UniformDistributionGenerator(0, 1)
    for i in [next(gen) for _ in xrange(n)]:
        frequency[array.index(filter(lambda (_, (mi, ma)): mi <= i <= ma, array)[0])] += 1

    previous_delta = array[0][0]
    x, y = [], []
    for q in zip(map(lambda xw: xw[0], array[1:]), frequency[:-1]):
        x.append(previous_delta)
        x.append(q[0])
        previous_delta = q[0]
        y.append(q[1])
        y.append(q[1])
    x.append(previous_delta)
    x.append(1)
    y.append(frequency[-1])
    y.append(frequency[-1])

    plt.subplot(1, 1, 1)
    axes = plt.gca()
    axes.set_xlim([0, 1])
    axes.set_ylim([0, max(*frequency)])
    plt.plot(x, y)
    plt.title('Discrete')
    plt.show()


def test_distribution_generators():
    build_hist_from_generator('Triangular', TriangularDistributionGenerator(3, 7, max), 10000, 100)
    build_hist_from_generator('Triangular', TriangularDistributionGenerator(3, 7, min), 10000, 100)

    exit()

    build_hist_from_generator('Exponential', ExponentialDistributionGenerator(1), 10000, 100)
    build_hist_from_generator('Gauss', GaussGenerator(5, 2), 10000, 100)
    build_hist_from_generator('Uniform', UniformDistributionGenerator(3, 9), 10000, 100)
    build_hist_from_generator('Simpson', SimpsonDistributionGenerator(2, 5), 10000, 100)
    build_hist_from_generator('Gauss', GaussGenerator(5, 1), 10000, 100)

    exit()

    build_hist_from_generator('Gauss', GaussGenerator(0, 0.2), 100000, 100)
    build_hist_from_generator('Gauss', GaussGenerator(0, 0.5), 100000, 100)
    build_hist_from_generator('Gauss', GaussGenerator(0, 1), 100000, 100)
    build_hist_from_generator('Gauss', GaussGenerator(-2, 5), 100000, 100)

    for i in xrange(123, 4000, 1000):
        print calculate_ter_ver_values_from_generator(MiddleOfSquareGenerator(i), 10000)
        print calculate_r(MiddleOfSquareGenerator(i), 10000, 15)
        build_hist_from_generator('Middle square method', MiddleOfSquareGenerator(i), 10000, 20)

    for i in (9929, 9059, 7873, 6949, 5791, 4547, 2287):
        print calculate_ter_ver_values_from_generator(MultiCongGenerator(i, 63018038201, 123), 63010)
        print calculate_r(MultiCongGenerator(i, 63018038201, 123), 63010, 15)
        build_hist_from_generator(
            'Multiplicative congruent method',
            MultiCongGenerator(i, 63018038201, 123),
            63010,
            20
        )


def imitation_model():
    channel_phases = [
        dict(identifier=1, hoarder_size=3, channels_size=4, distribution_class=GaussGenerator,
             distribution_arguments=dict(m=5, d=2)),
        dict(identifier=2, hoarder_size=3, channels_size=3, distribution_class=UniformDistributionGenerator,
             distribution_arguments=dict(a=3, b=9)),
        dict(identifier=3, hoarder_size=3, channels_size=5, distribution_class=SimpsonDistributionGenerator,
             distribution_arguments=dict(a=2, b=5)),
        dict(identifier=4, hoarder_size=3, channels_size=4, distribution_class=GaussGenerator,
             distribution_arguments=dict(m=5, d=1))
    ]

    channel_phases = [
        dict(identifier=1, hoarder_size=3, channels_size=4, distribution_class=GaussGenerator,
             distribution_arguments=dict(m=5, d=1)),
        dict(identifier=2, hoarder_size=3, channels_size=3, distribution_class=SimpsonDistributionGenerator,
             distribution_arguments=dict(a=2, b=5)),
        dict(identifier=3, hoarder_size=3, channels_size=5, distribution_class=TriangularDistributionGenerator,
             distribution_arguments=dict(a=3, b=7, func=min)),
        dict(identifier=4, hoarder_size=3, channels_size=4, distribution_class=GaussGenerator,
             distribution_arguments=dict(m=5, d=1)),
        dict(identifier=5, hoarder_size=3, channels_size=5, distribution_class=UniformDistributionGenerator,
             distribution_arguments=dict(a=3, b=9))
    ]

    n = 10000
    model = Model(n, channel_phases)
    model.run()

    intervals = []
    times_in_model = []
    processed_requests = model.processed_requests_watcher.get_all()
    times_in_model.append(processed_requests[0].time_in_model())
    for num, request in enumerate(processed_requests[1:]):
        times_in_model.append(request.time_in_model())
        intervals.append(request.processed_time - processed_requests[num].processed_time)

    build_hist(
        'Intervals: m={0}, d={1}'.format(*map(round, calculate_ter_ver_values(intervals), [5, 5])),
        intervals, 100
    )
    build_hist(
        'Times in model: m={0}, d={1}'.format(*map(round, calculate_ter_ver_values(times_in_model), [5, 5])),
        times_in_model, 100
    )
    print float(len(model.rejected_requests_watcher.get_all())) / n

    for phase_watcher in model.phase_watchers:
        print 'phase {id}:'.format(id=phase_watcher.phase_id)
        print '--hoarder: {0}'.format(sum(phase_watcher.hoarder_lengths) / float(phase_watcher.views))
        for identifier, state in phase_watcher.channels_states.iteritems():
            print '--channel {id}: free {free}, working {working}, blocked {blocked}'.format(
                id=identifier,
                free=state[0] / float(phase_watcher.views),
                working=state[1] / float(phase_watcher.views),
                blocked=state[2] / float(phase_watcher.views)
            )


if __name__ == '__main__':
    # test_distribution_generators()
    # exit()
    # test_discrete()
    # discrete(
    #     [
    #         (0.0, (0.0, 0.2)),
    #         (0.2, (0.2, 0.25)),
    #         (0.4, (0.25, 0.30)),
    #         (0.6, (0.30, 0.50)),
    #         (0.8, (0.50, 1)),
    #     ],
    #     10000
    # )
    # discrete(
    #     [
    #         (0.0, (0.0, 0.49)),
    #         (0.33, (0.49, 0.98)),
    #         (0.66, (0.98, 1.0)),
    #     ],
    #     10000
    # )
    imitation_model()
