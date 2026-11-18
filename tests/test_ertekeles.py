import numpy as np
import pytest

from alertagg import ertekeles


def test_perfect_and_inverted_ranking():
    y = [1, 1, 0, 0, 0]
    assert ertekeles.auroc(y, [5, 4, 3, 2, 1]) == 1.0
    assert ertekeles.auroc(y, [1, 2, 3, 4, 5]) == 0.0
    assert ertekeles.average_precision(y, [5, 4, 3, 2, 1]) == 1.0


def test_top_fraction_counts_ties_proportionally():
    # 10 riasztás, első 10% = 1 hely; két azonos pontszámú közül az egyik valódi -> 0,5 várható találat
    y = [1, 0] + [0] * 8
    s = [9, 9] + list(range(8))
    assert ertekeles.true_in_top_fraction(y, s, 0.10) == pytest.approx(0.5)
    assert ertekeles.recall_at_fraction(y, s, 0.10) == pytest.approx(0.5)


def test_workload_at_recall():
    y = np.array([1, 0, 1, 0, 0, 0, 0, 0, 0, 1])
    s = np.arange(10, 0, -1)  # az eredeti sorrend a rangsor
    # mindhárom valódi csak a 10. helyig van meg
    assert ertekeles.workload_at_recall(y, s, 0.98) == 1.0
    # kettő a harmadik helyig
    assert ertekeles.workload_at_recall(y, s, 0.6) == pytest.approx(0.3)


def test_workload_is_pessimistic_on_ties():
    y = [1, 0, 0, 0]
    assert ertekeles.workload_at_recall(y, [1, 1, 1, 1], 1.0) == 1.0


def test_fazis_tisztasag_es_wilcoxon_holm():
    import numpy as np

    from alertagg.ertekeles import csoport_tisztasag_fazis, holm, paros_wilcoxon

    # két csoport: az elsőben 2 scan + 1 normál, a másodikban 2 webshell
    assert csoport_tisztasag_fazis(["scan", "scan", "normál", "webshell", "webshell"],
                                   [1, 1, 1, 2, 2]) == 4 / 5
    uj = np.array([0.9, 0.8, 0.7, 0.95, 0.6, 0.85, 0.9, 0.75])
    regi = uj - np.array([0.1, 0.05, 0.02, 0.2, 0.01, 0.03, 0.04, 0.06])
    r = paros_wilcoxon(uj, regi)
    assert r["javult"] == 8 and r["rang_biszerialis"] == 1.0
    assert abs(r["p"] - 1 / 2**8) < 1e-12  # a legkisebb elérhető p-érték 8 párnál (6.3)
    # kisebb = jobb irány (terhelés)
    assert paros_wilcoxon(regi, uj, nagyobb_jobb=False)["javult"] == 8
    # nulla különbség
    assert paros_wilcoxon(uj, uj)["p"] == 1.0
    assert list(holm([0.01, 0.04, 0.03])) == [0.03, 0.06, 0.06]
