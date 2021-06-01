from blob import *
import pytest



@pytest.fixture(scope='module')
def blobs():
    limits = np.array([100, 100])
    blobs = {
        'blob1': Blob((4 / (3 * pi)), 1, 0, np.array([1, 0], dtype=float), limits, state=Contagious, active_virus=True),
        'blob2': Blob((4 / (3 * pi)), 3, 0, np.array([-1, 0], dtype=float), limits),
        'blob3': Blob(8, 50, 101, np.array([2, 2], dtype=float), limits),
        'blob4': Blob(8, 101, 50, np.array([2, 2], dtype=float), limits, state=Contagious),
        'blob5': Blob(6, 3, 4, np.array([1, 0], dtype=float), limits)
    }
    yield blobs


def test_distance(blobs):
    assert blobs['blob1'].distance_from(blobs['blob2']) == 2


def test_is_collision(blobs):
    assert blobs['blob1'].is_collision(blobs['blob2']) is True


def test_out_of_bounds(blobs):
    v1 = np.array([1, 0], dtype=float)
    blobs['blob1'].out_of_bounds()
    assert np.array_equal(v1, blobs['blob1'].V)

    v_after = np.array([2, -2])
    blobs['blob3'].out_of_bounds()
    assert np.array_equal(v_after, blobs['blob3'].V)

    v_after = np.array([-2, 2])
    blobs['blob4'].out_of_bounds()
    assert np.array_equal(v_after, blobs['blob4'].V)


def test_state_by_collision(blobs):
    blobs['blob1'].change_state_by_collision(blobs['blob4'])


def test_get_force(blobs):
    assert blobs['blob1'].get_force(blobs['blob2'])[0] < 0
    assert blobs['blob2'].get_force(blobs['blob1'])[0] > 0


def test_change_speed(blobs):
    v_i = np.array([-1, 0], dtype=float)
    blobs['blob1'].change_speed(blobs['blob2'])
    assert np.array_equal(v_i, blobs['blob1'].V)


def test_change_position(blobs):
    after_change = np.array([4, 4])
    blobs['blob5'].change_position()
    assert np.array_equal(after_change, blobs['blob5'].position)


def test_infected_blob(blobs):
    blobs['blob2'].change(blobs['blob1'])
    assert blobs['blob2'].virus.is_active()
    assert blobs['blob2'].color == Red
    assert blobs['blob2'].state == Contagious


def test_recovered_blob(blobs):
    for _ in range(virus_living_time+10):
        blobs['blob1'].move_and_age()
    assert blobs['blob1'].color is Green
    assert blobs['blob1'].virus.is_active() is False
    assert blobs['blob1'].state is Recovered


@pytest.fixture(scope='module')
def viruses():
    viruses = {
        'virus1': Virus(living_time=10),
        'virus2': Virus(living_time=20)
    }
    yield viruses


def test_virus_not_there(viruses):
    assert viruses['virus1'].is_active() is False

    viruses['virus1'].activate()
    assert viruses['virus1'].is_active() is True


def test_v_dies_of(viruses):
    viruses['virus1'].activate()
    viruses['virus2'].activate()
    for day in range(10):
        viruses['virus1'].aging()
        viruses['virus2'].aging()
    assert viruses['virus1'].is_active() is False
    assert viruses['virus2'].is_active() is True



