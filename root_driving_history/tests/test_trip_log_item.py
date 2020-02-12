"""Provides unit tests for the TripLogItem object"""

import pytest

from root_driving_history.trip import Trip
from root_driving_history.trip import TripTime
from root_driving_history.driver import Driver
from root_driving_history.trip_log import TripLogItem


class TestInterface:

    def test_a_driver_and_trip_are_needed(self):
        assert TripLogItem(
            Driver("Dan"), Trip(TripTime(1, 0), TripTime(2, 0), 60)
        )

    def test_non_driver_object_raises_error(self):
        with pytest.raises(ValueError):
            TripLogItem(42, Trip(TripTime(1, 0), TripTime(2, 0), 60))

    def test_non_trip_object_raises_error(self):
        with pytest.raises(ValueError):
            TripLogItem(Driver("Dan"), 42)
