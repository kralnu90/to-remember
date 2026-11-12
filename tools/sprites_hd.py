"""Hi-res battle sprites for 30 x to Remember: 2x the old 10x14 sprites, same palette letters.
Lowercase letter = palette colour, UPPERCASE = a darker shade of that colour ('G' stays its own colour),
'#' = outline. Classes face left; creatures face right (as before)."""
import json, math
from PIL import Image, ImageDraw

class S:
    def __init__(s, w, h): s.w, s.h = w, h; s.g = [['.'] * w for _ in range(h)]
    def px(s, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < s.w and 0 <= y < s.h: s.g[y][x] = c
    def rect(s, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): s.px(x, y, c)
    def ell(s, cx, cy, rx, ry, c):
        for y in range(s.h):
            for x in range(s.w):
                if ((x - cx) / (rx + .5)) ** 2 + ((y - cy) / (ry + .5)) ** 2 <= 1: s.px(x, y, c)
    def line(s, x0, y0, x1, y1, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n + 1):
            t = i / max(1, n); s.px(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, c)
    def poly(s, pts, c):
        for y in range(s.h):
            for x in range(s.w):
                ins = False; j = len(pts) - 1
                for i in range(len(pts)):
                    xi, yi = pts[i]; xj, yj = pts[j]
                    if (yi > y + .5) != (yj > y + .5) and x + .5 < (xj - xi) * (y + .5 - yi) / (yj - yi) + xi: ins = not ins
                    j = i
                if ins: s.px(x, y, c)
    def shade_right(s, x0, letters):
        """darken the right-hand part of the given letters from column x0"""
        for y in range(s.h):
            for x in range(x0, s.w):
                if s.g[y][x] in letters: s.g[y][x] = s.g[y][x].upper()
    def shade_rows(s, y0, y1, letters):
        for y in range(y0, y1 + 1):
            for x in range(s.w):
                if s.g[y][x] in letters: s.g[y][x] = s.g[y][x].upper()
    def outline(s):
        g = s.g; out = [r[:] for r in g]
        for y in range(s.h):
            for x in range(s.w):
                if g[y][x] == '.':
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < s.w and 0 <= yy < s.h and g[yy][xx] not in '.#':
                            out[y][x] = '#'; break
        s.g = out; return s
    def rows(s): return [''.join(r) for r in s.g]

W, H = 20, 28

def legs(k, boots='o', pants='a', wide=False):
    l, r = (6, 11) if not wide else (5, 12)
    k.rect(l, 20, l + 2, 24, pants); k.rect(r, 20, r + 2, 24, pants)
    k.rect(l - 1, 25, l + 2, 27, boots); k.rect(r - 1, 25, r + 2, 27, boots)
    k.rect(r, 20, r + 2, 24, pants.upper() if pants != 's' else 'S')

def face(k, skin='s', eye='e', x0=6, y0=4, w=7, h=7):
    k.rect(x0, y0, x0 + w - 1, y0 + h - 1, skin)
    k.px(x0 - 1, y0 + 3, skin); k.px(x0 - 1, y0 + 4, skin)          # nose to the left
    k.px(x0 + 1, y0 + 3, eye); k.px(x0 + 1, y0 + 2, '#')             # eye + brow
    k.rect(x0 + w - 2, y0, x0 + w - 1, y0 + h - 1, skin.upper())

def torso(k, c='a', x0=5, x1=14, y0=11, y1=19):
    k.rect(x0, y0, x1, y1, c); k.rect(x0 + 1, y0 - 1, x1 - 1, y0 - 1, c)
    k.shade_right(x1 - 2, c)

def hero():
    k = S(W, H)
    # cloak behind
    k.poly([(9, 10), (17, 11), (18, 25), (12, 25)], 'A')
    legs(k)
    torso(k, 'a')
    k.rect(5, 18, 14, 19, 'b'); k.px(9, 18, 'g')                     # belt
    k.rect(8, 12, 9, 14, 'g'); k.px(8, 13, 'b'); k.px(9, 13, 'b')    # hourglass clasp
    k.rect(5, 11, 14, 11, 'b')
    face(k)
    # hair
    k.rect(5, 2, 14, 4, 'h'); k.rect(11, 2, 14, 9, 'h'); k.rect(5, 3, 6, 5, 'h')
    for x, y in ((6, 1), (9, 1), (12, 1), (14, 2), (15, 4)): k.px(x, y, 'h')
    k.shade_right(13, 'h')
    # arm + short blade forward
    k.rect(2, 13, 4, 16, 'a'); k.rect(1, 16, 3, 17, 's')
    k.line(0, 15, 0, 6, 'w'); k.line(1, 15, 1, 7, 'W'); k.rect(-1, 16, 3, 16, 'b') if False else k.rect(0, 16, 2, 16, 'b')
    return k.outline()

def warrior():
    k = S(W, H)
    k.line(17, 18, 19, 3, 'w'); k.line(18, 18, 19, 5, 'W')           # sword raised behind
    k.rect(15, 17, 18, 18, 'b')
    legs(k, pants='a', wide=True)
    torso(k, 'a', 4, 15)
    k.rect(4, 11, 15, 12, 'w'); k.rect(13, 10, 17, 12, 'w')          # pauldrons
    k.rect(4, 18, 15, 19, 'b')
    face(k, x0=6, y0=5, w=7, h=6)
    k.rect(5, 1, 14, 4, 'w'); k.rect(5, 5, 5, 9, 'w'); k.rect(12, 5, 14, 10, 'w'); k.rect(9, 4, 9, 7, 'W')
    k.px(9, 0, 'w'); k.px(10, 0, 'w'); k.shade_right(12, 'w')
    # big shield in front (left)
    k.ell(3, 15, 4, 6, 'b'); k.ell(3, 15, 3, 5, 'B'); k.rect(2, 13, 4, 17, 'w'); k.rect(3, 10, 3, 20, 'w')
    return k.outline()

def paladin():
    k = S(W, H)
    k.rect(17, 9, 18, 19, 't'); k.ell(17.5, 7, 2, 2, 'b')             # mace behind
    legs(k, wide=True)
    torso(k, 'a', 4, 15)
    k.rect(4, 11, 15, 12, 'w'); k.rect(8, 13, 11, 17, 'b'); k.rect(9, 12, 10, 18, 'b')   # tabard sun
    k.rect(4, 18, 15, 19, 'b')
    face(k, x0=6, y0=5, w=7, h=6)
    k.rect(5, 1, 14, 4, 'w'); k.rect(12, 5, 14, 10, 'w'); k.rect(5, 5, 5, 10, 'w')
    k.rect(8, 0, 11, 1, 'b'); k.rect(5, 3, 14, 3, 'b'); k.shade_right(12, 'w')
    # tower shield
    k.rect(0, 9, 5, 22, 'w'); k.rect(1, 10, 4, 21, 'b'); k.rect(2, 11, 3, 20, 'w'); k.rect(1, 14, 4, 15, 'w'); k.shade_rows(18, 22, 'w')
    return k.outline()

def robe(k, c='a', x0=5, x1=14, y0=11):
    k.poly([(x0 + 1, y0 - 1), (x1 - 1, y0 - 1), (x1 + 2, 26), (x0 - 2, 26)], c)
    k.shade_right(x1 - 1, c)
    k.rect(x0 - 2, 26, x0 + 2, 27, 'o'); k.rect(x1 - 2, 26, x1 + 1, 27, 'o')

def cleric():
    k = S(W, H)
    robe(k)
    k.rect(5, 17, 14, 18, 'b'); k.rect(9, 11, 10, 25, 'b')
    face(k, y0=5, h=6)
    k.rect(4, 2, 15, 4, 'h'); k.rect(12, 2, 15, 13, 'h'); k.rect(4, 2, 5, 9, 'h'); k.shade_right(13, 'h')   # hood
    # staff with glowing head
    k.rect(1, 6, 1, 26, 't'); k.rect(2, 6, 2, 26, 'T'); k.ell(1.5, 4, 2, 2, 'g'); k.px(1, 3, 'w')
    k.rect(2, 14, 4, 15, 's')
    return k.outline()

def mage():
    k = S(W, H)
    robe(k)
    k.rect(5, 16, 14, 17, 'b')
    face(k, y0=6, h=5)
    k.poly([(3, 6), (17, 6), (12, 0), (9, -1)], 'h'); k.rect(3, 5, 17, 6, 'h'); k.px(13, 0, 'h'); k.px(15, 1, 'h')
    k.shade_right(13, 'h'); k.rect(4, 5, 16, 5, 'b')
    k.rect(12, 7, 14, 12, 'h')                                         # hair under hat
    k.rect(1, 7, 1, 26, 't'); k.rect(2, 7, 2, 26, 'T'); k.ell(1.5, 5, 2, 2, 'g'); k.px(0, 3, 'g'); k.px(3, 3, 'g')
    k.rect(2, 15, 4, 16, 's')
    return k.outline()

def rogue():
    k = S(W, H)
    k.poly([(8, 9), (16, 10), (18, 24), (11, 23)], 'A')                # cloak
    legs(k)
    torso(k, 'a', 5, 13, 12, 19)
    k.rect(5, 18, 13, 19, 'b'); k.line(5, 12, 13, 18, 'b')
    face(k, y0=5, h=6)
    k.rect(4, 2, 14, 4, 'h'); k.rect(11, 2, 14, 12, 'h'); k.rect(4, 2, 5, 6, 'h'); k.rect(6, 8, 10, 10, 'h')   # hood + mask
    k.shade_right(12, 'h')
    k.rect(2, 13, 4, 15, 'a'); k.rect(1, 15, 3, 16, 's'); k.line(0, 15, -1, 10, 'w'); k.px(0, 12, 'w'); k.px(0, 11, 'w'); k.px(0, 14, 'w')
    return k.outline()

def ranger():
    k = S(W, H)
    k.rect(14, 8, 16, 17, 'b'); k.px(14, 7, 'w'); k.px(16, 6, 'w')    # quiver + fletching
    legs(k)
    torso(k, 'a', 5, 14)
    k.rect(5, 18, 14, 19, 'b'); k.line(6, 11, 14, 17, 'b')
    face(k, y0=5, h=6)
    k.rect(5, 2, 14, 4, 'h'); k.rect(11, 2, 14, 11, 'h'); k.rect(5, 2, 6, 6, 'h'); k.shade_right(13, 'h')
    # bow
    for y in range(4, 25):
        x = 2 - int(round(2.2 * math.sin((y - 4) / 20 * math.pi)))
        k.px(x, y, 'w')
    k.line(2, 4, 2, 24, 'W') if False else k.rect(3, 4, 3, 24, 'W')
    k.rect(3, 13, 5, 14, 's')
    return k.outline()

def monk():
    k = S(W, H)
    k.rect(6, 20, 8, 24, 'a'); k.rect(11, 20, 13, 24, 'A')
    k.rect(5, 25, 8, 27, 's'); k.rect(10, 25, 13, 27, 'S')             # bare feet
    torso(k, 'a', 5, 14)
    k.rect(7, 11, 9, 16, 's')                                           # open robe
    k.rect(5, 17, 14, 18, 'b'); k.rect(14, 18, 15, 22, 'b')
    face(k, y0=3, h=7)
    k.rect(6, 2, 12, 3, 's'); k.rect(12, 3, 13, 9, 'S'); k.px(9, 2, 'W') if False else k.px(8, 2, 's')
    for x in range(6, 14, 2): k.px(x, 11, 'b')                          # beads
    k.rect(2, 12, 4, 15, 's'); k.rect(1, 15, 3, 17, 's'); k.rect(15, 12, 17, 15, 'S'); k.rect(16, 15, 18, 16, 'S')
    return k.outline()

def bard():
    k = S(W, H)
    legs(k)
    torso(k, 'a', 5, 14)
    k.rect(5, 18, 14, 19, 'b')
    face(k, y0=5, h=6)
    k.rect(5, 4, 14, 5, 'h'); k.rect(12, 5, 14, 10, 'h'); k.px(5, 6, 'h')        # curls
    k.rect(4, 2, 15, 3, 'b'); k.rect(6, 1, 13, 1, 'b'); k.shade_right(13, 'b')   # cap
    k.line(13, 1, 18, -2, 'g'); k.line(13, 0, 18, -3, 'g')                       # feather
    # lute held across the body
    k.ell(8, 16, 4, 3, 't'); k.ell(8, 16, 1, 1, '#'); k.line(4, 14, -1, 9, 'T'); k.rect(-1, 8, 0, 9, 't')
    k.shade_right(11, 't')
    k.rect(12, 14, 14, 16, 's')
    return k.outline()

# ---------- creatures (face right) ----------
def hound():
    k = S(28, 18)
    k.ell(13, 8, 9, 4, 'k'); k.ell(22, 5, 4, 3, 'k'); k.poly([(24, 4), (27, 6), (24, 8)], 'k')
    k.poly([(20, 2), (21, -1), (23, 2)], 'k'); k.poly([(22, 2), (24, -1), (25, 3)], 'K')
    k.px(23, 5, 'e'); k.px(26, 7, '#')
    for x in (6, 9, 13, 16, 19): k.px(x, 3, 'c'); k.px(x - 1, 4, 'c')          # glowing spines
    for x0, d in ((6, 0), (9, 1), (16, 0), (19, 1)):
        k.rect(x0, 11, x0 + 1, 15, 'k' if d == 0 else 'K'); k.rect(x0 - 1 + d, 16, x0 + 1 + d, 17, 'K')
    k.poly([(4, 7), (0, 3), (1, 6), (4, 9)], 'k')                                # tail
    k.shade_rows(10, 12, 'k')
    return k.outline()

def rat():
    k = S(20, 10)
    k.ell(9, 6, 6, 3, 'k'); k.ell(15, 6, 3, 2, 'k'); k.poly([(16, 5), (19, 7), (16, 8)], 'k')
    k.px(16, 5, 'e'); k.ell(13, 3, 1, 1, 'k')
    k.ell(8, 4, 3, 2, 'g'); k.ell(8, 4, 1, 1, 'G'); k.px(8, 1, 'g'); k.px(5, 3, 'g'); k.px(11, 3, 'g')
    k.line(3, 6, 0, 3, 'k'); k.line(0, 3, 0, 1, 'K')
    for x in (5, 8, 11, 14): k.rect(x, 9, x, 9, 'K')
    k.shade_rows(8, 9, 'k')
    return k.outline()

def thorn():
    k = S(16, 16)
    k.ell(8, 8, 6, 5, 'g'); k.ell(7, 7, 4, 3, 'G')
    for (x, y) in ((2, 3), (5, 1), (10, 1), (13, 3), (1, 8), (15, 8), (3, 12), (13, 12)): k.line(8, 8, x, y, 'g'); k.px(x, y, 'G')
    k.rect(5, 7, 6, 8, 'e'); k.rect(10, 7, 11, 8, 'e'); k.px(5, 7, '#'); k.px(10, 7, '#')
    k.rect(6, 11, 10, 11, '#')
    k.line(6, 13, 4, 15, 'b'); k.line(10, 13, 12, 15, 'b'); k.line(8, 13, 8, 15, 'b')
    return k.outline()

def boar():
    k = S(28, 18)
    k.ell(12, 9, 10, 5, 'k'); k.ell(22, 9, 5, 4, 'k'); k.rect(24, 9, 27, 12, 'k')
    k.ell(11, 4, 9, 3, 'm'); k.ell(9, 3, 6, 2, 'M')
    k.px(23, 7, 'e'); k.px(26, 10, '#'); k.px(26, 11, '#')
    k.line(25, 12, 27, 9, 'w'); k.px(27, 8, 'w')                                  # tusk
    k.poly([(20, 5), (21, 2), (23, 5)], 'K')
    for x0, d in ((5, 0), (8, 1), (17, 0), (20, 1)):
        k.rect(x0, 13, x0 + 2, 16, 'k' if d == 0 else 'K'); k.rect(x0, 17, x0 + 2, 17, '#')
    k.shade_rows(12, 14, 'k')
    return k.outline()

def wisp():
    k = S(14, 14)
    k.ell(7, 7, 5, 5, 'g'); k.ell(6, 6, 3, 3, 'G'); k.px(5, 4, 'G')
    for (x, y) in ((7, 0), (3, 1), (11, 1), (1, 5), (13, 6)): k.px(x, y, 'g')
    k.rect(4, 7, 5, 8, 'e'); k.rect(8, 7, 9, 8, 'e')
    k.line(4, 12, 3, 13, 'g'); k.line(10, 12, 11, 13, 'g'); k.px(7, 13, 'g')
    return k.outline()

def spider():
    k = S(28, 14)
    k.ell(10, 7, 6, 4, 'k'); k.ell(18, 7, 4, 3, 'k'); k.ell(9, 6, 4, 2, 'K')
    k.px(20, 6, 'e'); k.px(21, 7, 'e'); k.px(19, 5, 'e')
    for sx, ex, ey in ((12, 3, 1), (13, 1, 8), (15, 6, 13), (16, 25, 1), (17, 27, 8), (17, 22, 13), (14, 9, 13), (18, 26, 12)):
        mx = (sx + ex) / 2; my = min(7, ey) - 3 if ey < 7 else ey - 2
        k.line(sx, 7, mx, my, 'k'); k.line(mx, my, ex, ey, 'K')
    return k.outline()

def mite():
    k = S(16, 10)
    k.ell(7, 6, 5, 3, 'k'); k.ell(12, 6, 2, 2, 'K')
    k.line(12, 4, 14, 0, 'c'); k.line(13, 5, 15, 2, 'c')
    k.px(12, 6, 'e'); k.ell(7, 5, 2, 1, 'c')
    for x in (4, 7, 10): k.px(x, 9, '#'); k.px(x - 1, 9, 'K')
    return k.outline()

def leech():
    k = S(24, 10)
    k.ell(12, 5, 11, 4, 'g'); k.ell(14, 3, 4, 1, 'G'); k.ell(20, 5, 3, 3, 'g')
    k.px(21, 4, 'e'); k.px(20, 4, 'e'); k.px(23, 6, '#')
    for x in range(3, 20, 3): k.px(x, 8, 'G')
    k.shade_rows(7, 9, 'g')
    return k.outline()

HD = {'hero': hero(), 'warrior': warrior(), 'paladin': paladin(), 'cleric': cleric(), 'mage': mage(), 'rogue': rogue(),
      'ranger': ranger(), 'monk': monk(), 'bard': bard(), 'hound': hound(), 'rat': rat(), 'thorn': thorn(), 'boar': boar(),
      'wisp': wisp(), 'spider': spider(), 'mite': mite(), 'leech': leech()}
out = {k: v.rows() for k, v in HD.items()}
json.dump(out, open('hd.json', 'w'), separators=(',', ':'))

# ---------- preview with game palettes ----------
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def shade(c): return tuple(int(v * .68) for v in c)
HERO = {'h': '#4a3020', 's': '#f0c8a0', 'e': '#1a1420', 'a': '#7a6aa8', 'b': '#e0ae52', 'w': '#c8ccd8', 't': '#8a5a2b', 'g': '#e0ae52', 'o': '#2b2230'}
def comp(a, b='#e0ae52', g='#ffffff', arm=False):
    return {'h': '#7a4a2a', 's': '#d9a47a', 'e': '#1a1420', 'a': '#7a8090' if arm else a, 'b': b, 'w': '#c8ccd8', 't': '#8a5a2b', 'g': g, 'o': '#2b2230'}
PALS = {'hero': HERO, 'warrior': comp('#7a8090', '#e39ac7', arm=True), 'paladin': comp('#8a8f9a', '#e0ae52', arm=True), 'cleric': comp('#eeeeee', '#e0ae52', '#f2e6a0'),
        'mage': comp('#8fd3d0', '#e0ae52', '#8fd3d0'), 'rogue': comp('#4a4458', '#c8ccd8'), 'ranger': comp('#5a8a3a', '#8a5a2b'), 'monk': comp('#d8862a', '#c0392b'),
        'bard': comp('#3a6ab0', '#9a3a8a', '#f0e070'),
        'hound': {'k': '#5a4f6e', 'e': '#e0ae52', 'c': '#8fd3d0'}, 'rat': {'k': '#a8822a', 'e': '#e24b4a', 'g': '#e0ae52', 'G': '#f6d78f'},
        'thorn': {'g': '#2f5a2a', 'G': '#5a8a3a', 'e': '#f2d27a', 'b': '#6b4a2a'}, 'boar': {'k': '#5a3f2e', 'm': '#5a8a3a', 'e': '#e24b4a', 'w': '#ece3cc'},
        'wisp': {'g': '#c0603a', 'G': '#f0c27a', 'e': '#16141d'}, 'spider': {'k': '#5a5468', 'e': '#e24b4a'}, 'mite': {'k': '#2a5a6a', 'e': '#e0ae52', 'c': '#8fd3d0'},
        'leech': {'g': '#5a4a7a', 'G': '#d7a6ff', 'e': '#f2d27a'}}
def render(rows, pal):
    im = Image.new('RGBA', (len(rows[0]), len(rows)), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == '.': continue
            if ch == '#': c = (20, 18, 26)
            elif ch in pal: c = hexc(pal[ch])
            elif ch.lower() in pal: c = shade(hexc(pal[ch.lower()]))
            else: raise SystemExit(f'missing {ch}')
            im.putpixel((x, y), c + (255,))
    return im
SC = 8
cells = [(k, render(out[k], PALS[k])) for k in out]
cw = 30 * SC; chh = 30 * SC
sheet = Image.new('RGBA', (6 * cw, 3 * chh), (40, 44, 64, 255))
for i, (k, im) in enumerate(cells):
    x = (i % 6) * cw + (cw - im.width * SC) // 2; y = (i // 6) * chh + (chh - im.height * SC) // 2
    sheet.alpha_composite(im.resize((im.width * SC, im.height * SC), Image.NEAREST), (x, y))
sheet.save('hd_preview.png'); print('ok', len(cells))
