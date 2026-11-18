# Írási csomag (DM III.) – 8. fejezet: Eredmények az AIT-ADS-en (ablációs vizsgálat)

2026-11-18 · **VÁZ.** A fejezet végleges szövege csak mind a 8 forgatókönyv mérése után írható meg
(6.3: Wilcoxon-próba a 8 forgatókönyvön, tanult súlyok egy-kihagyással). Most a szerkezetet és a már
véglegesnek tekinthető részeket rögzítjük. D20 szerint a kódblokkok átvehetők.

- **Útmutató:** 9. pont – eredmények és összevetés. **Feladatlap:** F6. **Terjedelem:** kb. 8–10 oldal.
- **Fájl:** `chapters/8_Eredmenyek_AIT.tex`.

## A fejezet tervezett szerkezete

| Alfejezet | Tartalom | Adat | Állapot |
| --- | --- | --- | --- |
| 8.1 Az összehasonlítási alap | A visszamérés röviden (a részletek a 7.3-ban) | `results/01_…` | kész |
| 8.2 A csoportosítás (2. lépés) | tételszám-csökkenés, tisztaság, csoportszintű terhelés | `results/05_…` + 8 forgatókönyv | russellmitchell kész (mintán belüli) |
| 8.3 A gép fontossága (4. lépés) | rangsor- és terhelésmérőszámok, ellenpróba, érzékenység | `results/04_…` + 8 forgatókönyv | russellmitchell kész |
| 8.4 Az alkalmazhatóság (5. lépés) | ugyanígy | `results/06_…` + 8 forgatókönyv | russellmitchell kész |
| 8.5 Statisztikai összevetés | páros Wilcoxon-próba a 8 forgatókönyvön, hatásnagyság | – | a 8 forgatókönyv után |
| 8.6 Szakértői és tanult súlyok | egy-kihagyásos tanult súlyok vs. AHP | – | a 8 forgatókönyv után |
| 8.7 Összegzés | | | a végén |

## Szabály a fejezet megírásához

- **Minden eredményt a rögzített beállításokkal kell közölni**, akkor is, ha romlást mutat (a
  russellmitchell Wazuh-riasztásainál a 4. lépés ront). A magyarázatot nem a beállítás utólagos
  módosítása adja, hanem az értelmezés (10. fejezet).
- A russellmitchell a csoportosítás hangoló forgatókönyve: a 2. lépés eredményét ott mintán belülinek kell jelölni.
- A számok forrása mindig a `results/` mappa egy fájlja; a táblázat feliratában jelöld.

---

## 8.0 Nyitó bekezdés (átvehető, a végleges változatban is érvényes)

```latex
Ez a fejezet a nyilvános AIT-ADS adathalmazon végzett mérések eredményeit mutatja be.
A mérések a 6. fejezetben leírt lépésenkénti bővítést követik: a súlyosság szerinti sorrendből
kiindulva előbb a csoportosítás, majd a kockázatalapú pontozás, végül egyenként a környezeti
mérőszámok hatását vizsgálom.
Minden eredmény az előzetesen rögzített beállításokkal készült (\ref{sec:rogzites}.~alfejezet), és
a hálózati, illetve a gépi riasztásokat külön adathalmazként kezeli.
```

## 8.1 Az összehasonlítási alap (átvehető)

```latex
\subsection{Az összehasonlítási alap}

A kockázatalapú pontozás visszamérése (\ref{sec:visszameres}.~alfejezet) a közölt eredményeket
legfeljebb 0,01-es eltéréssel adta vissza, így a 3. lépés hiteles összehasonlítási alap.
A további lépések javulását vagy romlását ehhez az alaphoz mérem.
```

## 8.2–8.7

Még nem írható meg végleges formában. A russellmitchell eddigi számai a `results/04_…` és a
`results/05_…` fájlokban vannak; ezek a 8 forgatókönyv táblázatának egy sorát adják majd.
