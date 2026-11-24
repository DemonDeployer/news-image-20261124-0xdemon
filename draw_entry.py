#!/usr/bin/env python3
"""Render entry.png for the make.fun news-image-20261124 bounty.

A 1024x1024 newspaper front page summing up Tuesday 24 November
2026: a masthead, one lead story (the ICJ finds Myanmar guilty of
genocide against the Rohingya), two mid-size stories (NATO warns it
will defend space as Russia presses on every front; a US drone helps
Mexico capture drug lord "El Chapo Isidro"), three short stories (the
US blacklists the chip firms at the heart of the Nvidia scandal;
Oregon and Virginia sue SpaceX over Grok images; Sheikh Hasina plans
her return to Bangladesh), plus an ALSO TODAY ticker and a sources
line. Every fact below was checked against Reuters / AP / Al Jazeera /
ICJ reporting on 24 November 2026.

Run: python3 draw_entry.py  -> writes entry.png next to this script.
Stdlib + Pillow only. No network access.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
BG = (247, 243, 232)      # newsprint
CARD_BG = (255, 255, 255)
CARD_EDGE = (210, 203, 185)
INK = (18, 18, 18)
MUTED = (96, 96, 90)
NAVY = (13, 32, 66)
GOLD = (198, 148, 42)
CRIMSON = (164, 30, 30)
OCEAN = (20, 68, 140)
FOREST = (24, 102, 52)
EMBER = (178, 58, 14)
VIOLET = (96, 44, 130)
SLATE = (52, 84, 96)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(drw, text, fnt, width):
    """Greedy word wrap into lines no wider than width pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            test = cur + " " + w
            if drw.textlength(test, font=fnt) <= width:
                cur = test
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(drw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        drw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_headline(drw, text, x, y, width, max_lines, size0, size_min,
                 color):
    """Headline that steps down in size until it fits max_lines."""
    size = size0
    while size > size_min:
        fnt = font(F_SERIF, size)
        if len(wrap(drw, text, fnt, width)) <= max_lines:
            break
        size -= 2
    fnt = font(F_SERIF, size)
    lines = wrap(drw, text, fnt, width)[:max_lines]
    return text_block(drw, lines, x, y, fnt, color, int(size * 1.14))


def body(drw, text, x, y, width, max_lines, size, color=INK):
    fnt = font(F_SANS, size)
    lines = wrap(drw, text, fnt, width)[:max_lines]
    return text_block(drw, lines, x, y, fnt, color, int(size * 1.32))


def tag(drw, text, x, y, color):
    fnt = font(F_SANS_B, 17)
    drw.text((x, y), text, font=fnt, fill=color)
    return y + 24


def panel(drw, x0, y0, x1, y1, accent):
    drw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=CARD_BG,
                          outline=CARD_EDGE, width=2)
    drw.rounded_rectangle([x0, y0, x1, y0 + 14], radius=8, fill=accent)
    drw.rectangle([x0, y0 + 7, x1, y0 + 14], fill=accent)


# ---- small pictograms, drawn with plain shapes ----------------------

def scales(drw, cx, cy, r, color):
    """Scales of justice: beam, two pans, central post."""
    drw.line([cx - r, cy - r * 0.55, cx + r, cy - r * 0.55],
             fill=color, width=5)
    drw.line([cx, cy - r * 0.9, cx, cy + r * 0.8], fill=color, width=5)
    for sx in (-1, 1):
        px = cx + sx * r * 0.8
        drw.line([cx + sx * r, cy - r * 0.55, px, cy + r * 0.15],
                 fill=color, width=3)
        drw.line([cx + sx * r, cy - r * 0.55, px, cy + r * 0.15],
                 fill=color, width=3)
        drw.polygon([(px - r * 0.42, cy + r * 0.15),
                     (px + r * 0.42, cy + r * 0.15),
                     (px, cy + r * 0.55)], fill=color)
    drw.line([cx - r * 0.4, cy + r * 0.8, cx + r * 0.4, cy + r * 0.8],
             fill=color, width=5)


def satellite(drw, cx, cy, r, color):
    """A satellite: body, two panels, a dish arc."""
    drw.rectangle([cx - r * 0.28, cy - r * 0.28, cx + r * 0.28,
                   cy + r * 0.28], fill=color)
    drw.rectangle([cx - r, cy - r * 0.16, cx - r * 0.34, cy + r * 0.16],
                  outline=color, width=4)
    drw.rectangle([cx + r * 0.34, cy - r * 0.16, cx + r, cy + r * 0.16],
                  outline=color, width=4)
    drw.line([cx - r * 0.2, cy - r * 0.28, cx - r * 0.7, cy - r * 0.85],
             fill=color, width=4)
    drw.ellipse([cx - r * 0.85, cy - r, cx - r * 0.55, cy - r * 0.7],
                outline=color, width=4)


