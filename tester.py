import matplotlib.pyplot as plt

from generators import MiddleOfSquareGenerator, MultiCongGenerator, \
    GaussGenerator, UniformDistributionGenerator, SimpsonDistributionGenerator, \
    ExponentialDistributionGenerator
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


def test_distribution_generators():
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

    n = 100
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
        print '{id}:'.format(id=phase_watcher.phase_id)
        print '--hoarder: {0}'.format(sum(phase_watcher.hoarder_lengths) / float(phase_watcher.views))
        for identifier, state in phase_watcher.channels_states.iteritems():
            print '--channel {id}: free {free}, working {working}, blocked {blocked}'.format(
                id=identifier,
                free=state[0] / float(phase_watcher.views),
                working=state[1] / float(phase_watcher.views),
                blocked=state[2] / float(phase_watcher.views)
            )


if __name__ == '__main__':
    imitation_model()
