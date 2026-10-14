"""Kutatási eredmények – 7 diás deck a NIK-prezentációsablonból (python-pptx).

Használat: python scripts/build_kutatasi_deck.py NIK_prezentacio_sablon_2025.pptx kimenet.pptx
"""
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.opc.packuri import PackURI

SRC, OUT = sys.argv[1], sys.argv[2]
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

# --- csak a 2. sablondiát (fehér, kék sávos címdia) tartjuk meg ---
sldIdLst = prs.slides._sldIdLst
ids = list(sldIdLst)
for idx in (2, 0):
    rid = ids[idx].rId
    prs.part.drop_rel(rid)
    sldIdLst.remove(ids[idx])

prs.slides[0].part.partname = PackURI("/ppt/slides/slide1.xml")

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
            p.space_after = Pt(4)
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


def table(slide, x, y, widths, rows, size=11, row_h=0.4, header_fill=NAVY,
          highlight_last=False, first_col_bold=True, name=None):
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
    for i, row in enumerate(rows):
        t.rows[i].height = Inches(row_h)
        last = highlight_last and i == nrows - 1
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.fill.solid()
            if i == 0:
                c.fill.fore_color.rgb = header_fill
            elif last:
                c.fill.fore_color.rgb = AMBER_T
            else:
                c.fill.fore_color.rgb = WHITE if i % 2 else GREY_T
            c.margin_left = c.margin_right = Inches(0.06)
            c.margin_top = c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.size = Pt(size)
            r.font.color.rgb = WHITE if i == 0 else TEXT
            r.font.bold = i == 0 or last or (first_col_bold and j == 0)
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


def source(slide, text, y=6.62):
    txt(slide, 0.3, y, 9.4, 0.28, text, size=9, color=MUTED, name="Forrás")


# ============ 1. Címdia ============
t = prs.slides[0]
vals = {
    0: "Agent-alapú, metrika-vezérelt IDS-riasztásaggregáció SOC-környezetben",
    13: "Kutatási eredmények – Diplomamunka II.",
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
    "Jó napot kívánok! Nagy József vagyok, a diplomamunkám témája a behatolásérzékelő rendszerek "
    "riasztásainak csoportosítása és rangsorolása egy biztonsági műveleti központban, együttműködő "
    "agentekkel. Ebben a rövid összefoglalóban a szakirodalmi kutatás eredményét mutatom be: milyen "
    "adathalmazokon lehet mérni, milyen módszerek léteznek és mi a gyengeségük, hogyan épül fel a "
    "tervezett rendszer, miben különbözik a meglévő megoldásoktól, és milyen eredményt várok a mérésektől."
)

# ============ 2. Probléma és rés ============
s = content_slide(
    "A probléma és a kutatási rés",
    "A biztonsági műveleti központok elemzőit elárasztják a riasztások, és ezek túlnyomó része nem "
    "valódi támadás. A nyilvános AIT-ADS adathalmaz egyik forgatókönyvében a Suricata 9186 riasztásából "
    "mindössze 44 tartozott a támadáshoz, ez fél százalék.\n\n"
    "A szakirodalom legerősebb, tanítóadatot nem igénylő módszere a kockázatalapú riasztás-pontozás. "
    "Uetz és szerzőtársai 2026-ban nyolc adathalmazon mérték: a rangsor-pontosság – annak valószínűsége, "
    "hogy egy valódi riasztás egy téves elé kerül – 0,72-ről 0,92-re nőtt a csak súlyosság szerinti "
    "sorrendhez képest.\n\n"
    "Ez a módszer viszont csak a riasztások folyamából dolgozik: nem tudja, mennyire fontos a gép, fut-e "
    "rajta sérülékeny szoftver, és mennyire látjuk. Az iparban a Splunk használ ilyen adatot, de nincs "
    "nyilvános mérés arról, mennyit ad hozzá. Ráadásul egy friss áttekintés szerint 87 tanulmányból csak 9 "
    "alapult éles SOC-adaton. Ez a dolgozat rése: megmérni, mennyit javít a környezeti információ egy már "
    "erős módszeren.",
)
cards = [
    ("0,5%", "a Suricata-riasztások közül ennyi jelzett valódi támadást (44 / 9186, AIT-ADS)", NAVY, WHITE),
    ("0,72 → 0,92", "rangsor-pontosság (AUROC): csak súlyosság vs. kockázatalapú pontozás", AMBER, NAVY),
    ("9 / 87", "tanulmány alapult éles SOC-adaton a riasztási fáradtság irodalmában", SKY, NAVY),
]
cw, gap, x0, y0 = 2.95, 0.3, 0.3, 1.95
for k, (big, small, fill, fg) in enumerate(cards):
    x = x0 + k * (cw + gap)
    box(s, x, y0, cw, 2.05, fill, name=f"Kártya {k+1}")
    txt(s, x + 0.2, y0 + 0.2, cw - 0.4, 0.75, big, size=32, bold=True, color=fg,
        anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + 0.2, y0 + 1.0, cw - 0.4, 0.95, small, size=13, color=fg)
