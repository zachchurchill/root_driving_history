"""Provides unit tests for the reporting function"""

import copy

import pytest

from root_driving_history.report import create_driving_report
from root_driving_history.report import create_summary_for_trip_log
from root_driving_history.report import _add_no_trips_line
from root_driving_history.report import _add_had_trips_line
from root_driving_history.report import _remove_slow_and_fast_trips
from root_driving_history.trip_log import TripLog
from root_driving_history.driver import Driver
from root_driving_history.trip import Trip
from root_driving_history.trip import TripTime


class TestCreateSummaryForTripLog:

    def test_non_trip_log_parameter_raises_error(self):
        with pytest.raises(TypeError):
            create_summary_for_trip_log(42)

        with pytest.raises(TypeError):
            create_summary_for_trip_log("Not a TripLog")

        with pytest.raises(TypeError):
            create_summary_for_trip_log([TripLog(Driver("Dan"))])

    def test_empty_trip_log(self):
        trip_log = TripLog(Driver("Dan"))
        assert create_summary_for_trip_log(trip_log) == "Dan: 0 miles"


class TestAddNoTripsLine:

    def test_non_trip_log_parameter_raises_error(self):
        with pytest.raises(TypeError):
            _add_no_trips_line(42)

        with pytest.raises(TypeError):
            _add_no_trips_line("Not a TripLog")

        with pytest.raises(TypeError):
            _add_no_trips_line([TripLog(Driver("Dan"))])

    def test_trip_log_with_trips_raises_error(self):
        trip_log = TripLog(Driver("Dan"))
        trip_log.add_trip(Trip(TripTime(0, 0), TripTime(1, 0), 60))
        with pytest.raises(ValueError):
            _add_no_trips_line(trip_log)

    def test_empty_trip_log(self):
        assert _add_no_trips_line(TripLog(Driver("Dan"))) == "Dan: 0 miles"


class TestAddHadTripsLine:

    def test_non_trip_log_parameter_raises_error(self):
        with pytest.raises(TypeError):
            _add_had_trips_line(42)

        with pytest.raises(TypeError):
            _add_had_trips_line("Not a TripLog")

        with pytest.raises(TypeError):
            _add_had_trips_line([TripLog(Driver("Dan"))])

    def test_trip_log_with_no_trips_raises_error(self):
        trip_log = TripLog(Driver("Dan"))
        with pytest.raises(ValueError):
            _add_had_trips_line(trip_log)

    def test_trip_log_with_one_trip(self):
        dan = "Dan"
        trip_log = TripLog(Driver(dan))
        trip = Trip(TripTime(0, 0), TripTime(1, 0), 60)
        trip_log.add_trip(trip)

        expected_output = "{}: {} miles @ {} mph".format(
            dan, round(trip.miles_driven), round(trip.mph)
        )
        assert _add_had_trips_line(trip_log) == expected_output


class TestRemoveSlowAndFastTrips:

    def test_parameters_not_list_of_trip_log_raises_error(self):
        with pytest.raises(TypeError):
            _remove_slow_and_fast_trips(42)

        with pytest.raises(TypeError):
            _remove_slow_and_fast_trips("list of TripLogs")

        with pytest.raises(TypeError):
            _remove_slow_and_fast_trips(TripLog)

        with pytest.raises(TypeError):
            _remove_slow_and_fast_trips(["not", "trip", "logs"])

        with pytest.raises(TypeError):
            _remove_slow_and_fast_trips([TripLog(Driver("Dan")), "not a log"])

    def test_empty_trip_log_returns_empty_trip_log(self):
        dan = Driver("Dan")
        assert _remove_slow_and_fast_trips(TripLog(dan)) == TripLog(dan)

    def test_trip_log_with_good_trips_remains_the_same(self):
        trip_log = TripLog(Driver("Dan")).add_trip(
            Trip(TripTime(0, 0), TripTime(1, 0), 60)
        )
        assert _remove_slow_and_fast_trips(trip_log) == trip_log

    def test_trip_log_with_slow_trip(self):
        trip_log = TripLog(Driver("Dan")).add_trip(
            Trip(TripTime(0, 0), TripTime(1, 0), 60)
        )
        trip_log_with_slow_trip = copy.deepcopy(trip_log).add_trip(
            Trip(TripTime(0, 0), TripTime(1, 0), 4)
        )
        assert _remove_slow_and_fast_trips(trip_log_with_slow_trip) == trip_log

    def test_trip_log_with_fast_trip(self):
        trip_log = TripLog(Driver("Dan")).add_trip(
            Trip(TripTime(0, 0), TripTime(1, 0), 60)
        )
        trip_log_with_fast_trip = copy.deepcopy(trip_log).add_trip(
            Trip(TripTime(0, 0), TripTime(1, 0), 101)
        )
        assert _remove_slow_and_fast_trips(trip_log_with_fast_trip) == trip_log


