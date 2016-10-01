class RejectedRequestsWatcher(object):
    def __init__(self):
        self.rejected_requests = []

    def append(self, time):
        self.rejected_requests.append(time)


class Request(object):
    def __init__(self, initial_time):
        self.initial_time = initial_time
        self.processed_time = None

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
