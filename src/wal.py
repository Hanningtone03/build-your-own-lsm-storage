import os
import json

class WAL:
    def __init__(self, path="data/wal.log"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        self.file = open(path, "a")

    def append(self, key, value):
        entry = json.dumps({"key": key, "value": value}) + "\n"
        self.file.write(entry)
        self.file.flush()
        os.fsync(self.file.fileno())

    def replay(self):
        entries = []
        if not os.path.exists(self.path):
            return entries
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries

    def clear(self):
        self.file.close()
        open(self.path, "w").close()
        self.file = open(self.path, "a")