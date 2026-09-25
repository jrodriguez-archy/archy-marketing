"""Shared style builders for the Offsite dumps.

A dump is Paper's own answers, transcribed: `get_tree_summary` verbatim plus the
`get_computed_styles` map. These helpers only shorten the transcription - every value
still comes from Paper, never from a guess about what a layer "should" be.
"""
import json, io, os

import sys; sys.dont_write_bytecode = True   # never write __pycache__ into the plugin folder

import archywork   # dumps are written to <work>/dump, never beside this file

def abs_(l, t, **kw):
    d = {"position": "absolute", "left": "%spx" % l, "top": "%spx" % t}
    d.update(kw); return d

def flex(col=False, gap=0, justify=None, align=None, **kw):
    d = {"display": "flex"}
    if col: d["flexDirection"] = "column"
    if gap: d["gap"] = "%spx" % gap
    if justify: d["justifyContent"] = justify
    if align: d["alignItems"] = align
    d.update(kw); return d

def txt(font, size, line, color, track=None, upper=False, one=False, **kw):
    d = {"fontFamily": font, "fontSize": "%spx" % size,
         "lineHeight": "%spx" % line, "color": color}
    if track is not None: d["letterSpacing"] = "%sem" % track
    if upper: d["textTransform"] = "uppercase"
    if one: d.update(whiteSpace="pre", width="max-content")
    d.update(kw); return d

def fill(color, **kw):
    d = {"backgroundColor": color}; d.update(kw); return d

def ruler(l, t, color="var(--color-light-border)", opacity=None):
    d = abs_(l, t, backgroundColor=color)
    if opacity is not None: d["opacity"] = str(opacity)
    return d

def image(l, t, path, size="cover", **kw):
    """A local capture. Paper stores it percent-encoded behind file://; the converter
    undoes that, so the dump keeps the exact string Paper reported."""
    from urllib.parse import quote
    url = "file://" + quote(path)
    d = abs_(l, t, backgroundImage='url("%s")' % url, backgroundSize=size)
    d.update(kw); return d

