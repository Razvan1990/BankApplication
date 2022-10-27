import os
import sys

from helper import constants


class Helper:

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
        if dictionary_client[constants.CARD_INFO[0]] != "0065" and dictionary_client[
            constants.CARD_INFO[1]] != "UNGUREANU IOAN RAZVAN":
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
    def check_PIN_card(self, dictionary_bank):
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
