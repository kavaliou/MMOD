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
