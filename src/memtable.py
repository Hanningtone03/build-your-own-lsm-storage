class MemTable:
    def __init__(self, max_size=1024):
        self.data = {}
        self.max_size = max_size
        self.size = 0

    def put(self, key, value):
        if key not in self.data:
            self.size += len(key) + len(str(value))
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            self.data[key] = None

    def is_full(self):
        return self.size >= self.max_size

    def get_sorted(self):
        return sorted(self.data.items())

    def clear(self):
        self.data = {}
        self.size = 0