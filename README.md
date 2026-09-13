# Koliko rešitev ima sudoku?

Ta repozitorij vsebuje programsko kodo, uporabljeno pri raziskovalni nalogi **Koliko rešitev ima sudoku?**.

Program je napisan v Pythonu in temelji na algoritmu **povratnega iskanja (backtracking)**. Omogoča preverjanje začetnega stanja, iskanje ene ali vseh rešitev, primerjavo različnih strategij preiskovanja in uporabo grafičnega uporabniškega vmesnika.

## Vsebina repozitorija

- `solver.py` – jedro programa: preverjanje sudokuja, backtracking in iskanje vseh rešitev.
- `strategies.py` – tri strategije izbire praznega polja:
  - po vrsticah,
  - po stolpcih,
  - MRV (*minimum remaining values* – polje z najmanj možnostmi).
- `gui.py` – grafični uporabniški vmesnik v knjižnici Tkinter.
- `benchmark.py` – primerjava hitrosti in števila korakov različnih strategij.
- `research.py` – preverjanje vzorca sudokujev in štirih orientacij posamezne uganke.
- `tests/test_sudokuji.py` – testni primeri sudokuja z eno, nič in več rešitvami.
- `data/sudokuji_template.csv` – prazna predloga za dejanske raziskovalne podatke.

## Zagon

Potreben je Python 3.10 ali novejši. Dodatne knjižnice niso potrebne.

Grafični vmesnik:

```bash
python gui.py
```

Primerjava strategij:

```bash
python benchmark.py
```

Testi:

```bash
python -m unittest discover -s tests
```

Raziskava na CSV-datoteki:

```bash
python research.py data/sudokuji.csv -o results.csv
```

Vhodni CSV mora imeti stolpce:

```text
id,difficulty,grid
```

Polje `grid` vsebuje 81 znakov. Število `0` ali pika `.` pomeni prazno polje.

## Grafični vmesnik

Vmesnik omogoča:

- ročni vnos sudokuja,
- preverjanje pravilnosti začetnega stanja,
- reševanje sudokuja,
- prikaz vseh najdenih rešitev,
- pomikanje med več rešitvami s puščicama,
- prikaz začetnih števil **rdeče** in izračunanih števil **črno**,
- izbiro strategije reševanja.

## Raziskovalni del

Pri raziskavi se lahko vsak sudoku preveri v štirih različicah:

1. original,
2. vodoravno zrcaljenje,
3. navpično zrcaljenje,
4. obrat za 180°.

Program pri vsakem preverjanju zabeleži število rešitev, število poskusov, rekurzivne klice, povratke in čas izvajanja.

## Avtor

**Anže Plahutnik**  
I. osnovna šola Celje  
Raziskovalna naloga, šolsko leto 2026/27
