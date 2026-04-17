# 🔑 Secure Storage Extractor

Extract Android Keystore and SharedPreferences for forensic analysis (root/ADB required).

## Usage
```bash
python3 extract.py --keystore --prefs --output storage.json
```

## Features
- Dumps Keystore entries (encrypted at rest)
- Extracts SharedPreferences from all apps
- JSON export for analysis
- No GUI dependencies
