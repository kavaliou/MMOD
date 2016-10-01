class RejectedRequestsWatcher(object):
    def __init__(self):
        self.rejected_requests = []

    def append(self, time):
        self.rejected_requests.append(time)


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

