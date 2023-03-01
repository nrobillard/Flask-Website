from Money_Manager.Entities.Recurring_Payments import RecurringPayment
from unittest import TestCase
import pytest


class TestRecurringPayment(TestCase):

    def test_invalid_input(self):

        with pytest.raises(ValueError):

            RecurringPayment("name", -100, True)