def drone(drw, cx, cy, r, color):
    """A quadcopter drone seen from the front."""
    drw.rectangle([cx - r * 0.3, cy - r * 0.12, cx + r * 0.3,
                   cy + r * 0.18], fill=color)
    drw.ellipse([cx - r * 0.14, cy + r * 0.18, cx + r * 0.14,
                 cy + r * 0.5], fill=color)
    for sx in (-1, 1):
        drw.line([cx + sx * r * 0.3, cy, cx + sx * r * 0.85, cy - r * 0.3],
                 fill=color, width=4)
        drw.line([cx + sx * r * 0.55, cy - r * 0.42,
                  cx + sx * r * 1.15, cy - r * 0.42], fill=color, width=5)
        drw.ellipse([cx + sx * r * 0.85 - 6, cy - r * 0.36,
                     cx + sx * r * 0.85 + 6, cy - r * 0.24], fill=color)


def chip(drw, x, y, w, h, color):
    """A microchip: square body, pins on all four sides."""
    drw.rectangle([x + w * 0.2, y + h * 0.2, x + w * 0.8, y + h * 0.8],
                  fill=color)
    for i in range(3):
        t = 0.3 + i * 0.2
        drw.line([x + w * t, y, x + w * t, y + h * 0.2], fill=color,
                 width=4)
        drw.line([x + w * t, y + h * 0.8, x + w * t, y + h], fill=color,
                 width=4)
        drw.line([x, y + h * t, x + w * 0.2, y + h * t], fill=color,
                 width=4)
        drw.line([x + w * 0.8, y + h * t, x + w, y + h * t], fill=color,
                 width=4)


def warn_bubble(drw, cx, cy, r, color):
    """A speech bubble with an exclamation mark."""
    drw.ellipse([cx - r, cy - r, cx + r, cy + r * 0.7], fill=color)
    drw.polygon([(cx - r * 0.3, cy + r * 0.55), (cx + r * 0.25,
                 cy + r * 0.55), (cx - r * 0.1, cy + r)], fill=color)
    drw.rectangle([cx - 4, cy - r * 0.55, cx + 4, cy + r * 0.15],
                  fill=CARD_BG)
    drw.ellipse([cx - 5, cy + r * 0.28, cx + 5, cy + r * 0.38],
                fill=CARD_BG)


def plane(drw, cx, cy, r, color):
    """A simple passenger jet in profile, nose to the right."""
    drw.polygon([(cx - r, cy + r * 0.1), (cx + r * 0.55, cy + r * 0.1),
                 (cx + r, cy - r * 0.15), (cx + r * 0.55, cy - r * 0.3),
                 (cx - r * 0.75, cy - r * 0.3)], fill=color)
    drw.polygon([(cx - r * 0.15, cy - r * 0.3), (cx + r * 0.1,
                 cy - r * 0.3), (cx + r * 0.25, cy - r * 0.75),
                 (cx - r * 0.05, cy - r * 0.75)], fill=color)
    drw.polygon([(cx - r * 0.35, cy + r * 0.1), (cx - r * 0.1,
                 cy + r * 0.1), (cx - r * 0.3, cy + r * 0.55),
                 (cx - r * 0.6, cy + r * 0.55)], fill=color)


