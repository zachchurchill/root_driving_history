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
