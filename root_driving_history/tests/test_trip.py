"""Provides unit tests for the TripTime and Trip object"""

import pytest

from root_driving_history.trip import TripTime
from root_driving_history.trip import Trip


class TestTripStartTimeBeforeEndTime:

    def test_less_than_hours(self):
        start_hour = 13
        with pytest.raises(ValueError):
            Trip(
                start_time=TripTime(start_hour, 0),
                end_time=TripTime(start_hour - 1, 0),
                miles_driven=10
            )

    def test_equal_hours(self):
        start_hour = 13
        with pytest.raises(ValueError):
            Trip(
                start_time=TripTime(start_hour, 0),
                end_time=TripTime(start_hour, 0),
                miles_driven=10
            )

    def test_less_than_minutes(self):
        start_min = 30
        with pytest.raises(ValueError):
            Trip(
                start_time=TripTime(1, start_min),
                end_time=TripTime(1, start_min - 1),
                miles_driven=10
            )

    def test_equal_to_minutes(self):
        start_min = 30
        with pytest.raises(ValueError):
            Trip(
                start_time=TripTime(1, start_min),
                end_time=TripTime(1, start_min),
                miles_driven=10
            )


class TestDurationProperty:

    def test_duration_property_is_available(self):
        assert hasattr(Trip, 'duration')

    def test_duration_provides_correct_minutes_between_times(self):
        assert Trip(TripTime(1, 15), TripTime(2, 35), 10).duration == 80
        assert Trip(TripTime(1, 15), TripTime(1, 16), 10).duration == 1


class TestMphProperty:

    def test_mph_property_is_available(self):
        assert hasattr(Trip, 'mph')

    def test_mph_provides_correct_results(self):
        assert round(Trip(TripTime(1, 15), TripTime(2, 15), 60).mph) == 60
        assert round(Trip(TripTime(1, 15), TripTime(3, 0), 80).mph, 2) == 45.71
