"""Provides unit tests for the TripLog object"""

from root_driving_history.trip import Trip
from root_driving_history.trip import TripTime
from root_driving_history.driver import Driver
from root_driving_history.trip_log import TripLog


class TestInterface:

    def test_no_parameters_needed(self):
        assert TripLog()

    def test_provides_an_items_property(self):
        assert hasattr(TripLog, "items")

    def test_provides_method_to_add_trip_log(self):
        assert hasattr(TripLog, "add_trip_log_item")

    def test_provides_a_method_to_get_total_miles_driven_for_driver(self):
        assert hasattr(TripLog, "get_total_miles_driven")

    def test_provides_a_method_to_get_average_speed_for_driver(self):
        assert hasattr(TripLog, "get_average_speed")


class TestTripLogProperty:

    def test_trip_log_is_initially_empty_list(self):
        trip_log = TripLog()
        assert trip_log.items == []

    def test_trip_logs_can_be_saved(self):
        trip_log = TripLog()

        dan = Driver("Dan")
        trip1 = Trip(TripTime(1, 0), TripTime(2, 0), 60)
        trip_log.add_trip_log_item(dan, trip1)

        assert len(trip_log.items) == 1
        assert trip_log.items[0].driver == dan
        assert trip_log.items[0].trip == trip1

        trip2 = Trip(TripTime(4, 50), TripTime(5, 10), 35)
        trip_log.add_trip_log_item(dan, trip2)

        assert len(trip_log.items) == 2
        assert trip_log.items[0].driver == dan
        assert trip_log.items[0].trip == trip1
        assert trip_log.items[1].driver == dan
        assert trip_log.items[1].trip == trip2


class TestGetTotalMilesDriverHasDriven:

    def test_total_miles_driven_after_one_trip_equals_trip_miles_driven(self):
        trip_log = TripLog()

        dan = Driver("Dan")
        trip = Trip(TripTime(1, 15), TripTime(2, 15), 60)
        trip_log.add_trip_log_item(dan, trip)

        assert trip_log.get_total_miles_driven(dan) == trip.miles_driven

    def test_total_miles_driven_for_driver_without_trips_is_zero(self):
        trip_log = TripLog()

        dan = Driver("Dan")
        assert trip_log.get_total_miles_driven(dan) == 0

        lauren = Driver("Lauren")
        trip = Trip(TripTime(1, 15), TripTime(2, 15), 60)
        trip_log.add_trip_log_item(lauren, trip)

        # Checking that Dan still doesn't have any trips/miles driven
        assert trip_log.get_total_miles_driven(dan) == 0

    def test_total_miles_driven_equals_sum_of_all_trips_taken(self):
        trip_log = TripLog()

        dan = Driver("Dan")
        trip1 = Trip(TripTime(1, 0), TripTime(2, 0), 60)
        trip2 = Trip(TripTime(5, 15), TripTime(6, 40), 75)

        trip_log.add_trip_log_item(dan, trip1)
        trip_log.add_trip_log_item(dan, trip2)

        total_miles_driven = trip1.miles_driven + trip2.miles_driven
        assert trip_log.get_total_miles_driven(dan) == total_miles_driven


class TestGetAverageSpeed:

    def test_average_speed_for_driver_with_no_trips_is_none(self):
        trip_log = TripLog()

        dan = Driver("Dan")

        assert trip_log.get_average_speed(dan) is None

    def test_average_speed_for_driver_with_one_trip_is_mph_of_trip(self):
        trip_log = TripLog()

        dan = Driver("Dan")
        trip = Trip(TripTime(1, 0), TripTime(2, 0), 60)
        trip_log.add_trip_log_item(dan, trip)

        assert trip_log.get_average_speed(dan) == trip.mph

    def test_average_speed_for_driver_with_many_trips_is_avg_of_mph(self):
        trip_log = TripLog()

        dan = Driver("Dan")
        trip1 = Trip(TripTime(1, 0), TripTime(2, 0), 60)
        trip2 = Trip(TripTime(4, 0), TripTime(5, 30), 120)
        trip_log.add_trip_log_item(dan, trip1)
        trip_log.add_trip_log_item(dan, trip2)

        average_speed = ((trip1.mph + trip2.mph) / 2)
        assert trip_log.get_average_speed(dan) == average_speed

        trip3 = Trip(TripTime(6, 0), TripTime(7, 0), 50)
        trip_log.add_trip_log_item(dan, trip3)

        average_speed = ((trip1.mph + trip2.mph + trip3.mph) / 3)
        assert trip_log.get_average_speed(dan) == average_speed
