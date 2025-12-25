import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

OUTPUT_DIR = "images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ITEMS = [

    # 👶 Kids (AU + HK)
    "bluey",
    "peppa pig",
    "pikachu",
    "mario",
    "minions",
    "spider man",
    "elsa frozen",
    "lightning mcqueen",
    "mickey mouse",
    "hello kitty",
    "winnie the pooh",
    "sonic the hedgehog",
    "among us crewmate",
    "lego minifigure",
    "teddy bear",
    "balloon",
    "ice cream",
    "school bus",
    "soccer ball",
    "birthday cake",

    # 🧒 Shared brands & objects (kids → teens)
    "mcdonalds logo",
    "kfc logo",
    "coca cola logo",
    "youtube logo",
    "netflix logo",
    "disney logo",
    "pokemon pokeball",
    "nintendo switch",
    "ipad",
    "backpack",
    "playground slide",
    "traffic light",
    "bus stop sign",

    # 🧑 Teenagers
    "tiktok logo",
    "instagram logo",
    "snapchat logo",
    "spotify logo",
    "airpods",
    "iphone camera",
    "gaming controller",
    "playstation logo",
    "nike swoosh",
    "adidas logo",
    "supreme logo",
    "vr headset",
    "mechanical keyboard",
    "rgb gaming mouse",
    "anime eyes",
    "manga panel",
    "concert crowd",
    "basketball hoop",

    # 🇦🇺 Australian icons (teens + adults)
    "sydney opera house",
    "sydney harbour bridge",
    "kangaroo",
    "koala",
    "emu",
    "vegemite jar",
    "tim tam",
    "meat pie",
    "lamington cake",
    "waratah flower",
    "australian flag",
    "aboriginal flag",
    "akubra hat",
    "bunnings warehouse sign",
    "woolworths logo",
    "coles logo",
    "australia post logo",
    "qantas kangaroo",
    "holden badge",

    # 🧑 Adults (Australia-leaning)
    "newspaper front page",
    "coffee cup flat white",
    "wine glass",
    "bbq grill",
    "lawn mower",
    "power drill",
    "garden hose",
    "sunglasses",
    "wristwatch",
    "car steering wheel",
    "office keyboard",
    "calculator",
    "shopping receipt",
    "supermarket aisle",
    "petrol pump",

    # 🌏 Hong Kong specific
    "hong kong skyline",
    "star ferry hong kong",
    "hong kong double decker bus",
    "mtr train",
    "octopus card",
    "dim sum basket",
    "bubble tea",
    "hong kong red taxi",
    "lion dance costume",
    "neon chinese sign",
    "hong kong flag",

    # 🎯 Texture / zoom-friendly items (great clues)
    "animal fur close up",
    "lego studs close up",
    "fabric weave close up",
    "brick wall texture",
    "shoe sole tread",
    "keyboard key close up",
    "printed text close up",
    "fruit skin texture",
    "chocolate texture",
    "ice cream sprinkles",
    "wood grain texture"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

def title_case(name):
    return re.sub(r"\s+", " ", name.title()).strip()

def download(url, path):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    with open(path, "wb") as f:
        f.write(r.content)

def fetch_best_image(query):
    search_url = (
        "https://www.bing.com/images/search?q="
        + quote(query)
        + "&form=HDRSC2"
    )

    html = requests.get(search_url, headers=HEADERS, timeout=20).text
    soup = BeautifulSoup(html, "html.parser")

    images = []
    for tag in soup.select("a.iusc"):
        try:
            meta = json.loads(tag.get("m"))
            images.append(meta)
        except:
            continue

    if not images:
        return None

    # Pick highest resolution
    best = max(
        images,
        key=lambda m: m.get("ow", 0) * m.get("oh", 0)
    )

    return best.get("murl")

def main():
    for item in ITEMS:
        print(f"Searching: {item}")
        try:
            url = fetch_best_image(item)
            if not url:
                print("  ❌ No image found")
                continue

            filename = title_case(item) + ".jpg"
            path = os.path.join(OUTPUT_DIR, filename)
            download(url, path)
            print(f"  ✅ Saved {filename}")

        except Exception as e:
            print(f"  ⚠️ Failed: {e}")

if __name__ == "__main__":
    main()