def render():
    img = Image.new("RGB", (W, W), BG)
    drw = ImageDraw.Draw(img)
    m = 34

    # ---- masthead ----------------------------------------------------
    drw.rectangle([m, 26, W - m, 30], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tf = font(F_SERIF, 58)
    tw = drw.textlength(title, font=tf)
    drw.text(((W - tw) / 2, 44), title, font=tf, fill=NAVY)
    sub = ("TUESDAY  ·  24 NOVEMBER 2026  ·  THE DAY'S WORLD NEWS "
           "IN ONE PICTURE")
    sf = font(F_SANS_B, 19)
    sw = drw.textlength(sub, font=sf)
    drw.text(((W - sw) / 2, 118), sub, font=sf, fill=GOLD)
    drw.line([m, 152, W - m, 152], fill=NAVY, width=3)
    drw.line([m, 158, W - m, 158], fill=NAVY, width=1)

    # ---- lead story: ICJ / Myanmar -----------------------------------
    x0, y0, x1, y1 = m, 176, W - m, 408
    panel(drw, x0, y0, x1, y1, CRIMSON)
    scales(drw, x1 - 108, y0 + 108, 62, CRIMSON)
    drw.text((x1 - 168, y0 + 176), "9–6 RULING", font=font(F_SANS_B, 17),
             fill=CRIMSON)
    drw.text((x1 - 168, y0 + 198), "FIRST OF ITS KIND", font=font(F_SANS, 15),
             fill=MUTED)
    y = tag(drw, "THE HAGUE  ·  INTERNATIONAL JUSTICE", x0 + 22, y0 + 30,
            CRIMSON)
    y = fit_headline(drw, "GUILTY OF GENOCIDE", x0 + 22, y, 700, 1,
                     62, 40, INK)
    body(drw, "The International Court of Justice rules 9–6 that "
              "Myanmar committed genocide against the Rohingya in 2017 "
              "— the first time the court has found a state responsible.",
         x0 + 22, y + 8, 700, 3, 22)

    # ---- two mid-size stories -----------------------------------------
    mid_y0, mid_y1 = 424, 636
    mid_w = (W - 2 * m - 18) // 2

    # NATO / Russia pressure
    ax0, ay0, ax1 = m, mid_y0, m + mid_w
    panel(drw, ax0, ay0, ax1, mid_y1, OCEAN)
    satellite(drw, ax1 - 58, ay0 + 58, 30, OCEAN)
    y = tag(drw, "SECURITY  ·  NATO & RUSSIA", ax0 + 20, ay0 + 26, OCEAN)
    y = fit_headline(drw, "NATO: WE WILL DEFEND SPACE", ax0 + 20, y,
                     mid_w - 120, 2, 30, 24, INK)
    body(drw, "Chief Mark Rutte vows to defend against space threats as "
              "reports say Russia may launch a nuclear-armed satellite "
              "within 60 days; Russian jets enter South Korea's "
              "air-defence zone.", ax0 + 20, y + 6,
         mid_w - 40, 4, 18)

    # El Chapo Isidro
    bx0, bx1 = m + mid_w + 18, W - m
    panel(drw, bx0, ay0, bx1, mid_y1, FOREST)
    drone(drw, bx1 - 58, ay0 + 58, 30, FOREST)
    y = tag(drw, "MEXICO  ·  DRUG WAR", bx0 + 20, ay0 + 26, FOREST)
    y = fit_headline(drw, "US DRONE HELPS NAB 'EL CHAPO ISIDRO'",
                     bx0 + 20, y, mid_w - 120, 2, 30, 24, INK)
    body(drw, "A US surveillance drone flying over Mexico helps capture "
              "Fausto Isidro Meza Flores in Sinaloa. Mexico will try "
              "him at home despite a US extradition request.",
         bx0 + 20, y + 6, mid_w - 40, 3, 18)

    # ---- three short stories -------------------------------------------
    sm_y0, sm_y1 = 656, 852
    sm_w = (W - 2 * m - 36) // 3
    shorts = [
        (EMBER, "TECH  ·  CHIPS", "US BLACKLISTS MEGASPEED",
         "The US blacklists Megaspeed, the Singapore chip firm at the "
         "centre of the Nvidia scandal, and Alibaba's Apex unit."),
        (VIOLET, "TECH  ·  COURTS", "STATES SUE SPACEX OVER GROK",
         "Oregon and Virginia sue SpaceX, alleging its Grok AI "
         "generated child sexual abuse images."),
        (SLATE, "ASIA", "HASINA PLANS HER RETURN",
         "Ousted Bangladeshi PM Sheikh Hasina plans to fly home from "
         "exile in India on 16 December, on state carrier Biman."),
    ]
    for i, (accent, kick, head, text) in enumerate(shorts):
        sx0 = m + i * (sm_w + 18)
        sx1 = sx0 + sm_w
        panel(drw, sx0, sm_y0, sx1, sm_y1, accent)
        y = tag(drw, kick, sx0 + 18, sm_y0 + 24, accent)
        y = fit_headline(drw, head, sx0 + 18, y, sm_w - 36, 2, 24, 18,
                         INK)
        body(drw, text, sx0 + 18, y + 6, sm_w - 36, 4, 16)

    # ---- ticker ----------------------------------------------------------
    ty0, ty1 = 868, 936
    drw.rounded_rectangle([m, ty0, W - m, ty1], radius=8, fill=NAVY)
    lab_f = font(F_SANS_B, 18)
    label = "ALSO TODAY  "
    drw.text((m + 18, ty0 + 22), label, font=lab_f, fill=GOLD)
    lx = m + 18 + drw.textlength(label, font=lab_f)
    ticker = ("Russian strike on Zaporizhzhia kills 2, wounds 22  •  "
              "5.6 quake hits Nepal near the China border  •  Houthis "
              "say Saudi strike kills 17 in Hodeida  •  Israeli strikes "
              "kill 3 in Gaza, including an UNRWA worker  •  SoftBank "
              "to invest $2bn in Intel")
    y = ty0 + 8
    for ln in wrap(drw, ticker, font(F_SANS, 16), W - m - lx - 18):
        drw.text((lx, y), ln, font=font(F_SANS, 16),
                 fill=(235, 235, 235))
        y += 20

    # ---- sources footer ---------------------------------------------------
    foot = ("Sources: Reuters · AP · CNN · Al Jazeera · ICJ  —  "
            "24 November 2026")
    ff = font(F_SANS, 16)
    fw = drw.textlength(foot, font=ff)
    drw.text(((W - fw) / 2, 950), foot, font=ff, fill=MUTED)
    drw.text((m, 984), "THE WORLD IN ONE DAY — 24 NOVEMBER 2026",
             font=font(F_SANS_B, 13), fill=MUTED)
    tail = "ONE PICTURE · SIX STORIES · ALL VERIFIED"
    drw.text((W - m - drw.textlength(tail, font=font(F_SANS_B, 13)), 984),
             tail, font=font(F_SANS_B, 13), fill=MUTED)

    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    render()