box(s, 0.3, 4.35, 9.4, 2.1, SKY_T, name="Rés doboz")
txt(s, 0.55, 4.5, 8.9, 1.85, [
    [("Kutatási rés", {"bold": True, "size": 18})],
    "A legerősebb nyilvános, tanítás nélküli módszer, a kockázatalapú pontozás nem használja a "
    "környezetet: a gép fontosságát, a sérülékenységeket és a megfigyeltséget.",
    [("Kérdés: ", {"bold": True}), ("mennyit javít a környezeti információ egy már erős rangsoroláson? "
                                    "Erre ma nincs nyilvános, megismételhető mérés.", {})],
], size=14)
source(s, "Forrás: Uetz és mtsai. 2026 (arXiv:2609.02465); Ndichu és mtsai. 2026; Landauer és mtsai. 2024 (AIT-ADS)")

# ============ 3. Adathalmazok ============
s = content_slide(
    "Adathalmazok: mire lehet mérni?",
    "Riasztás-rangsorolást csak olyan adaton lehet mérni, ahol riasztások vannak, és tudjuk, melyik "
    "tartozik támadáshoz. A klasszikus adathalmazok, mint a DARPA 2000 vagy a CIC-IDS2017, nyers forgalmat "
    "vagy folyamstatisztikát tartalmaznak, osztályozásra készültek, és nincs bennük környezeti információ.\n\n"
    "Az AIT-ADS ezzel szemben kész Suricata- és Wazuh-riasztásokat ad, nyolc eltérő hálózati "
    "környezetben lejátszott, több lépésből álló támadással, címkével. A legfontosabb: ugyanezen mérték a "
    "kockázatalapú pontozást, így az eredményeim közvetlenül összevethetők. Hátránya, hogy nincs benne "
    "sérülékenység-azonosító, ezért itt csak szolgáltatás szintjén tudom vizsgálni, működhet-e a támadás.\n\n"
    "A CATS-változattal ellenőrzöm, hogy ugyanazokat a riasztásokat dolgozom-e fel. A CVE-szintű "
    "illesztést a saját laborban mérem: VMware-gépek Wazuh-agentekkel, Suricata, és Dockerben egy "
    "sérülékeny WordPress, ahol a gépnyilvántartást én töltöm fel.",
)
table(s, 0.3, 1.9, [1.55, 2.45, 1.35, 1.65, 2.4], [
    ["Adathalmaz", "Tartalom", "Címkézett riasztás", "Környezeti adat", "Szerepe"],
    ["DARPA 2000", "Régi hálózati forgalom, egy támadás", "nem (forgalom)", "nincs", "Elavult; a riasztást elő kellene állítani"],
    ["CIC-IDS2017", "Forgalom és folyamstatisztika", "nem (folyam)", "nincs", "Osztályozásra készült, nem riasztásokra"],
    ["AIT-LDSv2", "Gépi és hálózati naplók, 8 környezet", "nem (napló)", "hálózatleírás", "Az AIT-ADS forrása"],
    ["AIT-ADS", "Suricata- és Wazuh-riasztások, 8 forgatókönyv", "igen", "gépnév, szolgáltatás (CVE nincs)", "Fő mérés; a kockázatalapú pontozással összevethető"],
    ["CATS-változat", "AIT-ADS 1 forgatókönyv, jellemzőkkel", "igen", "–", "Ellenőrzés: ugyanazok a riasztások?"],
    ["Saját labor", "VMware + Docker; WordPress 5.8.2 + wpDiscuz (CVE-2020-24186)", "saját címkézés", "teljes: gépnyilvántartás, CVE", "CVE-szintű mérés valósághűbb környezetben"],
], size=11, row_h=0.62, highlight_last=False, name="Adathalmaz-táblázat")
source(s, "Forrás: Landauer és mtsai. 2024 (AIT-ADS, Zenodo 8263181); Uetz és mtsai. 2026 (CATS); saját összeállítás", y=6.6)

