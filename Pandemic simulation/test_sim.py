from simulation import *
import pytest

@pytest.fixture(scope='module')
def sims():
    sims = {
        'board': Board()
    }
    sims['board'].set_up()
    yield sims


def test_running(sims):
    assert sims['board'].is_running() is True

    sims['board'].terminate()
    assert sims['board'].is_running() is False
