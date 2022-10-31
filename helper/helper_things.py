import os
import sys
import time
from datetime import datetime

from helper import constants
from operations.bank_reader import BankReader


class Helper:

    def __init__(self):
        self.bank_reader = BankReader()

    def print_bank_operation(self):
        x = int(input("Please introduce your option "))
        while x < 0 or x > 5:
            print("Option does not exist. Please repeat action")
            x = int(input(""))
        return x

    def ask_certainty_operation(self, name_operation):
        print('''Press "enter" if you would like to continue operation ''' + name_operation)
        print('''Type "back" if you would like to cancel operation ''' + name_operation)

    def card_bank(self, dictionary_client):
        if dictionary_client[constants.CARD_INFO[0]] != "0065" and dictionary_client[constants.CARD_INFO[1]] != "UNGUREANU IOAN RAZVAN":
            return True
        else:
            return False

    def choose_amount(self, option, *args):
        if option == args[0]:
            return args[0]
        if option == args[1]:
            return args[1]
        if option == args[2]:
            return args[2]
        if option == args[3]:
            return args[3]
        if option == args[4]:
            return args[4]
        if option == args[5]:
            return args[5]

    def count_spaces(self, account_number):
        counter = 0
        for letter in account_number:
            if letter == " ":
                counter += 1
        return counter

    def check_account_number(self, account_number, dictionary_full):
        index = -1
        counter_spaces = self.count_spaces(account_number)
        if constants.NUMBER_SPACES_ACCOUNT != counter_spaces:
            return 1, index
        elif len(str(account_number)) != 29:
            return 2, index
        for key in dictionary_full:
            if key == constants.CARD_INFO[5]:
                for number in dictionary_full[constants.CARD_INFO[5]]:
                    if number == account_number:
                        index = dictionary_full[key].index(number)
        if index == -1:
            return 3, index
        return 0, index

    # from account number, but simpler to use in pay_bills method
    def check_IBAN_number(self, account_number, correct_number1, *args):
        counter_spaces = self.count_spaces(account_number)
        if constants.NUMBER_SPACES_ACCOUNT != counter_spaces:
            return 1
        elif len(account_number) != 29:
            return 2
        elif args[1] == 3:
            if account_number != correct_number1:
                return 3
        elif args[1] == 4:
            if account_number != args[0]:
                return 3
        else:
            return 0
        
     def check_allowed_pin(self, dictionary_full, dictionary_client, introduced_pin_number):
        helper_dict={}
        name_client = dictionary_client[constants.CARD_INFO[1]]
        bank_account_client = dictionary_client[constants.CARD_INFO[5]]
        for key in dictionary_full:
            if key == constants.CARD_INFO[1]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                    if name_client == value and bank_account_client!=dictionary_full[constants.CARD_INFO[5]][index]:
                        helper_dict.update({constants.CARD_INFO[0]:dictionary_full[constants.CARD_INFO[0]][index]})
                        helper_dict.update({constants.CARD_INFO[1]: dictionary_full[constants.CARD_INFO[1]][index]})
                        helper_dict.update({constants.CARD_INFO[2]: dictionary_full[constants.CARD_INFO[2]][index]})
                        helper_dict.update({constants.CARD_INFO[3]: dictionary_full[constants.CARD_INFO[3]][index]})
                        helper_dict.update({constants.CARD_INFO[4]: dictionary_full[constants.CARD_INFO[4]][index]})
                        helper_dict.update({constants.CARD_INFO[5]: dictionary_full[constants.CARD_INFO[5]][index]})
                        if helper_dict[constants.CARD_INFO[0]]==introduced_pin_number:
                            return True
        return False


    def modify_bank_details(self, dictionary_full):
        counter_values = 0
        file_new = ""
        os.chdir(constants.OUTPUT_PATH)
        dict_values = list(dictionary_full.values())
        for value in dict_values:
            for value_list in value:
                counter_values += 1
            break
        for x in range(0, counter_values):
            for key in dictionary_full:
                file_new += key + ":" + str(dictionary_full[key][x]) + '\n'
        f = open(os.path.join(constants.OUTPUT_PATH, constants.FILENAME), mode='w', encoding="utf-8")
        f.write(file_new)

    def create_receipt_file(self, word):
        os.chdir(constants.OUTPUT_PATH)
        new_file = os.path.join(constants.OUTPUT_PATH, constants.OUTPUT_FILENAME)
        with open(new_file, mode="w", encoding="utf-8") as f:
            f.write(word)
        print("Receipt is available here {}".format(new_file))
        os.system(new_file)

    def check_amount_value(self, amount_introduced, amount_available):
        cause = 0
        is_10_multiple = amount_introduced % 10
        if amount_introduced < 10:
            cause = 1
        elif amount_introduced > 5000:
            cause = 2
        elif is_10_multiple != 0:
            cause = 3
        elif self.check_retreat_amount(amount_introduced, amount_available):
            cause = 4
        return cause

    def check_retreat_amount(self, value1, value2):
        return value1 > value2

    def check_if_pin_has_just_digits(self, pin_introduced_new):
        return pin_introduced_new.isnumeric()

    # define here a function which creates a dictionary with the details for which we have the pin
    def check_pin_card(self, dictionary_bank):
        working_dict = {}
        index_list = -1
        is_correct_pin = True
        counter_errors = 0
        while is_correct_pin:
            if counter_errors > 2:
                raise SystemError("Too many attempts to access the card. Please contact the bank!")
            print("Please enter your pin number")
            print("____")
            x = (input(""))
            for key in dictionary_bank:
                if key == constants.CARD_INFO[0]:
                    for pin_number in dictionary_bank[key]:
                        if x == pin_number:
                            # get the index of the pin in the list to create dictionary for that person
                            index_list = dictionary_bank[key].index(pin_number)
                            is_correct_pin = False
            if index_list == -1:
                counter_errors += 1
                if counter_errors < 3:
                    print("PIN number incorrect. Please re-type the pin number")
            else:
                for key in dictionary_bank:
                    working_dict.update({key: dictionary_bank[key][index_list]})
        if self.card_bank(working_dict):
            print("Operations will be charged in regards with bank policies")
            print('''Press "enter" if you would like to continue or type "back" if you don't approve''')
            answer = input("")
            if answer == "":
                print("Hello ", working_dict[constants.CARD_INFO[1]])
                return working_dict
            elif answer == "back":
                sys.exit(0)
        else:
            print("Hello ", working_dict[constants.CARD_INFO[1]])
            return working_dict

    def pay_eon_bill(self, option_client, dictionary_client, dictionary_full):
        global dict_eon
        are_valid_numbers = True
        is_raifaissen = self.card_bank(dictionary_client)
        if is_raifaissen:
            print("Operation is 4 RON")
        else:
            print("Operation is 2 RON")
        time.sleep(1)
        if option_client == 1:
            dict_eon = self.bank_reader.create_billing_dict(constants.EON_ELEC)
        elif option_client == 2:
            dict_eon = self.bank_reader.create_billing_dict(constants.EON_GAZ)
        print("Introduce the client number")
        print("__________")
        client = input("")
        while len(client) != 10 or not client.isnumeric():
            print("Client number bill must have 10 characters and must be just numeric")
            client = input("")
        print("Introduce the bill number")
        print("__________")
        bill = input()
        while len(bill) != 10 or not bill.isnumeric():
            print("Bill number must have 10 characters and must be just numeric")
            bill = input("")
        while are_valid_numbers:
            if client in dict_eon and bill in dict_eon[client]:
                are_valid_numbers = False
                print("Enter the amount to pay")
                amount = int(input(""))
                amount_available = dictionary_client[constants.CARD_INFO[2]]
                amount_available_int = int(amount_available)
                while amount_available_int - amount < 0:
                    print("Not enough money on card")
                    print("Introduce a smaller sum or cancel operation by pressing back")
                    option2 = input("")
                    if option2 == "back":
                        return dictionary_client
                    else:
                        option2_int = int(option2)
                        amount = option2_int
                for key in dictionary_client:
                    if key == constants.CARD_INFO[2]:
                        for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                            if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                                if is_raifaissen:
                                    dictionary_client[constants.CARD_INFO[2]] = str(
                                        amount_available_int - amount - constants.TAXES[1])
                                    dictionary_full[constants.CARD_INFO[2]][index] = str(
                                        amount_available_int - amount - 2 * constants.TAXES[1])
                                    self.modify_bank_details(dictionary_full)
                                    self.create_payment_bill_receipt(option_client, dictionary_client, amount)
                                    break
                                dictionary_client[constants.CARD_INFO[2]] = str(
                                    amount_available_int - amount - constants.TAXES[1])
                                dictionary_full[constants.CARD_INFO[2]][index] = str(
                                    amount_available_int - amount - constants.TAXES[1])
                                self.modify_bank_details(dictionary_full)
                                self.create_payment_bill_receipt(option_client, dictionary_client, amount)
                                break
            else:
                print("Client number and/or bill number invalid.Please re-type again")
                print("__________")
                client = input("client number ")
                print("___________")
                bill = input("bill number")
        return dictionary_client

    def pay_other_things(self, client_option, dictionary_client, dictionary_full):
        global is_iban_ok
        counter_tries = 0
        is_raifaissen = self.card_bank(dictionary_client)
        if is_raifaissen:
            print("Operation is 4 RON")
        else:
            print("Operation is 2 RON")
        time.sleep(1)
        print("Introduce bank IBAN number")
        print("____ ____ ____ ____ ____ ____")
        iban_number = input("")
        is_iban_ok = self.check_IBAN_number(iban_number, constants.FLAT_BILLS, constants.BANK_ACCOUNT, client_option)
        while is_iban_ok == 1 or is_iban_ok == 2 or is_iban_ok == 3:
            if counter_tries > 3:
                print("Cancelling opeartion cause of too many tries...")
                return dictionary_client
            if is_iban_ok == 1:
                print("Please introduce a space between every 4 digits")
                iban_number = input("iban NUMBER ")
                is_iban_ok = self.check_IBAN_number(iban_number, constants.FLAT_BILLS, constants.BANK_ACCOUNT,
                                                    client_option)
                counter_tries += 1
            elif is_iban_ok == 2:
                print("IBAN number should contain 24 digits. Please verify again and reintroduce")
                iban_number = input(" iban NUMBER")
                is_iban_ok = self.check_IBAN_number(iban_number, constants.FLAT_BILLS, constants.BANK_ACCOUNT,
                                                    client_option)
                counter_tries += 1
            elif is_iban_ok == 3:
                print("IBAN number is not the correct one for this transfer. Please recheck")
                iban_number = input("iban NUMBER ")
                is_iban_ok = self.check_IBAN_number(iban_number, constants.FLAT_BILLS, constants.BANK_ACCOUNT,
                                                    client_option)
                counter_tries += 1
        print("Enter the amount to pay")
        amount = int(input(""))
        amount_available = dictionary_client[constants.CARD_INFO[2]]
        amount_available_int = int(amount_available)
        while amount_available_int - amount < 0:
            print("Not enough money on card")
            print("Introduce a smaller sum or cancel operation by pressing back")
            option2 = input("")
            if option2 == "back":
                return dictionary_client
            else:
                option2_int = int(option2)
                amount = option2_int
        for key in dictionary_client:
            if key == constants.CARD_INFO[2]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                    if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                        if is_raifaissen:
                            dictionary_client[constants.CARD_INFO[2]] = str(
                                amount_available_int - amount - constants.TAXES[1])
                            dictionary_full[constants.CARD_INFO[2]][index] = str(
                                amount_available_int - amount - 2 * constants.TAXES[1])
                            self.modify_bank_details(dictionary_full)
                            time.sleep(1)
                            self.create_payment_bill_receipt(client_option, dictionary_client, amount)
                            break
                        dictionary_client[constants.CARD_INFO[2]] = str(
                            amount_available_int - amount - constants.TAXES[1])
                        dictionary_full[constants.CARD_INFO[2]][index] = str(
                            amount_available_int - amount - constants.TAXES[1])
                        self.modify_bank_details(dictionary_full)
                        time.sleep(1)
                        self.create_payment_bill_receipt(client_option, dictionary_client, amount)
                        break

        return dictionary_client

    def create_payment_bill_receipt(self, client_option, dictionary_client, amount_paid):
        name_opeartion = ""
        masked_result_card_number = ""
        now = datetime.now()
        year = '{:02d}'.format(now.year)
        month = '{:02d}'.format(now.month)
        day = '{:02d}'.format(now.day)
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        seconds = '{:02d}'.format(now.second)
        date_formated = day + "-" + month + "-" + year + "   " + hour + ":" + minute + ":" + seconds
        if client_option == 1:
            name_opeartion = constants.BILLING_NAMES[0]
        elif client_option == 2:
            name_opeartion = constants.BILLING_NAMES[1]
        elif client_option == 3:
            name_opeartion = constants.BILLING_NAMES[2]
        elif client_option == 4:
            name_opeartion = constants.BILLING_NAMES[3]
        # get card_number
        for key in dictionary_client:
            if key == constants.CARD_INFO[4]:
                card_number = dictionary_client[constants.CARD_INFO[4]]
                card_number_trimed = card_number.replace(" ", "")
                visible_number = card_number_trimed[-4:]
                for i in range(0, len(card_number_trimed) - 4):
                    masked_result_card_number += "X"
                masked_result_card_number += visible_number
        # make string
        final_string = date_formated + '\n' + constants.NAME_BANK + '\n\n' + "CARD NUMBER:  " + masked_result_card_number + '\n' + "PLATA FACTURA" + '\n' + name_opeartion + '\n\n' + "SUMA\t\t" + str(
            amount_paid) + " RON" + "\n\n" + "####################" + "THANK YOU!" + "####################"
        file_path = constants.OUTPUT_PATH
        filename_trimed = constants.OUTPUT_FILENAME[:-4]
        filename_now = os.path.join(file_path, filename_trimed)
        filename_final = filename_now + "_" + name_opeartion + ".txt"
        with open(file=filename_final, mode="w", encoding="utf-8") as receipt_file:
            receipt_file.write(final_string)
        os.system(filename_final)

    def calculate_conversion_currency(self, user_option, amount_transfered):
        if user_option == 1:
            result = amount_transfered / constants.DICTIONARY_CURRENCY[constants.NAMES_CURRENCY[0]]
            print("You have transferred ", round(result, 2), end=" ")
            print(constants.NAMES_CURRENCY_ABREVIATED[0])
        if user_option == 2:
            result = amount_transfered / constants.DICTIONARY_CURRENCY[constants.NAMES_CURRENCY[1]]
            print("You have transferred ", round(result, 2), end=" ")
            print(constants.NAMES_CURRENCY_ABREVIATED[1])
        if user_option == 3:
            result = amount_transfered / constants.DICTIONARY_CURRENCY[constants.NAMES_CURRENCY[2]]
            print("You have transferred ", round(result, 2), end=" ")
            print(constants.NAMES_CURRENCY_ABREVIATED[2])
        if user_option == 4:
            result = amount_transfered / constants.DICTIONARY_CURRENCY[constants.NAMES_CURRENCY[3]]
            print("You have transferred ", round(result, 2), end=" ")
            print(constants.NAMES_CURRENCY_ABREVIATED[3])