# ============ 4. Módszerek ============
s = content_slide(
    "A meglévő módszerek és gyengeségeik",
    "A szakirodalmat hat módszercsaládba soroltam. A súlyosság szerinti sorrend egyszerű, de a "
    "környezettől független. A többszempontú módszerek, például a páros összehasonlítás vagy a fuzzy "
    "logika, használnak környezetet, de a súlyokat ritkán vizsgálják, és régi adatokon mértek.\n\n"
    "A környezetre és a sérülékenységre épülő ellenőrzés szűr: ha hiányos a nyilvántartás, valódi támadást "
    "is eltávolíthat. A kockázatalapú pontozás a legerősebb tanítás nélküli módszer, de nem használ "
    "környezetet. A tanuló és a származáskövető módszerek, mint a NoDoze vagy az AlertPro, pontosak, de "
    "címkét vagy részletes gépi naplót igényelnek.\n\n"
    "A nyelvi modellekre épülő agentrendszerek jól magyaráznak, de lassúak: a CORTEX például nagyjából "
    "5,7-szer több szöveget dolgoz fel, és 3,4-szer lassabb, mint egyetlen modell. A kimenetük ráadásul "
    "nem megismételhető. Az utolsó sor mutatja, hogy a saját megoldásom mindhárom szempontot teljesíti.",
)
table(s, 0.3, 1.9, [2.0, 1.05, 1.1, 1.4, 3.85], [
    ["Módszercsalád", "Környezet", "Tanítás nélkül", "Megismételhető", "Fő gyengeség"],
    ["Súlyosság szerint", "nem", "igen", "igen", "Durva fokozatok, a géptől független"],
    ["Többszempontú (páros összehasonlítás, fuzzy)", "igen", "igen", "igen", "Szakértői súlyok vizsgálat nélkül; régi adathalmazokon mérve"],
    ["Környezet és ellenőrzés", "igen", "igen", "igen", "Szűr: hiányos nyilvántartásnál valódi támadást is eltávolít"],
    ["Kockázatalapú pontozás", "nem", "igen", "igen", "Csak a riasztások folyamából dolgozik"],
    ["Tanuló, származáskövető", "részben", "nem", "részben", "Címkét vagy részletes gépi naplót igényel; nehezen magyarázható"],
    ["Nyelvimodell-agentek", "részben", "igen", "nem", "Lassú, költséges; kiértékelés saját adaton"],
    ["Saját megoldás", "igen, súlyként", "igen", "igen", "Környezet súlyként, nyilvános mérés, a nyelvi modell csak magyaráz"],
], size=11, row_h=0.52, highlight_last=True, name="Módszer-táblázat")
source(s, "Forrás: Anuar és mtsai. 2013; Alsubhi és mtsai. 2011; Kruegel és mtsai. 2004; Njogu és mtsai. 2013; "
          "Uetz és mtsai. 2026; Hassan és mtsai. 2019; Wang és mtsai. 2024; Wei és mtsai. 2025", y=6.55)

# ============ 5. Agentek ============
s = content_slide(
    "A tervezett rendszer: hét agent",
    "A rendszer hét agentből áll, mindegyik egy önálló, tesztelhető Python-modul, meghatározott bemenettel "
    "és kimenettel. Az egységesítő közös formára hozza a Suricata- és a Wazuh-riasztásokat. A csoportosító "
    "összefogja az összetartozókat: közös IP-cím vagy felhasználó, időbeli közelség. A környezeti agent "
    "kikeresi a gép fontosságát, zónáját és megfigyeltségét, a sérülékenységi agent pedig azt, hogy "
    "működhet-e a támadás azon a gépen.\n\n"
    "A rangsoroló súlyozott összeget számol; a súlyokat páros összehasonlítással, a mérés előtt rögzítem. "
    "Kék színnel jelöltem a kiszámítható programrészeket: ezek adják a pontszámot. Egyetlen agent használ "
    "nyelvi modellt, a magyarázó: helyben futó modellel rövid összefoglalót ír, amelyet egy ellenőrző lépés "
    "átnéz. A nyelvi modell soha nem dönt a sorrendről és nem ad pontszámot.\n\n"
    "A megvalósítás három rétegű: először a sima Python-mag, amin az AIT-mérések futnak, utána a LangGraph "
    "vezérlés, végül opcionálisan egy csak olvasható MCP-csatlakozó a gépnyilvántartáshoz.",
)
table(s, 0.3, 1.85, [0.4, 1.7, 4.2, 3.1], [
    ["#", "Agent", "Bemenet → kimenet", "Megvalósítás"],
    ["1", "Egységesítő", "Suricata- és Wazuh-riasztás → közös riasztásforma", "Python, determinisztikus"],
    ["2", "Csoportosító", "riasztások → csoportok (közös IP / felhasználó, időablak)", "Python, determinisztikus"],
    ["3", "Környezet", "gépnév, IP → fontosság, zóna, megfigyeltség", "relációs gépnyilvántartás (SQLite)"],
    ["4", "Sérülékenységi", "szabály + gép → működhet-e a támadás", "szoftverazonosító (CPE) illesztése"],
    ["5", "Rangsoroló", "mérőszámok → pontszám és sorrend", "súlyozott összeg, páros összehasonlítás"],
    ["6", "Magyarázó", "csoport → rövid szöveges összefoglaló", "helyi nyelvi modell (Ollama) + ellenőrzés"],
    ["7", "Vezérlő", "sorrend, naplózás, időmérés – végig", "Python, később LangGraph"],
], size=11, row_h=0.44, name="Agent-táblázat")
# kiemeljük a magyarázó sort borostyánnal
tbl = s.shapes[-1].table
for j in range(4):
    tbl.cell(6, j).fill.solid()
    tbl.cell(6, j).fill.fore_color.rgb = AMBER_T
