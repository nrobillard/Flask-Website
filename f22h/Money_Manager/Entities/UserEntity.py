# from Money_Manager.Entities.Bank import Bank
from Money_Manager.Entities.Recurring_Payments import RecurringPayment
from Money_Manager.Entities.Loan import Loan
from datetime import datetime


class User:
    """
    class to represent a user
    methods to change balance and getters and setters for all data
    """

    def __init__(self, username: str, email: str, first_name: str, last_name: str, password: str) -> None:
        """
        method to initialize account data

        :param username: account username
        :param email: account holder's email
        :param first_name: Account holders first name
        :param last_name: account holders last name
        :param password: account password
        """
        self._username: str = username
        self._email: str = email
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._password: str = password
        self._current_balance: float = 0
        self._prev_balance: float = self._current_balance
        self._balance_list: [float] = []
        self._loan_list: [Loan] = []
        self._recurring_payment_list: [RecurringPayment] = []
        self._balance_list.append(self._current_balance)
        self._balance_list_date: [(int, int, int)] = []

    def get_current_balance(self) -> float:
        """
        method to get current account balance value

        :return: current account balance value
        """
        return self._current_balance

    def get_previous_balance(self) -> float:
        """
        method to get the account balance  value before the last transaction

        :return: the previous account balance value
        """
        return self._prev_balance

    def get_first_name(self) -> str:
        """
        method to get account holders first name

        :return: account owners first name
        """
        return self._first_name

    def get_last_name(self) -> str:
        """
        method to get account holders last name

        :return: account owners last name
        """
        return self._last_name

    def get_username(self) -> str:
        """
        method to get account username

        :return: account username
        """
        return self._username

    def get_password(self) -> str:
        """
        method to get account's password

        :return: account password
        """
        return self._password

    def get_email(self) -> str:
        """
        method to get account email

        :return: account email
        """
        return self._email

    def get_balance_list(self) -> [float]:
        """
        method to get list of previous balances

        :return: balance_list
        """
        return self._balance_list

    def get_list(self) -> [float]:
        """
        method to get list of previous balances

        :return: balance_list
        """
        return self._balance_list

    def get_balance_date(self) -> [(int, int, int)]:
        """
        method to get list of dates corresponding to previous balance list
        :return:
        """
        return self._balance_list_date

    def set_first_name(self, new_first: str) -> None:
        """
        set account holders first name

        :param new_first:
        :return:
        """
        self._first_name = new_first

    def set_last_name(self, new_last: str) -> None:
        """
        method to set account holders last name
        :param new_last: last name
        :return:
        """
        self._last_name = new_last

    def set_username(self, username: str) -> None:
        """
        set username

        :param username:
        :return:
        """
        self._username = username

    def set_password(self, password: str) -> None:
        """
        set password for account

        :param password:
        :return:
        """
        self._password = password

    def set_email(self, email: str) -> None:
        """
        set account email address

        :param email:
        :return:
        """
        self._email = email

    def set_balance_list(self, new_list: [float]) -> None:
        """
        set balance list

        :param new_list: balance list
        :return:
        """
        self._balance_list = new_list

    def subtract_balance(self, charge_amount: float) -> None:
        """
        method to represent withdrawal from account

        :param charge_amount: amount to be subtracted from balance
        :return:
        """
        self._prev_balance = self._current_balance
        self._current_balance -= charge_amount
        self._balance_list.append(self._current_balance)
        date = (datetime.now().month, datetime.now().day, datetime.now().year)

        self._balance_list_date.append(date)

    def add_balance(self, deposit_amount: float) -> None:
        """
        method to represent a deposit

        :param deposit_amount:
        :return:
        """
        self._prev_balance = self._current_balance
        self._current_balance += deposit_amount
        self._balance_list.append(self._current_balance)
        date = (datetime.now().month, datetime.now().day, datetime.now().year)
        self._balance_list_date.append(date)

    def check_loan(self) -> None:
        """
        checks to see if it is time for the loan to be paid
        if it is time subtract from account balance and loan balance
        :return:
        """
        for i in range(len(self._loan_list)):
            if not self._loan_list[i].check_valid_recurring_payment:
                break
            valid_date: bool = self._loan_list[i].check_month
            deposit: bool = self._loan_list[i].get_type

            if valid_date and deposit:
                self.subtract_balance(self._loan_list[i].get_amount)
                self._loan_list[i].subtract_balance()

    def check_recurring_payments(self) -> None:
        """
        check to see if it is time for a recurring balacne
        if it is updates account balance
        :return:
        """
        for i in range(len(self._recurring_payment_list)):
            valid_date: bool = self._recurring_payment_list[i].check_month
            deposit: bool = self._recurring_payment_list[i].get_type

            if valid_date and deposit:
                self.add_balance(self._recurring_payment_list[i].get_amount)

            if valid_date and not deposit:
                self.subtract_balance(self._recurring_payment_list[i].get_amount)

    def append_loans_list(self, new_loan: Loan) -> None:
        """
        method to set the loan list
        :param new_loan: new loans
        :return:
        """
        self._loan_list.append(new_loan)

    def append_recurring_payment_list(self, new_recurring_payment: RecurringPayment) -> None:
        """
        method to set the loan list
        :param new_recurring_payment: new recurring payment
        :return:
        """
        self._recurring_payment_list.append(new_recurring_payment)

    # def set_recurring_payment_list(self, new_list: ) -> None:
    #     """
    #     :param new_list: recurring payments
    #     :return:
    #     """
    #     self._recurring_payment_list.append(new_list)

    def get_loan_list(self) -> [Loan]:
        """
        "return: users loans
        """
        return self._loan_list

    def get_recurring_payment_list(self) -> [RecurringPayment]:
        """
        "return: users loans
        """
        return self._recurring_payment_list
