# Map Generator

A procedural map generation tool written in Python 3.13+.

It generates deterministic maps based on a radius parameter using a CLI interface.

---

## ✨ Features

- Procedural map generation
- Seed-based deterministic output
- Radius-controlled world size
- Simple CLI interface
- Lightweight Python implementation

---

## 📦 Requirements

- Python 3.13 or newer

Install dependencies (if applicable):

```bash
pip install -r requirements.txt
```

# Usage

```
python -m cli --redius 50
```

# How it works 

The generator builds a map using a procedural pipeline:

- Define world bounds
	- A circular region is created based on the provided radius.
- Generate sample space
	- Points or grid data are created within the region.
- Construct map structure
	- Spatial relationships are computed to form regions.
- Apply procedural rules
	- Terrain or region properties are assigned algorithmically.
- Output result
	- The final map is rendered or exported depending on configuration.