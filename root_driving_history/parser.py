"""Contains the Parser object definition"""

import re
from io import StringIO
from collections import defaultdict
from typing import Union, List

from .trip_log import TripLog
from .driver import Driver
from .trip import Trip
from .trip import TripTime


DRIVER_KEYWORD_REGEX = "Driver [A-Za-z]{2,}"
TRIP_KEYWORD_REGEX = r"Trip [A-Za-z]{2,} \d{2}:\d{2} \d{2}:\d{2} \d+\.?\d*"


def parse_input_log(raw_data: Union[str, StringIO]) -> List[TripLog]:
    if raw_data.__class__ not in [str, StringIO]:
        raise TypeError(
            "'raw_data' needs to be a str or io.StringIO buffer, if given"
        )

    if raw_data.__class__ == StringIO:
        raw_data = raw_data.getvalue()

    driver_lines = re.findall(DRIVER_KEYWORD_REGEX, raw_data)
    trip_lines = re.findall(TRIP_KEYWORD_REGEX, raw_data)

    if driver_lines:
        drivers = [
            _create_driver_from_regex_driver_line(driver_line)
            for driver_line in driver_lines
        ]
        trip_logs = [TripLog(driver) for driver in drivers]

        # Add trips to each Driver's TripLog
        trips_by_driver = defaultdict(list)
        for trip_line in trip_lines:
            trips_by_driver[_get_driver_of_regex_trip_line(trip_line)].append(
                _create_trip_from_regex_trip_line(trip_line)
            )

        driver_names = [trip_log.driver.name for trip_log in trip_logs]
        for driver_name, trips in trips_by_driver.items():
            try:
                driver_log_index = driver_names.index(driver_name)
            except ValueError:
                continue

            for trip in trips:
                trip_logs[driver_log_index].add_trip(trip)

    else:
        trip_logs = []

    return trip_logs


def _create_driver_from_regex_driver_line(
        regex_driver_line: str
) -> Union[None, Driver]:
    if not re.match(DRIVER_KEYWORD_REGEX, regex_driver_line):
        return None

    keyword, driver_name = regex_driver_line.split(" ")

    return Driver(driver_name)


def _create_trip_from_regex_trip_line(
        regex_trip_line: str
) -> Union[None, Trip]:
    if not re.match(TRIP_KEYWORD_REGEX, regex_trip_line):
        return None

    keyword, driver, start_time, end_time, miles = regex_trip_line.split(" ")

    start_time_hour, start_time_min = [int(p) for p in start_time.split(":")]
    end_time_hour, end_time_min = [int(p) for p in end_time.split(":")]
    miles_driven = float(miles)

    return Trip(
        TripTime(start_time_hour, start_time_min),
        TripTime(end_time_hour, end_time_min),
        miles_driven
    )


def _get_driver_of_regex_trip_line(
        regex_trip_line: str
) -> Union[None, Driver]:
    if not re.match(TRIP_KEYWORD_REGEX, regex_trip_line):
        return None

    _, driver_name, _, _, _ = regex_trip_line.split(" ")

    return driver_name
