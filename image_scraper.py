import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

OUTPUT_DIR = "images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ITEMS = [

# =========================
# 🇦🇺 AUSTRALIA (80)
# =========================

"bondi beach",
"manly ferry",
"uluru ayers rock",
"great barrier reef coral",
"twelve apostles victoria",
"blue mountains three sisters",
"tasmanian devil",
"wombat",
"kookaburra bird",
"cockatoo",
"frilled neck lizard",
"echidna",
"australian dollar coin",
"australian fifty dollar note",
"surf lifesaving flag",
"lifesaver tower",
"boomerang",
"op shop sign",
"milk crate",
"school hat legionnaire",
"australian street sign",
"speed camera sign australia",
"zebra crossing australia",
"roadwork witches hat",
"esky cooler",
"thongs flip flops australia",
"stubby holder",
"snag sausage",
"tomato sauce bottle",
"footy afl ball",
"cricket bat close up",
"cricket stumps",
"backyard hills hoist",
"letterbox australia",
"wheelie bin",
"recycling bin australia",
"council rubbish truck",
"bunnings sausage sizzle",
"hardware aisle",
"sausage tongs",
"emergency exit sign australia",
"school bell",
"classroom whiteboard",
"public library australia",
"university lecture hall",
"bus stop shelter australia",
"train platform australia",
"opal card",
"vline train",
"tram tracks melbourne",
"myki card",
"traffic cone australia",
"pedestrian crossing button",
"parking meter australia",
"weatherboard house",
"brick veneer house",
"tin roof australia",
"gum tree bark",
"eucalyptus leaves",
"dry creek bed",
"red dirt outback",
"beach sand close up",
"rock pool",
"tide pool algae",
"coastal cliff australia",
"fishing jetty australia",
"boat ramp",
"marina pontoon",
"suburban street australia",

# =========================
# 🇭🇰 HONG KONG (80)
# =========================

"hong kong housing estate",
"public housing corridor hong kong",
"estate playground hong kong",
"wet market stall",
"seafood tank restaurant",
"cha chaan teng interior",
"pineapple bun",
"egg tart hong kong",
"milk tea hong kong",
"soy sauce bottle chinese",
"chopsticks rest",
"rice bowl ceramic",
"street food cart hong kong",
"fish ball skewer",
"siu mai dumpling",
"steamed bun basket",
"bamboo scaffolding",
"construction netting hong kong",
"neon shop sign",
"vertical signboard",
"alleyway hong kong",
"narrow street hong kong",
"overhead footbridge",
"pedestrian subway tunnel",
"traffic light hong kong",
"crosswalk stripes hong kong",
"street name sign hong kong",
"road barrier hong kong",
"double yellow line road",
"red minibus",
"green minibus",
"public light bus sign",
"taxi roof sign hong kong",
"tram ding ding",
"tram tracks hong kong",
"ferry pier hong kong",
"pier bollard",
"harbour water wake",
"container ship",
"cargo crane",
"port container stack",
"apartment balcony hong kong",
"air conditioner window unit",
"laundry hanging outside",
"bamboo clothes pole",
"metal security gate",
"roller shutter shopfront",
"wet pavement night",
"rainy street reflection",
"typhoon signal pole",
"no swimming sign hong kong",
"lifebuoy pier",
"concrete seawall",
"rocky shoreline hong kong",
"hiking trail hong kong",
"country park sign",
"staircase hillside hong kong",
"urban hillside houses",
"cemetery hong kong",
"ancestral hall exterior",
"temple incense coils",
"temple roof ornament",
"stone lion statue",
"feng shui mirror",
"lucky red decoration",
"chinese calendar page",

# =========================
# 🌍 GLOBAL / NEUTRAL (40)
# =========================

"alarm clock close up",
"wall calendar",
"desk lamp",
"paper clip",
"binder clip",
"spiral notebook",
"graph paper",
"ballpoint pen tip",
"highlighter ink",
"whiteboard marker",
"eraser rubber",
"sticky notes stack",
"scissors handle",
"ruler markings",
"tape dispenser",
"calculator buttons",
"usb cable end",
"power plug pins",
"extension cord",
"light switch",
"door handle",
"keyring keys",
"padlock",
"zipper close up",
"fabric label tag",
"shoelace knot",
"button sewing",
"belt buckle",
"backpack zipper",
"wallet leather",
"credit card chip",
"barcode close up",
"qr code",
"price tag",
"receipt thermal paper",
"coin stack",
"glass reflection",
"window raindrops",
"shadow silhouette",
"paper texture"
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
