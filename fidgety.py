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
        print(f"   🧬 schemaVersion: {data.get('schemaVersion', '1 (implicit)')}")
        for key in ("image", "sound", "meta"):
            if key in data:
                print(f"   ✅ contains: {key}")
        print(f"   📦 size: {os.path.getsize(path)} bytes\n")
    except Exception as e:
        print(f"⚠️ Failed to read {path}: {e}")

def extract_asset(path, key, out):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if key not in data:
            raise KeyError(f"'{key}' not found in {path}")
        content = base64.b64decode(data[key])
        with open(out, "wb") as out_file:
            out_file.write(content)
        print(f"✅ Extracted '{key}' to {out}")
    except Exception as e:
        print(f"❌ Error: {e}")

def scaffold_blank(name):
    obj = {
        "name": name,
        "type": "toggle",
        "image": "",  # base64 image content goes here
        "meta": {
            "created": "2025-07-01",
            "author": "you"
        },
        "schemaVersion": 1
    }
    output = f"{name}.fidget"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    print(f"✨ Created new .fidget scaffold at {output}")

def validate_fidget(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"✅ JSON structure valid in {path}")
    except Exception as e:
        print(f"❌ Invalid JSON: {e}")

def pack_directory(folder, out):
    try:
        base = Path(folder)
        with open(base / "meta.json", "r", encoding="utf-8") as f:
            obj = json.load(f)
        for field, filename in [("image", "image.png"), ("sound", "sound.mp3")]:
            asset_path = base / filename
            if asset_path.exists():
                with open(asset_path, "rb") as b:
                    obj[field] = base64.b64encode(b.read()).decode("utf-8")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)
        print(f"📦 Packed {folder} → {out}")
    except Exception as e:
        print(f"❌ Packing failed: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="🧩 Fidgety CLI – build, inspect, and unpack .fidget widget files",
        epilog="""
📚 EXAMPLES:
  fidgety.py inspect myWidget.fidget
  fidgety.py scaffold coolSpin
  fidgety.py extract myWidget.fidget --key=image --out=logo.png
  fidgety.py pack ./src/clicktoggle --out=click.fidget
  fidgety.py validate anything.fidget
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    sub = parser.add_subparsers(dest="cmd")

    inspect = sub.add_parser("inspect", help="Inspect a .fidget file's metadata and structure")
    inspect.add_argument("file")

    extract = sub.add_parser("extract", help="Extract embedded image or sound from a .fidget file")
    extract.add_argument("file")
    extract.add_argument("--key", required=True, help="Name of field to extract (e.g. image, sound)")
    extract.add_argument("--out", required=True, help="Output file path")

    validate = sub.add_parser("validate", help="Validate the structure of a .fidget file")
    validate.add_argument("file")

    scaffold = sub.add_parser("scaffold", help="Create a blank .fidget scaffold")
    scaffold.add_argument("name", help="Name to use for the new .fidget file")

    pack = sub.add_parser("pack", help="Bundle assets from a folder into a .fidget")
    pack.add_argument("folder", help="Folder containing meta.json and optional image/sound")
    pack.add_argument("--out", required=True, help="Destination .fidget filename")

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
