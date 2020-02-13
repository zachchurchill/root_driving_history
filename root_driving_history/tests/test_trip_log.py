"""Provides unit tests for the TripLog object"""

import pytest

from root_driving_history.trip import Trip
from root_driving_history.trip import TripTime
from root_driving_history.driver import Driver
from root_driving_history.trip_log import TripLog


class TestInterface:

    def test_driver_needed_to_create_trip_log(self):
        with pytest.raises(TypeError):
            TripLog(42)

        with pytest.raises(TypeError):
            TripLog("Dan")

        assert TripLog(Driver("Dan"))

    def test_provides_a_trips_property(self):
        assert hasattr(TripLog, "trips")

    def test_provides_method_to_add_trip(self):
        assert hasattr(TripLog, "add_trip")

    def test_provides_a_method_to_get_total_miles_driven_for_driver(self):
        assert hasattr(TripLog, "get_total_miles_driven")

    def test_provides_a_method_to_get_average_speed_for_driver(self):
        assert hasattr(TripLog, "get_average_speed")

    def test_provides_a_isempty_method(self):
        assert hasattr(TripLog, "isempty")


class TestTripLogItems:

    def test_trip_log_is_initially_empty_list(self):
        trip_log = TripLog(Driver("Dan"))
        assert trip_log.trips == []
        assert trip_log.isempty()

    def test_trip_logs_can_be_saved(self):
        trip_log = TripLog(Driver("Dan"))

        trip1 = Trip(TripTime(1, 0), TripTime(2, 0), 60)
        trip_log.add_trip(trip1)

        assert len(trip_log.trips) == 1
        assert trip_log.trips[0] == trip1

        trip2 = Trip(TripTime(4, 50), TripTime(5, 10), 35)
        trip_log.add_trip(trip2)

        assert len(trip_log.trips) == 2
        assert trip_log.trips[0] == trip1
        assert trip_log.trips[1] == trip2


class TestGetTotalMilesDriverHasDriven:

    def test_total_miles_driven_for_driver_without_trips_is_zero(self):
        trip_log = TripLog(Driver("Dan"))
        assert trip_log.get_total_miles_driven() == 0

    def test_total_miles_driven_after_one_trip_equals_trip_miles_driven(self):
        trip_log = TripLog(Driver("Dan"))

        trip = Trip(TripTime(1, 15), TripTime(2, 15), 60)
        trip_log.add_trip(trip)

        assert trip_log.get_total_miles_driven() == trip.miles_driven

    def test_total_miles_driven_equals_sum_of_all_trips_taken(self):
        trip_log = TripLog(Driver("Dan"))

        trip1 = Trip(TripTime(1, 0), TripTime(2, 0), 60)
        trip2 = Trip(TripTime(5, 15), TripTime(6, 40), 75)

        trip_log.add_trip(trip1)
        trip_log.add_trip(trip2)

        total_miles_driven = trip1.miles_driven + trip2.miles_driven
        assert trip_log.get_total_miles_driven() == total_miles_driven


class TestGetAverageSpeed:

    def test_average_speed_for_driver_with_no_trips_is_none(self):
        trip_log = TripLog(Driver("Dan"))
        assert trip_log.get_average_speed() is None

    def test_average_speed_for_driver_with_one_trip_is_mph_of_trip(self):
        trip_log = TripLog(Driver("Dan"))

        trip = Trip(TripTime(1, 0), TripTime(2, 0), 60)
        trip_log.add_trip(trip)

        assert trip_log.get_average_speed() == trip.mph

    def test_average_speed_for_driver_with_many_trips_is_avg_of_mph(self):
        trip_log = TripLog(Driver("Dan"))

        trip1 = Trip(TripTime(1, 0), TripTime(2, 0), 60)
        trip2 = Trip(TripTime(4, 0), TripTime(5, 30), 120)
        trip_log.add_trip(trip1)
        trip_log.add_trip(trip2)

        average_speed = (
            (trip1.miles_driven + trip2.miles_driven) /
            (trip1.duration / 60 + trip2.duration / 60)
        )
        assert trip_log.get_average_speed() == average_speed

        trip3 = Trip(TripTime(6, 0), TripTime(7, 0), 50)
        trip_log.add_trip(trip3)

        average_speed = (
            (trip1.miles_driven + trip2.miles_driven + trip3.miles_driven) /
            (trip1.duration / 60 + trip2.duration / 60 + trip3.duration / 60)
        )
        assert trip_log.get_average_speed() == average_speed
