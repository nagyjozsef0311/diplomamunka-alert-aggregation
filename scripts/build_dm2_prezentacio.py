#!/usr/bin/env python3
"""A Diplomamunka II. beszámoló diasora (8 perc, 8 dia: címdia, 6 tartalmi dia, záródia), a korábbi diasor kinézetével (python-pptx).

Minden adat a dolgozat v0.5-ös változatából (thesis/, v0.17) származik.
Felépítés (a konzulensi visszajelzés és a szerző kérése szerint): probléma → csoportosítás →
rangsorolás → kutatási rés és a választás indoka → architektúra és a döntések indoka → várt eredmények.

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


def dia_szam(slide):
    """A dia sorszáma a lábléc jobb oldalán."""
    txt(slide, 7.75, 7.12, 2.0, 0.3, str(len(prs.slides)), size=14, bold=True, color=WHITE,
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, name="Diaszám")



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
    "[kb. 15 mp] Jó napot kívánok! Nagy József vagyok. A diplomamunkám a behatolásérzékelők "
    "riasztásainak csoportosításáról és rangsorolásáról szól: a problémával kezdem, utána a "
    "szakirodalom eredményével és a kutatási réssel, végül a tervezett rendszerrel és a mérés tervével."
)

# ============ 2. Probléma (kb. 60 mp) ============
s = content_slide(
    "Túl sok riasztás, kevés valódi támadás",
    "[kb. 60 mp] A biztonsági műveleti központok elemzőit elárasztják a riasztások. A nyilvános "
    "AIT-ADS adathalmaz egyik forgatókönyvében a hálózati riasztásoknak kevesebb mint fél százaléka "
    "valódi. Ez nem csak beállítási hiba: Axelsson alapgyakoriság-hibája szerint ha tízezer eseményből "
    "egy a támadás, és az érzékelő a többi egy százalékára is jelez, száz riasztásból csak egy valódi. "
    "Az elemzőkkel készült felmérés szerint a téves riasztások nagy részét a szervezet jóindulatú "
    "működése váltja ki.\n\n"
    "A túlterhelt csapatok elnyomó szabályokat írnak, vagy csak a súlyosságra hagyatkoznak, ez "
    "vakfoltokat hagy. A cél ezért az, hogy a már kiadott riasztásokat csoportosítsuk és "
    "rangsoroljuk – úgy, hogy egyetlen riasztás se tűnjön el.",
)
dia_szam(s)
card(s, 0.3, 1.9, 2.95, 2.15, "< 0,5%", "az AIT-ADS egyik forgatókönyvében a hálózati riasztások "
     "közül ennyi valódi", NAVY, WHITE, name="Kártya 1")
card(s, 3.55, 1.9, 2.95, 2.15, "1 : 100", "1 támadás 10 000 eseményből, 1% téves jelzés mellett: "
     "100 riasztásból 1 valódi (alapgyakoriság-hiba)", AMBER, NAVY, name="Kártya 2")
card(s, 6.8, 1.9, 2.95, 2.15, "jóindulatú", "a téves riasztások nagy részét a szervezet szokásos "
     "működése váltja ki, nem hibás észlelés", SKY, NAVY, name="Kártya 3")
box(s, 0.3, 4.35, 9.4, 2.05, SKY_T, name="Cél doboz")
txt(s, 0.55, 4.5, 8.9, 1.8, [
    [("Következmény: ", {"bold": True}), (("elnyomó szabályok és csak súlyosság szerinti szűrés – "
                                         "a támadó számára kihasználható vakfoltok."), {})],
    [("A dolgozat célja", {"bold": True, "size": 17})],
    ("a Suricata hálózati és a Wazuh gépi riasztásait mérőszámok és a környezetről szóló információ "
    "alapján csoportosítani és rangsorolni – szűrés nélkül, megismételhetően mérve."),
], size=14)

# ============ 3. Csoportosítás (kb. 65 mp) ============
s = content_slide(
    "Szakirodalom: a riasztások csoportosítása",
    "[kb. 65 mp] A csoportosításban öt módszercsaládot vizsgáltam. A kulcsmezők és időablak alapján "
    "összevonó módszer a gyakorlatban a legelterjedtebb: gyors, nem kell tanítani, és az elemző "
    "látja, miért került két riasztás egy csoportba. A tartományfüggetlen hasonlóság kb. 80%-kal "
    "kevesebb csoportot adott, de zajban a csoportok összemosódnak. Az ok-feltárás a zaj okát "
    "szünteti meg, de utólagos. A többlépcsős korreláció és a tanuló módszerek pontosabbak – a "
    "DeepCASE az események 86,72%-át kezelte automatikusan –, de előre rögzített tudást vagy "
    "tanítóadatot igényelnek, és nehezen magyarázhatók.\n\n"
    "Ezért választottam a kulcsmezős, időközös csoportosítást: ugyanazt a gépet érintő, egymáshoz "
    "időben közeli riasztások kerülnek egy csoportba. Tanítás nélkül működik és átlátható. A fontos "
    "tanulság viszont az, hogy a csoportosítás csak a tételek számát csökkenti; azt, hogy melyik "
    "csoport a legfontosabb, a rangsorolásnak kell eldöntenie.",
)
dia_szam(s)
table(s, 0.3, 1.85, [2.35, 2.25, 2.55, 2.25], [
    ["Módszercsalád", "Erősség", "Gyengeség", "Mért eredmény"],
    ["Kulcsmezők és időablak", "gyors, tanítás nélküli, átlátható", "az ablak és a mezők megválasztásától függ", "a gyakorlatban legelterjedtebb"],
    ["Tartományfüggetlen hasonlóság", "tetszőleges riasztásformára", "zajban a csoportok összemosódnak", "kb. 80%-kal kevesebb csoport"],
    ["Ok-feltárás", "a zaj okát szünteti meg", "utólagos, nem rangsorol", "néhány tucat ok → a riasztások > 90%-a"],
    ["Többlépcsős korreláció", "a támadási láncot mutatja", "előre rögzített tudás vagy tanítás kell", "–"],
    ["Gépi tanulás, gráf", "pontos, zajtűrő", "tanítás kell, nehezen magyarázható", "86,72% automatikusan kezelve"],
], size=10.5, row_h=0.52, highlight={1: AMBER_T}, name="Csoportosítás-táblázat")
box(s, 0.3, 5.1, 9.4, 1.35, NAVY, name="Választás")
txt(s, 0.5, 5.18, 9.0, 1.2, [
    [("Választás: ", {"bold": True, "color": AMBER}),
     ("kulcsmezők és időköz – ugyanazt a gépet érintő, időben közeli riasztások egy csoportba.",
      {"color": WHITE})],
    [("Miért? ", {"bold": True, "color": AMBER}),
     (("tanítás nélkül működik, megismételhető és átlátható. De a csoportosítás nem dönti el, melyik "
      "csoport a fontos – ehhez rangsorolás kell."), {"color": WHITE})],
], size=13, anchor=MSO_ANCHOR.MIDDLE)

# ============ 4. Rangsorolás (kb. 70 mp) ============
s = content_slide(
    "Szakirodalom: a riasztások rangsorolása",
    "[kb. 70 mp] A rangsorolásban öt családot találtam. A súlyosság szerinti sorrend a mai gyakorlat, "
    "de durva. A többszempontú módszerek – például páros összehasonlítás – a gép fontosságát is "
    "súlyozzák: Anuar és szerzőtársainál minden incidens rangsorolható volt, míg a CVSS alapján "
    "csak 17%-uk; a súlyok hatását viszont nem vizsgálták. A környezetet használó módszerek a gép "
    "fontosságát és sérülékenységét nézik, de szűrnek: Sommestad és Franke kísérletében a szűrés "
    "valódi támadásokat is eltávolított. A tanuló módszerek 86%-kal kevesebb téves riasztást adtak, "
    "de címkét vagy részletes gépi naplót igényelnek – valós SOC-ban ez ritkán van.\n\n"
    "A legerősebb, tanítás nélküli, nyilvánosan mért módszer a kockázatalapú pontozás: nyolc "
    "adathalmazon 0,72-ről 0,92-re emelte a rangsor-pontosságot, és a lista első 10%-ában a 44 "
    "valódi riasztásból 43-at mutatta. Ezt választottam alapnak – csakhogy ez a módszer a "
    "környezetről semmit nem tud.",
)
dia_szam(s)
table(s, 0.3, 1.85, [2.25, 1.1, 1.0, 5.05], [
    ["Módszercsalád", "Környezet", "Tanítás", "Fő eredmény és gyengeség"],
    ["Súlyosság", "nem", "nem", "a mai gyakorlat; durva, a környezettől független"],
    ["Többszempontú (AHP, fuzzy)", "igen", "nem", "minden incidens rangsorolható (CVSS-sel 17,23%); súlyok érzékenységvizsgálat nélkül"],
    ["Környezet és ellenőrzés", "igen", "nem", "szűr: hiányos nyilvántartásnál valódi támadást is eltávolít"],
    ["Tanuló, származáskövető", "részben", "igen", "86%-kal kevesebb téves riasztás; címke vagy gépi napló kell"],
    ["Kockázatalapú pontozás", "nem", "nem", "a legerősebb nyilvánosan mért, tanítás nélküli módszer"],
], size=10.5, row_h=0.48, highlight={5: AMBER_T}, name="Rangsorolás-táblázat")
card(s, 0.3, 4.95, 3.0, 1.5, "0,72 → 0,92", "rangsor-pontosság, 8 adathalmaz: súlyosság vs. "
     "kockázatalapú", NAVY, WHITE, big_size=22, small_size=11, name="Kártya RBA 1")
card(s, 3.5, 4.95, 3.0, 1.5, "43 / 44", "valódi riasztás a lista első 10%-ában (súlyosság szerint: "
     "28,6)", AMBER, NAVY, big_size=22, small_size=11, name="Kártya RBA 2")
box(s, 6.7, 4.95, 3.0, 1.5, SKY_T, name="Választás 2")
txt(s, 6.85, 5.02, 2.7, 1.38, [[("Választás: ", {"bold": True}),
                               ("a kockázatalapú pontozás az alap – de nem használja a környezetet.", {})]],
    size=12, anchor=MSO_ANCHOR.MIDDLE)

# ============ 5. Kutatási rés és a választás (kb. 75 mp) ============
s = content_slide(
    "A kutatási rés – és miért ez a megoldás",
    "[kb. 75 mp] Öt követelményt fogalmaztam meg: a rendszer tanítóadat nélkül működjön, mert valós "
    "SOC-ban alig van címkézett riasztás; legyen megismételhető, különben a mérések nem vethetők "
    "össze; használja a környezetet; ne szűrjön, mert hiányos nyilvántartásnál valódi támadás "
    "tűnhet el; és a sorrend indoka legyen követhető.\n\n"
    "A táblázat mutatja, hogy egyik módszercsalád sem teljesíti mind az ötöt. A kockázatalapú "
    "pontozás négyet teljesít, de nem használja a környezetet. A környezeti módszerek szűrnek. A "
    "nyelvimodell-agentek nem megismételhetők: ugyanarra a riasztásra két futás más választ adhat, "
    "és a magyarázatuk ellenőrizetlen. Ezért nem nyelvi modellre építettem a rangsorolást.\n\n"
    "A kutatási rés tehát: mennyit javít a környezeti információ egy már erős, nyilvánosan mért "
    "rangsoroláson, ha nem szűrünk vele, és megismételhetően mérjük? A választott megoldás a "
    "kockázati pontszámot egészíti ki a gép fontosságával, a támadás alkalmazhatóságával és a "
    "megfigyeltséggel, súlyozott összeggel, páros összehasonlításból kapott súlyokkal.",
)
dia_szam(s)
table(s, 0.3, 1.85, [2.6, 1.25, 1.35, 1.2, 1.1, 1.9], [
    ["Módszercsalád", "Tanítás nélkül", "Megismételhető", "Környezet", "Nem szűr", "Követhető indok"],
    ["Súlyosság szerint", "igen", "igen", "nem", "igen", "igen"],
    ["Többszempontú (AHP, fuzzy)", "igen", "igen", "igen", "igen", "régi adaton mérve"],
    ["Környezet és ellenőrzés", "igen", "igen", "igen", "nem", "igen"],
    ["Kockázatalapú pontozás", "igen", "igen", "nem", "igen", "igen"],
    ["Tanuló, származáskövető", "nem", "részben", "részben", "igen", "nehezen"],
    ["Nyelvimodell-agentek", "igen", "nem", "részben", "igen", "ellenőrizetlen szöveg"],
    ["Választott megoldás", "igen", "igen", "igen", "igen", "igen"],
], size=10.5, row_h=0.4, highlight={7: AMBER_T}, name="Követelmény-táblázat")
box(s, 0.3, 5.2, 9.4, 1.25, NAVY, name="Kérdés doboz")
txt(s, 0.5, 5.26, 9.0, 1.15, [
    [("Kutatási kérdés: ", {"bold": True, "color": AMBER}),
     (("mennyit javít a környezeti információ egy már erős, nyilvánosan mért rangsoroláson – szűrés "
      "nélkül, megismételhető méréssel?"), {"color": WHITE})],
    [("Megoldás: ", {"bold": True, "color": AMBER}),
     (("kockázati pontszám + gép fontossága + alkalmazhatóság + megfigyeltség, súlyozott összeggel "
      "(páros összehasonlítás)."), {"color": WHITE})],
], size=13, anchor=MSO_ANCHOR.MIDDLE)

# ============ 6. Architektúra és döntések (kb. 75 mp) ============
s = content_slide(
    "Tervezett architektúra: hét együttműködő agent",
    "[kb. 75 mp] A rendszer hét agentből áll. Az egységesítő közös formára hozza a két érzékelő "
    "riasztásait, a csoportosító összefogja az összetartozókat, a környezeti és a sérülékenységi "
    "agent a gépnyilvántartásból dolgozik, a rangsoroló a mérés előtt rögzített súlyokkal számol. "
    "Ez az öt agent kiszámítható program: a pontszám és a sorrend csak tőlük származik.\n\n"
    "Miért nem nyelvi modellre építettem? A szakirodalomban a CORTEX nyelvimodell-agentjei "
    "3,4-szer lassabbak voltak és 5,7-szer több szöveget dolgoztak fel, az AgentSOC futásidejének "
    "95%-át a modell tette ki; a kimenetük nem megismételhető, és hihető, de hamis állításokat is "
    "tehetnek. A kis, helyi modellek pedig önállóan nem tudnak végigvinni egy vizsgálatot. Ezért "
    "a nyelvi modell nálam csak magyarázatot ír, ellenőrzéssel, és helyben fut, hogy a naplóadat "
    "ne hagyja el a szervezetet. A lépések sorrendjét rögzített vezérlés adja, nem a modellek "
    "beszélgetése.",
)
dia_szam(s)
s.shapes.add_picture(ARCH, Inches(0.3), Inches(1.75), height=Inches(4.8))
x0 = 4.85
decisions = [
    ("Pontszám: kiszámítható program", "ugyanarra a bemenetre mindig ugyanaz a sorrend – csak így mérhető", SKY_T),
    ("Nyelvi modell: csak magyaráz", ("CORTEX: 3,4× lassabb, 5,7× több szöveg; AgentSOC: a futásidő 95%-a; "
     "nem megismételhető, hamis állítást is tehet"), AMBER_T),
    ("Helyi modell (Ollama)", "a naplóadat nem hagyja el a szervezetet; díjmentes; rögzíthető változat", SKY_T),
    ("Rögzített vezérlés (LangGraph)", "a sorrendet nem a modellek beszélgetése alakítja (mint az AutoGenben)", SKY_T),
]
y = 1.8
for h, d, fill in decisions:
    hh = 1.25 if fill == AMBER_T else 1.05
    box(s, x0, y, 4.85, hh, fill, name="Döntés")
    txt(s, x0 + 0.15, y + 0.07, 4.55, hh - 0.12, [[(h, {"bold": True, "size": 13})], d], size=11)
    y += hh + 0.12

# ============ 7. Várt eredmények (kb. 65 mp) ============
s = content_slide(
    "Mérési terv és várt eredmények",
    "[kb. 65 mp] A hatást lépésenként mérem: a súlyosság szerinti sorrendből indulok, jön a "
    "csoportosítás, a kockázatalapú pontozás mint összehasonlítási alap, majd egyenként a gép "
    "fontossága, az alkalmazhatóság és a megfigyeltség. Így minden lépés az új információ "
    "hozzájárulását mutatja. A nyilvános AIT-ADS nyolc forgatókönyvén és egy saját laborban mérek, "
    "páros Wilcoxon-próbával.\n\n"
    "A várakozás: a közölt eredmények szerint az alap már 0,98–0,99 rangsor-pontosságú, ezért "
    "plafonhatás várható; a javulás a lista elején és az átnézendő riasztások arányában "
    "látszhat. A CVE-szintű alkalmazhatóságot és a megfigyeltséget csak a laborban lehet mérni. "
    "A torzítás ellen a súlyokat a mérés előtt rögzítem, és ellenpróbát végzek összekevert "
    "gépfontossággal. Köszönöm a figyelmet!",
)
dia_szam(s)
steps = [("1", "súlyosság"), ("2", "csoportosítás"), ("3", "kockázati pontszám"),
         ("4", "+ gép fontossága"), ("5", "+ alkalmazhatóság"), ("6", "+ megfigyeltség")]
w = 1.5
for k, (n, d) in enumerate(steps):
    x = 0.3 + k * (w + 0.08)
    fill = AMBER if k == 2 else (SKY if k >= 3 else GREY_T)
    box(s, x, 1.85, w, 1.0, fill, name=f"Lépés {n}")
    txt(s, x + 0.1, 1.9, w - 0.2, 0.9, [[(n + ". lépés", {"bold": True, "size": 12})], d],
        size=12, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0.3, 2.92, 9.4, 0.3, "szürke: kiindulás · sárga: összehasonlítási alap (visszamérve) · kék: a "
    "környezeti mérőszámok egyenként", size=10, color=MUTED)
cards = [("Hol mérek?", "AIT-ADS, 8 forgatókönyv (nyilvános) + saját labor (teljes környezet, CVE-szint)"),
         ("Mivel?", "rangsor-pontosság, átlagos pontosság, első 10%, a 98%-hoz átnézendő listarész; Wilcoxon-próba"),
         ("Torzítás ellen", "előzetesen rögzített súlyok, ±20%, tanult súlyok, ellenpróba összekevert fontossággal")]
for k, (h, d) in enumerate(cards):
    x = 0.3 + k * 3.25
    box(s, x, 3.35, 2.9, 1.55, SKY_T, name=f"Módszer {k+1}")
    txt(s, x + 0.15, 3.43, 2.6, 1.4, [[(h, {"bold": True, "size": 13})], d], size=11)
box(s, 0.3, 5.1, 9.4, 1.35, NAVY, name="Várakozás doboz")
txt(s, 0.5, 5.16, 9.0, 1.25, [
    [("Várakozás: ", {"bold": True, "color": AMBER}),
     (("az alap már 0,98–0,99 (plafonhatás) – a környezet hatása a lista elején és az átnézendő "
      "riasztások arányában látszhat; a CVE-szintű hatás és a megfigyeltség a laborban."),
      {"color": WHITE})],
], size=13, anchor=MSO_ANCHOR.MIDDLE)

# ============ 8. Záródia (kb. 5 mp) ============
z = prs.slides.add_slide(next(lay for lay in prs.slide_masters[0].slide_layouts
                              if lay.name == "1 Záródia"))
z.background.fill.solid()  # sötét záródia a sablon sötétkékjével
z.background.fill.fore_color.rgb = NAVY
for ph in z.placeholders:
    if ph.placeholder_format.idx == 0:
        ph.text_frame.text = "KÖSZÖNÖM A FIGYELMET!"
        for r in ph.text_frame.paragraphs[0].runs:
            r.font.color.rgb = WHITE
            r.font.bold = True
            r.font.size = Pt(40)
box(z, 3.5, 4.55, 3.0, 0.06, AMBER, name="Kiemelő vonal")
txt(z, 0.8, 4.85, 8.4, 0.9, ["Nagy József", ("Agent-alapú, metrika-vezérelt IDS-riasztásaggregáció "
    "SOC-környezetben")], size=16, color=WHITE, align=PP_ALIGN.CENTER, name="Elköszönés")
z.notes_slide.notes_text_frame.text = "[kb. 5 mp] Köszönöm a figyelmet! Szívesen válaszolok a kérdésekre."

prs.save(OUT)
print("ok", len(prs.slides))
