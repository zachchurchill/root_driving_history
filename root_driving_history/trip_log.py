"""Contains the TripLog and TripLogItem definition"""

from typing import List, Union

import attr

from .driver import Driver
from .trip import Trip


@attr.s
class TripLogItem(object):
    driver: Driver = attr.ib()
    trip: Trip = attr.ib()

    @driver.validator
    def is_a_driver_object(self, attribute, value):
        if value.__class__ != Driver:
            raise ValueError("'driver' needs to be a Driver object")

    @trip.validator
    def is_a_trip_object(self, attribute, value):
        if value.__class__ != Trip:
            raise ValueError("'trip' needs to be a Trip object")


@attr.s
class TripLog(object):
    _items: List[TripLogItem] = attr.ib(init=False, default=attr.Factory(list))

    @property
    def items(self):
        return self._items

    def _get_driver_logs(self, driver) -> List[TripLogItem]:
        return [
            log_item for log_item in self._items if log_item.driver == driver
        ]

    def add_trip_log_item(self, driver: Driver, trip: Trip) -> "TripLog":
        self._items.append(TripLogItem(driver, trip))
        return self

    def get_total_miles_driven(self, driver: Driver) -> float:
        driver_logs = self._get_driver_logs(driver)
        return sum(
            [driver_log.trip.miles_driven for driver_log in driver_logs]
        )

    def get_average_speed(self, driver: Driver) -> Union[None, float]:
        driver_logs = self._get_driver_logs(driver)
        if driver_logs:
            average_speed = (
                sum([driver_log.trip.mph for driver_log in driver_logs]) /
                len(driver_logs)
            )
        else:
            average_speed = None
        return average_speed
