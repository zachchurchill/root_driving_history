"""Contains the definition for report functions"""

from typing import List

from .trip_log import TripLog


def create_driving_report(trip_logs: List[TripLog]) -> str:
    if any([trip_log.__class__ != TripLog for trip_log in trip_logs]):
        raise TypeError("'trip_logs' should be a list of TripLog objects")

    if trip_logs:
        prepared_trip_logs = [
            _remove_slow_and_fast_trips(trip_log)
            for trip_log in trip_logs
        ]
        report_items_with_total_miles = [
            (
                prepared_trip_log.get_total_miles_driven(),
                create_summary_for_trip_log(prepared_trip_log)
            )
            for prepared_trip_log in prepared_trip_logs
        ]
        sorted_report_items = [
            report_item
            for _, report_item in sorted(
                report_items_with_total_miles, key=lambda k: k[0], reverse=True
            )
        ]
        report = "\n".join(sorted_report_items)
    else:
        report = "No data collected"

    return report


def create_summary_for_trip_log(trip_log: TripLog) -> str:
    if trip_log.__class__ != TripLog:
        raise TypeError("'trip_log' needs to be a TripLog object")

    return _add_no_trips_line(trip_log) \
        if trip_log.isempty() \
        else _add_had_trips_line(trip_log)


def _add_no_trips_line(trip_log: TripLog) -> str:
    if trip_log.__class__ != TripLog:
        raise TypeError("'trip_log' needs to be a TripLog object")

    if not trip_log.isempty():
        raise ValueError("'trip_log' is expected to be empty")

    return "{}: 0 miles".format(trip_log.driver.name)


def _add_had_trips_line(trip_log: TripLog) -> str:
    if trip_log.__class__ != TripLog:
        raise TypeError("'trip_log' needs to be a TripLog object")

    if trip_log.isempty():
        raise ValueError("'trip_log' is expected to have at least one trip")

    return "{name}: {total_miles} miles @ {avg_speed} mph".format(**{
        "name": trip_log.driver.name,
        "total_miles": round(trip_log.get_total_miles_driven()),
        "avg_speed": round(trip_log.get_average_speed())
    })


def _remove_slow_and_fast_trips(
        trip_log: TripLog, slow_threshold=5, fast_threshold=100
) -> TripLog:
    if trip_log.__class__ != TripLog:
        raise TypeError("'trip_log' needs to be a TripLog object")

    driver = trip_log.driver
    trips = [
        trip
        for trip in trip_log.trips
        if slow_threshold <= trip.mph <= fast_threshold
    ]

    return_log = TripLog(driver)
    for trip in trips:
        return_log.add_trip(trip)

    return return_log
