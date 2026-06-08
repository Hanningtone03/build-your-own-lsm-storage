# Build Your Own LSM Storage Engine

A log-structured merge-tree storage engine built in Python; the same architecture used internally by LevelDB, RocksDB, and Cassandra.

## How it works

Traditional databases update data in place. LSM engines append everything to a log, buffer writes in memory, and periodically flush to disk. This makes writes extremely fast:

- All writes go to a Write-Ahead Log first — guaranteeing crash recovery
- Data is buffered in a MemTable sorted in memory
- When the MemTable is full it flushes to disk as an immutable SSTable
- Reads check the MemTable first then search SSTables newest to oldest
- Compaction periodically merges SSTables to reclaim space and speed up reads

## Project structure

```
src/
├── engine.py
├── wal.py
├── memtable.py
├── sstable.py
├── compaction.py
└── cli.py
```

## Running locally

```bash
python -m src.cli put <key> <value>
python -m src.cli get <key>
python -m src.cli delete <key>
python -m src.cli compact
```

## Example

```bash
python -m src.cli put name Hanningtone
python -m src.cli put city Nairobi
python -m src.cli get name
python -m src.cli delete city
python -m src.cli get city
```

## Tech

- Python 3
- `os`, `json` modules
- No external dependencies
