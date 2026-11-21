#!/usr/bin/env python3
"""Draw entry.png for news-image-20261121 — "The World Today".

One image summing up Saturday 21 November 2026: 46 real stories from
7 regions, laid out as a newspaper front page. Everything here is fixed —
the same text, the same geometry, no network, no randomness, no clock —
so running this script twice writes byte-identical PNG bytes.

Python 3 + Pillow, DejaVu fonts from the system. Usage: python3 render.py
"""
from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAPER = (252, 252, 246)
INK = (20, 20, 20)
GREY = (95, 95, 95)
RULE = (175, 175, 165)
CARD = (255, 255, 255)
CARD_EDGE = (200, 200, 190)
LEAD_FILL = (232, 238, 245)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def shrink_to_fit(draw, text, path, size, max_width, floor=10):
    """Biggest size at or under `size` that fits, else truncate with …."""
    s = size
    while s > floor:
        f = load_font(path, s)
        if draw.textlength(text, font=f) <= max_width:
            return f, text
        s -= 1
    f = load_font(path, floor)
    while text and draw.textlength(text + "…", font=f) > max_width:
        text = text[:-1]
    return f, text + "…"


def wrap_text(draw, text, f, max_width):
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ------------------------------------------------------------------ content
LEAD_KICKER = "LEAD  —  SHENZHEN, CHINA"
LEAD_HEADLINE = "Trump, Xi and Putin: a nuclear war “cannot be won”"
LEAD_DECK = ("First-ever trilateral summit at APEC signs a four-point "
             "peace declaration; Ukraine and nuclear arms lead the agenda. "
             "(WSJ · Reuters)")

BIG_STORIES = [
    ("UKRAINE", (192, 0, 0),
     "Russia’s biggest air assault of the war hits Kyiv",
     "400+ drones and 110+ missiles; 8 killed; three Dnipro bridges struck. (Reuters)"),
    ("EUROPE", (110, 45, 155),
     "EU and UK seal Brexit reset in Brussels",
     "Youth mobility for 100,000; food checks end; £17bn boost. (The Times)"),
    ("ASIA", (185, 140, 0),
     "Cyclone Akvan slams India’s east coast",
     "80,000 evacuated in Odisha; third cyclone in a month; 70–80 kph winds. (Reuters)"),
    ("MARKETS", (10, 80, 145),
     "Anthropic’s record IPO can’t stop the slide",
     "$81.3bn debut pops 17%, then falls; S&P −2%, Dow −1,101. (WSJ)"),
    ("JUSTICE", (45, 120, 48),
     "World Court: Myanmar committed genocide",
     "ICJ rules against Myanmar over the Rohingya — a first against a state. (UN News)"),
    ("CLIMATE", (0, 128, 140),
     "COP31 draft drops fossil fuels",
     "Antalya text omits phase-out; 1.5°C overshoot admitted; talks overtime. (UN News)"),
]

