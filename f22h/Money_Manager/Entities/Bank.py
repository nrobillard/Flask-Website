from __future__ import annotations


"""
The Banking class is meant to be used in collaboration with the Loan class. Each loan will be associated with a bank.
A loan can have one bank, but a bank may have many loans (many to one relationship). The utility of this class is that
a user can filter their loans by Banking. But we also want to establish the relationship so a user can easily transfer 
all their loans to another bank rather than one at a time. This way the user can properly track where their finances
belong. For example, if you moved from Capital One to NFCU, and you re-financed all your loans through them, 
rather than closing each loan in the app and re-opening it,we can switch the Banking object so we know where the users
 funds are allocated. 

 The Banking class also supports direct relationships with a User for similar ideas above. A user can indicate what bank
 their balance is in. This way they can track which bank has which funds. With a user-bank relationship, a user
 can have many banks and a bank can have many users (many to many). This can be useful so a user can transfer funds 
 between banks to have better knowledge of where their funds are located.
"""


class Bank:
    def __init__(self, bank_name: str, bank_type: str, overdraft_fee: float) -> None:
        """
        Initializes a bank object. This will also intialize two empty lists. One that stores the user objects
        associated with the given bank, as well as a list that stores the loan objects associated with the bank

        :param bank_name: The name pf the new bank
        :type bank_name: String

        :param bank_type: The type of bank (Credit union, commercial, retail, etc)
        :type bank_type: str

        :param overdraft_fee: Each bank has an overdraft fee that will be applied if a user spends more than their balance
        :type overdraft_fee: float

        :returns: None
        :raises ValueError: If either parameter is a blank string " "
        :raises ValueError: If overdraft fee is negative
        """

        if overdraft_fee < 0:
            raise ValueError("You can not have a negative overdraft fee")

        if bank_name == " " or bank_type == " ":
            raise ValueError("Parameters can not be blank. Please include a name")

        self._bank_name: str = bank_name
        self._bank_type: str = bank_type
        self._overdraft_fee: float = overdraft_fee
        from UserEntity import User
        from Loan import Loan
        self._user_list: [User] = []
        self._loan_list: [Loan] = []

    def get_overdraft_fee(self) -> float:
        """
        Gets the banks overdraft fee

        :returns: The banks overdraft fee
        """

        return self._overdraft_fee

    def set_overdraft_fee(self, new_fee) -> None:
        """
        Sets the new fee

        :param new_fee: The new fee
        :returns: None
        """

        if new_fee < 0:
            raise ValueError("Fee can not be less than 0")

        self._overdraft_fee = new_fee

    def get_bank_name(self) -> str:
        """
        Gets the banks name

        :returns: The banks name
        """

        return self._bank_name

    def set_bank_name(self, new_bank_name) -> None:
        """
        Sets the new bank name

        :param new_bank_name: The new desired name
        :returns: None
        """

        self._bank_name = new_bank_name

    def get_bank_type(self) -> str:
        """
        Gets the banks type

        :returns: The banks type
        """

        return self._bank_type

    def set_bank_type(self, new_bank_type) -> None:
        """
        Sets the new bank type

        :param new_bank_type: The new desired type
        :returns: None
        """

        self._bank_type = new_bank_type

    from UserEntity import User
    def get_user_list(self) -> [User]:

        """
        Gets all current users that have associated their balance with the current bank object

        :returns: The current user list associated with this bank
        """

        return self._user_list

    def add_user_to_bank(self, new_user: User) -> None:
        """
        Appends the user object to the list of users associated with this bank

        :param new_user: The user object that is now associated with this bank
        :returns: None
        """

        self._user_list.append(new_user)

    from Loan import Loan
    def get_loan_list(self) -> [Loan]:
        """
        Gets all current loans that have associated their balance with the current bank object

        :returns: The current loan list associated with this bank
        """

        return self._loan_list

    def add_loan_to_bank(self, new_loan: Loan) -> None:
        """
        Appends the loan object to the list of loans associated with this bank

        :param new_loan: The loan object that is now associated with this bank
        :returns: None
        """

        self._loan_list.append(new_loan)

    def get_all_user_balances(self) -> float:
        """
        This method can be used if we need to determine the balances of all users associated with this bank

        :returns: A floating point of all user balances
        """

        sum: float = 0

        for user in self._user_list:
            sum += user.get_current_balance()
            # Go through each user associated with the bank, and then add the current user objects balance to a
            # rolling sum. When the loop is over we will have all balances

        return sum

    def money_loaned_out(self) -> float:
        """
        Checks how much money a single bank has loaned out

        :returns: A floating point of an accumulation of all loan balances
        """

        sum: float = 0

        for loan in self._loan_list:
            sum += loan.get_balance()
            # Go through each loan associated with the bank, and then add the current loan objects balance to a
            # rolling sum. When the loop is over we will have all balances

        return sum

    def apply_over_draft_fee(self, current_user: User) -> None:
        """
        Whenever the user enters a negative balance, that means we have to apply the overdraft fee to their account
        This method should only be called after the transaction has been applied to their account and after checking
        if balance is negative

        :param current_user: User that the overdraft fee should apply too
        :raises ValueError: If users balance is not negative, it can not be overdrafted
        :returns: None
        """

        if current_user.get_current_balance() >= 0:
            raise ValueError("Users balance must be negative to over draft")

        # First get the user objects balance and then subtract the overdraft fee from it
        # Then set the users balance to the result of the above arithmetic
        current_balance: float = current_user.get_current_balance()
        balance_after_overdraft = current_balance - self._overdraft_fee
        current_user.set_current_balance(balance_after_overdraft)

    def forgive_all_loans(self) -> None:
        """
        This will set all loans balances that were loaned out by the bank to 0

        Use this method if a bank decides to forgive all of their users loans. This will be used if we implement
        a login for banks

        :returns: None
        """

        # Loop through each loan and set its current balance to 0
        for loan in self._loan_list:
            loan.set_balance(0)

    def add_balance_to_user(self, current_user: User, money_amount: float) -> None:
        """
        This will add a specified amount to a desired users balance. This will be used when logged in as a bank
        and viewing all of their current customers and their balances

        :param current_user: User whos balance will be affected
        :param money_amount: Amount to be added to users balance
        :raises ValueError: If money_amount is >= 0
        :returns: None
        """

        if money_amount < 0:
            raise ValueError("Amount must be greater than or equal 0")

        # get the current users balance, add the desired amount to that, then apply the new balance to the user
        current_balance: float = current_user.get_current_balance()
        new_balance: float = money_amount + current_balance
        current_user.set_current_balance(new_balance)

    def subtract_balance_from_user(self, current_user: User, money_amount: float) -> None:
        """
        This will subtract a specified amount to a desired users balance. This will be used when logged in as a bank
        and viewing all of their current customers and their balances. If the balance falls negative,
        we will apply the overdraft fee

        :param current_user: User whos balance will be affected
        :param money_amount: Amount to be subtracted to users balance
        :returns: None
        """

        # get the current users balance, subtract the desired amount from that, then apply the new balance to the user
        current_balance: float = current_user.get_current_balance()
        new_balance: float = current_balance - money_amount
        current_user.set_current_balance(new_balance)

        # If the above calculation made the user go into a negative balance, we have to apply an over draft fee
        if current_user.get_current_balance() < 0:
            self.apply_over_draft_fee(current_user)

    def transfer_loans(self, current_user: User, new_bank: Bank) -> None:
        """
        Transfers all the loans associated with one user from one bank to another bank
        :param current_user: User whose loans we are accessing
        :param new_bank: New bank that the loans will go to
        :returns: None
        """

        # Go through each loan associated with the user, and set the current loans bank to the new bank
        # Then remove the current loan object from the current banks loan list
        # Then add the current loan to the list of total loans in new bank
        for loan in current_user.get_loan_list():
            loan.set_bank(new_bank)
            self._loan_list.remove(loan)
            new_bank.add_loan_to_bank(loan)

    def transfer_balance(self, current_user: User, new_bank: Bank) -> None:
        """
        Transfers users balance from one bank object to another
        :param current_user: User whose balance we are accessing
        :param new_bank: New bank that the balance will go to
        :returns: None
        """

        # Sets the users associated bank to new bank
        current_user.set_bank(new_bank)
        # Remove user object from current instance of bank
        self._user_list.remove(current_user)
        # Add user object to new bank instance
        new_bank.add_user_to_bank(current_user)



