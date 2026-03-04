import json
import os

def load_theme():
    theme_path = os.path.join(os.path.dirname(__file__), "theme.json")
    with open(theme_path, "r", encoding="utf-8") as fh:
        return json.load(fh)

THEME = load_theme()
