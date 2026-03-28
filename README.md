# 🔑 Secure Storage Extractor

Extract Android Keystore, SharedPreferences, and SQLite databases via ADB.

## Tools

| Script | Purpose |
|--------|---------|
| `shared_prefs_extract.py` | Dump SharedPreferences XML as JSON |
| `sqlite_extractor.py` | Extract SQLite databases as JSON |

## Usage

```bash
# Extract all SharedPreferences
python3 shared_prefs_extract.py --output prefs.json

# Extract app database
python3 sqlite_extractor.py --app com.example.app --output db.json
```

## Requirements

```bash
pip install pycryptodome
adb devices  # rooted device recommended
```
