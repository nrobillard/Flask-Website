from Money_Manager.Entities.Loan import Loan
from unittest import TestCase
import pytest
from math import isclose


class TestLoan(TestCase):

    def test_negative_interest_rate(self):

        with pytest.raises(ValueError):

            Loan("Test", -1, 1, "uri.edu", 1)

    def test_negative_monthly_payment(self):

        with pytest.raises(ValueError):

            Loan("Test", 1, -1, "uri.edu", 1)

    def test_negative_balance(self):

        with pytest.raises(ValueError):

            Loan("Test", 1, 1, "uri.edu", -1)

    def test_change_monthly_payment(self):

        loan = Loan("Test", 1, 1, "uri.edu", 1)
        loan.change_monthly_payment(300)

        assert loan._monthly_payment == 300

    def test_negative_monthly_payment_change(self):

        loan = Loan("Test", 1, 1, "uri.edu", 1)

        with pytest.raises(ValueError):

            loan.change_monthly_payment(-300)

    def test_months_left(self):

        loan = Loan("test", 0.06, 300, "uri.edu", 20_000)

        assert isclose(81.29558, loan.months_left(), abs_tol=0.00001)

    def test_invalid_estimated_months_left_input(self):

        loan = Loan("Test", 1, 1, "uri.edu", 1)

        with pytest.raises(ValueError):

            loan.estimated_months_left(-1)

    def test_valid_estimated_months_left_input(self):

        loan = Loan("test", 0.06, 300, "uri.edu", 20_000)

        assert isclose(138.97572, loan.estimated_months_left(200), abs_tol=0.00001)


