"""30 x to Remember - dialogue portraits (48x48, closed + talk frames)."""
import json
from PIL import Image, ImageDraw, ImageFont

N = 48

class C:
    def __init__(s): s.g = [['.'] * N for _ in range(N)]
    def px(s, r, c, ch):
        if 0 <= r < N and 0 <= c < N: s.g[r][c] = ch
    def rect(s, r0, r1, c0, c1, ch):
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1): s.px(r, c, ch)
    def ell(s, cr, cc, rr, rc, ch, r0=0, r1=N - 1, only=None):
        for r in range(max(0, r0), min(N - 1, r1) + 1):
            for c in range(N):
                if ((r - cr) / rr) ** 2 + ((c - cc) / rc) ** 2 <= 1:
                    if only is None or s.g[r][c] in only: s.g[r][c] = ch
    def recolour(s, r0, r1, c0, c1, frm, to):
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if 0 <= r < N and 0 <= c < N and s.g[r][c] in frm: s.g[r][c] = to
    def outline(s):
        g = s.g; out = [row[:] for row in g]
        for r in range(N):
            for c in range(N):
                if g[r][c] == '.':
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        rr, cc = r + dr, c + dc
                        if 0 <= rr < N and 0 <= cc < N and g[rr][cc] not in '.K':
                            out[r][c] = 'K'; break
        s.g = out
        return s

# ---------- shared pieces ----------
def shoulders(k, A='A', a='a'):
    k.ell(48, 23.5, 9, 23, A, 39)
    k.recolour(39, 47, 32, 47, A, a)

def neck(k):
    k.rect(35, 41, 19, 28, 's')
    k.rect(35, 41, 19, 25, 'S'); k.rect(35, 36, 19, 28, 's')

def head(k, ears=True):
    if ears:
        k.rect(24, 29, 13, 14, 'S'); k.rect(24, 29, 33, 34, 's')
    k.ell(25, 23.5, 12, 9.6, 'S')
    k.recolour(14, 37, 30, 34, 'S', 's')
    k.rect(36, 37, 17, 30, 's') if False else None

def eyes(k, iris='E', narrow=False, glow=False, hollow=False):
    rows = (24, 25) if narrow else (23, 25)
    for c0, ir in ((17, (19, 20)), (27, (27, 28))):
        if hollow:
            k.rect(rows[0], rows[1], c0, c0 + 3, 'K')
            k.rect(24, 24, ir[0], ir[0], iris)
            continue
        if glow:
            k.rect(rows[0], rows[1], c0, c0 + 3, iris)
            continue
        k.rect(rows[0], rows[1], c0, c0 + 3, 'W')
        k.rect(rows[0], rows[1], ir[0], ir[1], iris)
        k.px(24, ir[1] if c0 == 17 else ir[0], 'K')
        k.rect(rows[0] - 1, rows[0] - 1, c0, c0 + 3, 'K')

def brows(k, ch='B', angry=False, bushy=False):
    if angry:
        k.rect(21, 21, 16, 18, ch); k.rect(22, 22, 19, 21, ch)
        k.rect(21, 21, 29, 31, ch); k.rect(22, 22, 26, 28, ch)
    else:
        k.rect(21, 21, 16, 21, ch); k.rect(21, 21, 26, 31, ch)
        if bushy:
            k.rect(20, 20, 16, 21, ch); k.rect(20, 20, 26, 31, ch)

def nose(k):
    k.rect(27, 29, 24, 24, 's'); k.rect(30, 30, 22, 25, 's')

def mouth(k, talk, lip='K'):
    if talk:
        k.rect(32, 34, 20, 27, 'K'); k.rect(33, 34, 21, 26, 'M'); k.rect(32, 32, 21, 26, 'W')
    else:
        k.rect(33, 33, 21, 26, lip); k.px(33, 21, 's'); k.px(33, 26, 's')

