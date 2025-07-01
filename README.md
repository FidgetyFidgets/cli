# 🧩 Fidgety CLI

A fast and friendly command-line tool for inspecting, building, and extracting `.fidget` widget files. No spinning required—unless you want to.

![version](https://img.shields.io/badge/status-internal--alpha-blueviolet)  
[Download latest .exe release](https://github.com/your-username/fidgety-cli/releases/latest)

## ✨ Features

- 🔍 Inspect `.fidget` widget metadata
- 🛠 Extract embedded assets like images or audio
- 📦 Pack folders into portable `.fidget` files
- ✨ Scaffold new blank widgets
- ✅ Validate file format integrity
- 💻 Portable single `.exe` — no installer or Python required

## 📦 Installation

**Option 1:** Download the latest `.exe` from [GitHub Releases](https://github.com/your-username/fidgety-cli/releases)

**Option 2:** Run from source (requires Python 3.7+)

```
python fidgety.py inspect myWidget.fidget
```

## 🧪 Usage

```
fidgety.exe inspect myWidget.fidget
fidgety.exe extract myWidget.fidget --key=image --out=icon.png
fidgety.exe scaffold newToggle
fidgety.exe pack ./my-folder --out=bouncy.fidget
fidgety.exe validate bouncy.fidget
```

Run `--help` to see all available commands.

## 📁 Folder Packing

Use a folder like this to create a `.fidget`:

```
my-widget/
├── meta.json       # required
├── image.png       # optional
└── sound.mp3       # optional
```

Then pack it:

```
fidgety.exe pack my-widget --out widget.fidget
```

## 📌 File Format

`.fidget` files are JSON-based bundles with optional base64-encoded `image`, `sound`, and metadata fields. Some tools may also support `schemaVersion` for validation or compatibility targeting.

## 🧱 Built With

- Python 3
- Standard library only — no external dependencies required
- Optional: [`pyinstaller`](https://pyinstaller.org/) for bundling to `.exe`

## 🚀 Roadmap

- `convert` command for older `.fidget` schema migration
- `explain` to debug toggle/spring logic visually
- `devserver` or offline previewer for local dev testing

## 📣 Feedback

Found a bug? Have a feature idea?  
Open an issue or discuss it on the [GitHub repo](https://github.com/your-username/fidgety-cli).

MIT licensed. Fork it, mod it, ship it.
