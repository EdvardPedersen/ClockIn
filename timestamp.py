class Timestamp:
    def __init__(self, checkin_type = None, timestamp = None):
        if checkin_type:
            self.type = checkin_type
        else:
            self.type = "checkin"
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = 0
