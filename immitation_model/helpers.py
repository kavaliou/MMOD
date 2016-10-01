from generators import GaussGenerator, SimpsonDistributionGenerator, \
    UniformDistributionGenerator, ExponentialDistributionGenerator


class RejectedRequestsWatcher(object):
    def __init__(self):
        self.rejected_requests = []

    def append(self, time):
        self.rejected_requests.append(time)


class Channel(object):
    STATE_FREE = 0
    STATE_WORKING = 1
    STATE_BLOCKED = 2

    def __init__(self, distribution_generator):
        self.generator = distribution_generator
        self.state = self.STATE_FREE
        self.work_end_time = None

    def calculate_work_end_time(self, current_time):
        self.state = self.STATE_WORKING
        working_time = next(self.generator)
        if working_time < 0:
            working_time = 0
        self.work_end_time = current_time + working_time

    def has_response(self, current_time):
        return self.state != self.STATE_FREE and current_time >= self.work_end_time

    def is_free(self):
        return self.state == self.STATE_FREE

    def take_away_response(self):
        self.state = self.STATE_FREE

    def block(self):
        self.state = self.STATE_BLOCKED


class InputChannel(Channel):
    def __init__(self, distribution_generator, rejected_requests_watcher=None):
        super(InputChannel, self).__init__(distribution_generator)
        self.rejected_requests_watcher = rejected_requests_watcher

    def block(self):
        if self.rejected_requests_watcher is not None:
            self.rejected_requests_watcher.append(round(self.work_end_time, 5))
        self.state = self.STATE_FREE
        self.calculate_work_end_time(self.work_end_time)


class Hoarder(object):
    def __init__(self, size):
        self.size = size
        self.requests = 0

    def inc(self):
        self.requests += 1

    def dec(self):
        self.requests -= 1

    def has_requests(self):
        return self.requests > 0

    def has_place(self):
        return self.requests < self.size


class Phase(object):
    def __init__(self, channels_size, distribution_class=None, distribution_arguments=None,
                 channel_class=None, channel_kwargs=None):
        channel_class = channel_class or Channel
        channel_kwargs = channel_kwargs or {}
        self.channels = [
            channel_class(distribution_class(**distribution_arguments), **channel_kwargs)
            for _ in xrange(channels_size)
        ]

    def get_channels_with_response(self, current_time):
        return filter(lambda channel: channel.has_response(current_time), self.channels)

    def has_channel_with_response(self, current_time):
        return len(self.get_channels_with_response(current_time)) > 0

    def get_channel_with_response(self, current_time):
        return self.get_channels_with_response(current_time)[0]

    def get_free_channels(self):
        return filter(lambda channel: channel.is_free(), self.channels)

    def process(self, current_time, previous_phase):
        raise NotImplementedError()


class InputPhase(Phase):
    def __init__(self, channels_size, distribution_class, distribution_arguments, rejected_requests_watcher=None):
        super(InputPhase, self).__init__(
            channels_size, distribution_class, distribution_arguments,
            channel_class=InputChannel, channel_kwargs=dict(rejected_requests_watcher=rejected_requests_watcher)
        )

    def process(self, current_time, previous_phase):
        for channel in self.get_free_channels():
            channel.calculate_work_end_time(current_time)


class OutputPhase(Phase):
    def __init__(self):
        super(OutputPhase, self).__init__(0)
        self.responses_times = []

    def process(self, current_time, previous_phase):
        for previous_phase_channel in previous_phase.get_channels_with_response(current_time):
            previous_phase_channel.take_away_response()
            self.responses_times.append(round(current_time, 5))


class ChannelPhase(Phase):
    def __init__(self, hoarder_size, channels_size,
                 distribution_class, distribution_arguments):
        super(ChannelPhase, self).__init__(
            channels_size, distribution_class, distribution_arguments
        )
        self.hoarder = Hoarder(hoarder_size)

    def process(self, current_time, previous_phase):
        for channel in self.get_free_channels():
            if self.hoarder.has_requests():
                channel.calculate_work_end_time(current_time)
                self.hoarder.dec()
            elif previous_phase.has_channel_with_response(current_time):
                previous_phase_channel = previous_phase.get_channel_with_response(current_time)
                channel.calculate_work_end_time(current_time)
                previous_phase_channel.take_away_response()

        for previous_phase_channel in previous_phase.get_channels_with_response(current_time):
            if self.hoarder.has_place():
                previous_phase_channel.take_away_response()
                self.hoarder.inc()
            else:
                previous_phase_channel.block()


class Model(object):
    def __init__(self, number_of_requests, channel_phases, time_delta=0.01):
        self.number_of_requests = number_of_requests
        self.current_time = 0.0
        self.time_delta = time_delta
        self.phases = []
        self.rejected_requests_watcher = RejectedRequestsWatcher()

        input_phase = InputPhase(1, ExponentialDistributionGenerator, dict(lamb=1), self.rejected_requests_watcher)
        input_phase.channels[0].calculate_work_end_time(self.current_time)

        self.phases.append(input_phase)
        for channel_phase in channel_phases:
            self.phases.append(ChannelPhase(**channel_phase))
        self.phases.append(OutputPhase())

    def run(self):
        while self.current_time <= 30:
            for current_phase, previous_phase in reversed(zip(self.phases, [None] + self.phases[:-1])):
                current_phase.process(self.current_time, previous_phase)

            self.current_time += self.time_delta

        print self.phases[-1].responses_times
        print self.rejected_requests_watcher.rejected_requests


if __name__ == '__main__':
    channel_phases = [
        dict(hoarder_size=1, channels_size=5, distribution_class=GaussGenerator,
             distribution_arguments=dict(m=5, d=2)),
        dict(hoarder_size=2, channels_size=2, distribution_class=GaussGenerator,
             distribution_arguments=dict(m=5, d=2))
    ]

    model = Model(100, channel_phases)
    model.run()
