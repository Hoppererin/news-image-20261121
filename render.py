#!/usr/bin/env python3
"""Render entry.png for news-image-20261121 — "The World Today".

46 real stories from 7 regions, reported 20-21 November 2026, drawn as a
newspaper front page. Deterministic: fixed text, fixed geometry, no network,
no randomness, no timestamps — re-running writes byte-identical bytes.
Python 3 + Pillow, DejaVu fonts (system). Run: python3 render.py
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 253, 248)
INK = (17, 17, 17)
MUTED = (90, 90, 90)
RULE = (180, 180, 170)
CARD_BG = (255, 255, 255)
CARD_LINE = (205, 205, 195)
LEAD_BG = (234, 240, 247)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, fpath, size, max_w, min_size=10):
    """Largest font size <= size that fits max_w, else the text truncated."""
    s = size
    while s > min_size:
        f = font(fpath, s)
        if draw.textlength(text, font=f) <= max_w:
            return f, text
        s -= 1
    f = font(fpath, min_size)
    while text and draw.textlength(text + "\u2026", font=f) > max_w:
        text = text[:-1]
    return f, text + "\u2026"


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- data
LEAD_TAG = "LEAD  \u2014  SHENZHEN, CHINA"
LEAD_HEAD = "Trump, Xi and Putin: a nuclear war \u201ccannot be won\u201d"
LEAD_BODY = "First-ever trilateral summit at the APEC meeting signs a four-point peace declaration; Ukraine and nuclear arms top the agenda.  (WSJ \u00b7 Reuters)"

MAJORS = [
    ("UKRAINE", (192, 0, 0),
     "Russia\u2019s biggest air assault of the war hits Kyiv",
     "400+ drones and 110+ missiles; 8 killed; three Dnipro bridges struck. (Reuters)"),
    ("EUROPE", (112, 48, 160),
     "EU and UK seal Brexit reset in Brussels",
     "Youth mobility for 100,000; food checks end; \u00a317bn boost claimed. (The Times)"),
    ("ASIA", (191, 144, 0),
     "Cyclone Akvan slams India\u2019s east coast",
     "80,000 evacuated in Odisha; third cyclone in a month; 70\u201380 kph winds. (Reuters)"),
    ("MARKETS", (11, 83, 148),
     "Anthropic\u2019s record IPO can\u2019t stop the slide",
     "$81.3bn debut pops 17%, then falls; S&P \u22122%, Dow \u22121,101. (WSJ)"),
    ("JUSTICE", (46, 125, 50),
     "World Court: Myanmar committed genocide",
     "ICJ rules against Myanmar over the Rohingya \u2014 a first against a state. (UN News)"),
    ("CLIMATE", (0, 131, 143),
     "COP31 draft drops fossil fuels",
     "Antalya text omits phase-out; 1.5\u00b0C overshoot admitted; talks overtime. (UN News)"),
]

BRIEFS = [
    ("NORTH AMERICA", (11, 83, 148), [
        "Trump: no decision on Iran war until next year",
        "Record floods swamp Florida\u2019s St Johns River",
        "Wet practice opens F1\u2019s Las Vegas Grand Prix",
        "IMF: global public debt nears 100% of GDP",
        "White House fires cyber chief after outages",
    ]),
    ("LATIN AMERICA", (197, 90, 17), [
        "Bukele formally seeks a third term in El Salvador",
        "El Salvador sends 2,500 troops to fight Haiti gangs",
        "Haiti police kill 34 gang members in capital raid",
        "Lula backs S\u00e1nchez ahead of Spain\u2019s snap vote",
        "42% of Brazilians see fraud in 2026 election",
        "Jailed ex-president Pe\u00f1a moved to military jail",
    ]),
    ("EUROPE", (112, 48, 160), [
        "Estonia to shut Russia border for six months",
        "Ukraine\u2019s allies meet in Berlin, open to talks",
        "S\u00e1nchez admits \u2018mistakes\u2019 before Spain\u2019s election",
        "Italy fines Meta \u20ac805m over photo access",
        "Youth strike in 25 countries over living costs",
    ]),
    ("AFRICA", (192, 0, 0), [
        "Sudan court sentences RSF chief Hemeti to death",
        "Somalia orders UAE ambassador to leave in 72 hours",
        "Ethiopia, Eritrea mass troops on tense border",
        "DR Congo Ebola cases pass 10,000; trial begins",
        "Four dead as migrant boat capsizes off Senegal",
        "African Union chief welcomes new IGAD treaty",
    ]),
    ("MIDDLE EAST", (46, 125, 50), [
        "Houthi missile damages Riyadh\u2019s tallest tower",
        "Mossad chief pressed US for new Iran strikes",
        "Israeli forces cross Yellow Line in central Gaza",
        "Three tankers hit mines east of Strait of Hormuz",
        "Third US carrier reaches the Middle East",
        "Iraq moves on Iran-backed Kataib Hezbollah",
    ]),
    ("ASIA", (191, 144, 0), [
        "India, Japan deepen defence ties in Tokyo talks",
        "IAEA: North Korea expanding uranium enrichment",
        "South Korea exports pass $1 trillion on AI chips",
        "TSMC, Samsung pause some China chip shipments",
        "Bangladesh unrest grows as Hasina plans return",
        "US panel: India targeting Muslims in voter rolls",
    ]),
    ("OCEANIA & PACIFIC", (0, 131, 143), [
        "Nicholls 175* as New Zealand post 368 vs India",
        "Australia sanctions Israeli settlers in West Bank",
        "US opens deep-sea mining sale near American Samoa",
        "Kiwis debate becoming Australia\u2019s seventh state",
        "Qantas to cut 850 jobs in AI outsourcing deal",
    ]),
]

# ---------------------------------------------------------------- draw
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 28                      # side margin
    CW = W - 2 * MX              # content width

    # Masthead
    f = font(SERIF_B, 54)
    d.text((W / 2, 22), "THE WORLD TODAY", font=f, fill=INK, anchor="ma")
    f = font(SANS, 19)
    d.text((W / 2, 84), "SATURDAY 21 NOVEMBER 2026   \u00b7   46 STORIES FROM 7 REGIONS",
           font=f, fill=INK, anchor="ma")
    d.line([(MX, 116), (W - MX, 116)], fill=INK, width=3)
    d.line([(MX, 121), (W - MX, 121)], fill=INK, width=1)

    # Lead story
    ly, lh = 132, 96
    d.rectangle([MX, ly, W - MX, ly + lh], fill=LEAD_BG, outline=CARD_LINE)
    d.rectangle([MX, ly, MX + 7, ly + lh], fill=(11, 83, 148))
    f = font(SANS_B, 12)
    d.text((MX + 18, ly + 8), LEAD_TAG, font=f, fill=(11, 83, 148))
    fh, lh_head = fit(d, LEAD_HEAD, SANS_B, 24, CW - 36)
    d.text((MX + 18, ly + 26), lh_head, font=fh, fill=INK)
    bl = wrap(d, LEAD_BODY, font(SANS, 14), CW - 36)
    yy = ly + 58
    for ln in bl[:2]:
        d.text((MX + 18, yy), ln, font=font(SANS, 14), fill=MUTED)
        yy += 17

    # Major stories: 2 cols x 3 rows
    y0 = 244
    f = font(SANS_B, 15)
    d.text((MX, y0), "THE DAY\u2019S BIG STORIES", font=f, fill=INK)
    d.line([(MX + 218, y0 + 8), (W - MX, y0 + 8)], fill=RULE, width=1)
    gw, gh, gap = (CW - 12) // 2, 72, 12
    for i, (tag, color, head, body) in enumerate(MAJORS):
        x = MX + (i % 2) * (gw + gap)
        y = y0 + 24 + (i // 2) * (gh + gap)
        d.rectangle([x, y, x + gw, y + gh], fill=CARD_BG, outline=CARD_LINE)
        d.rectangle([x, y, x + 6, y + gh], fill=color)
        f = font(SANS_B, 11)
        d.text((x + 14, y + 6), tag, font=f, fill=color)
        fh, hh = fit(d, head, SANS_B, 16, gw - 24)
        d.text((x + 14, y + 21), hh, font=fh, fill=INK)
        bl = wrap(d, body, font(SANS, 12), gw - 24)
        yy = y + 40
        for ln in bl[:2]:
            d.text((x + 14, yy), ln, font=font(SANS, 12), fill=MUTED)
            yy += 14

    # World in brief: two columns of region blocks
    by = y0 + 24 + 3 * gh + 2 * gap + 14
    f = font(SANS_B, 15)
    d.text((MX, by), "THE WORLD IN BRIEF", font=f, fill=INK)
    d.line([(MX + 196, by + 8), (W - MX, by + 8)], fill=RULE, width=1)
    by += 26
    col_w = (CW - 12) // 2
    left = BRIEFS[:4]
    right = BRIEFS[4:]

    def draw_column(regions, x, y):
        for name, color, stories in regions:
            f = font(SANS_B, 13)
            d.rectangle([x, y + 3, x + 10, y + 13], fill=color)
            d.text((x + 16, y), "%s (%d)" % (name, len(stories)), font=f, fill=color)
            y += 19
            for s in stories:
                ff, ss = fit(d, s, SANS, 12, col_w - 4)
                d.text((x + 16, y), "\u2022  " + ss, font=ff, fill=INK)
                y += 15
            y += 5
        return y

    end_left = draw_column(left, MX, by)
    end_right = draw_column(right, MX + col_w + 12, by)

    # Sources box under the shorter (right) column
    sy = max(end_right, by + 330)
    d.rectangle([MX + col_w + 12, sy, W - MX, sy + 74], fill=CARD_BG, outline=CARD_LINE)
    f = font(SANS_B, 12)
    d.text((MX + col_w + 26, sy + 8), "HOW TO READ THIS PAGE", font=f, fill=INK)
    f = font(SANS, 12)
    for j, ln in enumerate(wrap(d, "One day, seven regions: every story below was reported "
                                 "on 20\u201321 November 2026.", f, col_w - 28)):
        d.text((MX + col_w + 26, sy + 28 + j * 15), ln, font=f, fill=MUTED)
    d.text((MX + col_w + 26, sy + 28 + 2 * 15),
           "Lead + 6 big stories + 39 in brief = 46 stories.", font=f, fill=MUTED)

    # Footer
    fy = H - 30
    d.line([(MX, fy), (W - MX, fy)], fill=RULE, width=1)
    f = font(SANS, 11)
    d.text((W / 2, fy + 6),
           "THE WORLD TODAY \u2014 21 November 2026  \u00b7  All stories as reported 20\u201321 Nov 2026",
           font=f, fill=MUTED, anchor="ma")

    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
