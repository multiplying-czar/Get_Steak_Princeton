# Firestone Library Steak Map

An interactive map of steak restaurants and raw-steak markets accessible
from Firestone Library without a car.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 firestone_steak_map.py
open index.html
```

## Publish

The generated map is stored as `index.html`, so the repository can be
published directly with GitHub Pages from the repository root.

Restaurant menus, inventory, pedestrian access, and transit schedules can
change. Verify them before traveling.
