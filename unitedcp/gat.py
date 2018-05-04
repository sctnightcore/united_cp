import struct
from PIL import Image, ImageDraw
from ragnarokcp import settings


class Gat:
    def __init__(self, fh):
        fh.read(6)  # Not Needed(Header)
        self._xs, = struct.unpack('i', fh.read(4))
        self._ys, = struct.unpack('i', fh.read(4))

        n = self._xs * self._ys
        x = 0
        y = 0
        self._m = dict()
        fh.read(16)
        for xy in range(0, n):
            if x not in self._m:
                self._m[x] = dict()
            flag, = struct.unpack('i', fh.read(4))
            if flag == 0:
                self._m[x][y] = True
            else:
                self._m[x][y] = False
            x += 1
            if x == self._xs:
                x = 0
                y += 1
            fh.read(16)

    def c(self, x, y):
        if x < 0 or x >= self._xs or y < 0 or y >= self._ys:
            return False
        return self._m[x][y]

    def near_free(self, x, y, mr=8):
        s = [[1, 0], [0, -1], [-1, 0], [0, 1]]
        if self.c(x, y):
            return [x, y]
        for r in range(1, mr + 1):
            ax = x - r
            ay = y + r
            for j in range(0, 4):
                for k in range(0, 2 * r):
                    if self.c(ax, ay):
                        return [ax, ay]
                    ax += s[j][0]
                    ay += s[j][1]
        return False

    def r(self, x, y):
        if x < 0 or x >= self._xs or y < 0 or y >= self._ys:
            return False
        return self.r(x, y)

    def draw_map(self, xc, yc, ret=False, scale=2, mapname=''):
        im = Image.new('RGB', (self._xs * scale, self._ys * scale), (128, 128, 128))
        d = ImageDraw.Draw(im)
        x1 = ((xc * scale) - (scale / 2))
        y1 = ((yc * scale) - (scale / 2))

        for x in range(0, self._xs - 1):
            for y in range(0, self._ys - 1):
                if not self.c(x, y):
                    continue
                d.rectangle([((x * scale) - (scale / 2), (self._ys * scale) - (y * scale) - (scale / 2)),
                             ((x * scale) + (scale / 2), (self._ys * scale) - (y * scale) + (scale / 2))],
                            fill=(0, 0, 0))

        d.ellipse([(x1 - 5, (self._ys * scale) - y1 - 5), (x1 + 5, (self._ys * scale) - y1 + 5)], fill=(255, 0, 0),
                  outline=(0, 0, 0))

        if ret:
            return d
        im.save(settings.os.path.join(settings.BASE_DIR, 'unitedcp/static/images/ragnarok/data/maps/' + mapname + '.png'), 'PNG')
        del d
        return True