# rétegek
layers = [("1. Mag", "sima Python-modulok; az AIT-mérések ezen futnak", NAVY, WHITE),
          ("2. Vezérlés", "LangGraph-gráf; ugyanazt kell adnia, mint a mag", SKY, NAVY),
          ("3. Csatlakozó", "MCP, csak olvasható gépnyilvántartás (opcionális)", SKY_T, NAVY)]
lw, lg = 2.95, 0.3
for k, (h, d, fill, fg) in enumerate(layers):
    x = 0.3 + k * (lw + lg)
    box(s, x, 5.55, lw, 0.95, fill, name=f"Réteg {k+1}")
    txt(s, x + 0.15, 5.62, lw - 0.3, 0.82, [[(h, {"bold": True, "size": 14})], d], size=12, color=fg)
    if k < 2:
        a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + lw + 0.04), Inches(5.9),
                               Inches(0.22), Inches(0.25))
        a.fill.solid()
        a.fill.fore_color.rgb = AMBER
        a.line.fill.background()
txt(s, 0.3, 6.6, 9.4, 0.28, "Borostyán sor: az egyetlen nyelvi modellt használó lépés – nem dönt a sorrendről, nem ad pontszámot.",
    size=10, color=MUTED, name="Megjegyzés")

# ============ 6. Mitől más ============
s = content_slide(
    "Mitől más ez a megoldás?",
    "Hat ponton térek el a kutatások többségétől. Először: a környezetet nem szűrésre használom, hanem "
    "súlyként, így egy hiányos nyilvántartás miatt nem tűnik el riasztás, legfeljebb hátrébb kerül.\n\n"
    "Másodszor: nem a gyenge, csak súlyosság szerinti sorrenddel hasonlítok össze, hanem a legerősebb "
    "nyilvános módszerrel, a kockázatalapú pontozással, és lépésenként mérem, mit ad hozzá a gép fontossága, "
    "a sérülékenység és a megfigyeltség.\n\n"
    "Harmadszor: nyilvános, címkézett adathalmazon mérek, ezért az eredmény megismételhető és összevethető. "
    "Negyedszer: nem kell tanítóadat, a tanult súlyokat csak összehasonlításként használom, egy forgatókönyv "
    "kihagyásával. Ötödször: a nyelvi modell csak magyaráz, helyben fut, tehát a naplók nem hagyják el a "
    "szervezetet. Végül a súlyokat a mérés előtt rögzítem, és plusz-mínusz húsz százalékos "
    "érzékenységvizsgálattal ellenőrzöm.",
)
table(s, 0.3, 1.9, [1.75, 3.6, 4.05], [
    ["Szempont", "A kutatások többsége", "Saját megoldás"],
    ["Környezet", "nem használja, vagy szűr vele", "súlyként módosítja a sorrendet, riasztást nem töröl"],
    ["Összehasonlítás", "gyenge alap (csak súlyosság)", "a legerősebb nyilvános módszer, lépésenként bővítve"],
    ["Mérés", "saját, nem nyilvános vagy mesterséges adat", "nyilvános AIT-ADS + saját labor"],
    ["Tanítóadat", "címkét vagy elemzői visszajelzést igényel", "nem kell; tanult súlyok csak összevetésre"],
    ["Nyelvi modell", "dönt és sorrendet ad; lassú, nem megismételhető", "csak magyaráz, helyben fut, ellenőrzött"],
    ["Súlyok", "szakértői, érzékenységvizsgálat nélkül", "páros összehasonlítás, mérés előtt rögzítve, ±20% vizsgálat"],
], size=12, row_h=0.66, name="Különbség-táblázat")
tbl = s.shapes[-1].table
for i in range(1, 7):
    c = tbl.cell(i, 2)
    c.fill.solid()
    c.fill.fore_color.rgb = AMBER_T
    for r in c.text_frame.paragraphs[0].runs:
        r.font.bold = True
