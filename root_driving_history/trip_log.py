"""Contains the TripLog and TripLogItem definition"""

from typing import List, Union

import attr

from .driver import Driver
from .trip import Trip


@attr.s
class TripLog(object):
    driver: Driver = attr.ib()
    _trips: List[Trip] = attr.ib(init=False, default=attr.Factory(list))

    @driver.validator
    def is_a_driver(self, attribute, value):
        if value.__class__ != Driver:
            raise TypeError("'driver' needs to be a Driver object")

    @property
    def trips(self):
        return self._trips

    def isempty(self):
        return len(self._trips) == 0

    def add_trip(self, trip: Trip) -> "TripLog":
        self._trips.append(trip)
        return self

    def get_total_miles_driven(self) -> float:
        return sum([trip.miles_driven for trip in self._trips])

    def get_average_speed(self) -> Union[None, float]:
        if self.isempty():
            return None
        return (
            sum([trip.miles_driven for trip in self._trips]) /
            sum([trip.duration / 60 for trip in self._trips])
        )