def standard_face(k, talk, iris='E', brow='B', **kw):
    head(k)
    eyes(k, iris, **{x: kw[x] for x in ('narrow', 'glow', 'hollow') if x in kw})
    brows(k, brow, kw.get('angry', False), kw.get('bushy', False))
    nose(k)
    mouth(k, talk)

# ---------- portraits ----------
def hero(talk):
    k = C(); shoulders(k); neck(k)
    # cloak collar + hourglass clasp
    k.rect(38, 41, 13, 34, 'A'); k.recolour(38, 41, 29, 34, 'A', 'a')
    k.rect(38, 39, 17, 30, 'a')
    k.rect(40, 45, 22, 25, 'G'); k.rect(41, 44, 23, 24, 'P'); k.rect(42, 43, 23, 24, 'g')
    standard_face(k, talk, iris='E')
    # messy hair
    k.ell(17, 23.5, 7, 12, 'H', 9, 22)
    k.rect(14, 22, 13, 15, 'H'); k.rect(14, 26, 32, 34, 'H')
    k.rect(18, 20, 16, 21, 'H'); k.rect(18, 19, 26, 31, 'H')
    for c in (15, 19, 24, 28): k.px(21, c, 'H'); k.px(22, c + 1, 'H')
    for c in (12, 35): k.rect(16, 23, c, c, 'H')
    for c, r in ((14, 9), (20, 8), (27, 8), (33, 10)): k.px(r, c, 'H'); k.px(r + 1, c, 'H')
    k.recolour(8, 26, 29, 36, 'H', 'h')
    k.rect(11, 14, 17, 18, 'P'); k.rect(15, 18, 18, 18, 'P')   # time-touched streak
    return k.outline()

def wizard(talk):
    k = C(); shoulders(k); neck(k)
    k.rect(38, 47, 21, 26, 'C')   # robe trim
    head(k)
    eyes(k, 'E'); brows(k, 'W', bushy=True); nose(k)
    # beard + moustache
    k.ell(35, 23.5, 10, 10, 'W', 29, 47)
    k.recolour(29, 47, 29, 34, 'W', 'w')
    k.rect(30, 31, 18, 29, 'W'); k.rect(31, 31, 27, 29, 'w')
    if talk:
        k.rect(33, 34, 21, 26, 'K'); k.rect(34, 34, 22, 25, 'M')
    else:
        k.rect(33, 33, 21, 26, 'w')
    # hat
    k.rect(15, 18, 9, 38, 'A'); k.recolour(15, 18, 31, 38, 'A', 'a')
    k.rect(18, 18, 9, 38, 'a')
    for r, (c0, c1) in enumerate([(22, 25), (21, 26), (20, 27), (19, 28), (18, 29), (17, 30),
                                  (17, 30), (16, 31), (16, 31), (15, 32), (15, 32), (14, 33)]):
        k.rect(3 + r, 3 + r, c0, c1, 'A')
    k.rect(0, 2, 25, 28, 'A'); k.rect(0, 0, 28, 31, 'A'); k.rect(1, 1, 31, 32, 'a')
    k.recolour(0, 14, 27, 34, 'A', 'a')
    k.rect(13, 14, 14, 33, 'G')                        # band
    k.ell(9, 22, 2.5, 2.5, 'G'); k.ell(9, 22, 1.5, 1.5, 'W'); k.px(8, 22, 'K'); k.px(9, 22, 'K'); k.px(9, 23, 'K')  # clock
    for r, c in ((5, 25), (11, 28), (6, 19)): k.px(r, c, 'P')
    return k.outline()

