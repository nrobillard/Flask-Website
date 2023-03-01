from math import log
from Money_Manager.Entities.Recurring_Payments import RecurringPayment
import decimal


class Loan:
    """
    Class that handles Loans
    data includes loan name, monthly payment, loan balance, if it is a recurring payment
    """
    def __init__(self, loan_name: str, apr: float, monthly_payment: float, balance: float, minimum_payment: float,
                 loan_term: int) -> None:
        """
        initializes loan with parameters
        :param loan_name: title of loan
        :param apr: annual percentage rate
        :param monthly_payment: amount paid monthly
        :param balance:  loan balance
        :param minimum_payment: minimum due each month
        :param loan_term: how many years to pay off loan
        """
        # if apr < 0 or monthly_payment < 0 or balance < 0:
        # raise ValueError("Cannot have negative values for such inputs")

        # If no recurring payment
        self._loan_term: int = loan_term
        self._loan_name: str = loan_name
        self._apr: float = apr
        self._monthly_payment: float = monthly_payment
        self._balance: float = balance
        self._prev_balance: float = balance
        self._balance_history: [float] = [balance]
        self._valid_recurring_payment: bool = False
        self._recurring_payment = None
        self._minimum_payment = minimum_payment


    def set_loan_term(self, loan_term: int) -> None:
        """
        Sets the loan length
        :return:
        """
        self._loan_term = loan_term

    def get_loan_term(self) -> int:
        """
        Gets the loan length
        :Return Gets loan length
        """
        return self._loan_term

    def set_loan_name(self, loan_name: str) -> None:
        """
        Sets the loans name
        :return:
        """
        self._loan_name = loan_name

    def get_loan_name(self) -> str:
        """
        Gets the loans name
        :Return: Loan Name
        """
        return self._loan_name

    def set_apr(self, apr: float) -> None:
        """
        Sets the loans name
        :return:
        """
        self._apr = apr

    def get_apr(self) -> float:
        """
        Gets the apr
        :Return: APR
        """
        return self._apr

    def set_monthly_payment(self, monthly_payment: float) -> None:
        """
        Sets the monthly payment
        :return:
        """
        self._monthly_payment = monthly_payment

    def get_monthly_payment(self) -> float:
        """
        Gets the Monthly Payment
        :Return: Monthly Payment
        """
        return self._monthly_payment

    def set_minimum_payment(self, minimum_payment: float) -> None:
        """
        Sets the minimum payment
        :return:
        """
        self._minimum_payment = minimum_payment

    def get_minimum_payment(self) -> float:
        """
        Gets the Minimum Payment
        :Return: Minimum Payment
        """
        return self._minimum_payment

    def set_balance(self, balance: float) -> None:
        """
        Sets Balance
        :Return:
        """
        self._balance = balance

    def get_balance(self) -> float:
        """
        Gets balance
        :Return Balance
        """
        return self._balance

    def subtract_balance(self) -> None:
        """
        when user makes payment updates loan balacne
        :return:
        """
        self._balance -= self._monthly_payment

    def check_valid_recurring_payment(self) -> bool:
        return self._valid_recurring_payment

    def set_recurring_payment(self) -> None:
        """
        Enables the Loan to have a recurring payment option
        """

        self._recurring_payment: RecurringPayment = RecurringPayment(self._loan_name, self._monthly_payment, False)
        self._valid_recurring_payment = True

    def _calc_num_payment_left(self, monthly_payment: float) -> float:
        """
        Calculates the amount of payments left on the current loan in
        respect to the apr rate. Uses the formula N = [-log(1-(P/A)*r]/[log(1+r)]
        where N is the amount of payments left, P is the current amount balance, and r is the apr
        rate per month

        :return: How many more monthly payments required until loan is paid off
        """

        if monthly_payment < 0:
            raise ValueError("new monthly payment can not be negative")
        apr_rate_per_month: float = self._apr / 12
        payments_left: float = 1 - ((self._balance / monthly_payment) * apr_rate_per_month)
        apr_rate_per_month += 1

        negative_log: float = -1 * log(payments_left, 10)

        apr_rate_per_month = log(apr_rate_per_month, 10)

        return negative_log / apr_rate_per_month

    def change_monthly_payment(self, new_payment: float) -> None:
        """
        Changes the monthly payment amount depending on
        user input

        :param new_payment: new monthly payment
        """

        if new_payment < 0:
            raise ValueError("new_payment cannot be negative")

        if self._valid_recurring_payment:

            self._recurring_payment.set_amount(new_payment)
            self._monthly_payment = new_payment

        else:

            self._monthly_payment = new_payment

    def months_left(self) -> float:
        """
        Uses private method to calculate how many months left on payment of loan
        using current monthly payment

        :return: number of months left in loan
        """

        return self._calc_num_payment_left(self._monthly_payment)

    def estimated_months_left(self, input_monthly_payment: float) -> float:
        """
        Uses private method to calculate how many months left on payment of loan if
        the monthly payment were to change

        :param input_monthly_payment: new user input for changed loan payment
        :return:
        """

        return self._calc_num_payment_left(input_monthly_payment)

    def basic_loan_calc(self, loan_amount: float, loan_term: int, interest_rate: float, loan_name: str) -> int:

        """
        Uses private method to calculate how many months left on payment of loan

        :param loan_amount: new user input for loan amount
        :param loan_term: amount of years
        :param interest_rate: apr
        :param loan_name: title
        :return:
        """

        # 400 status code means bad response
        if float(loan_amount) < 0 or int(loan_term) < 0 or float(interest_rate) < 0 or len(loan_name) == 0: return 400

        loan_amount = float(loan_amount)
        loan_term = int(loan_term)
        interest_rate = float(interest_rate)

        r = interest_rate / 100

        monthly_payment = loan_amount * r * loan_term

        decimalValue = decimal.Decimal(monthly_payment)
        monthly_payment = decimalValue.quantize(decimal.Decimal('0.00'))

        if monthly_payment < 0:
            monthly_payment = 0
            return 400 # If user messes up, we dont want to display a negative number

        self.set_monthly_payment(float(monthly_payment))

        return 200
