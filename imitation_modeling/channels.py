from helpers import Request


class Channel(object):
    STATE_FREE = 0
    STATE_WORKING = 1
    STATE_BLOCKED = 2

    def __init__(self, distribution_generator):
        self.generator = distribution_generator
        self.state = self.STATE_FREE
        self.work_end_time = None
        self.current_request = None

    def push_request(self, current_time, request):
        self.current_request = request
        self.calculate_work_end_time(current_time)

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
        result = self.current_request
        self.current_request = None
        return result

    def block(self):
        self.state = self.STATE_BLOCKED


class InputChannel(Channel):
    def __init__(self, distribution_generator, rejected_requests_watcher=None):
        super(InputChannel, self).__init__(distribution_generator)
        self.rejected_requests_watcher = rejected_requests_watcher

    def block(self):
        if self.rejected_requests_watcher is not None:
            self.rejected_requests_watcher.append(self.current_request)
        self.state = self.STATE_FREE
        self.push_request(self.work_end_time, Request(self.work_end_time))