def tavern(talk):
    k = C(); shoulders(k, 'A', 'a'); neck(k)
    k.rect(39, 47, 15, 18, 'C'); k.rect(39, 47, 29, 32, 'C')   # apron straps
    k.rect(41, 47, 19, 28, 'W')                               # shirt
    standard_face(k, talk, iris='E', brow='h')
    k.rect(29, 30, 16, 18, 'R'); k.rect(29, 30, 29, 31, 'R')   # rosy cheeks
    # bandana / headscarf
    k.ell(17, 23.5, 6, 11, 'P', 10, 20)
    k.rect(17, 19, 13, 34, 'P'); k.rect(19, 19, 13, 34, 'p')
    k.recolour(10, 19, 30, 35, 'P', 'p')
    k.rect(18, 22, 35, 37, 'P'); k.rect(21, 24, 37, 38, 'p')   # knot tail
    for r, c in ((13, 18), (15, 24), (12, 28), (16, 30)): k.px(r, c, 'W')
    k.rect(20, 24, 13, 14, 'H')                                 # hair tufts
    # towel over shoulder
    k.rect(39, 46, 33, 38, 'W'); for_c = [k.px(r, 35, 'w') for r in range(39, 47)]
    return k.outline()

def warrior(talk):
    k = C(); shoulders(k, 'X', 'x')
    k.recolour(43, 47, 36, 47, 'x', 'D')
    k.rect(42, 47, 20, 27, 'A'); k.rect(42, 47, 26, 27, 'a'); k.rect(42, 42, 20, 27, 'G')
    k.rect(37, 41, 15, 32, 'x'); k.rect(37, 41, 29, 32, 'D'); k.rect(38, 38, 16, 28, 'X')
    k.ell(5, 27, 3.5, 7, 'A', 1, 9); k.ell(7, 33, 3, 5, 'a', 4, 10); k.ell(3, 25, 2, 4, 'A', 1, 5)
    k.ell(22, 23.5, 15, 13.5, 'X', 7, 40)
    k.recolour(7, 40, 30, 37, 'X', 'x'); k.recolour(7, 40, 34, 37, 'x', 'D')
    k.rect(11, 12, 13, 26, 'W'); k.rect(14, 14, 11, 36, 'G'); k.rect(15, 15, 11, 36, 'g')
    k.rect(19, 37, 15, 32, 'S'); k.rect(19, 19, 15, 32, 's'); k.rect(31, 37, 30, 32, 's'); k.rect(37, 37, 16, 31, 's')
    k.rect(18, 39, 12, 15, 'x'); k.rect(18, 39, 12, 12, 'X')
    k.rect(18, 39, 32, 35, 'D'); k.rect(18, 39, 32, 32, 'x')
    for r in (22, 30): k.px(r, 13, 'G'); k.px(r, 34, 'G')
    k.rect(16, 29, 23, 24, 'x'); k.rect(17, 29, 23, 23, 'X'); k.rect(28, 29, 22, 25, 'x')
    k.rect(30, 30, 22, 25, 's')
    brows(k); eyes(k)
    mouth(k, talk)
    return k.outline()