source(s, "Forrás: saját összeállítás a 3. fejezet szakirodalmi áttekintése alapján", y=6.62)

# ============ 7. Várt eredmények ============
s = content_slide(
    "Milyen eredményt várok?",
    "Az értékelés lépésenként bővül. A 0. lépés a nyers riasztáslista, az 1. a súlyosság szerinti sorrend, "
    "a 2. a csoportosítás. A 3. lépésben újra előállítom a kockázatalapú pontozást; ha jól dolgozom, a "
    "rangsor-pontosságnak a közölt 0,92 körül kell lennie. Ez a hiteles kiindulópont.\n\n"
    "Ezután egyenként adom hozzá a gép fontosságát, a sérülékenységet és a megfigyeltséget. Azt várom, hogy "
    "a javulás főleg a lista elején jelentkezik: a fontos gépeket érintő valódi támadások előrébb kerülnek. "
    "Az AIT-ADS-en a sérülékenység hatása várhatóan kisebb, mert ott csak szolgáltatás szintjén illeszthető, "
    "a laborban viszont CVE szintjén is, ezért ott nagyobb hatást várok.\n\n"
    "Sikeresnek akkor tekintem, ha legfeljebb két százalék valódi támadás csúszik hátra, miközben az elemző "
    "elé kerülő tételek száma csökken, és a különbség a nyolc forgatókönyvön Wilcoxon-próbával is "
    "kimutatható. Ezek most még várakozások; a mérési eredményeket a következő félévben mutatom be.",
)
table(s, 0.3, 1.85, [0.7, 2.45, 2.95, 3.3], [
    ["Lépés", "Mit rangsorolunk", "Mit adunk hozzá", "Várakozás"],
    ["0", "nyers riasztások", "–", "kiindulópont"],
    ["1", "súlyosság szerint", "szabály szintje", "≈ 0,72 rangsor-pontosság (közölt)"],
    ["2", "csoportosítás után", "összetartozók összevonása", "kevesebb tétel az elemző előtt"],
    ["3", "kockázatalapú pontozás", "5 részpontszám", "≈ 0,92 visszamérve – az erős alap"],
    ["4", "+ gép fontossága", "kritikus gépek előre", "javulás a lista első 10%-ában"],
    ["5", "+ sérülékenység", "működhet-e a támadás", "AIT-en kisebb, laborban nagyobb hatás"],
    ["6", "+ megfigyeltség", "vakfoltok figyelembevétele", "kisebb, de mérhető hatás"],
], size=11, row_h=0.4, name="Lépés-táblázat")
tbl = s.shapes[-1].table
for i in range(4, 8):
    for j in range(4):
        tbl.cell(i, j).fill.solid()
        tbl.cell(i, j).fill.fore_color.rgb = SKY_T if i == 4 else AMBER_T
cards = [
    ("AIT-ADS (8 forgatókönyv)", "sérülékenység szolgáltatás szintjén; közvetlenül összevethető a közölt eredménnyel", SKY_T),
    ("Saját labor", "teljes gépnyilvántartás, CVE-szintű illesztés; a nyelvi modell futásideje is mérve", SKY_T),
    ("Siker feltétele", "≤ 2% átcsúszó valódi támadás mellett kevesebb tétel; Wilcoxon-próba 8 forgatókönyvön", AMBER_T),
]
cw = 2.95
for k, (h, d, fill) in enumerate(cards):
    x = 0.3 + k * (cw + 0.3)
    box(s, x, 5.3, cw, 1.3, fill, name=f"Várakozás-kártya {k+1}")
    txt(s, x + 0.15, 5.38, cw - 0.3, 1.15, [[(h, {"bold": True, "size": 13})], d], size=11)
source(s, "A 0,72 és a 0,92 közölt érték: Uetz és mtsai. 2026. A 4–6. lépés várakozása hipotézis, mérés még nincs.", y=6.68)

prs.save(OUT)
print("ok", len(prs.slides))
