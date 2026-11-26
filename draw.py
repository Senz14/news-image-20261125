#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world news
of Wednesday 25 November 2026. Original illustration, drawn with Pillow shapes
only -- no photographs, no copied artwork. Run: python3 draw.py"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 24, 22)
NAVY = (18, 34, 58)
RED = (172, 36, 28)
GOLD = (198, 158, 38)
GREY = (108, 106, 98)
CARD = (255, 255, 255)
RULE = (203, 195, 175)
FLAME = (226, 124, 24)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def burst(draw, cx, cy, r, col):
    """Starburst explosion: 8 spikes around a centre."""
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=col)


def mine_blast(draw, cx, cy, s, col):
    """Tanker hull under a mine explosion."""
    draw.polygon([(cx - s, cy + s * 0.3), (cx + s, cy + s * 0.3),
                  (cx + s * 0.8, cy + s * 0.65), (cx - s * 0.8, cy + s * 0.65)],
                 fill=col)
    draw.rectangle([cx - s * 0.5, cy - s * 0.2, cx - s * 0.1, cy + s * 0.3],
                   fill=col)
    burst(draw, cx + s * 0.25, cy - s * 0.55, s * 0.55, FLAME)
    draw.ellipse([cx - s * 1.05, cy - s * 0.85, cx - s * 0.75, cy - s * 0.55],
                 fill=INK)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        draw.line([(cx - s * 0.9 + dx * s * 0.22, cy - s * 0.7 + dy * s * 0.22),
                   (cx - s * 0.9 + dx * s * 0.38, cy - s * 0.7 + dy * s * 0.38)],
                  fill=INK, width=3)


def refinery(draw, cx, cy, s, col):
    """Distillation columns with a flame and a pipe."""
    draw.rectangle([cx - s * 0.85, cy - s * 0.5, cx - s * 0.45, cy + s * 0.6],
                   fill=col)
    draw.rectangle([cx - s * 0.3, cy - s * 0.85, cx + s * 0.1, cy + s * 0.6],
                   fill=col)
    draw.rectangle([cx + s * 0.25, cy - s * 0.3, cx + s * 0.65, cy + s * 0.6],
                   fill=col)
    draw.polygon([(cx - s * 0.1, cy - s * 1.25), (cx + s * 0.25, cy - s * 0.85),
                  (cx + s * 0.45, cy - s * 1.25)], fill=FLAME)
    draw.line([(cx - s * 0.85, cy + s * 0.2), (cx + s * 0.85, cy + s * 0.2)],
              fill=col, width=4)


def rocket(draw, cx, cy, s, col):
    """Rocket climbing through an orbit ring, with a star."""
    draw.ellipse([cx - s * 1.1, cy - s * 0.4, cx + s * 1.1, cy + s * 0.7],
                 outline=col, width=4)
    draw.polygon([(cx - s * 0.28, cy - s * 0.9), (cx + s * 0.28, cy - s * 0.9),
                  (cx + s * 0.28, cy + s * 0.1), (cx, cy + s * 0.45),
                  (cx - s * 0.28, cy + s * 0.1)], fill=col)
    draw.polygon([(cx - s * 0.28, cy - s * 0.1), (cx - s * 0.62, cy + s * 0.35),
                  (cx - s * 0.28, cy + s * 0.25)], fill=col)
    draw.polygon([(cx + s * 0.28, cy - s * 0.1), (cx + s * 0.62, cy + s * 0.35),
                  (cx + s * 0.28, cy + s * 0.25)], fill=col)
    draw.ellipse([cx - s * 0.14, cy - s * 0.55, cx + s * 0.14, cy - s * 0.27],
                 fill=PAPER)
    burst(draw, cx + s * 0.95, cy - s * 0.95, s * 0.22, GOLD)


def tariff(draw, cx, cy, s, col):
    """Rising bar chart with a percent sign."""
    for i, bh in enumerate([0.45, 0.75, 1.1]):
        bx = cx - s * 0.9 + i * s * 0.62
        draw.rectangle([bx, cy + s * 0.6 - bh * s, bx + s * 0.42,
                        cy + s * 0.6], fill=col)
    draw.line([(cx - s * 1.05, cy + s * 0.6), (cx + s * 1.05, cy + s * 0.6)],
              fill=INK, width=4)
    draw.text((cx + s * 0.55, cy - s * 1.15), "%", font=font(SANS_B, 44),
              fill=FLAME)


def road_fire(draw, cx, cy, s, col):
    """Flame over a highway with lane dashes."""
    draw.polygon([(cx, cy - s * 1.1), (cx + s * 0.35, cy - s * 0.5),
                  (cx + s * 0.55, cy - s * 0.7), (cx + s * 0.45, cy - s * 0.1),
                  (cx, cy + s * 0.25), (cx - s * 0.45, cy - s * 0.1),
                  (cx - s * 0.55, cy - s * 0.7), (cx - s * 0.35, cy - s * 0.5)],
                 fill=FLAME)
    draw.line([(cx - s * 1.05, cy + s * 0.5), (cx + s * 1.05, cy + s * 0.5)],
              fill=col, width=5)
    draw.line([(cx - s * 1.05, cy + s * 0.8), (cx + s * 1.05, cy + s * 0.8)],
              fill=col, width=5)
    for i in range(4):
        x = cx - s * 0.9 + i * s * 0.55
        draw.line([(x, cy + s * 0.65), (x + s * 0.3, cy + s * 0.65)],
                  fill=(255, 255, 255), width=4)


