from imitation_modeling.channels import Channel, InputChannel
from imitation_modeling.helpers import Hoarder


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
    def __init__(self, channels_size, distribution_class, distribution_arguments,
                 requests_factory, rejected_requests_watcher=None):
        super(InputPhase, self).__init__(
            channels_size, distribution_class, distribution_arguments,
            channel_class=InputChannel,
            channel_kwargs=dict(
                requests_factory=requests_factory, rejected_requests_watcher=rejected_requests_watcher
            )
        )

    def process(self, current_time, previous_phase):
        for channel in self.get_free_channels():
            if channel.requests_factory.need_request():
                channel.push_request(current_time, channel.requests_factory.create_request(current_time))


class OutputPhase(Phase):
    def __init__(self):
        super(OutputPhase, self).__init__(0)
        self.responses_times = []

    def process(self, current_time, previous_phase):
        for previous_phase_channel in previous_phase.get_channels_with_response(current_time):
            request = previous_phase_channel.take_away_response()
            request.processed_time = current_time
            self.responses_times.append(request)


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
                request = self.hoarder.pop()
                channel.push_request(current_time, request)
            elif previous_phase.has_channel_with_response(current_time):
                previous_phase_channel = previous_phase.get_channel_with_response(current_time)
                request = previous_phase_channel.take_away_response()
                channel.push_request(current_time, request)

        for previous_phase_channel in previous_phase.get_channels_with_response(current_time):
            if self.hoarder.has_place():
                request = previous_phase_channel.take_away_response()
                self.hoarder.append(request)
            else:
                previous_phase_channel.block()
