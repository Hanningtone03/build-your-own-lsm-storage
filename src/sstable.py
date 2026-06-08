import os
import json

class SSTable:
    def __init__(self, path):
        self.path = path

    def write(self, sorted_entries):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            for key, value in sorted_entries:
                f.write(json.dumps({"key": key, "value": value}) + "\n")

    def read_all(self):
        entries = {}
        if not os.path.exists(self.path):
            return entries
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    entries[entry["key"]] = entry["value"]
        return entries

    def get(self, key):
        if not os.path.exists(self.path):
            return None
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    if entry["key"] == key:
                        return entry["value"]
        return None

    @staticmethod
    def list_all(directory="data/sstables"):
        if not os.path.exists(directory):
            return []
        return sorted([
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.endswith(".sst")
        ])