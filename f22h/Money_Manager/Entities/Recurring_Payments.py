from datetime import datetime


class RecurringPayment:
    """
    Class that handles recurring payments
    data include: Name of transaction, value of transaction, date it happens, and whether it adds or subtracts from balance
    methods include: methods to get and set all the data( name, amount, date, deposit/charge), and print the name, date, value, and type of transaction
    """

    def __init__(self, input_title: str, input_amount: float, input_type: bool) -> None:
        """
        Method to initialize all data values.

        :param input_title: name of recurrence
        :param input_amount: value of transaction each time
        :param input_type: True = deposit, false = charge
        """

        self._title: str = input_title
        self._date: datetime = datetime.now()
        self._curr_month: int = self._date.month
        self._curr_day: int = self._date.day

        self._prev_month: int = self._date.month
        self._amount: float = input_amount
        self._type: bool = input_type

    # Getter Functions
    def get_title(self) -> str:
        """
        method to get payment name

        :return: _title: name of recurring payment
        """

        return self._title

    def get_date(self) -> datetime:
        """
        method to get date the transaction happens on
        :return: _date: date of each month the transaction happens
        """
        return self._date

    def get_amount(self) -> float:
        """
        method to get value of recurring transaction

        :return: _amount: exact value of transaction
        """
        return self._amount

    def get_type(self) -> str:
        """
        method to get type of transaction

        :return: _type: True = deposit, false = charge
        """

        return "Deposit" if self._type else "Charge"

    # Setter Functions
    def _set_title(self, new_title: str) -> None:
        """
        method to set new title for transaction

        :param new_title:
        :return:
        """
        self._title = new_title

    def _set_date(self) -> None:  # Updates time
        """
        method to set the date for transaction

        :return:
        """
        self._date = datetime.now()
        self._curr_month = datetime.month
        self._curr_day = datetime.day

    def set_amount(self, new_amount: float) -> None:
        """
        method to set amount of the recurring transaction

        :param new_amount: new transaction amount
        :return:
        """
        self._amount = new_amount

    def _set_type(self, new_type: bool) -> None:
        """
        method to set transaction type(deposit/charge)

        :param new_type: True = deposit, false = charge
        :return:
        """
        self._type = new_type

    def update(self, title: str, input_amount: float, new_type: bool) -> None:
        """
        Function that updates the current private data of title, amount charged, date of recurrence, and type of
        recurrence depending on user input.

        :param title: If "title" is empty, it does not change the title, otherwise the title of the object is changed
        :param input_amount: If input amount is -1, the amount of the recurrence does not change, otherwise it does
        :param new_type: If true, it will swap the current type of the recurrence to the other.
        """

        if title != "":
            self._set_title(title)

        if input_amount != -1:
            self.set_amount(input_amount)

        self._set_date()

        if new_type:
            self._set_type(new_type)

    def check_month(self) -> bool:
        """
        Constantly checks if the current month overlaps with the next month on the same date, and if it does,
        affect the users balance.
        """

        return True if datetime.month == (self._curr_month + 1) and datetime.day == self._curr_day else False

    def print_all(self) -> None:
        """
        method to print name, date, amount, and type of transaction
        :return:
        """
        print(f' {self.get_title()} \n {self.get_date().month}/{self.get_date().day} \n {self.get_amount()} \n '
              f'{self.get_type()}')



