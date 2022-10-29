import time
import datetime
from helper import constants
from helper.helper_things import Helper
from operations.bank_reader import BankReader


class BankOperations:

    def __init__(self):
        self.helper_things = Helper()
        self.banker = BankReader()

    def change_PIN_number(self, dictionary_full, dictionary_client):
        global key
        global new_pin_conversed
        self.helper_things.ask_certainty_operation("change pin number")
        user_input = input("")
        if user_input == "":
            print("Enter new pin number")
            print("____")
            new_pin = input("")
            while len(new_pin) != 4:
                print("PIN must have 4 numbers. Try again")
                new_pin = input("")
            while not self.helper_things.check_if_pin_has_just_digits(new_pin):
                print("PIN must contain just digits. Make sure to add digits")
                new_pin = input()
                self.helper_things.check_if_pin_has_just_digits(new_pin)
            for key in dictionary_client:
                if key == constants.CARD_INFO[0]:
                    for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                        if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                            if self.helper_things.card_bank(dictionary_client):
                                dictionary_full[key][index] = new_pin
                                dictionary_client[key] = new_pin
                                print("Operation is 1 leu")
                                sum_available_string = dictionary_full[constants.CARD_INFO[2]][index]
                                sum_available = int(sum_available_string)
                                dictionary_client[constants.CARD_INFO[2]] = str(sum_available - constants.TAXES[0])
                                dictionary_full[constants.CARD_INFO[2]][index] = str(sum_available - constants.TAXES[0])
                                break
                            else:
                                dictionary_full[key][index] = new_pin
                                dictionary_client[key] = new_pin
                                break
                    # create new file
            self.helper_things.modify_bank_details(dictionary_full)
        elif user_input == "back":
            return dictionary_client
        return dictionary_client

    def cash_interogation(self, dictionary_full, dictionary_client):
        for key in dictionary_client:
            if key == constants.CARD_INFO[2]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                    if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                        if self.helper_things.card_bank(dictionary_client):
                            print("Operation is 1 leu")
                            sum_available_string = dictionary_full[constants.CARD_INFO[2]][index]
                            sum_available = int(sum_available_string)
                            dictionary_client[constants.CARD_INFO[2]] = str(sum_available - constants.TAXES[0])
                            dictionary_full[constants.CARD_INFO[2]][index] = str(sum_available - constants.TAXES[0])
                            print("Your current amount is {}".format(dictionary_client[key]))
                            self.helper_things.modify_bank_details(dictionary_full)
                            break
                        else:
                            print("Your current amount is {}".format(dictionary_client[key]))
                            break

    def add_cash(self, dictionary_full, dictionary_client):
        self.helper_things.ask_certainty_operation("add cash")
        user_input = input("")
        if user_input == "":
            print("1.10")
            print("2.50")
            print("3.100")
            print("4.200")
            print("5.500")
            print("6. Other sum")
            deposit_option = int(input(""))
            while deposit_option < 1 or deposit_option > 6:
                print("Not valid option. Choose again")
                deposit_option = int(input(""))
            result = self.helper_things.choose_amount(deposit_option, 1, 2, 3, 4, 5, 6)
            if result == 6:
                print("Enter the amount you want to add")
                x = int(input())
                constants.DICTIONARY_VALUES[result] = x
            selected_amount = constants.DICTIONARY_VALUES[result]
            available_amount_string = dictionary_client[constants.CARD_INFO[2]]
            available_amount = int(available_amount_string)
            not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
            while not_ok_amount_cause == 1 or not_ok_amount_cause == 2 or not_ok_amount_cause == 3:
                if not_ok_amount_cause == 1:
                    print("Please introduce a value greater than 10 RON")
                    x = int(input())
                    selected_amount = x
                    not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
                elif not_ok_amount_cause == 2:
                    print("Sum is too big. Introduce a smaller amount")
                    x = int(input())
                    selected_amount = x
                    not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
                elif not_ok_amount_cause == 3:
                    print("Please introduce a multiple of 10")
                    x = int(input())
                    selected_amount = x
                    not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
            for key in dictionary_client:
                if key == constants.CARD_INFO[2]:
                    for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                        if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                            if self.helper_things.card_bank(dictionary_client):
                                print("Operation is 2 lei")
                                new_amount = available_amount + selected_amount - constants.TAXES[1]
                                dictionary_full[key][index] = new_amount
                                dictionary_client[key] = new_amount
                                break
                            else:
                                new_amount = available_amount + selected_amount
                                dictionary_full[key][index] = new_amount
                                dictionary_client[key] = new_amount
                                break
            self.helper_things.modify_bank_details(dictionary_full)
        elif user_input == "back":
            return dictionary_client
        return dictionary_client

    def retreat_cash(self, dictionary_full, dictionary_client):
        self.helper_things.ask_certainty_operation("retreat cash")
        user_input = input("")
        if user_input == "":
            print("1.10")
            print("2.50")
            print("3.100")
            print("4.200")
            print("5.500")
            print("6. Other sum")
            depositOption = int(input(""))
            while depositOption < 1 or depositOption > 6:
                print("Not valid option. Choose again")
                depositOption = int(input(""))
            result = self.helper_things.choose_amount(depositOption, 1, 2, 3, 4, 5, 6)
            if result == 6:
                print("Enter the amount you want to retrieve")
                x = int(input())
                constants.DICTIONARY_VALUES[result] = x
            available_amount_string = dictionary_client[constants.CARD_INFO[2]]
            available_amount = int(available_amount_string)
            selected_amount = constants.DICTIONARY_VALUES[result]
            not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
            while not_ok_amount_cause == 1 or not_ok_amount_cause == 2 or not_ok_amount_cause == 3 or not_ok_amount_cause == 4:
                if not_ok_amount_cause == 1:
                    print("Please introduce a value greater than 10 RON")
                    x = int(input())
                    selected_amount = x
                    not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
                elif not_ok_amount_cause == 2:
                    print("Sum is too big. Introduce a smaller amount")
                    x = int(input())
                    selected_amount = x
                    not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
                elif not_ok_amount_cause == 3:
                    print("Please introduce a multiple of 10")
                    x = int(input())
                    selected_amount = x
                    not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
                elif not_ok_amount_cause == 4:
                    print("Not enough cash on card. Maximum to retreat is {}".format(available_amount))
                    print("1.10")
                    print("2.50")
                    print("3.100")
                    print("4.200")
                    print("5.500")
                    print("6. Other sum")
                    depositOption = int(input(""))
                    while depositOption < 1 or depositOption > 6:
                        print("Not valid option. Choose again")
                        depositOption = int(input(""))
                    result = self.helper_things.choose_amount(depositOption, 1, 2, 3, 4, 5, 6)
                    if result == 6:
                        print("Enter the amount you want to retrieve")
                        x = int(input())
                        constants.DICTIONARY_VALUES[result] = x
                    selected_amount = constants.DICTIONARY_VALUES[result]
                    not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
            for key in dictionary_client:
                if key == constants.CARD_INFO[2]:
                    for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                        if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                            if self.helper_things.card_bank(dictionary_client):
                                print("Operation is 2 lei")
                                new_amount = available_amount - selected_amount - constants.TAXES[1]
                                dictionary_full[key][index] = new_amount
                                dictionary_client[key] = new_amount
                                break
                            else:
                                new_amount = available_amount - selected_amount
                                dictionary_full[key][index] = new_amount
                                dictionary_client[key] = new_amount
                                break
            self.helper_things.modify_bank_details(dictionary_full)
        elif user_input == "back":
            return dictionary_client
        return dictionary_client

    def get_receipt(self, dictionary_full, client_dictionary):
        available_amount_string = client_dictionary[constants.CARD_INFO[2]]
        available_amount = int(available_amount_string)
        result_dict = ""
        masked_result_pin = ""
        masked_result_card_number = ""
        visibile_account_number1 = ""
        visibile_account_number2 = ""
        masked_result_account_number1 = ""
        masked_result_account_number2 = ""
        self.helper_things.ask_certainty_operation("retreat cash")
        user_input = input("")
        if user_input == "":
            if self.helper_things.card_bank(client_dictionary):
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                    if client_dictionary[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                        print("Operation is 1 leu")
                        new_amount = available_amount - constants.TAXES[0]
                        dictionary_full[constants.CARD_INFO[2]][index] = str(new_amount)
                        client_dictionary[constants.CARD_INFO[2]] = str(new_amount)
                        self.helper_things.modify_bank_details(dictionary_full)
                        break
            for key in client_dictionary:
                if key == constants.CARD_INFO[0]:
                    first_value = client_dictionary[constants.CARD_INFO[0]][0]
                    masked_result_pin += first_value
                    for i in range(1, len(client_dictionary[constants.CARD_INFO[0]])):
                        masked_result_pin += 'X'
            for key in client_dictionary:
                if key == constants.CARD_INFO[4]:
                    card_number = client_dictionary[constants.CARD_INFO[4]]
                    card_number_trimed = card_number.replace(" ", "")
                    visible_number = card_number_trimed[-4:]
                    for i in range(0, len(card_number_trimed) - 4):
                        masked_result_card_number += "X"
                    masked_result_card_number += visible_number
            for key in client_dictionary:
                if key == constants.CARD_INFO[5]:
                    account_number = client_dictionary[constants.CARD_INFO[5]]
                    account_number_trimed = account_number.replace(" ", "")
                    visibile_account_number1 = account_number_trimed[4:8]
                    visibile_account_number2 = account_number_trimed[-4:]
                    break
            for i in range(0, 4):
                masked_result_account_number1 += "X"
            for i in range(0, 13):
                masked_result_account_number2 += "X"
            masked_result_account_number = masked_result_account_number1 + visibile_account_number1 + masked_result_account_number2 + visibile_account_number2
            for key in client_dictionary:
                if key != constants.CARD_INFO[0] and key != constants.CARD_INFO[4] and key != constants.CARD_INFO[5]:
                    result_dict += key + ":" + str(client_dictionary[key]) + '\n'

            now = datetime.datetime.now()
            year = '{:02d}'.format(now.year)
            month = '{:02d}'.format(now.month)
            day = '{:02d}'.format(now.day)
            hour = '{:02d}'.format(now.hour)
            minute = '{:02d}'.format(now.minute)
            seconds = '{:02d}'.format(now.second)
            date_formated = day + "-" + month + "-" + year + "   " + hour + ":" + minute + ":" + seconds
            receipt_file = date_formated + '\n' + constants.NAME_BANK + '\n' + constants.CARD_INFO[
                0] + ":" + masked_result_pin + '\n' + result_dict + constants.CARD_INFO[
                               4] + ":" + masked_result_card_number + '\n' + constants.CARD_INFO[
                               5] + ":" + masked_result_account_number
            self.helper_things.create_receipt_file(receipt_file)
        elif user_input == "back":
            return client_dictionary
        return client_dictionary

    def transfer_money_accounts(self, dictionary_full, dictionary_client):
        recipient_dict = {}
        index = -1
        counter_tries = 0
        self.helper_things.ask_certainty_operation("transfer to another account")
        user_input = input("")
        if user_input == "":
            print("Operation is 5 lei")
            available_amount_string = dictionary_client[constants.CARD_INFO[2]]
            available_amount = int(available_amount_string)
            print("____ ____ ____ ____ ____ ____")
            account_number = input("Introduce the transfer account number ")
            is_ok_account_number = self.helper_things.check_account_number(account_number, dictionary_full)[0]
            while is_ok_account_number != 0:
                if is_ok_account_number == 1:
                    print("Please introduce a space between every 4 digits")
                    account_number = input("Introduce the transfer account number ")
                    is_ok_account_number = self.helper_things.check_account_number(account_number, dictionary_full)[0]
                elif is_ok_account_number == 2:
                    print("Account number should contain 24 digits. Please verify again and reintroduce")
                    account_number = input("Introduce the transfer account number ")
                    is_ok_account_number = self.helper_things.check_account_number(account_number, dictionary_full)[0]
                elif is_ok_account_number == 3:
                    print("Account number incorrect or does not exist. Please check again the account number")
                    account_number = input("Introduce the transfer account number ")
                    is_ok_account_number = self.helper_things.check_account_number(account_number, dictionary_full)[0]
            index = self.helper_things.check_account_number(account_number, dictionary_full)[1]
            for key in dictionary_full:
                recipient_dict.update({key: dictionary_full[key][index]})
            introduced_amount_transfer = int(input("Please introduce the amount to transfer"))
            while available_amount - introduced_amount_transfer < 0:
                print("You do not have the necessary amount on you account to transfer this sum. Choose another sum")
                counter_tries += 1
                if counter_tries > 2:
                    raise SystemError("Too many times tried to introduce unavailable transfer sum")
                introduced_amount_transfer = int(input(""))
            while introduced_amount_transfer > 5000:
                print(
                    "Amount is to large to transfer from ATM. Please go to your bank for values bigger than 5000 RON or re-introduce sum")
                print("1.Cancel operation")
                print("2. Introduce another sum")
                option = int(input(""))
                while option != 1 and option != 2:
                    print("Not a correct option. Re-introduce")
                    option = int(input(""))
                if option == 1:
                    return dictionary_client
                else:
                    introduced_amount_transfer = int(input(""))
            # make necessary updates in balance
            dictionary_client[constants.CARD_INFO[2]] = str(
                available_amount - constants.TAXES[2] - introduced_amount_transfer)
            receipient_amount = int(recipient_dict[constants.CARD_INFO[2]])
            dictionary_full[constants.CARD_INFO[2]][index] = str(receipient_amount + introduced_amount_transfer)
            for key in dictionary_full:
                if key == constants.CARD_INFO[5]:
                    for value in dictionary_full[key]:
                        if value == dictionary_client[constants.CARD_INFO[5]]:
                            index_client = dictionary_full[key].index(value)
                            dictionary_full[constants.CARD_INFO[2]][index_client] = dictionary_client[
                                constants.CARD_INFO[2]]
            print("Transferring...")
            time.sleep(3)
            print("Transfer success")
            self.helper_things.modify_bank_details(dictionary_full)
            return dictionary_client
        elif user_input == "back":
            return dictionary_client
        return dictionary_client

    def pay_bills(self, dictionary_full, dictionary_client):
        self.helper_things.ask_certainty_operation("pay bills")
        user_input = input("")
        if user_input == "":
            print("1.EON Electricitate")
            print("2.EON Gaze")
            print("3.Intretinere punct termic 1 Gura Humorului")
            print("4.Rata banca")
            option_client = int(input(""))
            while option_client < 1 or option_client > 4:
                print("Not correct option")
                option_client = int(input(""))
            if option_client == 1:
                self.helper_things.pay_eon_bill(option_client, dictionary_client, dictionary_full)
            elif option_client == 2:
                self.helper_things.pay_eon_bill(option_client, dictionary_client, dictionary_full)
            elif option_client == 3:
                self.helper_things.pay_other_things(option_client, dictionary_client, dictionary_full)
            elif option_client == 4:
                self.helper_things.pay_other_things(option_client, dictionary_client, dictionary_full)
        elif user_input == "back":
            return dictionary_client

    def transfer_money_abroad(self, dictionary_full, dictionary_client):
        is_iban_ok = True
        counter_tries = 0
        list_accounts = self.banker.get_account_numbers()
        self.helper_things.ask_certainty_operation("transfer money abroad")
        user_input = input("")
        if user_input == "":
            print("1. Transfer euro [RON->EUR conversion]")
            print("2. Transfer dollars [RON->USD conversion]")
            print("3. Transfer pounds [RON ->GBP conversion]")
            print("4. Transfer swiss francs [RON->CHF] conversion")
            option = int(input(""))
            while option < 1 or option > 4:
                print("Not correct option. Choose again")
                option = int(input(""))
            is_raifaissen = self.helper_things.card_bank(dictionary_client)
            if is_raifaissen:
                print("Operation is 13 RON")
            else:
                print("Operation is 10 RON")
            time.sleep(1)
            print("Introduce bank IBAN number: ")
            print("____ ____ ____ ____ ____ ____")
            iban_number = input("")
            counter_spaces = self.helper_things.count_spaces(iban_number)
            while is_iban_ok:
                if constants.NUMBER_SPACES_ACCOUNT != counter_spaces:
                    print("Please introduce a space between every 4 digits")
                    iban_number = input("iban number: ")
                elif len(iban_number) != 29:
                    print("Account number should contain 24 digits. Please verify again and reintroduce")
                    iban_number = input("Iban number: ")
                elif iban_number not in list_accounts:
                    print("Account IBAN number not correct. Please very again")
                    iban_number = input("Iban number: ")
                else:
                    is_iban_ok = False
            available_amount = int(dictionary_client[constants.CARD_INFO[2]])
            introduced_amount_transfer = int(input("Please introduce the amount to transfer"))
            while available_amount - introduced_amount_transfer < 0:
                print("You do not have the necessary amount on you account to transfer this sum. Choose another sum")
                counter_tries += 1
                if counter_tries > 2:
                    raise SystemError("Too many times tried to introduce unavailable transfer sum")
                introduced_amount_transfer = int(input(""))
            while introduced_amount_transfer > 5000:
                print("Amount is to large to transfer from ATM. Please go to your bank for values bigger than 5000 RON or re-introduce sum")
                print("1.Cancel operation")
                print("2. Introduce another sum")
                option = int(input(""))
                while option != 1 and option != 2:
                    print("Not a correct option. Re-introduce")
                    option = int(input(""))
                if option == 1:
                    return dictionary_client
                else:
                    introduced_amount_transfer = int(input("Introduce sum"))
            if self.helper_things.card_bank(dictionary_client):
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                        if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                            dictionary_client[constants.CARD_INFO[2]] = str(available_amount - (constants.TAXES[3] + 3) - introduced_amount_transfer)
                            dictionary_full[constants.CARD_INFO[2]][index] = str(available_amount - (constants.TAXES[3] + 3) - introduced_amount_transfer)
                            print("Transferring...")
                            time.sleep(3)
                            print("Transfer success")
                            self.helper_things.calculate_conversion_currency(option,introduced_amount_transfer)
                            self.helper_things.modify_bank_details(dictionary_full)
                            break
            else:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                        if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                            dictionary_client[constants.CARD_INFO[2]] = str(available_amount - constants.TAXES[3]  - introduced_amount_transfer)
                            dictionary_full[constants.CARD_INFO[2]][index] = str(available_amount - constants.TAXES[3]  - introduced_amount_transfer)
                            print("Transferring...")
                            time.sleep(3)
                            print("Transfer success")
                            self.helper_things.calculate_conversion_currency(option, introduced_amount_transfer)
                            self.helper_things.modify_bank_details(dictionary_full)
                            break
        elif user_input=="back":
            return dictionary_client
        return dictionary_client

