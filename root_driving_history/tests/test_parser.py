"""Provides unit tests for the Parser object"""

import pytest

from root_driving_history.parser import parse_input_log
from root_driving_history.parser import _create_trip_from_regex_trip_line
from root_driving_history.parser import _create_driver_from_regex_driver_line
from root_driving_history.parser import _get_driver_of_regex_trip_line
from root_driving_history.trip import Trip, TripTime
from root_driving_history.driver import Driver


class TestParseInputLog:

    def test_parameters_other_than_str_and_stringio_raise_error(self):
        with pytest.raises(TypeError):
            parse_input_log(42)

        with pytest.raises(TypeError):
            parse_input_log(["list", "of", "strings"])

    def test_returns_empty_list_when_given_empty_string(self):
        assert parse_input_log("") == []

    def test_returns_empty_list_when_given_string_without_keywords(self):
        assert parse_input_log("no keywords here") == []

    def test_returns_empty_list_with_lowercase_keys(self):
        assert parse_input_log("driver Dan") == []
        assert parse_input_log("trip Dan 01:15 02:35 10.0") == []

    def test_single_driver_returns_trip_log_with_no_trips(self):
        dan = "Dan"
        driver_trip_logs = parse_input_log("Driver {}".format(dan))
        assert len(driver_trip_logs) == 1
        assert driver_trip_logs[0].isempty()
        assert driver_trip_logs[0].driver.name == dan

    def test_only_drivers_returns_trip_logs_with_no_trips(self):
        dan = "Dan"
        lauren = "Lauren"
        driver_trip_logs = parse_input_log(
            "Driver {}\nDriver {}".format(dan, lauren)
        )
        assert len(driver_trip_logs) == 2
        assert driver_trip_logs[0].isempty()
        assert driver_trip_logs[0].driver.name == dan
        assert driver_trip_logs[1].isempty()
        assert driver_trip_logs[1].driver.name == lauren

    def test_one_driver_and_one_trip_returns_correct_trip_log(self):
        dan = "Dan"
        trip = Trip(TripTime(1, 15), TripTime(2, 35), 10)
        driver_trip_logs = parse_input_log(
            "Driver {name}\nTrip {name} {start} {end} {miles}".format(**{
                    "name": dan,
                    "start": trip.start_time,
                    "end": trip.end_time,
                    "miles": trip.miles_driven
            })
        )
        assert len(driver_trip_logs) == 1
        assert driver_trip_logs[0].driver.name == dan
        assert driver_trip_logs[0].isempty() is False
        assert len(driver_trip_logs[0].trips) == 1
        assert driver_trip_logs[0].trips[0] == trip

    def test_one_driver_and_two_trips_returns_correct_trip_log(self):
        dan = "Dan"
        trip1 = Trip(TripTime(1, 15), TripTime(2, 35), 10)
        trip2 = Trip(TripTime(6, 12), TripTime(7, 12), 60)
        raw_data = "\n".join([
            "Driver {name}",
            "Trip {name} {start1} {end1} {miles1}",
            "Trip {name} {start2} {end2} {miles2}"
        ]).format(**{
            "name": dan,
            "start1": trip1.start_time,
            "end1": trip1.end_time,
            "miles1": trip1.miles_driven,
            "start2": trip2.start_time,
            "end2": trip2.end_time,
            "miles2": trip2.miles_driven,
        })
        driver_trip_logs = parse_input_log(raw_data)

        assert len(driver_trip_logs) == 1
        assert driver_trip_logs[0].driver.name == dan
        assert driver_trip_logs[0].isempty() is False
        assert len(driver_trip_logs[0].trips) == 2
        assert driver_trip_logs[0].trips[0] == trip1
        assert driver_trip_logs[0].trips[1] == trip2

    def test_two_drivers_with_one_trip_each_returns_correct_trip_log(self):
        dan = "Dan"
        lauren = "Lauren"
        trip = Trip(TripTime(1, 15), TripTime(2, 35), 10)
        raw_data = "\n".join([
            "Driver {name1}",
            "Driver {name2}",
            "Trip {name1} {start} {end} {miles}",
            "Trip {name2} {start} {end} {miles}"
        ]).format(**{
            "name1": dan,
            "name2": lauren,
            "start": trip.start_time,
            "end": trip.end_time,
            "miles": trip.miles_driven,
        })
        driver_trip_logs = parse_input_log(raw_data)

        assert len(driver_trip_logs) == 2

        assert driver_trip_logs[0].driver.name == dan
        assert driver_trip_logs[0].isempty() is False
        assert len(driver_trip_logs[0].trips) == 1
        assert driver_trip_logs[0].trips[0] == trip

        assert driver_trip_logs[1].driver.name == lauren
        assert driver_trip_logs[1].isempty() is False
        assert len(driver_trip_logs[1].trips) == 1
        assert driver_trip_logs[1].trips[0] == trip


class TestCreateDriverFromRegexDriverLine:

    def test_input_that_does_not_match_regex_returns_none(self):
        assert _create_driver_from_regex_driver_line("Doesn't match") is None

    def test_input_that_does_match_regex_returns_correct_driver(self):
        driver_line = "Driver Dan"
        expected_driver = Driver("Dan")
        actual_driver = _create_driver_from_regex_driver_line(driver_line)
        assert actual_driver == expected_driver


class TestCreateTripFromRegexTripLine:

    def test_input_that_does_not_match_regex_returns_none(self):
        assert _create_trip_from_regex_trip_line("Doesn't match") is None

    def test_input_that_does_match_regex_returns_correct_trip(self):
        trip_line = "Trip Dan 07:15 07:45 17.3"
        expected_trip = Trip(TripTime(7, 15), TripTime(7, 45), 17.3)
        assert _create_trip_from_regex_trip_line(trip_line) == expected_trip

        trip_line = "Trip Dan 07:15 12:45 0.6"
        expected_trip = Trip(TripTime(7, 15), TripTime(12, 45), 0.6)
        assert _create_trip_from_regex_trip_line(trip_line) == expected_trip


class TestGetDriverNameOfRegexTripLine:

    def test_input_that_does_not_match_regex_returns_none(self):
        assert _get_driver_of_regex_trip_line("Doesn't match") is None

    def test_input_that_does_match_regex_returns_correct_driver(self):
        dan = "Dan"
        trip_line = "Trip {} 07:15 07:45 17.3".format(dan)
        assert _get_driver_of_regex_trip_line(trip_line) == dan
