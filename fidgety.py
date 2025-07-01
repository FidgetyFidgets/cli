#!/usr/bin/env python3
import argparse, json, base64, os
from pathlib import Path

def inspect_fidget(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"\n📄 {Path(path).name}")
        print(f"   🔤 name: {data.get('name', '[none]')}")
        print(f"   🛠  type: {data.get('type', '[unknown]')}")
        for k in ("image", "sound", "meta"):
            if k in data:
                print(f"   ✅ contains: {k}")
        print(f"   📦 size: {os.path.getsize(path)} bytes\n")
    except Exception as e:
        print(f"⚠️ Failed to read {path}: {e}")

def extract_asset(path, key, out):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if key not in data:
            raise KeyError(f"'{key}' not found in {path}")
        with open(out, "wb") as out_file:
            out_file.write(base64.b64decode(data[key]))
        print(f"✅ Extracted {key} to {out}")
    except Exception as e:
        print(f"❌ Error extracting: {e}")

def scaffold_blank(name):
    obj = {
        "name": name,
        "type": "toggle",
        "image": "",  # base64-encoded placeholder
        "meta": {
            "created": "2025-07-01",
            "author": "you"
        }
    }
    path = f"{name}.fidget"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    print(f"✨ Created blank .fidget at {path}")

def validate_fidget(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"✅ JSON structure valid for {path}")
    except Exception as e:
        print(f"❌ Invalid JSON: {e}")

def pack_directory(folder, out):
    try:
        meta = Path(folder) / "meta.json"
        img  = Path(folder) / "image.png"
        snd  = Path(folder) / "sound.mp3"
        with open(meta, "r", encoding="utf-8") as f:
            data = json.load(f)
        if img.exists():
            data["image"] = base64.b64encode(img.read_bytes()).decode("utf-8")
        if snd.exists():
            data["sound"] = base64.b64encode(snd.read_bytes()).decode("utf-8")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"📦 Packed folder into {out}")
    except Exception as e:
        print(f"❌ Failed to pack: {e}")

def main():
    parser = argparse.ArgumentParser(description="Fidgety CLI — inspect, build, and edit .fidget files")
    sub = parser.add_subparsers(dest="cmd")

    i = sub.add_parser("inspect")
    i.add_argument("file")

    e = sub.add_parser("extract")
    e.add_argument("file")
    e.add_argument("--key", required=True)
    e.add_argument("--out", required=True)

    v = sub.add_parser("validate")
    v.add_argument("file")

    s = sub.add_parser("scaffold")
    s.add_argument("name")

    p = sub.add_parser("pack")
    p.add_argument("folder")
    p.add_argument("--out", required=True)

    args = parser.parse_args()

    if args.cmd == "inspect":
        inspect_fidget(args.file)
    elif args.cmd == "extract":
        extract_asset(args.file, args.key, args.out)
    elif args.cmd == "validate":
        validate_fidget(args.file)
    elif args.cmd == "scaffold":
        scaffold_blank(args.name)
    elif args.cmd == "pack":
        pack_directory(args.folder, args.out)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()