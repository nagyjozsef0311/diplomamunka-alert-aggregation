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
