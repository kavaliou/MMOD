from generators import GaussGenerator, SimpsonDistributionGenerator, \
    UniformDistributionGenerator, ExponentialDistributionGenerator
from imitation_modeling.helpers import RejectedRequestsWatcher, Request
from imitation_modeling.phases import InputPhase, ChannelPhase, OutputPhase


class Model(object):
    def __init__(self, number_of_requests, channel_phases, time_delta=0.01):
        self.number_of_requests = number_of_requests
        self.current_time = 0.0
        self.time_delta = time_delta
        self.phases = []
        self.rejected_requests_watcher = RejectedRequestsWatcher()

        input_phase = InputPhase(1, ExponentialDistributionGenerator, dict(lamb=1), self.rejected_requests_watcher)
        input_phase.channels[0].push_request(self.current_time, Request(self.current_time))

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
