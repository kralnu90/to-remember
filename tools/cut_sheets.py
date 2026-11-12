import sys, json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

def cut(path, bgs, thr, name, grow=6, minarea=400):
    im = np.asarray(Image.open(path).convert('RGB')).astype(int)
    H, W, _ = im.shape
    near = np.zeros((H, W), bool)
    for bg in bgs:
        near |= np.sqrt(((im - np.array(bg)) ** 2).sum(2)) < thr
    # background = bg-like pixels connected to a bg region that touches a big bg area (flood from all "near" seeds of size)
    lab, n = nd.label(near)
    sizes = nd.sum(near, lab, range(1, n + 1))
    bgmask = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 3000])
    fg = ~bgmask
    fg = nd.binary_opening(fg, iterations=1)
    # group parts of one figure (sparkles, flames) by growing
    grown = nd.binary_dilation(fg, iterations=grow)
    lab2, n2 = nd.label(grown)
    frames = []
    for i in range(1, n2 + 1):
        ys, xs = np.where((lab2 == i) & fg)
        if len(ys) < minarea: continue
        frames.append((xs.min(), ys.min(), xs.max(), ys.max(), i))
    frames.sort(key=lambda f: (round(f[1] / 150), f[0]))
    rgba = np.dstack([im, (fg * 255)]).astype(np.uint8)
    out = []
    for k, (x0, y0, x1, y1, i) in enumerate(frames):
        a = rgba[y0:y1 + 1, x0:x1 + 1].copy()
        keep = (lab2[y0:y1 + 1, x0:x1 + 1] == i)
        a[..., 3] = np.where(keep, a[..., 3], 0)
        Image.fromarray(a).save(f'{name}_{k:02d}.png')
        out.append([k, int(x0), int(y0), int(x1 - x0 + 1), int(y1 - y0 + 1)])
    # overlay for review
    ov = Image.open(path).convert('RGB'); dr = ImageDraw.Draw(ov)
    for k, x0, y0, w, h in out:
        dr.rectangle([x0, y0, x0 + w - 1, y0 + h - 1], outline=(255, 60, 60)); dr.text((x0 + 2, y0 + 2), str(k), fill=(255, 255, 0))
    ov.save(f'{name}_overlay.png')
    json.dump(out, open(f'{name}.json', 'w'))
    print(name, len(out))

cut('/mnt/user-data/uploads/196d2cb0-image.jpg', [(34, 39, 69)], 26, 'hero')
cut('/mnt/user-data/uploads/03266357-image.jpg', [(56, 69, 103), (29, 34, 63)], 24, 'wiz')