def chart_up(draw, cx, cy, s, col):
    """Rising line chart with an arrowhead and a percent sign."""
    pts = [(cx - s, cy + s * 0.55), (cx - s * 0.45, cy + s * 0.2),
           (cx + s * 0.1, cy + s * 0.35), (cx + s * 0.55, cy - s * 0.35),
           (cx + s, cy - s * 0.6)]
    draw.line(pts, fill=col, width=5, joint="curve")
    draw.polygon([(cx + s, cy - s * 0.6), (cx + s * 0.72, cy - s * 0.52),
                  (cx + s * 0.88, cy - s * 0.28)], fill=col)
    draw.line([(cx - s * 1.05, cy + s * 0.75), (cx + s * 1.05, cy + s * 0.75)],
              fill=INK, width=4)
    draw.text((cx - s * 1.05, cy - s * 1.2), "%", font=font(SANS_B, 40),
              fill=FLAME)


ICONS = [mine_blast, refinery, rocket, tariff, road_fire, chart_up]

STORIES = [
    ("STRAIT OF HORMUZ", "Two tankers explode in Hormuz",
     "Iran's Revolutionary Guard says two oil tankers struck naval mines in the strait, exploding and catching fire.",
     (14, 110, 110)),
    ("SAUDI ARABIA", "Houthis hit Saudi refinery",
     "Yemen's Houthis say they attacked Saudi Arabia's Ras Tanura refinery, causing fires; a Riyadh tower strike injured 11.",
     (150, 44, 38)),
    ("SPACE · CHINA-PAKISTAN", "Pakistan's first astronaut in orbit",
     "China's Shenzhou-24 docks at the Tiangong station carrying Muhammad Zeeshan Ali, Pakistan's first astronaut.",
     (38, 84, 124)),
    ("UNITED STATES", "Trump unveils new tariffs",
     "The White House proposes new tariffs on 14 trading partners, with an extra 20% on Chinese goods and duties on the EU and Japan.",
     (88, 96, 44)),
    ("EGYPT", "Cairo tanker fire kills 31",
     "A fuel tanker crash ignites a massive fire on a highway around Cairo, killing at least 31 people, Egypt's Health Ministry says.",
     (70, 76, 88)),
    ("US ECONOMY", "Inflation still hot at 3.8%",
     "US prices rose 3.8% in October from a year earlier, the Commerce Department reports, even as the economy grew strongly.",
     (28, 110, 66)),
]

ALSO = ("Also: Australia–Solomon Islands treaty bars foreign bases  ·  "
        "Sudan drone strikes kill 19 civilians  ·  "
        "Thanksgiving parade postponed by storm  ·  "
        "Miss Universe 2026: Jennifer Barreto")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((512, 26), "THE WORLD IN ONE DAY", font=font(SERIF_B, 52),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 88), "WEDNESDAY  ·  25 NOVEMBER 2026", font=font(SANS_B, 21),
           fill=GOLD, anchor="ma")
    d.line([(0, 118), (W, 118)], fill=GOLD, width=3)

    # Standfirst
    d.text((512, 138), "Six stories that defined the day — from the Strait of Hormuz to the Tiangong station",
           font=font(SANS, 20), fill=INK, anchor="ma")
    d.line([(28, 168), (W - 28, 168)], fill=RULE, width=2)

    # Panel grid: 2 columns x 3 rows
    mx, gap = 28, 20
    top, panel_h = 186, 238
    pw = (W - 2 * mx - gap) // 2
    for i, (kicker, headline, summary, accent) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = mx + col * (pw + gap)
        y0 = top + row * (panel_h + 18)
        x1, y1 = x0 + pw, y0 + panel_h
        d.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=2)
        d.rectangle([x0, y0, x1, y0 + 8], fill=accent)
        # Pictogram on the left of the panel's top area
        icon_cx, icon_cy = x0 + 62, y0 + 78
        d.ellipse([icon_cx - 52, icon_cy - 52, icon_cx + 52, icon_cy + 52],
                  fill=(238, 233, 220))
        ICONS[i](d, icon_cx, icon_cy + 4, 34, accent)
        # Kicker + headline to the right of the pictogram
        tx = x0 + 132
        d.text((tx, y0 + 30), kicker, font=font(SANS_B, 15), fill=accent)
        head_lines = wrap(d, headline, font(SANS_B, 25), pw - 132 - 14)
        text_block(d, (tx, y0 + 52), head_lines[:2], font(SANS_B, 25), INK, 30)
        # Summary across the full panel width below
        sum_lines = wrap(d, summary, font(SANS, 17), pw - 28)
        text_block(d, (x0 + 14, y0 + 148), sum_lines[:3], font(SANS, 17),
                   (60, 58, 52), 23)

    # Footer
    fy = top + 3 * panel_h + 2 * 18 + 14
    d.line([(28, fy), (W - 28, fy)], fill=RULE, width=2)
    also_lines = wrap(d, ALSO, font(SANS_B, 16), W - 56)
    text_block(d, (28, fy + 10), also_lines, font(SANS_B, 16), INK, 21)
    d.text((512, H - 22), "Drawn from wire reports of 25 November 2026  ·  Reuters  ·  AP  ·  The New York Times",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
