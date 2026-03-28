#!/usr/bin/env python3
import subprocess, xml.etree.ElementTree as ET, json, sys, argparse

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def get_packages():
    out = adb("pm list packages -3")
    return [l.split(":")[1] for l in out.splitlines() if l.startswith("package:")]

def extract_prefs(pkg):
    prefs_dir = f"/data/data/{pkg}/shared_prefs"
    files = adb(f"ls {prefs_dir} 2>/dev/null || echo ''")
    if not files:
        return {}
    result = {}
    for fname in files.split("\n"):
        if not fname.endswith(".xml"):
            continue
        fpath = f"{prefs_dir}/{fname}"
        content = adb(f"cat {fpath} 2>/dev/null")
        if not content:
            continue
        try:
            root = ET.fromstring(content)
            prefs = {}
            for elem in root:
                key = elem.get("name")
                if elem.tag == "string": prefs[key] = elem.text or ""
                elif elem.tag == "int": prefs[key] = int(elem.get("value", 0))
                elif elem.tag == "boolean": prefs[key] = elem.get("value") == "true"
            result[fname.replace(".xml", "")] = prefs
        except:
            pass
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--app")
    parser.add_argument("--output")
    args = parser.parse_args()
    packages = [args.app] if args.app else get_packages()
    all_prefs = {}
    for pkg in packages:
        prefs = extract_prefs(pkg)
        if prefs:
            all_prefs[pkg] = prefs
            print(f"  ✓ {pkg.split('.')[-1]}")
    if args.output:
        with open(args.output, "w") as f:
            json.dump(all_prefs, f, indent=2)
    else:
        print(json.dumps(all_prefs, indent=2))

if __name__ == "__main__":
    main()
