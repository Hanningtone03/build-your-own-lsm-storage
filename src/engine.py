import os
import time
from .wal import WAL
from .memtable import MemTable
from .sstable import SSTable
from .compaction import compact

class Engine:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.sstable_dir = os.path.join(data_dir, "sstables")
        os.makedirs(self.sstable_dir, exist_ok=True)
        self.wal = WAL(os.path.join(data_dir, "wal.log"))
        self.memtable = MemTable()
        self._recover()

    def _recover(self):
        entries = self.wal.replay()
        for entry in entries:
            self.memtable.put(entry["key"], entry["value"])
        print(f"Recovered {len(entries)} entries from WAL")

    def put(self, key, value):
        self.wal.append(key, value)
        self.memtable.put(key, value)
        if self.memtable.is_full():
            self._flush()

    def get(self, key):
        value = self.memtable.get(key)
        if value is not None:
            return None if value == "<<deleted>>" else value
        for path in reversed(SSTable.list_all(self.sstable_dir)):
            table = SSTable(path)
            value = table.get(key)
            if value is not None:
                return None if value == "<<deleted>>" else value
        return None

    def delete(self, key):
        self.wal.append(key, "<<deleted>>")
        self.memtable.delete(key)

    def _flush(self):
        path = os.path.join(self.sstable_dir, f"{int(time.time())}.sst")
        table = SSTable(path)
        table.write(self.memtable.get_sorted())
        self.memtable.clear()
        self.wal.clear()
        print(f"Flushed memtable to {path}")
        if len(SSTable.list_all(self.sstable_dir)) >= 3:
            compact(self.sstable_dir)

    def compact(self):
        compact(self.sstable_dir)