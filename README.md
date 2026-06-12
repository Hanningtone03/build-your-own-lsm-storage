![CI](https://github.com/Hanningtone03/build-your-own-lsm-storage/actions/workflows/ci.yml/badge.svg)

# Build Your Own LSM Storage Engine

A log-structured merge-tree storage engine in Python; the architecture behind LevelDB, RocksDB, and Cassandra.

## How it works

Writes go to a WAL first for crash safety, then into a sorted in-memory MemTable. When the MemTable fills it flushes to an immutable SSTable on disk. Reads check the MemTable then SSTables newest to oldest. Compaction merges SSTables periodically.

Complements [build-your-own-database](https://github.com/Hanningtone03/build-your-own-database); that project covers the SQL layer, this one covers how data is actually written to disk.

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
python -m src.cli put name Hanningtone
python -m src.cli get name
python -m src.cli delete name
python -m src.cli compact
```

## Tech

- Python 3
- `os`, `json` modules
- No external dependencies
