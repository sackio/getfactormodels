"""Every exposed model must actually pull. ⛔ INTEGRATION — this reaches the network.

Run it deliberately:

    pytest -m integration

It is excluded from the default suite on purpose. tests/test_http.py once patched the wrong
method, so an "offline" unit test silently downloaded from example.com and compared that HTML
to its expected bytes — it failed loudly here, but the same defect passes silently against any
endpoint that returns the right value. Network tests are fine; network tests wearing a unit
test's clothes are not.
"""
import pytest

import getfactormodels as g

# ⚠️ Discovered, not hard-coded: a model added upstream must show up here without an edit, or
# this file quietly stops covering the thing it claims to cover.
MODEL_NAMES = sorted(n for n in dir(g) if n.endswith(("Factors", "CAPM")))

# HighIncomeCCAPM is annual-only and says so with a clear ValueError. That is correct behaviour,
# not a gap, so it is exercised at its own frequency rather than excused.
FREQUENCY = {"HighIncomeCCAPM": "y"}


def test_the_full_set_is_discovered():
    assert len(MODEL_NAMES) == 15, MODEL_NAMES


@pytest.mark.integration
@pytest.mark.parametrize("name", MODEL_NAMES)
def test_model_pulls(name):
    frame = getattr(g, name)(frequency=FREQUENCY.get(name, "m")).to_pandas()

    assert len(frame) > 50, f"{name} returned {len(frame)} rows"
    assert not frame.empty and len(frame.columns) >= 2, f"{name} columns: {list(frame.columns)}"
    # ⛔ A factor file that parsed into a single column, or an index that is not a date, is the
    # shape a silently-broken download takes — it is not empty, so a truthiness check passes it.
    assert frame.index.is_monotonic_increasing, f"{name} index is not ordered"
    assert str(frame.index.dtype).startswith("datetime"), f"{name} index dtype {frame.index.dtype}"


@pytest.mark.integration
def test_annual_only_model_rejects_monthly():
    """The one model that refuses a frequency must refuse it loudly, not return something wrong."""
    with pytest.raises(ValueError, match="annual"):
        g.HighIncomeCCAPM(frequency="m").to_pandas()
