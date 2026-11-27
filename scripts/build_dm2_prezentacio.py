#!/usr/bin/env python3
"""A Diplomamunka II. beszámoló diasora (8 perc, 10 dia), a korábbi diasor kinézetével (python-pptx).

Minden adat a dolgozat v0.5-ös változatából (thesis/, v0.17) származik; a diák alján a forrás.
Felépítés (a konzulensi visszajelzés szerint): probléma → irodalomkutatás (4 dia, kb. 4,5 perc) →
kutatási rés → javasolt megoldás → architektúra → várt eredmények → összegzés.

Használat:
    python scripts/build_dm2_prezentacio.py docs/prezentaciok/kutatasi_eredmenyek_2026-10-14.pptx \
        architektura.png kimenet.pptx
Az ábra képként: pdftoppm -r 220 -png -singlefile thesis/img/agent_architektura.pdf architektura
Az első argumentum a korábbi diasor (sablonként: fejléc, lábléc, címdia).
"""

from __future__ import annotations

import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

SRC, ARCH, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
NAVY = RGBColor(0x1D, 0x29, 0x4D)
AMBER = RGBColor(0xFC, 0xAF, 0x17)
SKY = RGBColor(0x9A, 0xD1, 0xF0)
SKY_T = RGBColor(0xE6, 0xF3, 0xFB)
AMBER_T = RGBColor(0xFE, 0xEF, 0xCF)
GREY_T = RGBColor(0xF3, 0xF4, 0xF7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x1D, 0x29, 0x4D)
MUTED = RGBColor(0x5A, 0x63, 0x7A)

prs = Presentation(SRC)
# a címdia marad, a többi dia törlődik (a sablon mesterdiája és elrendezései megmaradnak)
sld = prs.slides._sldIdLst
for s_id in list(sld)[1:]:
    prs.part.drop_rel(s_id.rId)
    sld.remove(s_id)
LAYOUT = next(lay for lay in prs.slide_masters[0].slide_layouts if lay.name == "1_8_tartalomrész")


