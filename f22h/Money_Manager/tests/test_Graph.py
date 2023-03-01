from unittest import TestCase
from Money_Manager.Entities.Graph import Graph


class Test(TestCase):
    def test_date_to_string(self):
        date_list = [1012000, 3012000, 6012000, 12012000]
        compare_list = ['01012000', '03012000', '06012000', '12012000']
        self.assertListEqual(compare_list, Graph.date_to_string(date_list))

    def test_valid_balance_list(self):
        bal_list = [1000.0, 1200.0, 1500.0, 2000.0, 2500.0]
        self.assertTrue(Graph.valid_balance_list(balance_list=bal_list))

    def test_valid_balance_list_fail(self):
        bal_list = [1000.0, 1200.0, 1500.0, 2000.0, 'a']
        self.assertFalse(Graph.valid_balance_list(balance_list=bal_list))

    def test_generate_tic_list(self):
        bal_list = [1000.0, 1200.0, 1800.0, 2400.0, 5000.0]
        tick_list = [1000, 2000, 3000, 4000, 5000]
        self.assertListEqual(tick_list, Graph.generate_tic_list(balance_list=bal_list))

    def test_check_overdraft(self):
        bal_list = [3000.0, 4000.0, 1200.0, -300.0]
        self.assertTrue(Graph.check_overdraft(bal_list))
