"""Contains the Trip object definition"""

import attr


@attr.s
class TripTime(object):
    hour: int = attr.ib()
    min: int = attr.ib()

    @hour.validator
    def is_between_zero_and_twenty_three(self, attribute, value):
        if value < 0 or value > 23:
            raise ValueError("'hour' should be between 0 and 23, inclusive")

    @min.validator
    def is_between_zero_and_fifty_nine(self, attribute, value):
        if value < 0 or value > 59:
            raise ValueError("'hour' should be between 0 and 59, inclusive")

    def __sub__(self, other: "TripTime") -> int:
        """Returns the number of minutes difference between two times."""
        hours_difference = self.hour - other.hour
        mins_difference = self.min - other.min
        return (hours_difference * 60) + mins_difference

    def __add__(self, other):
        raise NotImplementedError


@attr.s
class Trip(object):
    start_time: TripTime = attr.ib()
    end_time: TripTime = attr.ib()
    miles_driven: float = attr.ib()

    @start_time.validator
    def starts_before_end_time(self, attribute, value):
        if value >= self.end_time:
            raise ValueError(
                'start_time should be before end_time'
            )

    @property
    def duration(self) -> int:
        return self.end_time - self.start_time

    @property
    def mph(self) -> float:
        return self.miles_driven / ((self.end_time - self.start_time) / 60)