class TestCreateDrivingReport:

    def test_empty_list_returns_no_data_collected(self):
        assert create_driving_report([]).lower() == "no data collected"

    def test_parameters_not_list_of_trip_log_raises_error(self):
        with pytest.raises(TypeError):
            create_driving_report(42)

        with pytest.raises(TypeError):
            create_driving_report("list of TripLogs")

        with pytest.raises(TypeError):
            create_driving_report(TripLog)

        with pytest.raises(TypeError):
            create_driving_report(["not", "trip", "logs"])

        with pytest.raises(TypeError):
            create_driving_report([TripLog(Driver("Dan")), "not a log"])

    def test_trip_log_with_one_driver_and_no_trips(self):
        trip_logs = [TripLog(Driver("Dan"))]
        expected_output = "Dan: 0 miles"
        actual_output = create_driving_report(trip_logs)
        assert actual_output == expected_output

    def test_trip_log_with_two_drivers_and_no_trips(self):
        trip_logs = [TripLog(Driver("Dan")), TripLog(Driver("Lauren"))]
        expected_output = "Dan: 0 miles\nLauren: 0 miles"
        actual_output = create_driving_report(trip_logs)
        assert actual_output == expected_output

    def test_trip_log_with_one_driver_with_trips_and_one_without(self):
        trip = Trip(TripTime(0, 0), TripTime(1, 0), 60)
        trip_logs = [
            TripLog(Driver("Dan")).add_trip(trip),
            TripLog(Driver("Lauren"))
        ]
        expected_output = "Dan: {} miles @ {} mph\nLauren: 0 miles".format(
            round(trip.miles_driven), round(trip.mph)
        )
        actual_output = create_driving_report(trip_logs)
        assert actual_output == expected_output

    def test_driver_with_most_miles_is_listed_first(self):
        trip = Trip(TripTime(0, 0), TripTime(1, 0), 60)
        trip_logs1 = [
            TripLog(Driver("Lauren")),
            TripLog(Driver("Dan")).add_trip(trip)
        ]
        expected = "Dan: {} miles @ {} mph\nLauren: 0 miles".format(
            round(trip.miles_driven), round(trip.mph)
        )
        assert create_driving_report(trip_logs1) == expected

        trip1 = Trip(TripTime(0, 0), TripTime(1, 0), 60)
        trip2 = Trip(TripTime(10, 0), TripTime(11, 0), 80)
        trip_logs2 = [
            TripLog(Driver("Lauren")).add_trip(trip1),
            TripLog(Driver("Dan")).add_trip(trip2)
        ]
        expected = "Dan: {} miles @ {} mph\nLauren: {} miles @ {} mph".format(
            round(trip2.miles_driven), round(trip2.mph),
            round(trip1.miles_driven), round(trip1.mph)
        )
        assert create_driving_report(trip_logs2) == expected

    def test_driver_with_multiple_trips_has_correct_summary(self):
        trip1 = Trip(TripTime(0, 0), TripTime(1, 0), 60)
        trip2 = Trip(TripTime(10, 15), TripTime(11, 30), 50)

        trip_logs = [
            TripLog(Driver("Dan")).add_trip(trip1).add_trip(trip2)
        ]
        expected = "Dan: {} miles @ {} mph".format(
            round(trip_logs[0].get_total_miles_driven()),
            round(trip_logs[0].get_average_speed())
        )
        assert create_driving_report(trip_logs) == expected

    def test_multiple_drivers_each_with_multiple_trips_report(self):
        trip1 = Trip(TripTime(0, 0), TripTime(1, 0), 60)
        trip2 = Trip(TripTime(10, 15), TripTime(11, 30), 50)
        trip3 = Trip(TripTime(6, 30), TripTime(7, 50), 35)
        trip4 = Trip(TripTime(15, 15), TripTime(16, 30), 40)

        trip_logs = [
            TripLog(Driver("Dan")).add_trip(trip1).add_trip(trip2),
            TripLog(Driver("Lauren")).add_trip(trip3).add_trip(trip4)
        ]

        dan_total_miles = trip_logs[0].get_total_miles_driven()
        dan_average_mph = trip_logs[0].get_average_speed()
        lauren_total_miles = trip_logs[1].get_total_miles_driven()
        lauren_average_mph = trip_logs[1].get_average_speed()

        expected = "Dan: {} miles @ {} mph\nLauren: {} miles @ {} mph".format(
            round(dan_total_miles), round(dan_average_mph),
            round(lauren_total_miles), round(lauren_average_mph)
        )

        assert create_driving_report(trip_logs) == expected

    def test_trips_under_5mph_or_over_100mph_are_discarded(self):
        slow_trip = Trip(TripTime(0, 0), TripTime(1, 0), 4)
        good_trip = Trip(TripTime(0, 0), TripTime(1, 0), 60)
        fast_trip = Trip(TripTime(0, 0), TripTime(1, 0), 101)

        trip_logs = [
            TripLog(Driver("Dan")).add_trip(good_trip).add_trip(slow_trip)
        ]
        assert create_driving_report(trip_logs) == "Dan: 60 miles @ 60 mph"

        trip_logs = [
            TripLog(Driver("Dan")).add_trip(good_trip).add_trip(fast_trip)
        ]
        assert create_driving_report(trip_logs) == "Dan: 60 miles @ 60 mph"

    def test_example_given_in_problem_statement(self):
        dan_trip_log = TripLog(Driver("Dan"))
        dan_trip_log.add_trip(Trip(TripTime(7, 15), TripTime(7, 45), 17.3))
        dan_trip_log.add_trip(Trip(TripTime(6, 12), TripTime(6, 32), 21.8))

        lauren_trip_log = TripLog(Driver("Lauren"))
        lauren_trip_log.add_trip(Trip(TripTime(12, 1), TripTime(13, 16), 42))

        kumi_trip_log = TripLog(Driver("Kumi"))

        expected = "\n".join([
            "Lauren: 42 miles @ 34 mph",
            "Dan: 39 miles @ 47 mph",
            "Kumi: 0 miles"
        ])

        trip_logs = [dan_trip_log, lauren_trip_log, kumi_trip_log]
        assert create_driving_report(trip_logs) == expected
