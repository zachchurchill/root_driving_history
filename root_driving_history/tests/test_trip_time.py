"""Provides unit tests for the TripTime object"""

import pytest

from root_driving_history.trip import TripTime


def test_negative_hours_raises_error():
    with pytest.raises(ValueError):
        TripTime(-1, 0)


def test_hours_greater_than_23_raises_error():
    with pytest.raises(ValueError):
        TripTime(24, 0)


def test_negative_minutes_raises_error():
    with pytest.raises(ValueError):
        TripTime(0, -1)


def test_minutes_greater_than_59_raises_error():
    with pytest.raises(ValueError):
        TripTime(0, 60)


def test_inequality_implementations_between_two_times():
    # __gt__
    assert TripTime(1, 0) > TripTime(0, 0)
    assert TripTime(1, 0) > TripTime(0, 59)

    # __ge__
    assert TripTime(1, 0) >= TripTime(0, 0)
    assert TripTime(1, 0) >= TripTime(0, 59)
    assert TripTime(1, 0) >= TripTime(1, 0)

    # __lt__
    assert TripTime(0, 0) < TripTime(1, 0)
    assert TripTime(0, 59) < TripTime(1, 0)

    # __le__
    assert TripTime(0, 0) <= TripTime(1, 0)
    assert TripTime(0, 59) <= TripTime(1, 0)
    assert TripTime(1, 0) <= TripTime(1, 0)


def test_equality_implementation_between_two_times():
    assert TripTime(0, 0) == TripTime(0, 0)


def test_subtraction_between_two_times():
    assert TripTime(2, 35) - TripTime(1, 35) == 60
    assert TripTime(2, 35) - TripTime(1, 15) == 80
    assert TripTime(2, 35) - TripTime(1, 55) == 40
    assert TripTime(2, 35) - TripTime(3, 0) == -25


def test_addition_not_implemented():
    with pytest.raises(NotImplementedError):
        TripTime(2, 35) + TripTime(3, 0)
