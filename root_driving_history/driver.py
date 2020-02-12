"""Contains the Driver object definition"""

import attr


@attr.s
class Driver(object):
    name: str = attr.ib()

    @name.validator
    def is_name_at_least_one_character(self, attribute, value):
        if len(value) < 1:
            raise ValueError("'name' needs to be at least 1 character long")
