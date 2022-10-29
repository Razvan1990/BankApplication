import time

from operations.bank_operations import BankOperations
from operations.bank_reader import BankReader
from helper.helper_things import Helper


class Computation:

    def __init__(self):
        self.reader = BankReader()
        self.banker = BankOperations()
        self.helper = Helper()

    def manage_operations(self):
        database_dictionary = self.reader.create_needed_dict()
        client_dictionary = self.helper.check_PIN_card(database_dictionary)
        while True:
            print("1. Sold interogation")
            print("2. Deposit cash")
            print("3. Retrieve cash")
            print("4. Change PIN number")
            print("5. Get receipt info")
            print("6. Acount cash transfer")
            print("7. Pay bills")
            print("8. Western union")
            print("9. Exit")
            x = int(input(""))
            while x < 0 or x > 9:
                print("Not a valid option on ATM")
                x = int(input(""))
            if x == 1:
                self.banker.cash_interogation(database_dictionary, client_dictionary)
                time.sleep(1)
            if x == 2:
                client_dictionary = self.banker.add_cash(database_dictionary, client_dictionary)
                time.sleep(1)
            if x == 3:
                client_dictionary = self.banker.retreat_cash(database_dictionary, client_dictionary)
                time.sleep(1)
            if x == 4:
                client_dictionary = self.banker.change_PIN_number(database_dictionary, client_dictionary)
                time.sleep(1)
            if x == 5:
                self.banker.get_receipt(database_dictionary, client_dictionary)
                time.sleep(1)
            if x == 6:
                self.banker.transfer_money_accounts(database_dictionary, client_dictionary)
                time.sleep(1)
            if x==7:
                self.banker.pay_bills(database_dictionary,client_dictionary)
                time.sleep(1)
            if x ==8:
                self.banker.transfer_money_abroad(database_dictionary,client_dictionary)
                time.sleep(1)
            if x == 9:
                break
