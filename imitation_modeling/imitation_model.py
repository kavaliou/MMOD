from generators import ExponentialDistributionGenerator
from imitation_modeling.channels import Channel
from imitation_modeling.helpers import RejectedRequestsWatcher, ProcessedRequestsWatcher, \
    RequestsFactory, PhaseWatcher
from imitation_modeling.phases import InputPhase, ChannelPhase, OutputPhase


class Model(object):
    def __init__(self, number_of_requests, channel_phases, time_delta=0.01):
        self.number_of_requests = number_of_requests
        self.current_time = 0.0
        self.time_delta = time_delta
        self.phases = []
        self.rejected_requests_watcher = RejectedRequestsWatcher()
        self.processed_requests_watcher = ProcessedRequestsWatcher()
        self.requests_factory = RequestsFactory(number_of_requests)
        self.phase_watchers = []

        input_phase = InputPhase(
            None, 1, ExponentialDistributionGenerator, dict(lamb=1),
            self.requests_factory, self.rejected_requests_watcher
        )
        input_phase.channels[0].push_request(
            self.current_time,
            self.requests_factory.create_request(self.current_time)
        )

        self.phases.append(input_phase)
        for channel_phase in channel_phases:
            phase_watcher = PhaseWatcher(channel_phase.get('identifier'))
            self.phase_watchers.append(phase_watcher)
            self.phases.append(ChannelPhase(channel_phase_watcher=phase_watcher, **channel_phase))
        self.phases.append(OutputPhase(None, self.processed_requests_watcher))

    def has_requests_inside(self):
        return any([any(map(lambda x: x.state != Channel.STATE_FREE, phase.channels)) for phase in self.phases[1:-1]])

    def run(self):
        while self.has_requests_inside() or self.requests_factory.need_request():
            for current_phase, previous_phase in reversed(zip(self.phases, [None] + self.phases[:-1])):
                current_phase.process(self.current_time, previous_phase)

            self.current_time += self.time_delta
