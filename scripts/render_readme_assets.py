from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "screenshots"
BG = "#07111d"
CARD = "#102033"
CARD_ALT = "#15263c"
TEXT = "#f5eedf"
MUTED = "#afbdd0"
ACCENT = "#84cbff"
PINK = "#f6bfd8"
GREEN = "#93e3b1"
YELLOW = "#f4d07a"
RED = "#ff9d8f"
EDGE = "#2b4d74"


def f(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def rounded(draw, box, fill, outline=EDGE, width=2, radius=24):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def write(draw, xy, text, fill, size, bold=False, spacing=8):
    draw.multiline_text(xy, text, font=f(size, bold), fill=fill, spacing=spacing)


def hero():
    img = Image.new("RGB", (1600, 900), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, 1550, 860), CARD, radius=32)
    write(draw, (95, 95), "MESSAGE RETENTION GUARDIAN", ACCENT, 24)
    write(draw, (95, 155), "Retention policy, legal hold,\nand deletion pressure in one lane.", TEXT, 58, True)
    write(draw, (95, 330), "A governance service for deciding when retention windows stay on,\nwhen deletion needs to freeze, and where legal-hold scope is drifting.", MUTED, 28)
    cards = [
        ("Active policies", "5"),
        ("Legal holds", "3"),
        ("Deletion windows", "11"),
        ("Urgent risks", "2"),
    ]
    x = 95
    for label, value in cards:
        rounded(draw, (x, 450, x + 300, 620), CARD_ALT, radius=22)
        write(draw, (x + 22, 478), label.upper(), MUTED, 16)
        write(draw, (x + 22, 522), value, TEXT, 42, True)
        x += 320
    rounded(draw, (95, 680, 1505, 805), CARD_ALT, radius=22)
    write(draw, (125, 710), "CURRENT DECISION LANE", PINK, 18)
    write(draw, (125, 745), "Pause finance-message deletion jobs until the export backlog and shadow channel spread are contained.", TEXT, 26, True)
    return img


def policies():
    img = Image.new("RGB", (1600, 920), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, 1550, 880), CARD, radius=32)
    write(draw, (95, 95), "POLICY SURFACES", ACCENT, 24)
    write(draw, (95, 155), "Three retention lanes with very\ndifferent governance pressure.", TEXT, 54, True)
    items = [
        ("Finance Slack", "2555 day retention\nLegal hold enabled\nDeletion frozen", RED),
        ("HR Exchange", "2190 day retention\nDeletion scheduled\nResidency stable", YELLOW),
        ("Support Chat", "365 day retention\nDeletion scheduled\nLow queue pressure", GREEN),
    ]
    x = 95
    for title, body, color in items:
        rounded(draw, (x, 360, x + 440, 710), CARD_ALT, radius=24)
        write(draw, (x + 24, 390), title.upper(), color, 18)
        write(draw, (x + 24, 450), title, TEXT, 34, True)
        write(draw, (x + 24, 530), body, MUTED, 26)
        x += 470
    return img


def queue():
    img = Image.new("RGB", (1600, 940), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, 1550, 900), CARD, radius=32)
    write(draw, (95, 95), "REQUEST QUEUE", ACCENT, 24)
    write(draw, (95, 155), "Retention requests sorted by\nfreeze, watch, or clear.", TEXT, 54, True)
    rows = [
        ("request-7801", "Finance Slack", "Freeze", RED),
        ("request-7814", "HR Exchange", "Watch", YELLOW),
        ("request-7833", "Support Chat", "Clear", GREEN),
    ]
    y = 340
    for req_id, lane, status, color in rows:
        rounded(draw, (95, y, 1505, y + 145), CARD_ALT, radius=20)
        write(draw, (125, y + 26), req_id.upper(), MUTED, 16)
        write(draw, (125, y + 58), lane, TEXT, 30, True)
        rounded(draw, (1260, y + 42, 1460, y + 102), BG, outline=color, width=3, radius=16)
        write(draw, (1315, y + 58), status.upper(), color, 20, True)
        y += 170
    return img


def proof():
    img = Image.new("RGB", (1600, 920), BG)
    draw = ImageDraw.Draw(img)
    rounded(draw, (50, 40, 1550, 880), CARD, radius=32)
    write(draw, (95, 95), "VALIDATION PROOF", ACCENT, 24)
    write(draw, (95, 155), "Routes, scores, and next actions\nare all directly testable.", TEXT, 54, True)
    rounded(draw, (95, 340, 920, 790), "#071421", outline=EDGE, width=2, radius=24)
    write(draw, (135, 382), "> POST /api/analyze/request", GREEN, 26, True)
    write(draw, (135, 450), "{", MUTED, 24)
    write(draw, (165, 490), "\"team\": \"Finance\",", MUTED, 24)
    write(draw, (165, 530), "\"pending_deletions\": 1882,", MUTED, 24)
    write(draw, (165, 570), "\"retention_gap_days\": 14,", MUTED, 24)
    write(draw, (165, 610), "\"shadow_channels\": 4", MUTED, 24)
    write(draw, (135, 650), "}", MUTED, 24)
    rounded(draw, (980, 340, 1505, 790), CARD_ALT, radius=24)
    write(draw, (1015, 382), "ENGINE OUTPUT", PINK, 18)
    write(draw, (1015, 438), "Status: Freeze", TEXT, 34, True)
    write(draw, (1015, 500), "Risk score: 57.5", YELLOW, 30, True)
    write(draw, (1015, 570), "Next action:\nPause deletion jobs,\nlock the hold scope,\nand export the at-risk lane.", MUTED, 26)
    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, image in [
        ("01-hero.png", hero()),
        ("02-policy-surfaces.png", policies()),
        ("03-request-queue.png", queue()),
        ("04-proof.png", proof()),
    ]:
        image.save(OUT_DIR / name)


if __name__ == "__main__":
    main()

