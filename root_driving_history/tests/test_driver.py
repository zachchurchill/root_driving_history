"""Provides unit tests for the Driver object"""

import pytest

from root_driving_history.driver import Driver


class TestInterface:

    def test_empty_name_raises_error(self):
        with pytest.raises(ValueError):
            Driver("")

    def test_one_character_name_works(self):
        assert Driver("1")
