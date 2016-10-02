class PhaseWatcher(object):
    def __init__(self, identifier):
        self.phase_id = identifier
        self.hoarder_lengths = []
        self.channels_states = {}
        self.views = 0

    def init(self, channels_ids):
        for identifier in channels_ids:
            self.channels_states[identifier] = {
                0: 0,
                1: 0,
                2: 0
            }


class RequestsWatcher(object):
    def __init__(self):
        self.requests = []

    def append(self, request):
        self.requests.append(request)

    def get_all(self):
        return self.requests


class RejectedRequestsWatcher(RequestsWatcher):
    pass


class ProcessedRequestsWatcher(RequestsWatcher):
    pass


class Request(object):
    def __init__(self, initial_time):
        self.initial_time = initial_time
        self.processed_time = None

    def time_in_model(self):
        return self.processed_time - self.initial_time

    def __repr__(self):
        return 'Request: %s' % unicode(self)

    def __unicode__(self):
        return '%s - %s' % (self.initial_time, self.processed_time)


class RequestsFactory(object):
    def __init__(self, max_requests_count=None):
        self.max_requests_count = max_requests_count
        self.requests_count = 0

    def need_request(self):
        return self.max_requests_count is None or self.requests_count < self.max_requests_count

    def create_request(self, time):
        self.requests_count += 1

        print self.requests_count

        return Request(time)


class Hoarder(object):
    def __init__(self, size):
        self.size = size
        self.requests = []

    def append(self, request):
        self.requests.append(request)

    def pop(self):
        return self.requests.pop(0)

    def has_requests(self):
        return len(self.requests) > 0

    def has_place(self):
        return len(self.requests) < self.size

    def __len__(self):
        return len(self.requests)
