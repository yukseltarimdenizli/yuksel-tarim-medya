# Özgün cami silüeti (SVG) — Yüksel Tarım altın tonlarında
def cami_svg(w=1080, h=620, renk="#D4A445", renk2="#F5D58A", op=1.0):
    import itertools
    global _SAY
    _SAY = globals().get("_SAY", 0) + 1; u = f"c{_SAY}"
    cx = w/2; zemin = h-10
    p = []
    def kubbe(x, y, r):  # yarım küre + alem
        return (f'<path d="M{x-r},{y} A{r},{r*1.05} 0 0 1 {x+r},{y} Z"/>'
                f'<rect x="{x-1.5}" y="{y-r*1.05-34}" width="3" height="34"/>'
                f'<circle cx="{x}" cy="{y-r*1.05-38}" r="5"/>')
    def minare(x, top, gen=22):
        s = (f'<rect x="{x-gen/2}" y="{top}" width="{gen}" height="{zemin-top}"/>'
             f'<rect x="{x-gen/2-7}" y="{top+90}" width="{gen+14}" height="9" rx="3"/>'
             f'<rect x="{x-gen/2-7}" y="{top+190}" width="{gen+14}" height="9" rx="3"/>'
             f'<path d="M{x-gen/2},{top} L{x},{top-95} L{x+gen/2},{top} Z"/>'
             f'<rect x="{x-1.2}" y="{top-128}" width="2.4" height="34"/>')
        return s
    # gövde
    p.append(f'<rect x="{cx-300}" y="{zemin-150}" width="600" height="150"/>')
    p.append(f'<rect x="{cx-210}" y="{zemin-215}" width="420" height="70"/>')
    p.append(kubbe(cx, zemin-215, 170))           # ana kubbe
    p.append(kubbe(cx-240, zemin-150, 70)); p.append(kubbe(cx+240, zemin-150, 70))
    p.append(kubbe(cx-125, zemin-215, 48)); p.append(kubbe(cx+125, zemin-215, 48))
    p.append(minare(cx-390, zemin-470)); p.append(minare(cx+390, zemin-470))
    # kemerli kapılar/pencereler (boşluk)
    del_ = "".join(f'<path d="M{x-18},{zemin} L{x-18},{zemin-60} A18,22 0 0 1 {x+18},{zemin-60} L{x+18},{zemin} Z"/>' for x in (cx-150, cx-75, cx+75, cx+150))
    del_ += f'<path d="M{cx-34},{zemin} L{cx-34},{zemin-95} A34,40 0 0 1 {cx+34},{zemin-95} L{cx+34},{zemin} Z"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="opacity:{op}">'
            f'<defs><linearGradient id="g{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{renk2}"/><stop offset="1" stop-color="{renk}"/></linearGradient>'
            f'<mask id="m{u}"><rect width="{w}" height="{h}" fill="white"/><g fill="black">{del_}</g></mask></defs>'
            f'<g fill="url(#g{u})" mask="url(#m{u})">{"".join(p)}</g>'
            f'<rect x="0" y="{zemin}" width="{w}" height="10" fill="{renk}"/></svg>')
if __name__ == "__main__":
    open("cami.svg","w").write(cami_svg())