def txt(slide, x, y, w, h, runs, size=14, color=TEXT, bold=False, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, name=None):
    """runs: str vagy bekezdések listája; egy bekezdés lehet str vagy [(szöveg, {opciók})]."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        parts = para if isinstance(para, list) else [(para, {})]
        for t, o in parts:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(o.get("size", size))
            r.font.bold = o.get("bold", bold)
            r.font.italic = o.get("italic", False)
            r.font.color.rgb = o.get("color", color)
        if i < len(paras) - 1:
            p.space_after = Pt(5)
    return tb


def box(slide, x, y, w, h, fill, name=None, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    if name:
        s.name = name
    return s


def table(slide, x, y, widths, rows, size=11, row_h=0.4, highlight=(), name=None):
    """highlight: {sorindex: kitöltőszín}"""
    nrows, ncols = len(rows), len(widths)
    gt = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y),
                                Inches(sum(widths)), Inches(row_h * nrows))
    if name:
        gt.name = name
    t = gt.table
    t.first_row = True
    t.horz_banding = False
    for j, w in enumerate(widths):
        t.columns[j].width = Inches(w)
    hl = dict(highlight)
    for i, row in enumerate(rows):
        t.rows[i].height = Inches(row_h)
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.fill.solid()
            if i == 0:
                c.fill.fore_color.rgb = NAVY
            elif i in hl:
                c.fill.fore_color.rgb = hl[i]
            else:
                c.fill.fore_color.rgb = WHITE if i % 2 else GREY_T
            c.margin_left = c.margin_right = Inches(0.06)
            c.margin_top = c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            r = tf.paragraphs[0].add_run()
            r.text = val
            r.font.size = Pt(size)
            r.font.color.rgb = WHITE if i == 0 else TEXT
            r.font.bold = i == 0 or j == 0 or i in hl
    return gt


def content_slide(title, notes):
    s = prs.slides.add_slide(LAYOUT)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == 0:
            ph.text_frame.text = title
            for r in ph.text_frame.paragraphs[0].runs:
                r.font.size = Pt(28)
                r.font.bold = True
                r.font.color.rgb = NAVY
            ph.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
        elif ph.placeholder_format.idx == 1:
            ph._element.getparent().remove(ph._element)
    s.notes_slide.notes_text_frame.text = notes
    return s


def kicker(slide, text):
    """Felirat a lábléc jobb oldalán: hol tartunk az előadás ívében."""
    txt(slide, 4.3, 7.12, 5.45, 0.3, text, size=12, bold=True, color=WHITE, align=PP_ALIGN.RIGHT,
        anchor=MSO_ANCHOR.MIDDLE, name="Szakasz")


def source(slide, text, y=6.62):
    txt(slide, 0.3, y, 9.4, 0.28, text, size=9, color=MUTED, name="Forrás")


def card(slide, x, y, w, h, big, small, fill, fg, big_size=28, small_size=12, name=None):
    box(slide, x, y, w, h, fill, name=name)
    txt(slide, x + 0.18, y + 0.15, w - 0.36, 0.6, big, size=big_size, bold=True, color=fg,
        anchor=MSO_ANCHOR.MIDDLE)
    txt(slide, x + 0.18, y + 0.8, w - 0.36, h - 0.9, small, size=small_size, color=fg)


# ============ 1. Címdia (kb. 15 mp) ============
t = prs.slides[0]
vals = {
    0: "Agent-alapú, metrika-vezérelt IDS-riasztásaggregáció SOC-környezetben",
    13: "Diplomamunka II. – beszámoló",
    14: "Nagy József\nKiberbiztonsági mérnöki MSc",
    15: "Konzulens:\nVörösné Dr. Bánáti-Baumann Anna",
}
for ph in t.placeholders:
    i = ph.placeholder_format.idx
    if i in vals:
        ph.text_frame.text = vals[i]
        if i in (14, 15):
            for para in ph.text_frame.paragraphs:
                for r in para.runs:
                    r.font.size = Pt(16)
t.notes_slide.notes_text_frame.text = (
    "[kb. 15 mp] Jó napot kívánok! Nagy József vagyok, a diplomamunkám a behatolásérzékelők "
    "riasztásainak csoportosításáról és rangsorolásáról szól. "
    "Az előadás íve: a probléma, a szakirodalom eredménye és a kutatási rés, a javasolt megoldás "
    "és felépítése, végül az, hogyan mérem és mit várok."
)

# ============ 2. A probléma (kb. 50 mp) ============
s = content_slide(
    "Túl sok riasztás, kevés valódi támadás",
    "[kb. 50 mp] A biztonsági műveleti központok elemzőit elárasztják a riasztások, és ezek túlnyomó "
    "része nem valódi támadás. A nyilvános AIT-ADS adathalmaz egyik forgatókönyvében a hálózati "
    "riasztásoknak kevesebb mint fél százaléka valódi: minden valódi riasztásra kétszáz további jut.\n\n"
    "Axelsson az alapgyakoriság-hibára vezette vissza: ha tízezer "
    "eseményből egy támadás, és az érzékelő minden támadást észrevesz, de a többi esemény egy "
    "százalékára is jelez, akkor száz riasztásból csak egy lesz valódi.\n\n"
    "Alahmadi és szerzőtársai elemzőkkel készített felmérése szerint a téves riasztások nagy része "
    "nem hibás észlelés, hanem a szervezet jóindulatú működése váltja ki. A túlterhelt csapatok "
    "ezért elnyomó szabályokat írnak, vagy csak a súlyosságra hagyatkoznak – ez vakfoltokat hagy, "
    "amelyeket a támadó kihasználhat. Vagyis a már kiadott riasztásokat jól kell rangsorolni.",
)
kicker(s, "1 / 4 · PROBLÉMAFELVETÉS")
card(s, 0.3, 1.9, 2.95, 2.15, "< 0,5%", "az AIT-ADS egyik forgatókönyvében a hálózati riasztások "
     "közül ennyi valódi – 1 valódira 200 további jut", NAVY, WHITE, name="Kártya 1")
card(s, 3.55, 1.9, 2.95, 2.15, "1 : 100", "1 támadás 10 000 eseményből, 1% téves jelzés mellett: "
     "100 riasztásból 1 valódi (alapgyakoriság-hiba)", AMBER, NAVY, name="Kártya 2")
card(s, 6.8, 1.9, 2.95, 2.15, "jóindulatú", "a téves riasztások nagy része a szervezet szokásos "
     "működéséből fakad, nem hibás észlelésből (20 + 21 elemző)", SKY, NAVY, name="Kártya 3")
box(s, 0.3, 4.35, 9.4, 2.05, SKY_T, name="Következmény doboz")
txt(s, 0.55, 4.5, 8.9, 1.8, [
    [("A következmény", {"bold": True, "size": 18})],
    ("A túlterhelt elemzők elnyomó szabályokat írnak, vagy csak az eszköz súlyossági szintjére "
    "hagyatkoznak – ez a támadó számára kihasználható vakfoltokat hagy."),
    [("A feladat: ", {"bold": True}), (("a már kiadott riasztásokat úgy csoportosítani és rangsorolni, "
                                      "hogy az elemző figyelme a valószínűleg valódiakra jusson."), {})],
], size=14)
source(s, "Forrás: Uetz és mtsai. 2026; Axelsson 2000; Alahmadi és mtsai. 2022; Ndichu és mtsai. 2026 "
          "(a dolgozat 1.1 és 2.5 pontja)")

# ============ 3. Irodalom I: csoportosítás (kb. 65 mp) ============
s = content_slide(
    "Szakirodalom 1/4: csoportosítás",
    "[kb. 65 mp] Az irodalmat két fő feladat mentén dolgoztam fel: csoportosítás és rangsorolás, "
    "és külön megnéztem az agentes és nyelvi modelles megoldásokat.\n\n"
    "Csoportosításban öt módszercsaládot találtam. A legegyszerűbb a kulcsmezők és időablak alapján "
    "von össze: gyors és átlátható, de az ablak megválasztásától függ. Landauer tartományfüggetlen "
    "hasonlósággal kb. 80%-kal csökkentette az elemző elé kerülő csoportok számát. Julisch "
    "ok-feltárásnál néhány tucat kiváltó ok adta a riasztások több mint 90%-át – ha ezeket "
    "megszüntetjük, a zaj forrását szüntetjük meg. A többlépcsős korreláció a támadási láncot mutatja, "
    "de előre rögzített tudást igényel. A tanuló módszerek pontosak: a DeepCASE az események "
    "86,72%-át kezelte automatikusan – de tanítást igényelnek, és nehezen magyarázhatók.\n\n"
    "A fontos tanulság: a csoportosítás csökkenti a tételek számát, de egyik sem mondja meg, "
    "melyik csoport a legfontosabb.",
)
kicker(s, "2 / 4 · SZAKIRODALOM")
table(s, 0.3, 1.85, [2.35, 2.3, 2.35, 2.4], [
    ["Módszercsalád", "Erősség", "Gyengeség", "Mért eredmény"],
    ["Kulcsmezők és időablak", "gyors, tanítás nélküli, átlátható", "az ablak és a mezők megválasztásától függ", "a gyakorlatban legelterjedtebb"],
    ["Tartományfüggetlen hasonlóság", "tetszőleges riasztásformára", "zajban a csoportok összemosódnak", "kb. 80%-kal kevesebb csoport"],
    ["Ok-feltárás", "a zaj okát szünteti meg", "utólagos, nem rangsorol", "néhány tucat ok → a riasztások > 90%-a"],
    ["Többlépcsős korreláció", "a támadási láncot egyben mutatja", "előre rögzített tudás vagy tanítás kell", "–"],
    ["Gépi tanulás, gráf", "pontos, zajtűrő", "tanítást igényel, nehezen magyarázható", "86,72% automatikusan kezelve"],
], size=10.5, row_h=0.56, name="Csoportosítás-táblázat")
box(s, 0.3, 5.45, 9.4, 1.0, AMBER_T, name="Tanulság")
txt(s, 0.5, 5.53, 9.0, 0.85, [
    [("Tanulság: ", {"bold": True}), (("a csoportosítás a tételszámot csökkenti, de nem mondja meg, "
                                      "melyik csoport a legfontosabb – ehhez rangsorolás kell."), {})],
], size=14, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Forrás: a dolgozat 3.2 pontja és 3.1. táblázata – Valeur és mtsai. 2004; Landauer és mtsai. "
          "2022; Julisch 2003; van Ede és mtsai. 2022; Karner és mtsai. 2026")

# ============ 4. Irodalom II: rangsorolás (kb. 70 mp) ============
s = content_slide(
    "Szakirodalom 2/4: rangsorolás",
    "[kb. 70 mp] A rangsorolásnál öt családot különítettem el. A súlyosság szerinti sorrend ma a "
    "gyakorlat, de durva és a környezettől független.\n\n"
    "A többszempontú módszerek – például Anuar és szerzőtársai páros összehasonlítása – az érintett "
    "eszköz fontosságát is súlyozzák: náluk minden incidens sorba állítható volt, míg a "
    "sérülékenységek szabványos pontozásával csak 17%-uk. A környezetet használó módszerek – Porras, "
    "Kruegel, Njogu – a gép fontosságát és sérülékenységét veszik figyelembe, de szűrnek: hiányos "
    "nyilvántartásnál valódi támadást is eltávolítanak, ezt Sommestad és Franke kísérlete is "
    "megmutatta. A tanuló módszerek, mint a NoDoze, 86%-kal csökkentették a téves riasztásokat, de "
    "címkét vagy részletes gépi naplót igényelnek.\n\n"
    "A legerősebb, tanítás nélküli módszer a kockázatalapú pontozás: Uetz és szerzőtársai nyolc "
    "adathalmazon 0,72-ről 0,92-re emelték a rangsor-pontosságot, és ha az elemző csak a lista első "
    "10%-át nézi át, a 44 valódi riasztásból 43-at látja, súlyosság szerint csak 28,6-ot. Ez lesz az "
    "összehasonlítási alapom.",
)
kicker(s, "2 / 4 · SZAKIRODALOM")
table(s, 0.3, 1.85, [2.2, 1.15, 1.05, 5.0], [
    ["Módszercsalád", "Környezet", "Tanítás", "Fő eredmény és gyengeség"],
    ["Súlyosság", "nem", "nem", "a mai gyakorlat; durva, a környezettől független"],
    ["Többszempontú (AHP, fuzzy)", "igen", "nem", "minden incidens rangsorolható (CVSS-sel csak 17,23%); súlyok érzékenységvizsgálat nélkül"],
    ["Környezet és ellenőrzés", "igen", "nem", "szűr: hiányos nyilvántartásnál valódi támadást is eltávolít"],
    ["Tanuló, származáskövető", "részben", "igen", "86%-kal kevesebb téves riasztás; címke vagy gépi napló kell"],
    ["Kockázatalapú pontozás", "nem", "nem", "a legerősebb nyilvánosan mért, tanítás nélküli módszer"],
], size=10.5, row_h=0.5, highlight={5: AMBER_T}, name="Rangsorolás-táblázat")
card(s, 0.3, 5.05, 4.55, 1.45, "0,72 → 0,92", "rangsor-pontosság, 8 adathalmaz átlaga: súlyosság "
     "vs. kockázatalapú pontozás", NAVY, WHITE, big_size=24, small_size=12, name="Kártya RBA 1")
card(s, 5.15, 5.05, 4.55, 1.45, "43 / 44  vs.  28,6", "valódi riasztás a lista első 10%-ában: "
     "kockázatalapú vs. súlyosság szerinti sorrend", AMBER, NAVY, big_size=24, small_size=12,
     name="Kártya RBA 2")
source(s, "Forrás: a dolgozat 3.3 pontja és 3.2. táblázata – Anuar és mtsai. 2013; Porras és mtsai. 2002; "
          "Kruegel és mtsai. 2004; Njogu és mtsai. 2013; Sommestad, Franke 2015; Hassan és mtsai. 2019; "
          "Uetz és mtsai. 2026", y=6.58)

# ============ 5. Irodalom III: agentek és nyelvi modellek (kb. 65 mp) ============
s = content_slide(
    "Szakirodalom 3/4: agentek, nyelvi modellek",
    "[kb. 65 mp] Az agent-alapú felépítés nem új: a többágenses behatolásérzékelő rendszerek már "
    "régóta önálló, cserélhető összetevőkre bontják a feladatot, szabályalapú döntésekkel.\n\n"
    "Az új hullám a nagy nyelvi modelleké. A CORTEX több nyelvimodell-agenttel pontosabb lett: az "
    "F1-érték 0,66-ról 0,78-ra nőtt, a téves riasztási arány 24,9-ről 14,2%-ra csökkent. Az ára: "
    "riasztásonként 5,7-szer több szöveget dolgozott fel, és egy riasztás 152 másodpercig tartott, "
    "3,4-szeres lassulással. Az AgentSOC-nál a futásidő 95%-át a nyelvi modell tette ki, és egy kis, "
    "részben mesterséges környezetben mértek. Liu és Wang azt mutatta meg, hogy a kis, helyben "
    "futó modellek önállóan nem tudnak végigvinni egy vizsgálatot; ha viszont a lépések sorrendjét "
    "külső, kiszámítható vezérlő adja, a sikeres befejezés aránya 0,125-ről 1-re nő.\n\n"
    "A tanulság: a nyelvi modell a szöveg értelmezésére és magyarázatára jó, a pontozást és a "
    "lépések sorrendjét kiszámítható programra kell bízni.",
)
kicker(s, "2 / 4 · SZAKIRODALOM")
card(s, 0.3, 1.9, 2.95, 2.25, "0,66 → 0,78", "CORTEX: F1 több agenttel – de 5,7× több "
     "szöveg és 3,4× lassabb (152 s / riasztás)", NAVY, WHITE, big_size=26, name="Kártya CORTEX")
card(s, 3.55, 1.9, 2.95, 2.25, "95%", "AgentSOC: a futásidő ennyi részét a nyelvi modell teszi ki; "
     "kis, részben mesterséges környezetben mérve", AMBER, NAVY, big_size=26, name="Kártya AgentSOC")
card(s, 6.8, 1.9, 2.95, 2.25, "0,125 → 1,0", "HESP: helyi kis modell befejezési aránya, ha a "
     "lépések sorrendjét külső vezérlő adja", SKY, NAVY, big_size=26, name="Kártya HESP")
box(s, 0.3, 4.45, 9.4, 1.95, SKY_T, name="Tanulság doboz")
txt(s, 0.55, 4.6, 8.9, 1.7, [
    [("Tanulság a tervezéshez", {"bold": True, "size": 18})],
    ("A nyelvi modell lassú, költséges és nem megismételhető – a szöveg értelmezésére és a "
    "magyarázatra jó, a pontozásra és a vezérlésre nem."),
    [("Ezért: ", {"bold": True}), (("a pontszámot és a sorrendet kiszámítható program adja, a nyelvi "
                                   "modell csak ellenőrzött magyarázatot ír."), {})],
], size=14)
source(s, "Forrás: a dolgozat 3.4 pontja és 3.3. táblázata – Bougueroua és mtsai. 2021; Wei és mtsai. "
          "2025 (CORTEX); Roy és mtsai. 2026 (AgentSOC); Liu, Wang 2026 (HESP)")

# ============ 6. Irodalom IV: a kutatási rés (kb. 60 mp) ============
s = content_slide(
    "Szakirodalom 4/4: a kutatási rés",
    "[kb. 60 mp] Az irodalomkutatás eredményét ez a táblázat foglalja össze: minden sorban egy "
    "hiányosság, és mellette, hogyan válaszol rá a tervezett rendszer.\n\n"
    "A legfontosabb az első sor. A legerősebb nyilvános, tanítás nélküli módszer, a kockázatalapú "
    "pontozás csak a riasztások folyamából dolgozik: nem tudja, mennyire fontos az érintett gép, "
    "működhet-e rajta a támadás, és mennyire látjuk. A környezetet használó módszerek viszont szűrnek, "
    "és ezért hiányos nyilvántartásnál valódi támadást is elrejtenek. A nyelvimodelles megoldások "
    "lassúak és nem megismételhetők, és a legtöbbjük nem nyilvános vagy mesterséges adaton mér.\n\n"
    "A kutatási kérdésem ezért: mennyit javít a környezeti információ egy már erős, nyilvánosan "
    "mért rangsoroláson, ha nem szűrünk vele, és megismételhető módon mérjük?",
)
kicker(s, "2 / 4 · SZAKIRODALOM → KUTATÁSI RÉS")
table(s, 0.3, 1.85, [4.55, 4.85], [
    ["Hiányosság a szakirodalomban", "A tervezett rendszer válasza"],
    ["A legerősebb tanítás nélküli módszer nem használ környezetet", "a kockázati pontszám bővítése: gép fontossága, sérülékenység, megfigyeltség"],
    ["A környezeti módszerek szűrnek – valódi támadás is eltűnhet", "a környezet csak súly, riasztást nem töröl"],
    ["A szakértői súlyok hatását ritkán vizsgálják", "páros összehasonlítás, érzékenységvizsgálat, tanult súlyok"],
    ["A tanuló módszerek címkét igényelnek", "tanítóadat nélkül működik"],
    ["A nyelvimodell-agentek lassúak, nem megismételhetők", "kiszámítható pontozás és vezérlés; a modell csak magyaráz"],
    ["Nem nyilvános vagy mesterséges adaton mérnek", "nyilvános, felcímkézett adathalmaz (AIT-ADS)"],
], size=11, row_h=0.47, highlight={1: AMBER_T}, name="Rés-táblázat")
box(s, 0.3, 5.3, 9.4, 1.15, NAVY, name="Kérdés doboz")
txt(s, 0.55, 5.38, 8.9, 1.0, [
    [("Kutatási kérdés: ", {"bold": True, "color": AMBER}),
     (("mennyit javít a környezeti információ egy már erős, nyilvánosan mért rangsoroláson – "
      "szűrés nélkül, megismételhető méréssel?"), {"color": WHITE})],
], size=15, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Forrás: a dolgozat 3.5 pontja és 3.4. táblázata")

# ============ 7. A javasolt megoldás (kb. 55 mp) ============
s = content_slide(
    "Javasolt megoldás: pontszám + környezet",
    "[kb. 55 mp] A választott megoldás öt követelményből indul: tanítóadat nélkül működjön, "
    "megismételhető legyen, használja a környezetet, ne szűrjön, és az indoka követhető legyen. "
    "A meglévő módszerek egyike sem teljesíti mind az ötöt.\n\n"
    "Az alap a kockázatalapú pontszám, változtatás nélkül átvéve; ehhez adok három környezeti "
    "mérőszámot: a gép fontosságát a szerepéből és hálózati helyéből, a támadás alkalmazhatóságát a "
    "gépen futó szoftverekből, és a megfigyeltséget. Ismeretlen adatnál a semleges 0,5 érték jár, így "
    "a hiányos nyilvántartás sem előre, sem hátra nem sorol.\n\n"
    "A négy mérőszámot súlyozott összeg vonja össze. A súlyokat páros összehasonlítással határozom "
    "meg, a következetességi arány 0,1 alatt kell legyen, és a súlyokat a mérés előtt rögzítem, hogy "
    "az eredmény ne befolyásolhassa őket.",
)
kicker(s, "3 / 4 · JAVASOLT MEGOLDÁS")
box(s, 0.3, 1.85, 9.4, 0.85, NAVY, name="Képlet doboz")
txt(s, 0.5, 1.9, 9.0, 0.75, [[("S", {"bold": True, "color": AMBER, "size": 24}),
                              ("  =  w", {"size": 22, "color": WHITE}), ("r", {"size": 14, "color": WHITE}),
                              (" · r  +  w", {"size": 22, "color": WHITE}), ("g", {"size": 14, "color": WHITE}),
                              (" · g  +  w", {"size": 22, "color": WHITE}), ("a", {"size": 14, "color": WHITE}),
                              (" · a  +  w", {"size": 22, "color": WHITE}), ("m", {"size": 14, "color": WHITE}),
                              (" · m", {"size": 22, "color": WHITE})]],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, name="Képlet")
table(s, 0.3, 2.9, [2.35, 3.95, 3.1], [
    ["Mérőszám", "Jelentés", "Értékek"],
    ["r – kockázati pontszám", "5 részpontszám a riasztások folyamából (változatlanul átvéve)", "0–1, folytonos"],
    ["g – a gép fontossága", "a gép szerepéből és hálózati helyéből, rögzített szabályokkal", "0; 0,25; … ; 1 (ismeretlen: 0,5)"],
    ["a – alkalmazhatóság", "működhet-e a támadás a gépen (szoftverkészlet, CVE)", "0,25; 0,5; 0,75; 1"],
    ["m – megfigyeltség", "mennyire vakfoltos a gép (gépi és hálózati érzékelő)", "0; 0,5; 1"],
], size=11, row_h=0.45, highlight={1: SKY_T}, name="Mérőszám-táblázat")
cards = [("Nem szűr", "a környezet csak súly; riasztás nem tűnik el"),
         ("Semleges hiány", "ismeretlen gép vagy szoftver: 0,5"),
         ("Rögzített súlyok", "páros összehasonlítás, CR < 0,1, a mérés előtt")]
for k, (h, d) in enumerate(cards):
    x = 0.3 + k * 3.25
    box(s, x, 5.3, 2.9, 1.15, AMBER_T, name=f"Elv {k+1}")
    txt(s, x + 0.15, 5.38, 2.6, 1.0, [[(h, {"bold": True, "size": 14})], d], size=12)
source(s, "Forrás: a dolgozat 4. fejezete (4.1–4.3; 4.1–4.3. táblázat); Uetz és mtsai. 2026; Saaty 1990")

# ============ 8. Architektúra (kb. 55 mp) ============
s = content_slide(
    "Felépítés: hét együttműködő agent",
    "[kb. 50 mp] A rendszer hét agentből áll. Az egységesítő közös formára hozza a Suricata és a Wazuh riasztásait, a csoportosító összefogja "
    "az összetartozókat, a környezeti és a sérülékenységi agent a gépnyilvántartásból dolgozik, a "
    "rangsoroló kiszámolja a pontszámot a rögzített súlyokkal. Ez az öt agent kiszámítható program: "
    "a pontszám és a sorrend csak tőlük származik.\n\n"
    "A hatodik, magyarázó agent az egyetlen, amely nyelvi modellt használ – helyben futtatva, és a "
    "szövegét egy ellenőrző lépés vizsgálja: nem tartalmazhat a csoportban nem szereplő gépet vagy "
    "szabályt. A vezérlő a lépések sorrendjét tartja. A megvalósítás három rétegű: a mérések "
    "keretrendszer nélküli Python-modulokon futnak, erre épül a LangGraph-vezérlés, és opcionálisan "
    "egy csak olvasható MCP-csatlakozó.",
)
kicker(s, "3 / 4 · JAVASOLT MEGOLDÁS – ARCHITEKTÚRA")
s.shapes.add_picture(ARCH, Inches(0.3), Inches(1.75), height=Inches(4.8))
x0 = 5.0
layers = [("1. Mag", "keretrendszer nélküli Python-modulok; a mérések ezen futnak", SKY_T),
          ("2. Vezérlés", "LangGraph-állapotgráf; teszt igazolja, hogy ugyanazt a sorrendet adja", SKY_T),
          ("3. Csatlakozó", "MCP, csak olvasható gépnyilvántartás (opcionális)", GREY_T)]
for k, (h, d, fill) in enumerate(layers):
    y = 1.85 + k * 1.0
    box(s, x0, y, 4.7, 0.85, fill, name=f"Réteg {k+1}")
    txt(s, x0 + 0.15, y + 0.07, 4.4, 0.75, [[(h, {"bold": True, "size": 13})], d], size=11)
box(s, x0, 5.0, 4.7, 1.45, AMBER_T, name="Elv doboz")
txt(s, x0 + 0.15, 5.08, 4.4, 1.3, [
    [("A nyelvi modell szerepe", {"bold": True, "size": 13})],
    ("csak magyarázatot ír, helyben fut (Ollama), ellenőrzés vizsgálja; a sorrendet és a pontszámot "
    "nem befolyásolja"),
], size=11)
source(s, "Forrás: a dolgozat 5. fejezete, 5.1. ábra (saját ábra)")

# ============ 9. Várt eredmények (kb. 60 mp) ============
s = content_slide(
    "Mérési terv és várt eredmények",
    "[kb. 55 mp] A hatást lépésenkénti bővítéssel mérem: a súlyosság szerinti sorrendből indulok, "
    "jön a csoportosítás, a kockázatalapú pontozás mint összehasonlítási alap, majd egyenként a "
    "gép fontossága, az alkalmazhatóság és a megfigyeltség. Így minden lépés az új információ "
    "hatását mutatja.\n\n"
    "Két környezetben mérek: a nyilvános AIT-ADS nyolc forgatókönyvén, és egy saját laborban, ahol a "
    "környezeti információ teljes, és a sérülékenységek CVE szinten is illeszthetők. A különbségeket "
    "páros Wilcoxon-próbával vizsgálom a nyolc forgatókönyvön.\n\n"
    "Mit várok? A közölt eredmények szerint a kockázatalapú pontozás az AIT-ADS-en már 0,98–0,99 "
    "rangsor-pontosságú, ezért ott plafonhatás várható; a javulás a lista elején, az átlagos "
    "pontosságban és a terhelés csökkenésében jelentkezhet. A javulást ellenpróbával is ellenőrzöm: "
    "véletlenszerűen összekevert gépfontosság nem adhat ugyanilyen javulást.",
)
kicker(s, "4 / 4 · VÁRT EREDMÉNYEK")
table(s, 0.3, 1.85, [0.7, 3.2, 5.5], [
    ["Lépés", "Rangsorolás alapja", "Mit mutat meg"],
    ["1", "súlyosság", "a mai, egyszerű gyakorlat"],
    ["2", "csoportosítás", "a csoportosítás hatása (tételszám, tisztaság)"],
    ["3", "kockázati pontszám", "az erős, környezetet nem használó alap – visszamérve"],
    ["4", "+ gép fontossága", "a gépnyilvántartás hozzájárulása"],
    ["5", "+ alkalmazhatóság", "a szoftverkészlet hozzájárulása"],
    ["6", "+ megfigyeltség", "a teljes modell (csak a laborban)"],
], size=11, row_h=0.4, highlight={3: SKY_T}, name="Lépés-táblázat")
cards = [("Mérőszámok", "rangsor-pontosság, átlagos pontosság, első 10%, a 98%-hoz átnézendő listarész"),
         ("Statisztika", "páros Wilcoxon-próba, 8 forgatókönyv; hatásnagyság"),
         ("Torzítás ellen", "előzetes rögzítés, ±20%, tanult súlyok, ellenpróba")]
for k, (h, d) in enumerate(cards):
    x = 0.3 + k * 3.25
    box(s, x, 4.75, 2.9, 1.1, SKY_T, name=f"Módszer {k+1}")
    txt(s, x + 0.15, 4.82, 2.6, 0.95, [[(h, {"bold": True, "size": 13})], d], size=11)
box(s, 0.3, 5.95, 9.4, 0.6, AMBER_T, name="Várakozás doboz")
txt(s, 0.5, 5.98, 9.0, 0.55, [[("Várakozás: ", {"bold": True}),
                               (("az AIT-ADS-en plafonhatás (közölt 0,98–0,99) – a javulás a lista elején "
                                "és a terhelésben látszhat; a CVE-szintű hatás a laborban."), {})]],
    size=12, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Forrás: a dolgozat 6. fejezete (6.1–6.3; 6.2–6.3. táblázat); a közölt érték: Uetz és mtsai. 2026",
       y=6.68)

# ============ 10. Összegzés (kb. 25 mp) ============
s = content_slide(
    "Összegzés és a következő félév",
    "[kb. 20 mp] Összefoglalva: a legerősebb, tanítás nélküli módszer nem használja a környezetet, "
    "a környezeti módszerek pedig szűrnek. Az általam javasolt rendszer szűrés nélkül egészíti ki, "
    "és a hatást nyilvános adaton, megismételhetően méri. A "
    "következő félévben a megvalósítás, a mérések és a laboratóriumi tesztek következnek. "
    "Köszönöm a figyelmet!",
)
kicker(s, "ÖSSZEGZÉS")
steps = [("Probléma", "< 0,5% valódi riasztás; elnyomó szabályok, vakfoltok", NAVY, WHITE),
         ("Rés", "a legerősebb módszer nem használ környezetet; a környezetiek szűrnek", AMBER, NAVY),
         ("Megoldás", "kockázati pontszám + 3 környezeti mérőszám, hét agent, a nyelvi modell csak magyaráz", SKY, NAVY),
         ("Mérés", "lépésenként, AIT-ADS 8 forgatókönyv + labor, Wilcoxon-próba", SKY_T, NAVY)]
for k, (h, d, fill, fg) in enumerate(steps):
    y = 1.85 + k * 0.95
    box(s, 0.3, y, 9.4, 0.82, fill, name=f"Ív {k+1}")
    txt(s, 0.5, y + 0.06, 1.9, 0.7, h, size=16, bold=True, color=fg, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 2.4, y + 0.06, 7.1, 0.7, d, size=13, color=fg, anchor=MSO_ANCHOR.MIDDLE)
box(s, 0.3, 5.75, 9.4, 0.7, GREY_T, name="Következő félév")
txt(s, 0.5, 5.8, 9.0, 0.6, [[("Diplomamunka III.: ", {"bold": True}),
                            (("megvalósítás, mérés a 8 forgatókönyvön, laboratóriumi tesztek, "
                             "eredmények és elemzés."), {})]], size=13, anchor=MSO_ANCHOR.MIDDLE)

prs.save(OUT)
print("ok", len(prs.slides))
