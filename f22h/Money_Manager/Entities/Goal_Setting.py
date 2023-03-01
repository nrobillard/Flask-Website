from Money_Manager.Entities.UserEntity import User
import decimal


class GoalSetting:
    """ This class is responsible for goal setting
    it has the account balance, the account holder's goal balance, and a name for the goal
    methods include getting the balance, getting goal amount, getting goal name, setting the balance, setting goal amount, setting goal name, and printing all the data
    """

    def __init__(self, balance: float, goal: float, goal_name: str) -> None:
        """
        method to define all variables data
        :param balance: account balance
        :param goal: goal amount
        :param goal_name: name for goal
        """

        self._balance = balance
        self._goal = goal
        self._goal_name = goal_name

    # Getters

    def get_balance(self) -> float:
        """
        method to get the balance amount
        :return: _balance: value of balance
        """
        return self._balance

    def get_goal(self) -> float:
        """
        method to get the value of the goal
        :return: _goal:  goal amount
        """
        return self._goal

    def get_goal_name(self) -> str:
        """
        method to get the name of the goal
        :return: _goal_name: name of goal
        """
        return self._goal_name

    # Setters

    def set_balance(self, new_balance: float) -> None:
        """
        method to set value for balance
        :param new_balance: new balance amount
        :return:
        """
        self._balance = new_balance

    def set_goal(self, new_goal: float) -> None:
        """
        method to set new goal amount
        :param new_goal: new value of goal
        :return:
        """
        self._goal = new_goal

    def set_goal_name(self, new_goal_name: str) -> None:
        """
        method to set new goal name
        :param new_goal_name: Name of goal
        :return:
        """
        self._goal_name = new_goal_name

    def print_func(self) -> None:
        """
        method to print out balance, goal, and goal name
        :return:
        """
        print(self._balance, self._goal, self._goal_name)

    def needs_budget(self) -> float:
        """
        method to create a budget for your needs
        :return needs budget:
        """
        current_bal = self._balance
        needs = current_bal * 0.5

        decimal_value = decimal.Decimal(needs)
        needs = decimal_value.quantize(decimal.Decimal('0.00'))

        return float(needs)

    def wants_budget(self) -> float:
        """
        method to create a budget for your wants
        :return wants budget:
        """
        current_bal = self._balance
        wants = current_bal * 0.3

        decimal_value = decimal.Decimal(wants)
        wants = decimal_value.quantize(decimal.Decimal('0.00'))

        return float(wants)

    def savings_budget(self) -> float:
        """
        method to create a budget for your wants
        :return savings budget:
        """
        current_bal = self._balance
        savings = current_bal * 0.2

        decimal_value = decimal.Decimal(savings)
        savings = decimal_value.quantize(decimal.Decimal('0.00'))

        return float(savings)