def paladin(talk):
    k = C(); shoulders(k, 'X', 'x')
    k.rect(40, 47, 16, 31, 'W'); k.recolour(40, 47, 28, 31, 'W', 'w')   # tabard
    k.ell(44, 23.5, 2.5, 2.5, 'G')                                        # sun emblem
    for d in (-4, 4): k.px(44, 23 + d, 'G'); k.px(44 + d // 2, 23, 'G')
    k.rect(36, 39, 15, 32, 'X'); k.rect(36, 39, 29, 32, 'x'); k.rect(36, 36, 15, 32, 'G')
    # halo crest
    k.ell(6, 23.5, 4, 10, 'P', 2, 10); k.ell(6, 23.5, 2, 7, '.', 4, 8)
    k.ell(23, 23.5, 15, 13, 'X', 8, 38)
    k.recolour(8, 38, 30, 37, 'X', 'x')
    k.rect(8, 22, 23, 24, 'G')                        # gold ridge
    k.rect(17, 17, 11, 36, 'G')
    k.rect(19, 36, 16, 31, 'S'); k.rect(19, 19, 16, 31, 's'); k.rect(30, 36, 29, 31, 's')
    k.rect(18, 37, 12, 15, 'X'); k.rect(18, 37, 32, 35, 'x')
    k.rect(18, 37, 15, 15, 'G'); k.rect(18, 37, 32, 32, 'G')
    brows(k); eyes(k, 'E'); nose(k); mouth(k, talk)
    return k.outline()

def hooded(k, A, a, trim=None, mask=False):
    # hood shape around face
    k.ell(26, 23.5, 19, 16, A, 6, 47)
    k.recolour(6, 47, 31, 40, A, a)
    k.ell(27, 23.5, 13, 10.5, '.', 15, 40)

def cleric(talk):
    k = C(); shoulders(k, 'W', 'w')
    hooded(k, 'W', 'w')
    k.rect(38, 47, 21, 26, 'G'); k.rect(39, 47, 22, 25, 'W')   # stole
    neck(k); k.rect(38, 41, 18, 29, 'w')
    standard_face(k, talk, iris='E')
    k.rect(15, 19, 15, 32, 'H'); k.recolour(15, 19, 29, 32, 'H', 'h')   # fringe
    k.rect(19, 19, 17, 30, 'S')
    # gold trim on hood edge
    for r in range(13, 42):
        for c in range(N):
            if k.g[r][c] in 'Ww' and any(0 <= c + d < N and k.g[r][c + d] in 'SsHh' for d in (-1, 1)):
                k.g[r][c] = 'G'
    # lily emblem on brow of hood
    k.rect(9, 11, 23, 24, 'P'); k.px(10, 22, 'P'); k.px(10, 25, 'P'); k.px(12, 23, 'p'); k.px(12, 24, 'p')
    return k.outline()

def rogue(talk):
    k = C(); shoulders(k, 'A', 'a')
    hooded(k, 'A', 'a')
    neck(k)
    standard_face(k, False, iris='E', narrow=True)
    k.rect(15, 20, 15, 32, 'H'); k.rect(19, 20, 15, 22, 'h')   # swept fringe
    # mask over lower face
    k.rect(28, 41, 14, 33, 'C'); k.recolour(28, 41, 29, 33, 'C', 'c')
    k.rect(28, 28, 14, 33, 'c')
    if talk: k.rect(33, 33, 21, 26, 'c'); k.px(34, 22, 'c'); k.px(34, 25, 'c')
    k.rect(42, 46, 30, 33, 'x'); k.rect(40, 41, 31, 32, 'G')   # dagger hilt peeking
    return k.outline()

def ranger(talk):
    k = C(); shoulders(k, 'C', 'c')
    k.rect(39, 47, 12, 14, 'H'); k.rect(39, 47, 13, 13, 'h')  # quiver strap
    for c in (10, 12, 14): k.rect(37, 40, c, c, 'W')           # fletching
    hooded(k, 'A', 'a')
    neck(k)
    standard_face(k, talk, iris='E')
    k.rect(15, 19, 15, 32, 'H'); k.rect(19, 20, 26, 32, 'H'); k.recolour(15, 20, 29, 32, 'H', 'h')
    k.ell(41, 23.5, 2, 3, 'G')                                 # leaf clasp
    k.px(41, 23, 'g'); k.px(41, 24, 'g')
    for r, c in ((30, 16), (31, 18), (30, 29)): k.px(r, c, 's')   # freckles
    return k.outline()

def mage(talk):
    k = C(); shoulders(k, 'A', 'a')
    k.rect(38, 47, 22, 25, 'G')
    # long hair framing
    k.ell(26, 23.5, 17, 14, 'H', 9, 44)
    k.recolour(9, 44, 30, 38, 'H', 'h')
    neck(k)
    standard_face(k, talk, iris='P')
    k.rect(14, 18, 15, 32, 'H'); k.recolour(14, 18, 29, 32, 'H', 'h')
    # circlet with flame gem
    k.rect(17, 17, 13, 34, 'G')
    k.ell(17, 23.5, 2, 2, 'P'); k.px(16, 23, 'W')
    k.px(13, 23, 'P'); k.px(14, 24, 'P'); k.rect(14, 14, 23, 23, 'p')
    return k.outline()

def monk(talk):
    k = C(); shoulders(k, 'A', 'a')
    k.rect(39, 47, 13, 34, 'A'); k.recolour(39, 47, 25, 34, 'A', 'a')
    k.rect(39, 47, 21, 23, 'S')                                  # open robe
    for c in range(14, 34, 2): k.px(40 + abs(c - 24) // 4, c, 'H')  # prayer beads
    neck(k)
    standard_face(k, talk, iris='E')
    k.ell(23, 23.5, 12, 10, 'S', 11, 18)                         # shaved crown
    k.recolour(11, 20, 30, 34, 'S', 's')
    k.rect(17, 18, 13, 34, 'C'); k.rect(18, 18, 13, 34, 'c')     # headband
    k.rect(17, 22, 35, 36, 'C'); k.rect(20, 25, 36, 37, 'c')
    k.rect(12, 13, 21, 22, 'W')                                   # shine
    k.px(19, 23, 'P'); k.px(19, 24, 'P')                          # tilak-style dot
    return k.outline()

def bard(talk):
    k = C(); shoulders(k, 'A', 'a')
    k.rect(39, 43, 17, 30, 'W'); k.rect(42, 43, 17, 30, 'w')     # ruff collar
    # lute neck in corner
    k.rect(30, 47, 39, 41, 'C'); k.rect(28, 31, 38, 42, 'c')
    for r in (29, 30): k.px(r, 37, 'G'); k.px(r, 43, 'G')
    neck(k)
    standard_face(k, talk, iris='E')
    # curly hair
    for (r, c) in ((18, 13), (22, 12), (26, 13), (18, 34), (22, 35), (26, 34), (14, 16), (13, 22), (13, 28), (15, 32)):
        k.ell(r, c, 3, 3, 'H')
    k.recolour(10, 30, 30, 38, 'H', 'h')
    # feathered cap, tilted
    k.ell(14, 22, 5, 13, 'C', 8, 17); k.rect(16, 17, 9, 36, 'C'); k.rect(17, 17, 9, 36, 'c')
    k.recolour(8, 17, 28, 38, 'C', 'c')
    for i in range(10): k.px(10 - i // 2, 28 + i, 'P'); k.px(11 - i // 2, 28 + i, 'P')
    k.rect(3, 6, 36, 38, 'p')
    return k.outline()

def shadow(talk):
    k = C()
    k.ell(48, 23.5, 10, 23, 'A', 37)
    k.ell(26, 23.5, 18, 15, 'A', 5, 44)
    k.rect(3, 6, 22, 25, 'A'); k.rect(1, 3, 23, 24, 'A')      # hood point
    # smoke wisps curling off the edges
    for (r0, c) in ((8, 9), (14, 6), (20, 5)):
        k.rect(r0, r0 + 3, c, c + 1, 'A'); k.rect(r0 - 2, r0, c - 1, c, 'A')
    for (r0, c) in ((9, 37), (15, 40), (21, 41)):
        k.rect(r0, r0 + 3, c, c + 1, 'A'); k.rect(r0 - 2, r0, c + 1, c + 2, 'A')
    k.ell(27, 23.5, 12, 10, 'a', 15, 39)                      # void face
    # eyes
    e = 'P' if not talk else 'W'
    k.rect(23, 25, 17, 20, 'P'); k.rect(23, 25, 27, 30, 'P')
    k.rect(24, 24, 18, 19, e); k.rect(24, 24, 28, 29, e)
    if talk:
        k.rect(32, 33, 19, 28, 'p'); k.rect(32, 32, 21, 26, 'P')
    else:
        k.rect(33, 33, 21, 26, 'p')
    return k.outline()

def champion(talk):
    """Hollow Champion: the hero, emptied and twisted by fate."""
    k = hero(talk)
    g = k.g
    swap = {'S': 'S', 's': 's', 'H': 'H', 'h': 'h', 'A': 'A', 'a': 'a', 'P': 'P'}
    # re-key colours handled by palette; add cracks + hollow eyes
    for r in range(22, 27):
        for c in range(16, 32):
            if g[r][c] in 'WE': g[r][c] = 'K'
    g[24][19] = 'P'; g[24][28] = 'P'
    for (r, c) in ((26, 17), (27, 18), (28, 18), (29, 19), (20, 29), (21, 30), (22, 30), (31, 29), (32, 30)):
        g[r][c] = 'K'
    # cracked hourglass clasp
    for r in range(41, 45): g[r][23 + (r % 2)] = 'K'
    # tattered cloak edge
    for c in range(13, 35, 3): g[47][c] = '.'; g[46][c] = '.'
    return k

def rememberer(talk):
    """Last Rememberer: the wizard, warped into fate's keeper."""
    k = wizard(talk)
    g = k.g
    for r in range(22, 27):
        for c in range(16, 32):
            if g[r][c] in 'WE': g[r][c] = 'P'
    g[24][19] = 'W'; g[24][28] = 'W'
    # cracked clock face + tattered hat brim
    for (r, c) in ((7, 21), (8, 21), (10, 23), (11, 23)): g[r][c] = 'K'
    for c in range(10, 38, 4): g[18][c] = '.'
    for (r, c) in ((27, 17), (28, 18), (27, 30), (28, 29)): g[r][c] = 'K'   # gaunt lines
    return k

# ---------- palettes ----------
BASE = {'K': '#1a1a24', 'W': '#eef2f8', 'w': '#b9c2d0', 'M': '#5a1e1e', 'B': '#55331d',
        'G': '#e8b840', 'g': '#a07a20', 'X': '#c4ccd8', 'x': '#7d8796', 'D': '#4a5260',
        'S': '#e8b08a', 's': '#c4876a', 'E': '#3c6eaa', 'R': '#e0866e'}
def P(**kw): d = dict(BASE); d.update(kw); return d

CAST = [
    ('hero', 'The Fixed Point', hero, P(H='#5a3a24', h='#3e2818', A='#2f7f86', a='#1f5a60', P='#7fe8ff', g='#2f7f86')),
    ('wizard', 'The Wizard', wizard, P(A='#5b3aa0', a='#3e2672', C='#e8b840', P='#ffe680', E='#5a8ad0')),
    ('tavern', 'Tavern Keeper', tavern, P(A='#7a4a2a', a='#55331d', C='#3a2a1a', P='#c0392b', p='#8e2a20', H='#8a5a34', h='#5e3a20', S='#dca07a', s='#b87a5c')),
    ('warrior', 'Warrior', warrior, P(A='#c83a2b', a='#8e2a20')),
    ('paladin', 'Paladin', paladin, P(P='#ffe680', E='#3c6eaa', S='#c98e68', s='#a06a4c')),
    ('cleric', 'Cleric', cleric, P(H='#d8c27a', h='#a8924e', P='#f4f0ff', p='#9fd88a', E='#6a9a4a')),
    ('rogue', 'Rogue', rogue, P(A='#3a3a4a', a='#26262f', C='#4a2a3a', c='#2e1a24', H='#20202a', h='#16161c', E='#c0a040', S='#d8a27e', s='#b07c5e')),
    ('ranger', 'Ranger', ranger, P(A='#3f6b34', a='#2a4a22', C='#6a4a2a', c='#4a321c', H='#a8552a', h='#7a3a1c', E='#4a8a3a', G='#9fd060', g='#5f9030')),
    ('mage', 'Mage', mage, P(A='#9a2a3a', a='#6a1a26', H='#2a2a3a', h='#1a1a26', P='#ff8a3a', p='#ffd060', S='#f0c8a8', s='#cc9e80')),
    ('monk', 'Monk', monk, P(A='#d8862a', a='#a8601a', C='#c0392b', c='#8e2a20', H='#6a3a1a', P='#c0392b', S='#b07850', s='#8a5a3a')),
    ('bard', 'Bard', bard, P(A='#3a6ab0', a='#2a4a80', C='#9a3a8a', c='#6a2a60', H='#c07a30', h='#8a5420', P='#f0e070', p='#c0a040')),
    ('shadow', 'Shadow / Nemesis', shadow, P(A='#18141f', a='#2c2438', P='#c03ae0', p='#7a2a90')),
    ('champion', 'The Hollow Champion', champion, P(H='#3a3a44', h='#24242c', A='#3a1a24', a='#240e16', P='#ff3a3a', S='#9a9aa4', s='#6e6e7a', G='#6a6a72', g='#3a1a24')),
    ('rememberer', 'The Last Rememberer', rememberer, P(A='#1e1a26', a='#110e16', C='#6a5a8a', P='#b06aff', G='#5a4a7a', W='#9a9aa8', w='#6a6a7a', S='#a8a0b0', s='#7a7288', B='#55331d')),
]

def to_img(grid, pal):
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    for r in range(N):
        for c in range(N):
            ch = grid[r][c]
            if ch != '.':
                h = pal[ch].lstrip('#'); im.putpixel((c, r), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im

data, imgs = {}, []
for key, name, fn, pal in CAST:
    fr = {}
    for state in ('closed', 'talk'):
        g = fn(state == 'talk').g
        fr[state] = [''.join(row) for row in g]
    used = sorted(set(''.join(fr['closed'] + fr['talk'])) - {'.'})
    missing = [u for u in used if u not in pal]
    assert not missing, (key, missing)
    data[key] = {'name': name, 'pal': {u: pal[u] for u in used}, **fr}
    imgs.append((key, name, to_img(fr['closed'], pal), to_img(fr['talk'], pal)))

with open('portraits.js', 'w') as f:
    f.write('// 30 x to Remember - dialogue portraits. 48x48 text sprites, one char per pixel, "." = transparent.\n')
    f.write('// Each entry: name, pal (char -> colour), closed (mouth shut), talk (mouth open). Alternate closed/talk while text types.\n')
    f.write('const PORTRAITS = ' + json.dumps(data, indent=1) + ';\n')

# sprite sheet: one row per character, [closed, talk]
sheet = Image.new('RGBA', (N * 2, N * len(imgs)), (0, 0, 0, 0))
for i, (_, _, a, b) in enumerate(imgs):
    sheet.paste(a, (0, i * N)); sheet.paste(b, (N, i * N))
sheet.save('portraits_sheet.png')

# labelled preview grid
S, cols = 4, 4
cell_w, cell_h = N * S + 24, N * S + 44
rows = (len(imgs) + cols - 1) // cols
pv = Image.new('RGBA', (cols * cell_w + 12, rows * cell_h + 12), (30, 36, 64, 255))
d = ImageDraw.Draw(pv); f = ImageFont.load_default(15)
for i, (key, name, a, b) in enumerate(imgs):
    x = 12 + (i % cols) * cell_w; y = 12 + (i // cols) * cell_h
    d.rectangle([x - 2, y - 2, x + N * S + 1, y + N * S + 1], fill=(26, 26, 36))
    d.rectangle([x, y, x + N * S - 1, y + N * S - 1], fill=(60, 72, 110))
    pv.alpha_composite(b.resize((N * S, N * S), Image.NEAREST), (x, y))
    w = d.textlength(name, font=f)
    d.text((x + (N * S - w) / 2, y + N * S + 8), name, fill=(232, 184, 64), font=f)
pv.save('portraits_preview.png')
print('ok', len(imgs))