REGIONS = [
    ("NORTH AMERICA", (10, 80, 145), [
        "Trump: no decision on Iran war until next year",
        "Record floods swamp Florida’s St Johns River",
        "Wet practice opens F1’s Las Vegas Grand Prix",
        "IMF: global public debt nears 100% of GDP",
        "White House fires cyber chief after outages",
    ]),
    ("LATIN AMERICA", (195, 85, 15), [
        "Bukele formally seeks a third term in El Salvador",
        "El Salvador sends 2,500 troops to fight Haiti gangs",
        "Haiti police kill 34 gang members in capital raid",
        "Lula backs Sánchez ahead of Spain’s snap vote",
        "42% of Brazilians see fraud in 2026 election",
        "Jailed ex-president Peña moved to military jail",
    ]),
    ("EUROPE", (110, 45, 155), [
        "Estonia to shut Russia border for six months",
        "Ukraine’s allies meet in Berlin, open to talks",
        "Sánchez admits ‘mistakes’ before Spain’s election",
        "Italy fines Meta €805m over photo access",
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
    ("MIDDLE EAST", (45, 120, 48), [
        "Houthi missile damages Riyadh’s tallest tower",
        "Mossad chief pressed US for new Iran strikes",
        "Israeli forces cross Yellow Line in central Gaza",
        "Three tankers hit mines east of Strait of Hormuz",
        "Third US carrier reaches the Middle East",
        "Iraq moves on Iran-backed Kataib Hezbollah",
    ]),
    ("ASIA", (185, 140, 0), [
        "India, Japan deepen defence ties in Tokyo talks",
        "IAEA: North Korea expanding uranium enrichment",
        "South Korea exports pass $1 trillion on AI chips",
        "TSMC, Samsung pause some China chip shipments",
        "Bangladesh unrest grows as Hasina plans return",
        "US panel: India targeting Muslims in voter rolls",
    ]),
    ("OCEANIA & PACIFIC", (0, 128, 140), [
        "Nicholls 175* as New Zealand post 368 vs India",
        "Australia sanctions Israeli settlers in West Bank",
        "US opens deep-sea mining sale near American Samoa",
        "Kiwis debate becoming Australia’s seventh state",
        "Qantas to cut 850 jobs in AI outsourcing deal",
    ]),
]


# ------------------------------------------------------------------ drawing
def draw_masthead(d):
    mx = 28
    d.text((CANVAS_W / 2, 22), "THE WORLD TODAY",
           font=load_font(SERIF_BOLD, 54), fill=INK, anchor="ma")
    d.text((CANVAS_W / 2, 84),
           "SATURDAY 21 NOVEMBER 2026   ·   46 STORIES FROM 7 REGIONS",
           font=load_font(SANS, 19), fill=INK, anchor="ma")
    d.line([(mx, 116), (CANVAS_W - mx, 116)], fill=INK, width=3)
    d.line([(mx, 121), (CANVAS_W - mx, 121)], fill=INK, width=1)


def draw_lead(d):
    mx, cw = 28, CANVAS_W - 56
    top, height = 132, 96
    d.rectangle([mx, top, CANVAS_W - mx, top + height],
                fill=LEAD_FILL, outline=CARD_EDGE)
    d.rectangle([mx, top, mx + 7, top + height], fill=(10, 80, 145))
    d.text((mx + 18, top + 8), LEAD_KICKER,
           font=load_font(SANS_BOLD, 12), fill=(10, 80, 145))
    head_font, head_text = shrink_to_fit(
        d, LEAD_HEADLINE, SANS_BOLD, 24, cw - 36)
    d.text((mx + 18, top + 26), head_text, font=head_font, fill=INK)
    body_font = load_font(SANS, 14)
    y = top + 58
    for line in wrap_text(d, LEAD_DECK, body_font, cw - 36)[:2]:
        d.text((mx + 18, y), line, font=body_font, fill=GREY)
        y += 17


def draw_big_stories(d):
    mx, cw = 28, CANVAS_W - 56
    y0 = 244
    d.text((mx, y0), "THE DAY’S BIG STORIES",
           font=load_font(SANS_BOLD, 15), fill=INK)
    d.line([(mx + 218, y0 + 8), (CANVAS_W - mx, y0 + 8)], fill=RULE, width=1)
    card_w, card_h, gap = (cw - 12) // 2, 72, 12
    for i, (tag, color, headline, deck) in enumerate(BIG_STORIES):
        x = mx + (i % 2) * (card_w + gap)
        y = y0 + 24 + (i // 2) * (card_h + gap)
        d.rectangle([x, y, x + card_w, y + card_h],
                    fill=CARD, outline=CARD_EDGE)
        d.rectangle([x, y, x + 6, y + card_h], fill=color)
        d.text((x + 14, y + 6), tag, font=load_font(SANS_BOLD, 11), fill=color)
        head_font, head_text = shrink_to_fit(
            d, headline, SANS_BOLD, 16, card_w - 24)
        d.text((x + 14, y + 21), head_text, font=head_font, fill=INK)
        body_font = load_font(SANS, 12)
        y2 = y + 40
        for line in wrap_text(d, deck, body_font, card_w - 24)[:2]:
            d.text((x + 14, y2), line, font=body_font, fill=GREY)
            y2 += 14


def draw_region_column(d, regions, x, y, col_w):
    for name, color, stories in regions:
        d.rectangle([x, y + 3, x + 10, y + 13], fill=color)
        d.text((x + 16, y), "%s (%d)" % (name, len(stories)),
               font=load_font(SANS_BOLD, 13), fill=color)
        y += 19
        for story in stories:
            f, text = shrink_to_fit(d, story, SANS, 12, col_w - 4)
            d.text((x + 16, y), "•  " + text, font=f, fill=INK)
            y += 15
        y += 5
    return y


def draw_briefs(d):
    mx, cw = 28, CANVAS_W - 56
    y0 = 522
    d.text((mx, y0), "THE WORLD IN BRIEF",
           font=load_font(SANS_BOLD, 15), fill=INK)
    d.line([(mx + 196, y0 + 8), (CANVAS_W - mx, y0 + 8)], fill=RULE, width=1)
    top = y0 + 26
    col_w = (cw - 12) // 2
    left_end = draw_region_column(d, REGIONS[:4], mx, top, col_w)
    right_end = draw_region_column(d, REGIONS[4:], mx + col_w + 12, top, col_w)
    # Explainer box under the shorter (right) column.
    box_x = mx + col_w + 12
    box_y = max(right_end, top + 330)
    d.rectangle([box_x, box_y, CANVAS_W - mx, box_y + 74],
                fill=CARD, outline=CARD_EDGE)
    d.text((box_x + 14, box_y + 8), "HOW TO READ THIS PAGE",
           font=load_font(SANS_BOLD, 12), fill=INK)
    note_font = load_font(SANS, 12)
    note = ("One day, seven regions: every story below was reported "
            "on 20–21 November 2026.")
    y = box_y + 28
    for line in wrap_text(d, note, note_font, col_w - 28):
        d.text((box_x + 14, y), line, font=note_font, fill=GREY)
        y += 15
    d.text((box_x + 14, y),
           "Lead + 6 big stories + 39 in brief = 46 stories.",
           font=note_font, fill=GREY)
    return left_end


def draw_footer(d):
    mx = 28
    fy = CANVAS_H - 30
    d.line([(mx, fy), (CANVAS_W - mx, fy)], fill=RULE, width=1)
    d.text((CANVAS_W / 2, fy + 6),
           "THE WORLD TODAY — 21 November 2026  ·  All stories as reported 20–21 Nov 2026",
           font=load_font(SANS, 11), fill=GREY, anchor="ma")


def render():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_big_stories(d)
    draw_briefs(d)
    draw_footer(d)
    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    render()