def write(name, tree, styles, text=None, coords=None, svg=None, background=None, out=None):
    d = {"name": name, "tree": tree, "styles": styles}
    if text: d["text"] = text
    if coords: d["coords"] = coords
    if svg: d["svgAssets"] = svg
    if background: d["background"] = background
    os.makedirs(archywork.work("dump"), exist_ok=True)
    path = archywork.work("dump", out)
    io.open(path, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
    print("wrote dump/%s" % out)

WHITE  = "var(--color-white)"
NAVY   = "var(--color-light-text)"
ROYAL  = "var(--color-royal-blue-500)"
GREY   = "var(--color-neutral)"
GREY_L = "var(--color-neutral-light)"
TINT2  = "var(--color-blue-tint-200)"
TINT3  = "var(--color-blue-tint-300)"
BORDER = "var(--color-light-border)"


CDN = "https://app.paper.design/file-assets/01M1PF91YQFBYZZ1VGDN592AJP/%s"

def photo(asset, size="cover", **kw):
    """A Paper-hosted picture. fetch-photos.py caches it; the dump keeps the URL Paper
    reported, so the mapping is one place and the dump stays a transcript."""
    d = {"backgroundImage": "url(%s)" % (CDN % asset), "backgroundSize": size,
         "backgroundPosition": "50%"}
    d.update(kw); return d

def photo_frame(l, t, mat=False):
    """The deck's two photo containers: a plain clipping window, or the same with a 12px
    white mat down the top and right edge."""
    if mat:
        return abs_(l, t, overflow="clip", paddingTop="12px", paddingRight="12px",
                    backgroundColor=WHITE)
    return abs_(l, t, overflow="clip")

TITLE_BIG = lambda: txt("Onest-SemiBold", 94, 110, NAVY, track=-0.02)


EYEBROW = lambda: txt("Inter-SemiBold", 24, 28, ROYAL, track=0.05, upper=True, one=True)

def bordered(l, t, sides="all", width="2px"):
    """A screenshot frame. `sides` is a subset of 'trbl' when the shot butts against
    another one and the seam has to stay open - slide 12 does this between the nav strip
    and the hero."""
    d = abs_(l, t, overflow="clip")
    if sides == "all":
        d.update(borderWidth=width, borderStyle="solid", borderColor=BORDER)
    else:
        for side in sides:
            k = {"t": "Top", "r": "Right", "b": "Bottom", "l": "Left"}[side]
            d["border%sWidth" % k] = width
            d["border%sStyle" % k] = "solid"
            d["border%sColor" % k] = BORDER
    return d

def light(**kw):
    d = fill("var(--color-light-background)"); d.update(overflow="clip", **kw); return d

def royal(**kw):
    d = fill(ROYAL); d.update(overflow="clip", **kw); return d

def dark(**kw):
    d = fill("var(--color-dark-background)"); d.update(overflow="clip", **kw); return d


def growth_chart(name, ids, eyebrow, head1, head2, bars, notes, out,
                 legend=("ACTUAL", "2026 YTD")):
    """The growth-chart slide: a five-bar plot in the left column, three Ruler-separated
    figures in the right one.

    Every chart in the deck shares the baseline y=976 - the axis Ruler sits there and the
    tallest bar reaches up from it - which is what makes two chart slides read as the same
    system when you page between them. The bar heights are Paper's own measured values,
    not recomputed here: the placeholder data is still `NN`.

    `bars` is [(frameId, valueId, valueW, rectId, rectH, yearId, yearW, year, forecast)].
    `notes` is [(frameId, valueId, value, labelId, label)] - three of them.
    """
    (ab, rulers, rTop, rHead, rFoot, rvL, rvR, rvSplit, rAxis, rN1, rN2,
     metaF, metaT, headF, eyeT, hlF, hl1, hl2, chartF, legF,
     k1F, k1S, k1T, k2F, k2S, k2T, plotF) = ids

    lines = ['Frame "%s" (%s) 1920×1080' % (name, ab),
             '  Frame "Rulers" (%s) 1920×1080' % rulers]
    for nid, w, h in [(rTop,1920,2),(rHead,1920,2),(rFoot,1920,2),(rvL,2,814),(rvR,2,814),
                      (rvSplit,2,810),(rAxis,1056,2),(rN1,672,2),(rN2,672,2)]:
        lines.append('    Rectangle "Ruler" (%s) %d×%d' % (nid, w, h))
    lines += ['  Frame "Meta" (%s) 1728×28' % metaF,
              '    Text "ARCHY © 2026" (%s) 194×28 "ARCHY © 2026"' % metaT,
              '  Frame "Header" (%s) 1728×112' % headF,
              '    Text "Eyebrow" (%s) 1728×28 "%s"' % (eyeT, eyebrow),
              '    Frame "Headline" (%s) 1728×70' % hlF,
              '      Text "Headline Line 1" (%s) %d×70 "%s"' % (hl1[0], hl1[1], head1),
              '      Text "Headline Line 2" (%s) %d×70 "%s"' % (hl2[0], hl2[1], head2),
              '  Frame "Chart" (%s) 1056×810' % chartF,
              '    Frame "Legend" (%s) 976×24' % legF,
              '      Frame "Key" (%s) %d×24' % (k1F, 26 + len(legend[0]) * 0 + 89),
              '        Rectangle "Swatch" (%s) 16×16' % k1S,
              '        Text "%s" (%s) 89×24 "%s"' % (legend[0], k1T, legend[0]),
              '      Frame "Key" (%s) %d×24' % (k2F, 26 + 107),
              '        Rectangle "Swatch" (%s) 16×16' % k2S,
              '        Text "%s" (%s) 107×24 "%s"' % (legend[1], k2T, legend[1]),
              '    Frame "Plot" (%s) 976×658' % plotF]
    for (bf, vf, vw, rf, rh, yf, yw, year, fc) in bars:
        lines.append('      Frame "Bar %s" (%s) 128×%d' % (year, bf, 38 + 8 + rh + 8 + 24))
        lines.append('        Text "Value" (%s) %d×38 "NN"' % (vf, vw))
        lines.append('        Rectangle "Rectangle" (%s) 128×%d' % (rf, rh))
        lines.append('        Text "Year" (%s) %d×24 "%s"' % (yf, yw, year))
    for i, (nf, vf, value, lf, label) in enumerate(notes):
        lines.append('  Frame "Note %d" (%s) 592×%d' % (i + 1, nf, 269 if i < 2 else 268))
        lines.append('    Text "Value" (%s) 592×84 "%s"' % (vf, value))
        lines.append('    Text "Label" (%s) 592×24 "%s"' % (lf, label))

    st = {
      ab: dict(fill(WHITE), overflow="clip"),
      rulers: abs_(0, 0),
      rTop: ruler(0, 20), rHead: ruler(0, 244), rFoot: ruler(0, 1056),
      rvL: ruler(96, 244), rvR: ruler(1822, 244), rvSplit: ruler(1152, 246),
      rAxis: ruler(96, 976), rN1: ruler(1152, 515), rN2: ruler(1152, 786),
      metaF: dict(abs_(96, 96), **flex(justify="end")),
      metaT: txt("Inter-Medium", 24, 28, GREY_L, track=0.05),
      headF: dict(abs_(96, 96), **flex(col=True, gap=14)),
      eyeT: txt("Inter-SemiBold", 24, 28, ROYAL, track=0.05),
      hlF: flex(gap=16, align="baseline"),
      hl1[0]: txt("Onest-SemiBold", 60, 70, NAVY, track=-0.02, one=True),
      hl2[0]: txt("Onest-SemiBold", 60, 70, GREY, track=-0.02, one=True),
      chartF: dict(abs_(96, 246), **flex(col=True, gap=32,
                   paddingBlock="48px", paddingInline="40px")),
      legF: flex(gap=32, align="center"),
      k1F: flex(gap=10, align="center"),
      k1S: fill(TINT2),
      k1T: txt("Inter-SemiBold", 20, 24, GREY, track=0.05, one=True),
      k2F: flex(gap=10, align="center"),
      k2S: fill(ROYAL),
      k2T: txt("Inter-SemiBold", 20, 24, ROYAL, track=0.05, one=True),
      plotF: flex(gap=84, align="end"),
    }
    for (bf, vf, vw, rf, rh, yf, yw, year, fc) in bars:
        st[bf] = flex(col=True, gap=8, align="center", justify="end")
        st[vf] = txt("Inter-SemiBold", 30, 38, ROYAL if fc else GREY)
        st[rf] = fill(ROYAL if fc else TINT2)
        st[yf] = txt("Inter-SemiBold", 20, 24, ROYAL if fc else GREY, track=0.05)
    for i, (nf, vf, value, lf, label) in enumerate(notes):
        st[nf] = dict(abs_(1192, [246, 517, 788][i]), **flex(col=True, gap=6, justify="center"))
        st[vf] = txt("Onest-SemiBold", 80, 84, ROYAL, track=-0.02)
        st[lf] = txt("Inter-SemiBold", 20, 24, GREY, track=0.05)

    write(name, "\n".join(lines), st, out=out)


def session_divider(name, ids, number, eyebrow, title, lead, pill_label,
                    title_h, pill_w, label_w, eyebrow_w, out, lead_pin,
                    content_h, head_h, lead_w=1100):
    """A session divider: the ghost number at 25% opacity, a vertically centred content
    block, and the wordmark bottom-right. Royal-blue ground, so the wordmark is white."""
    (ab, rulers, rTop, rFoot, ghost, metaF, metaT, contentF, headF, eyeT, titleT,
     leadT, pillF, pillT, wordF, wordSvg) = ids
    # content_h and head_h are Paper's own measured values, straight off the tree. They
    # were derived here once and came out 9px short - a fit-content head with padding does
    # not add up to the sum of its parts, and guessing it moved the whole block.
    tree = '\n'.join([
      'Frame "%s" (%s) 1920×1080' % (name, ab),
      '  Frame "Rulers" (%s) 1920×1080' % rulers,
      '    Frame "Ruler H Top" (%s) 1920×2' % rTop,
      '    Frame "Ruler H Foot" (%s) 1920×2' % rFoot,
      '  Text "Ghost Number" (%s) 1728×520 "%s"' % (ghost, number),
      '  Frame "Meta" (%s) 1728×22' % metaF,
      '    Text "Meta Copyright" (%s) 146×22 "ARCHY © 2026"' % metaT,
      '  Frame "Content" (%s) 1100×%d' % (contentF, content_h),
      '    Frame "Head" (%s) 1100×%d' % (headF, head_h),
      '      Text "Eyebrow" (%s) %d×24 "%s"' % (eyeT, eyebrow_w, eyebrow),
      '      Text "Title" (%s) 1100×%d "%s"' % (titleT, title_h, title),
      '    Text "Lead" (%s) %d×76 "LEAD"' % (leadT, lead_w),
      '    Frame "Value Pill" (%s) %d×60' % (pillF, pill_w),
      '      Text "Value Label" (%s) %d×24 "%s"' % (pillT, label_w, pill_label),
      '  Frame "Wordmark" (%s) 180×70' % wordF,
      '    SVG "SVG" (%s) 180×70' % wordSvg,
    ])
    st = {
      ab: royal(),
      rulers: abs_(0, 0),
      rTop: ruler(0, 20, WHITE, 0.3), rFoot: ruler(0, 1056, WHITE, 0.3),
      ghost: dict(abs_(96, 278), **txt("Onest-SemiBold", 520, 520, WHITE, track=-0.02),
                  textAlign="right", opacity="0.25"),
      metaF: dict(abs_(96, 96), **flex(justify="end", align="center", gap=20)),
      metaT: txt("Inter-Medium", 18, 22, TINT2, track=0.05, upper=True, one=True),
      contentF: dict(flex(col=True, gap=40, align="start"),
                     position="absolute", left="96px", top="50%", translate="0 -50%"),
      headF: flex(col=True, gap=28, align="start", paddingBottom="18px"),
      eyeT: txt("Inter-SemiBold", 20, 24, TINT2, track=0.05, upper=True, one=True),
      titleT: txt("Onest-SemiBold", 96, 96, WHITE, track=-0.02),
      leadT: txt("Onest", 30, 38, TINT2),
      pillF: dict(flex(justify="center", align="center"),
                  paddingBlock="18px", paddingInline="32px",
                  borderRadius="var(--radius-pill)", backgroundColor=WHITE),
      pillT: txt("Inter-SemiBold", 20, 24, "var(--color-primary-blue-600)",
                 track=0.05, upper=True, one=True),
      wordF: abs_(1644, 926),
    }
    write(name, tree, st, text={leadT: lead}, coords={leadT: lead_pin},
          svg={wordSvg: "assets/archy-wordmark.png"}, out=out)


def chapter(name, ids, title, title_h, out):
    """A chapter card: one 160/160 title, vertically centred in the left half, with the
    full-height spine at 959. Royal-blue ground."""
    ab, rulers, rTop, rFoot, rDiv, metaF, metaT, chapF, chapT = ids
    tree = '\n'.join([
      'Frame "%s" (%s) 1920×1080' % (name, ab),
      '  Frame "Rulers" (%s) 1920×1080' % rulers,
      '    Frame "Ruler H Top" (%s) 1920×2' % rTop,
      '    Frame "Ruler H Foot" (%s) 1920×2' % rFoot,
      '    Frame "Ruler V Divider" (%s) 2×1038' % rDiv,
      '  Frame "Meta" (%s) 1728×22' % metaF,
      '    Text "Meta Copyright" (%s) 146×22 "ARCHY © 2026"' % metaT,
      '  Frame "Chapter" (%s) 864×%d' % (chapF, title_h),
      '    Text "Chapter Title" (%s) 864×%d "%s"' % (chapT, title_h, title),
    ])
    st = {
      ab: royal(),
      rulers: abs_(0, 0),
      rTop: ruler(0, 20, WHITE, 0.3), rFoot: ruler(0, 1056, WHITE, 0.3),
      rDiv: ruler(959, 20, WHITE, 0.3),
      metaF: dict(abs_(96, 96), **flex(justify="end", align="center", gap=20)),
      metaT: txt("Inter-Medium", 18, 22, TINT2, track=0.05, upper=True, one=True),
      chapF: dict(flex(col=True, align="start"),
                  position="absolute", left="96px", top="50%", translate="0px -50%"),
      chapT: txt("Onest-SemiBold", 160, 160, WHITE, track=-0.02),
    }
    write(name, tree, st, out=out)


def testimonials(name, ids, eyebrow, head1, h1w, head2, h2w, quotes, stats, out, pins):
    """Two quote columns and a stats column split in two.

    The portrait carries `margin-top: auto`, which is what holds both attributions on one
    lane however long the quotes run - the reason CLAUDE.md forbids shortening a quote to
    make it fit. Quote text is transcribed verbatim and never edited.
    """
    (ab, rulers, rTop, rHead, rFoot, rvL, rvQuotes, rvStats, rvRight, rStatsSplit,
     metaF, metaT, headF, eyeT, hlF, hl1, hl2) = ids
    lines = ['Frame "%s" (%s) 1920×1080' % (name, ab),
             '  Frame "Rulers" (%s) 1920×1080' % rulers]
    for nid, w, h in [(rTop,1920,2),(rHead,1920,2),(rFoot,1920,2),(rvL,2,814),
                      (rvQuotes,2,810),(rvStats,2,814),(rvRight,2,814),(rStatsSplit,576,2)]:
        lines.append('    Rectangle "Ruler" (%s) %d×%d' % (nid, w, h))
    lines += ['  Frame "Meta" (%s) 1728×28' % metaF,
              '    Text "ARCHY © 2026" (%s) 194×28 "ARCHY © 2026"' % metaT,
              '  Frame "Header" (%s) 1728×112' % headF,
              '    Text "Eyebrow" (%s) 1728×28 "%s"' % (eyeT, eyebrow),
              '    Frame "Headline" (%s) 1728×70' % hlF,
              '      Text "Headline Line 1" (%s) %d×70 "%s"' % (hl1, h1w, head1),
              '      Text "Headline Line 2" (%s) %d×70 "%s"' % (hl2, h2w, head2)]
    st = {
      ab: dict(fill(WHITE), overflow="clip"),
      rulers: abs_(0, 0),
      rTop: ruler(0, 20), rHead: ruler(0, 244), rFoot: ruler(0, 1056),
      rvL: ruler(96, 244), rvQuotes: ruler(672, 246), rvStats: ruler(1248, 244),
      rvRight: ruler(1822, 244), rStatsSplit: ruler(1248, 651),
      metaF: dict(abs_(96, 96), **flex(justify="end")),
      metaT: txt("Inter-Medium", 24, 28, GREY_L, track=0.05),
      headF: dict(abs_(96, 96), **flex(col=True, gap=14)),
      eyeT: txt("Inter-SemiBold", 24, 28, ROYAL, track=0.05),
      hlF: flex(gap=16, align="baseline"),
      hl1: txt("Onest-SemiBold", 60, 70, NAVY, track=-0.02, one=True),
      hl2: txt("Onest-SemiBold", 60, 70, GREY, track=-0.02, one=True),
    }
    text = {}
    for (qname, qid, x, markId, bodyId, bodyH, portraitId, asset,
         nameId, nameW, person, roleId, roleW, role, quote) in quotes:
        lines.append('  Frame "%s" (%s) 496×810' % (qname, qid))
        lines.append('    Text "Quote Mark" (%s) 70×116 "“"' % markId)
        lines.append('    Text "Quote Body" (%s) 496×%d "BODY"' % (bodyId, bodyH))
        lines.append('    Rectangle "Portrait" (%s) 120×120' % portraitId)
        lines.append('    Text "Name" (%s) %d×48 "%s"' % (nameId, nameW, person))
        lines.append('    Text "Role" (%s) %d×36 "%s"' % (roleId, roleW, role))
        st[qid] = dict(abs_(x, 246), **flex(col=True, align="start"), paddingBlock="44px")
        st[markId] = txt("Onest-SemiBold", 140, 116, ROYAL)
        st[bodyId] = dict(txt("Onest", 32, 46, NAVY), marginTop="20px")
        st[portraitId] = dict(marginTop="auto", borderRadius="calc(infinity * 1px)",
                              overflow="clip", flexShrink="0",
                              backgroundColor="var(--color-blue-tint-100)",
                              **photo(asset))
        st[nameId] = dict(txt("Onest-SemiBold", 40, 48, NAVY, track=-0.01), marginTop="20px")
        st[roleId] = dict(txt("Inter", 26, 36, GREY), marginTop="6px")
        text[bodyId] = quote
    for (sname, sid, y, h, valId, valW, value, labId, labW, label, noteId, noteW, note) in stats:
        lines.append('  Frame "%s" (%s) 496×%d' % (sname, sid, h))
        lines.append('    Text "Value" (%s) %d×124 "%s"' % (valId, valW, value))
        lines.append('    Text "Label" (%s) %d×28 "%s"' % (labId, labW, label))
        lines.append('    Text "Note" (%s) %d×30 "%s"' % (noteId, noteW, note))
        st[sid] = dict(abs_(1288, y), **flex(col=True, gap=8, align="start", justify="center"))
        st[valId] = txt("Onest-SemiBold", 120, 124, ROYAL, track=-0.02)
        st[labId] = dict(txt("Inter-SemiBold", 24, 28, NAVY, track=0.05), marginTop="8px")
        st[noteId] = txt("Inter", 22, 30, GREY)
    write(name, "\n".join(lines), st, text=text, coords=pins, out=out)


def shot_and_points(name, ids, eyebrow, head1, h1w, head2, h2w,
                    shot, points, out, pins):
    """A bordered product shot in the left column, three Ruler-separated points in the
    right. Slides 50 / 51 / 53 are all this shape."""
    (ab, rulers, rTop, rHead, rFoot, rvL, rvSplit, rvRight, rP1, rP2,
     metaF, metaT, headF, eyeT, hlF, hl1, hl2, shotId) = ids
    shotName, sx, sy, sw, sh, asset = shot
    lines = ['Frame "%s" (%s) 1920×1080' % (name, ab),
             '  Frame "Rulers" (%s) 1920×1080' % rulers]
    for nid, w, h in [(rTop,1920,2),(rHead,1920,2),(rFoot,1920,2),(rvL,2,814),
                      (rvSplit,2,810),(rvRight,2,814),(rP1,672,2),(rP2,672,2)]:
        lines.append('    Rectangle "Ruler" (%s) %d×%d' % (nid, w, h))
    lines += ['  Frame "Meta" (%s) 1728×28' % metaF,
              '    Text "ARCHY © 2026" (%s) 194×28 "ARCHY © 2026"' % metaT,
              '  Frame "Header" (%s) 1728×112' % headF,
              '    Text "Eyebrow" (%s) 1728×28 "%s"' % (eyeT, eyebrow),
              '    Frame "Headline" (%s) 1728×70' % hlF,
              '      Text "Headline Line 1" (%s) %d×70 "%s"' % (hl1, h1w, head1),
              '      Text "Headline Line 2" (%s) %d×70 "%s"' % (hl2, h2w, head2),
              '  Rectangle "%s" (%s) %d×%d' % (shotName, shotId, sw, sh)]
    st = {
      ab: dict(fill(WHITE), overflow="clip"),
      rulers: abs_(0, 0),
      rTop: ruler(0, 20), rHead: ruler(0, 244), rFoot: ruler(0, 1056),
      rvL: ruler(96, 244), rvSplit: ruler(1152, 246), rvRight: ruler(1822, 244),
      rP1: ruler(1152, 515), rP2: ruler(1152, 786),
      metaF: dict(abs_(96, 96), **flex(justify="end")),
      metaT: txt("Inter-Medium", 24, 28, GREY_L, track=0.05),
      headF: dict(abs_(96, 96), **flex(col=True, gap=14)),
      eyeT: txt("Inter-SemiBold", 24, 28, ROYAL, track=0.05),
      hlF: flex(gap=16, align="baseline"),
      hl1: txt("Onest-SemiBold", 60, 70, NAVY, track=-0.02, one=True),
      hl2: txt("Onest-SemiBold", 60, 70, GREY, track=-0.02, one=True),
      shotId: dict(abs_(sx, sy), borderWidth="2px", borderStyle="solid",
                   borderColor=BORDER, **photo(asset)),
    }
    text = {}
    for (pname, pid, y, h, tid, title, th, bid, bh, body) in points:
        lines.append('  Frame "%s" (%s) 592×%d' % (pname, pid, h))
        lines.append('    Text "Title" (%s) 592×%d "%s"' % (tid, th, title))
        lines.append('    Text "Body" (%s) 592×%d "BODY"' % (bid, bh))
        st[pid] = dict(abs_(1192, y), **flex(col=True, gap=12, align="start", justify="center"))
        st[tid] = txt("Onest-SemiBold", 40, 48, NAVY, track=-0.02)
        st[bid] = txt("Inter", 26, 36, GREY)
        text[bid] = body
    write(name, "\n".join(lines), st, text=text, coords=pins, out=out)
