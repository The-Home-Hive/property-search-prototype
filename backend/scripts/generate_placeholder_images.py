"""Generates the placeholder property images under backend/resources/media/.

Run from anywhere:  python backend/scripts/generate_placeholder_images.py

Pure standard library (writes SVG). Output is deterministic and committed, so
this only needs re-running when the illustrations are changed. Every property
of a given type shares that type's three images: 1 = exterior by day,
2 = exterior at golden hour, 3 = interior.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "resources" / "media" / "properties"
W, H = 800, 500

SKIES = {
    1: ("#8ec5fc", "#e0f2ff"),   # day
    2: ("#f6a86b", "#ffe8c2"),   # golden hour
}
GROUND = {1: "#7bb661", 2: "#8fa653"}

# type slug -> (wall colour, roof colour)
PALETTE = {
    "house": ("#f2e6d0", "#a4553a"),
    "villa": ("#fbf7ef", "#3f6f8f"),
    "townhouse": ("#d9c3a5", "#5b4636"),
    "bungalow": ("#e8d3c0", "#7a3e2f"),
    "apartment": ("#c9d3df", "#4a5a6e"),
    "studio-apartment": ("#d8cfe6", "#5a4f7a"),
    "office": ("#b8c7d6", "#2f4257"),
    "land": ("#000000", "#000000"),
}


def windows(x, y, cols, rows, w=34, h=44, gap=22, fill="#fff7cf"):
    return "".join(
        f'<rect x="{x + c * (w + gap)}" y="{y + r * (h + gap)}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="#3b4a5a" stroke-width="3"/>'
        for r in range(rows) for c in range(cols)
    )


def tree(x, y, s=1.0):
    return (f'<rect x="{x - 6 * s}" y="{y - 40 * s}" width="{12 * s}" height="{40 * s}" fill="#6b4a2f"/>'
            f'<circle cx="{x}" cy="{y - 62 * s}" r="{34 * s}" fill="#3f8f4a"/>')


def scene(sky, ground, body):
    top, bottom = sky
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">'
        f'<rect width="{W}" height="{H}" fill="{top}"/>'
        f'<rect y="200" width="{W}" height="160" fill="{bottom}" opacity=".6"/>'
        f'<circle cx="650" cy="90" r="42" fill="#fff6c9" opacity=".9"/>'
        f'<rect y="360" width="{W}" height="140" fill="{ground}"/>{body}</svg>'
    )


def gabled(wall, roof, w=360, floors=1, wings=False):
    x, base = (W - w) // 2, 380
    h = 110 * floors
    top = base - h
    body = f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{wall}"/>'
    body += f'<polygon points="{x - 25},{top} {x + w // 2},{top - 90} {x + w + 25},{top}" fill="{roof}"/>'
    body += windows(x + 30, top + 22, 3 if w > 300 else 2, floors, w=38, h=44, gap=(w - 60 - 114) // 2 if w > 300 else 50)
    body += f'<rect x="{W // 2 - 24}" y="{base - 70}" width="48" height="70" rx="4" fill="#6b4a2f"/>'
    if wings:
        body += f'<rect x="{x + w}" y="{base - 80}" width="120" height="80" fill="{wall}"/>'
        body += f'<rect x="{x + w + 20}" y="{base - 60}" width="30" height="40" fill="#fff7cf" stroke="#3b4a5a" stroke-width="3"/>'
    return body + tree(120, 400) + tree(700, 405, 0.9)


def tower(wall, roof, cols, floors):
    w = cols * 56 + 40
    x, base = (W - w) // 2, 400
    h = floors * 66 + 20
    body = f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" fill="{wall}" stroke="{roof}" stroke-width="4"/>'
    body += windows(x + 24, base - h + 20, cols, floors, w=32, h=38, gap=24)
    body += f'<rect x="{W // 2 - 26}" y="{base - 52}" width="52" height="52" fill="{roof}"/>'
    return body + tree(110, 410, 0.9) + tree(700, 410, 0.9)


def land():
    posts = "".join(f'<rect x="{x}" y="{y - 34}" width="6" height="34" fill="#6b4a2f"/>' for x, y in
                    [(150, 420), (300, 405), (450, 395), (600, 390)])
    rails = ('<path d="M150 400 L300 385 L450 375 L600 370" stroke="#6b4a2f" stroke-width="4" fill="none"/>'
             '<path d="M150 412 L300 397 L450 387 L600 382" stroke="#6b4a2f" stroke-width="4" fill="none"/>')
    plots = '<polygon points="140,470 640,470 600,395 190,395" fill="#a7c957" opacity=".55"/>'
    return plots + rails + posts + tree(90, 400, 1.1) + tree(720, 395, 1.0) + tree(690, 420, .7)


def exterior(slug, variant):
    wall, roof = PALETTE[slug]
    if slug == "land":
        body = land()
    elif slug in ("house", "bungalow"):
        body = gabled(wall, roof, w=360 if slug == "house" else 440, floors=2 if slug == "house" else 1)
    elif slug == "villa":
        body = gabled(wall, roof, w=400, floors=2, wings=True)
    elif slug == "townhouse":
        body = ""
        for i, dx in enumerate((110, 305, 500)):
            tint = wall if i % 2 else "#e3d2b8"
            body += (
                f'<g transform="translate({dx} 0)">'
                f'<rect y="270" width="190" height="120" fill="{tint}"/>'
                f'<polygon points="-8,270 95,220 198,270" fill="{roof}"/>'
                + windows(20, 285, 2, 1, w=34, h=40, gap=50)
                + '</g>'
            )
        body += tree(60, 410, .8)
    elif slug == "apartment":
        body = tower(wall, roof, 4, 5)
    elif slug == "studio-apartment":
        body = tower(wall, roof, 3, 4)
    else:  # office
        body = tower("#aebfcf", "#2f4257", 5, 5).replace("#fff7cf", "#9fd3ff")
    return scene(SKIES[variant], GROUND[variant], body)


def interior(slug):
    accent = PALETTE[slug][1] if slug != "land" else "#6b4a2f"
    if slug == "land":  # no interior: a survey-style plan view instead
        body = ('<rect width="800" height="500" fill="#eef3e6"/>'
                '<polygon points="150,90 650,120 690,400 120,430" fill="#c5dc9b" stroke="#5e7d2f" stroke-width="5"/>'
                '<path d="M150 260 L690 262" stroke="#5e7d2f" stroke-width="3" stroke-dasharray="14 10"/>'
                '<circle cx="400" cy="200" r="28" fill="#3f8f4a"/><circle cx="520" cy="330" r="22" fill="#3f8f4a"/>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">{body}</svg>'
    if slug == "office":
        furniture = ('<rect x="150" y="300" width="500" height="26" fill="#8a6a4a"/>'
                     '<rect x="180" y="326" width="16" height="80" fill="#5b4636"/><rect x="604" y="326" width="16" height="80" fill="#5b4636"/>'
                     '<rect x="330" y="230" width="140" height="70" rx="4" fill="#26323f"/><rect x="384" y="300" width="32" height="10" fill="#26323f"/>'
                     '<rect x="220" y="340" width="70" height="60" rx="10" fill="#4a5a6e"/><rect x="510" y="340" width="70" height="60" rx="10" fill="#4a5a6e"/>')
    else:
        furniture = (f'<rect x="150" y="290" width="330" height="90" rx="14" fill="{accent}"/>'
                     f'<rect x="150" y="260" width="330" height="50" rx="14" fill="{accent}" opacity=".85"/>'
                     '<rect x="540" y="330" width="130" height="14" fill="#8a6a4a"/><rect x="556" y="344" width="10" height="46" fill="#5b4636"/><rect x="644" y="344" width="10" height="46" fill="#5b4636"/>'
                     '<rect x="640" y="200" width="10" height="130" fill="#5b4636"/><polygon points="615,200 675,200 660,160 630,160" fill="#ffd97a"/>')
    body = ('<rect width="800" height="500" fill="#efe7db"/><rect y="400" width="800" height="100" fill="#c9a97f"/>'
            '<rect x="90" y="70" width="230" height="190" fill="#bfe3ff" stroke="#f8f8f8" stroke-width="10"/>'
            '<path d="M205 70 V260 M90 165 H320" stroke="#f8f8f8" stroke-width="8"/>'
            '<rect x="440" y="90" width="150" height="100" fill="#fff" stroke="#c9b79c" stroke-width="6"/>'
            '<polygon points="450,180 490,130 520,160 545,120 580,180" fill="#8ec5a4"/>' + furniture)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">{body}</svg>'


def main():
    for slug in PALETTE:
        folder = OUT / slug
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "1.svg").write_text(exterior(slug, 1))
        (folder / "2.svg").write_text(exterior(slug, 2))
        (folder / "3.svg").write_text(interior(slug))
    print(f"wrote {len(PALETTE) * 3} images to {OUT}")


if __name__ == "__main__":
    main()
