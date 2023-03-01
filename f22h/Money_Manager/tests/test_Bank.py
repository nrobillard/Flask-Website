
import pytest

from Money_Manager.Entities.Bank import Bank
from Money_Manager.Entities.Loan import Loan
from Money_Manager.Entities.UserEntity import User


class TestBank:
    def test_value_error_init_overdraft(self):
        """
        This Test ensures a value error is raised when a negative overdraft fee is applied in the constructor
        :return:
        """
        with pytest.raises(ValueError):
            bank = Bank("NFCU", "Credit Union", -35)

    def test_set_overdraft_fee(self):
        """
        Ensures overdraft fee is set correctly
        :return:
        """
        bank = Bank("NFCU","Credit Union",35)
        bank.set_overdraft_fee(77)
        assert bank.get_overdraft_fee() == 77

    def test_value_error_overdraft(self):
        """
        Ensures an error is raised when a negative over draft fee is set from the method
        :return:
        """
        bank = Bank("NFCU", "Credit Union", 35)
        with pytest.raises(ValueError):
            bank.set_overdraft_fee(-88)

    def test_add_user_to_bank(self):
        """
        Ensures a user is added to a banks list of user objects
        :return:
        """
        bank = Bank("NFCU", "Credit Union", 35)
        user = User("reid@uri.edu", "reidm77", "Reid ", "Morin", "password")
        bank.add_user_to_bank(user)

        assert user in bank.get_user_list()

    def test_add_loan_to_bank(self):
        """
        Ensures a loan is added to a banks list of loan objects
        return:
        """
        bank = Bank("NFCU", "Credit Union", 35)
        loan = Loan("Car Loan", 77.7, 77, 500, 33, 77, bank)
        bank.add_loan_to_bank(loan)

        assert loan in bank.get_loan_list()

    def test_get_all_user_balances(self):
        """
        Ensures the summation of all balances in the user object list
        :return:
        """
        bank = Bank("NFCU","Credit Union",35)
        user = User("reid@uri.edu", "reidm77", "Reid ", "Morin", "password")
        user2 = User("erin@uri.edu", "erin77", "erin ", "Morin", "password")
        user3 = User("jamie@uri.edu", "jamie77", "jamie ", "Morin", "password")

        user.set_current_balance(700)
        user2.set_current_balance(770)
        user3.set_current_balance(888)

        bank.add_user_to_bank(user)
        bank.add_user_to_bank(user2)
        bank.add_user_to_bank(user3)
        assert bank.get_all_user_balances() == 2358

    def test_money_loaned_out(self):

        """
        Ensures the summation of all loans in the loan object list
        :return:
        """

        bank = Bank("NFCU","Credit Union",35)
        loan = Loan("Car Loan", 77.7, 77, 500, 33, 77, bank)
        loan2 = Loan(" Loan", 77.7, 77, 500, 33, 77, bank)
        loan3 = Loan("House Loan", 77.7, 77, 500, 33, 77, bank)

        bank.add_loan_to_bank(loan)
        bank.add_loan_to_bank(loan2)
        bank.add_loan_to_bank(loan3)

        assert bank.money_loaned_out() == 1500

    def test_apply_over_draft_fee(self):
        """
        Ensures the overdraft fee is applied to the related user
        :return:
        """
        bank = Bank("NFCU", "Credit Union", 35)
        user = User("reid@uri.edu", "reidm77", "Reid ", "Morin", "password")
        user.set_current_balance(30)
        user.subtract_balance(31)
        bank.apply_over_draft_fee(user)

        assert user.get_current_balance() == -36

    def test_raises_value_error_apply_over_draft_fee(self):
        """
        Ensures an overdraft fee can not be applied if the users balance is greater than or equal to 0
        :return:
        """
        bank = Bank("NFCU", "Credit Union", 35)
        user = User("reid@uri.edu", "reidm77", "Reid ", "Morin", "password")
        user.set_current_balance(30)
        user.subtract_balance(1)

        with pytest.raises(ValueError):
            bank.apply_over_draft_fee(user)

    def test_forgive_all_loans(self):
        """
        Ensures all loans in banks loan list become a zero balance
        :return:
        """
        bank = Bank("NFCU", "Credit Union", 35)
        loan = Loan("Car Loan", 77.7, 77, 500, 33, 77, bank)
        loan2 = Loan(" Loan", 77.7, 77, 500, 33, 77, bank)
        loan3 = Loan("House Loan", 77.7, 77, 500, 33, 77, bank)

        bank.add_loan_to_bank(loan)
        bank.add_loan_to_bank(loan2)
        bank.add_loan_to_bank(loan3)

        bank.forgive_all_loans()

        for entity in bank.get_loan_list():
            assert entity.get_balance() == 0

    def test_add_balance_to_user(self):
        """
        Ensures a balance is added to a desired user from a bank login
        :return:
        """
        bank = Bank("NFCU", "Credit Union", 35)
        user = User("reid@uri.edu", "reidm77", "Reid ", "Morin", "password")

        user.set_current_balance(70)
        bank.add_balance_to_user(user,7)

        assert user.get_current_balance() == 77

    def test_raises_value_error_add_balance_to_user(self):
        """
        Ensures a value error is raised if a negative balance is trying to be added to a user
        :return:
        """
        bank = Bank("NFCU", "Credit Union", 35)
        user = User("reid@uri.edu", "reidm77", "Reid ", "Morin", "password")

        user.set_current_balance(70)

        with pytest.raises(ValueError):
            bank.add_balance_to_user(user,-8)

    def test_subtract_balance_from_user(self):

        """
        Ensures a balance is subtracted from a desired user from a bank login
        :return:
        """
        bank = Bank("NFCU", "Credit Union", 35)
        user = User("reid@uri.edu", "reidm77", "Reid ", "Morin", "password")

        user.set_current_balance(70)
        bank.subtract_balance_from_user(user, 5)
        assert user.get_current_balance() == 65

    def test_transfer_loans(self):
        """
        Ensures all loans associated from one user is removed from bank 1 and then transferred to bank 2
        :return:
        """
        bank1 = Bank("NFCU", "Credit Union", 35)
        bank2 = Bank("Bank of America", "Retail", 100)
        user = User("reid@uri.edu", "reidm77", "Reid ", "Morin", "password")
        loan = Loan("Car Loan", 77.7, 77, 500, 33, 77, bank1)
        loan2 = Loan(" Loan", 77.7, 77, 500, 33, 77, bank1)
        loan3 = Loan("House Loan", 77.7, 77, 500, 33, 77, bank1)


        bank1.add_loan_to_bank(loan)
        bank1.add_loan_to_bank(loan2)
        bank1.add_loan_to_bank(loan3)

        user.append_loans_list(loan)
        user.append_loans_list(loan2)
        user.append_loans_list(loan3)


        bank1.transfer_loans(user,bank2)

        for entity in user.get_loan_list():
            assert entity in bank2.get_loan_list()

    def test_transfer_balance(self):
        """
        Ensures bank1 is not associated with user anymore and transfers to bank 2
        :return:
        """
        bank1 = Bank("NFCU", "Credit Union", 35)
        bank2 = Bank("Bank of America", "Retail", 100)
        user = User("reid@uri.edu", "reidm77", "Reid ", "Morin", "password")

        bank1.add_user_to_bank(user)
        bank1.transfer_balance(user,bank2)

        assert user in bank2.get_user_list()
