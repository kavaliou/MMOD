from generators import GaussGenerator, SimpsonDistributionGenerator, \
    UniformDistributionGenerator, ExponentialDistributionGenerator
from imitation_modeling.channels import Channel
from imitation_modeling.helpers import RejectedRequestsWatcher, RequestsFactory
from imitation_modeling.phases import InputPhase, ChannelPhase, OutputPhase


class Model(object):
    def __init__(self, number_of_requests, channel_phases, time_delta=0.01):
        self.number_of_requests = number_of_requests
        self.current_time = 0.0
        self.time_delta = time_delta
        self.phases = []
        self.rejected_requests_watcher = RejectedRequestsWatcher()
        self.requests_factory = RequestsFactory(number_of_requests)

        input_phase = InputPhase(
            1, ExponentialDistributionGenerator, dict(lamb=1),
            self.requests_factory, self.rejected_requests_watcher
        )
        input_phase.channels[0].push_request(
            self.current_time,
            self.requests_factory.create_request(self.current_time)
        )

        self.phases.append(input_phase)
        for channel_phase in channel_phases:
            self.phases.append(ChannelPhase(**channel_phase))
        self.phases.append(OutputPhase())

    def has_requests_inside(self):
        return any([any(map(lambda x: x.state != Channel.STATE_FREE, phase.channels)) for phase in self.phases[1:-1]])

    def run(self):
        while self.has_requests_inside() or self.requests_factory.need_request():
            for current_phase, previous_phase in reversed(zip(self.phases, [None] + self.phases[:-1])):
                current_phase.process(self.current_time, previous_phase)

            self.current_time += self.time_delta

        print len(self.phases[-1].responses_times)
        print len(self.rejected_requests_watcher.rejected_requests)
        # print self.phases[-1].responses_times
        # print self.rejected_requests_watcher.rejected_requests


if __name__ == '__main__':
    channel_phases = [
        dict(hoarder_size=3, channels_size=4, distribution_class=GaussGenerator,
             distribution_arguments=dict(m=5, d=2)),
        dict(hoarder_size=3, channels_size=3, distribution_class=UniformDistributionGenerator,
             distribution_arguments=dict(a=3, b=9)),
        dict(hoarder_size=3, channels_size=5, distribution_class=SimpsonDistributionGenerator,
             distribution_arguments=dict(a=2, b=5)),
        dict(hoarder_size=3, channels_size=4, distribution_class=GaussGenerator,
             distribution_arguments=dict(m=5, d=1))
    ]

    model = Model(10000, channel_phases)
    model.run()
