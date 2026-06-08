import os
import time
from .sstable import SSTable

def compact(directory="data/sstables"):
    tables = SSTable.list_all(directory)
    if len(tables) < 2:
        return

    merged = {}
    for path in tables:
        table = SSTable(path)
        data = table.read_all()
        for key, value in data.items():
            merged[key] = value

    merged = {k: v for k, v in merged.items() if v is not None}
    sorted_entries = sorted(merged.items())

    new_path = os.path.join(directory, f"{int(time.time())}_compacted.sst")
    new_table = SSTable(new_path)
    new_table.write(sorted_entries)

    for path in tables:
        os.remove(path)

    print(f"Compacted {len(tables)} SSTables into {new_path}")