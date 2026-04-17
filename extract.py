#!/usr/bin/env python3
"""
extract.py -- Extract Android Keystore and SharedPreferences
Dumps encrypted credential storage for forensics (root required).
Usage: python3 extract.py --keystore --prefs --output creds.json
"""
import subprocess, json, sys, argparse, base64
from pathlib import Path

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def extract_keystore():
    """Extract Android Keystore entries"""
    print("  Extracting Keystore...")
    entries = []

    # List all keystore files
    files = adb("find /data/misc/keystore -type f 2>/dev/null").splitlines()
    for f in files:
        # Read file (will be encrypted in production)
        try:
            content = adb(f"cat {f}")
            entries.append({
                "path": f,
                "data": content[:100],  # First 100 chars
                "note": "Encrypted at rest on device"
            })
        except Exception:
            pass

    return entries

def extract_shared_prefs():
    """Extract SharedPreferences from apps"""
    print("  Extracting SharedPreferences...")
    prefs = {}

    # Get all apps
    apps = adb("pm list packages -3").splitlines()
    for app_line in apps[:20]:  # Limit to 20 apps for speed
        pkg = app_line.split(":")[1]
        pref_dir = f"/data/data/{pkg}/shared_prefs"

        # Check if dir exists
        exists = adb(f"test -d {pref_dir} && echo yes || echo no")
        if exists.strip() != "yes":
            continue

        # List pref files
        pref_files = adb(f"ls {pref_dir} 2>/dev/null").splitlines()
        for pf in pref_files[:5]:
            try:
                content = adb(f"cat {pref_dir}/{pf}")
                prefs[f"{pkg}/{pf}"] = content[:500]  # First 500 chars
            except Exception:
                pass

    return prefs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keystore", action="store_true", help="Extract Keystore")
    parser.add_argument("--prefs", action="store_true", help="Extract SharedPreferences")
    parser.add_argument("--output", help="JSON output file")
    args = parser.parse_args()

    if not args.keystore and not args.prefs:
        print("Usage: extract.py --keystore --prefs --output creds.json")
        sys.exit(1)

    print("\n🔑 Secure Storage Extractor")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    data = {}

    if args.keystore:
        data["keystore"] = extract_keystore()

    if args.prefs:
        data["shared_prefs"] = extract_shared_prefs()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n✅ Saved to {args.output}")
    else:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
