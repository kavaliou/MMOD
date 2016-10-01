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
