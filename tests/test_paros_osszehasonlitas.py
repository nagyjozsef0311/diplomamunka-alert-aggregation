import numpy as np
import pytest

from alertagg import paros_osszehasonlitas as ahp


def test_consistent_matrix_gives_exact_weights():
    # w = (4, 2, 1)/7 -> tökéletesen következetes mátrix, CR = 0
    sz = ["a", "b", "c"]
    m = ahp.matrix_itiletekbol(sz, {("a", "b"): 2, ("a", "c"): 4, ("b", "c"): 2})
    e = ahp.sulyok(sz, m)
    assert e.sulyok["a"] == pytest.approx(4 / 7)
    assert e.sulyok["c"] == pytest.approx(1 / 7)
    assert e.cr == pytest.approx(0, abs=1e-9) and e.kovetkezetes


def test_inconsistent_matrix_is_flagged():
    sz = ["a", "b", "c"]
    m = ahp.matrix_itiletekbol(sz, {("a", "b"): 9, ("b", "c"): 9, ("c", "a"): 9})
    assert not ahp.sulyok(sz, m).kovetkezetes


def test_missing_and_fraction():
    with pytest.raises(ValueError):
        ahp.matrix_itiletekbol(["a", "b", "c"], {("a", "b"): 3})
    assert ahp.eval_tort("1/3") == pytest.approx(1 / 3)
    assert ahp.renormalt({"r": 0.6, "g": 0.2, "a": 0.2}, ["r", "g"]) == pytest.approx(
        {"r": 0.75, "g": 0.25})
    assert np.isclose(sum(ahp.RANDOM_INDEX[4] for _ in [0]), 0.90)
