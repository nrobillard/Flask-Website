import matplotlib
from Money_Manager.Entities.UserEntity import User
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# Currently Not Functional

# Month, Day, Year
class Graph:
    def __init__(self):
        """
        Fetches data from User class and formats it into a dataframe with the balances and dates that can be accessed by Seaborn for graphing
        """
        bal_list = User.get_balance_list()
        date_list = User.get_balance_date()
        # Preparing and validating data to be graphed
        date_list = self.date_to_string(date_list)
        if self.valid_balance_list(bal_list):
            pass
        else:
            raise TypeError
        # Reshaping data to be formatted correctly to be graphed
        reshaped_data = []
        for i in range(len(bal_list)):
            reshaped_data.append([bal_list[i], date_list[i]])
        reshaped_data = np.array(reshaped_data)
        transactions_df = pd.DataFrame(reshaped_data, columns=['Balance', 'Transaction Date'])
        overdraft = self.check_overdraft()
        if overdraft:
            print("You have overdrafted in the past year")
        else:
            print("You have not overdrafted in the past year")
        self.over_time_plot()

    def over_time_plot(self) -> plt.savefig:
        """
        Creates the graph and sets tic marks to fit all the data
        :returns: Seaborn plot with transactions with dates from the past year
        """
        fig = plt.figure()
        fig.set_figwidth(len(self.bal_list))

        plt.title("Balance Over Time")
        plt.xlabel("Date")
        plt.ylabel("Balance ($)")
        plot = plt.plot(self.date_list, self.bal_list)
        # Returns plot as a jpg file
        plot_img = plt.savefig("balance_plot.jpg")
        return plot_img

    @staticmethod
    def check_overdraft(balance_list: [int]) -> bool:
        """
        Checks to see if the user has overdrafted their account in the past year
        :param balance_list: List of previous balances from the past year
        :returns: True if there is any value less than 0 indicating an overdraft or false if all numbers are positive
        """
        for i in balance_list:
            if i < 0:
                return True
        return False

    @staticmethod
    def date_to_string(date_list: [int]) -> [str]:
        """
        Converts all date values to strings to be used for graph
        :param date_list: List of all dates of transactions that occured in the past year
        :return date_string_list: Date list converted into strings in MMDDYYYY format
        """
        date_string_list = []
        for i in date_list:
            if len(str(i)) == 7:
                date_string_list.append('0' + str(i))
            else:
                date_string_list.append(str(i))
        for i in range(len(date_string_list)):
            date_string_list[i] = date_string_list[i[:2]] + '/' + date_string_list[i[2:4]] + '/' + date_string_list[
                i[4:]]
        return date_string_list

    @staticmethod
    def valid_balance_list(balance_list: [float]) -> bool:
        """
        Checks to make sure all values in balance list are floats
        :param balance_list: List of all balances from within the past year
        :return: True if all values are floats and false if there are any values that aren't floats
        """
        for i in balance_list:
            if type(i) != float:
                return False
        return True

    @staticmethod
    def generate_tic_list(balance_list: [float]) -> [int]:
        """
        Calculates the values for 5 tic marks total between the highest and lowest values
        :param balance_list: List of all balances from within the past year
        :return tic_list: List with the values for the 5 tic marks
        """
        tic = int((max(balance_list) - min(balance_list)) / 5)
        tic_list = [(min(balance_list) + (i * tic)) for i in range(0, 6)]
        return tic_list
