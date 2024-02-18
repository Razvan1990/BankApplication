import datetime
import tkinter

from helper import constants
from helper.helper_things import Helper
from operations.bank_reader import BankReader
from tkinter import messagebox
from tkinter import *


class BankOperations:

    def __init__(self):
        self.helper_things = Helper()
        self.banker = BankReader()

    def change_pin_number(self, dictionary_full, dictionary_client, new_pin, input_value):
        global key
        global new_pin_conversed
        if len(new_pin) != 4:
            messagebox.showerror("PIN INVALID", "PIN must have 4 numbers. Try again")
            return
        elif not self.helper_things.check_if_pin_has_just_digits(new_pin):
            messagebox.showerror("PIN INVALID", "PIN must contain just digits. Make sure to add digits")
            return
        elif self.helper_things.check_allowed_pin(dictionary_full, dictionary_client, new_pin):
            messagebox.showerror("PIN INVALID",
                                 "Pin is already used on another of your cards. Please type a different pin")
            return
        elif new_pin == dictionary_client[constants.CARD_INFO[0]]:
            messagebox.showerror("PIN INVALID", "PIN number must be different than the original one")
            return
        for key in dictionary_client:
            if key == constants.CARD_INFO[0]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                    if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                        if not self.helper_things.card_bank(dictionary_client):
                            messagebox.showinfo("TAX", "Operation is 1 leu")
                            dictionary_full[key][index] = new_pin
                            dictionary_client[key] = new_pin
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
        messagebox.showinfo("PIN CHANGED", "PIN number has been successfully changed")
        input_value.delete(0, END)
        input_value["state"] = tkinter.DISABLED
        return dictionary_client

    def cash_interrogation(self, dictionary_full, dictionary_client):
        for key in dictionary_client:
            if key == constants.CARD_INFO[2]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                    if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                        if not self.helper_things.card_bank(dictionary_client):
                            messagebox.showinfo("TAX", "Operation is 1 leu")
                            sum_available_string = dictionary_full[constants.CARD_INFO[2]][index]
                            sum_available = int(sum_available_string)
                            dictionary_client[constants.CARD_INFO[2]] = str(sum_available - constants.TAXES[0])
                            dictionary_full[constants.CARD_INFO[2]][index] = str(sum_available - constants.TAXES[0])
                            # print("Your current amount is {}".format(dictionary_client[key]))
                            self.helper_things.modify_bank_details(dictionary_full)
                            break
                        else:
                            # print("Your current amount is {}".format(dictionary_client[key]))
                            break

    def add_cash(self, dictionary_full, dictionary_client, *args):
        '''
        We use *args because we need to appeal the function if we enter from gui a different sum
        In order to not create 2 functions, if a button is selected just a single argument is used.
        Otherwise, we will need the input value entered by the user
        :param dictionary_full:
        :param dictionary_client:
        :param args:
        :return: the updated dictionary
        '''
        result = self.helper_things.choose_amount(args[0], 1, 2, 3, 4, 5, 6, 7)
        if result == 7:
            constants.DICTIONARY_VALUES[result] = int(args[1])  # in this case will be user_input.get()
        selected_amount = constants.DICTIONARY_VALUES[result]
        available_amount_string = dictionary_client[constants.CARD_INFO[2]]
        available_amount = int(available_amount_string)
        not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
        while not_ok_amount_cause == 1 or not_ok_amount_cause == 2 or not_ok_amount_cause == 3:
            if not_ok_amount_cause == 1:
                messagebox.showerror("INVALID VALUE", "Please introduce a value greater than 10 RON")
                return
            elif not_ok_amount_cause == 2:
                messagebox.showerror("INVALID VALUE", "Sum is too big. Introduce a smaller amount")
                return
            elif not_ok_amount_cause == 3:
                messagebox.showerror("INVALID VALUE", "Please introduce a multiple of 10")
                return
        for key in dictionary_client:
            if key == constants.CARD_INFO[2]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                    if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                        if not self.helper_things.card_bank(dictionary_client):
                            messagebox.showinfo("TAX", "Operation is 2 lei")
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
        messagebox.showinfo("OPERATION SUCCESSFUL", "The selected amount has been added to your balance")
        if result == 7:
            args[2].delete(0, END)
            args[2]["state"] = tkinter.DISABLED
        return dictionary_client

    def retreat_cash(self, dictionary_full, dictionary_client, *args):
        '''
               We use *args because we need to appeal the function if we enter from gui a different sum
               In order to not create 2 functions, if a button is selected just a single argument is used.
               Otherwise, we will need the input value entered by the user
               :param dictionary_full:
               :param dictionary_client:
               :param args:
               :return: the updated dictionary
         '''

        result = self.helper_things.choose_amount(args[0], 1, 2, 3, 4, 5, 6, 7)
        if result == 7:
            constants.DICTIONARY_VALUES[result] = int(args[1])
        available_amount_string = dictionary_client[constants.CARD_INFO[2]]
        available_amount = int(available_amount_string)
        selected_amount = constants.DICTIONARY_VALUES[result]
        not_ok_amount_cause = self.helper_things.check_amount_value(selected_amount, available_amount)
        while not_ok_amount_cause == 1 or not_ok_amount_cause == 2 or not_ok_amount_cause == 3 or not_ok_amount_cause == 4:
            if not_ok_amount_cause == 1:
                messagebox.showerror("INVALID VALUE", "Please introduce a value greater than 10 RON")
                return
            elif not_ok_amount_cause == 2:
                messagebox.showerror("INVALID VALUE", "Sum is too big. Introduce a smaller amount")
                return
            elif not_ok_amount_cause == 3:
                messagebox.showerror("INVALID VALUE", "Please introduce a multiple of 10")
                return
            elif not_ok_amount_cause == 4:
                message_max_sum = "Insufficient funds! Maximum to retreat is {}".format(available_amount)
                messagebox.showerror("INVALID VALUE", message=message_max_sum)
                return
        for key in dictionary_client:
            if key == constants.CARD_INFO[2]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                    if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                        if not self.helper_things.card_bank(dictionary_client):
                            messagebox.showinfo("TAX", "Operation is 2 lei")
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
        messagebox.showinfo("OPERATION SUCCESSFUL", "Please collect the cash from the slot")
        if result == 7:
            args[2].delete(0, END)
            args[2]["state"] = tkinter.DISABLED
        return dictionary_client

    def get_receipt(self, dictionary_full, client_dictionary):
        available_amount_string = client_dictionary[constants.CARD_INFO[2]]
        available_amount = int(available_amount_string)
        result_dict = ""
        masked_result_pin = ""
        masked_result_card_number = ""
        visible_account_number1 = ""
        visible_account_number2 = ""
        masked_result_account_number1 = ""
        masked_result_account_number2 = ""
        # self.helper_things.ask_certainty_operation("retreat cash")
        if not self.helper_things.card_bank(client_dictionary):
            for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                if client_dictionary[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                    messagebox.showinfo("TAX", "Operation is 1 leu")
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
                visible_account_number1 = account_number_trimed[4:8]
                visible_account_number2 = account_number_trimed[-4:]
                break
        for i in range(0, 4):
            masked_result_account_number1 += "X"
        for i in range(0, 13):
            masked_result_account_number2 += "X"
        masked_result_account_number = masked_result_account_number1 + visible_account_number1 + masked_result_account_number2 + visible_account_number2
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
        return client_dictionary

    def transfer_money_accounts(self, dictionary_full, dictionary_client, account_number, introduced_amount_transfer,
                                *args):
        recipient_dict = {}
        index = -1
        messagebox.showinfo("TAX", "Operation is 5 lei")
        available_amount_string = dictionary_client[constants.CARD_INFO[2]]
        available_amount = int(available_amount_string)
        is_ok_account_number = self.helper_things.check_account_number(account_number, dictionary_full)[0]
        while is_ok_account_number != 0:
            if is_ok_account_number == 1:
                messagebox.showerror("ACCOUNT INVALID",
                                     "Account number should contain 24 characters\n Please verify and type again")
                return
            elif is_ok_account_number == 2:
                messagebox.showerror("ACCOUNT INVALID",
                                     "Account number is invalid or does not exist.\n Please verify and type again")
                return
        index = self.helper_things.check_account_number(account_number, dictionary_full)[1]
        for key in dictionary_full:
            recipient_dict.update({key: dictionary_full[key][index]})
        if available_amount - int(introduced_amount_transfer) < 0:
            messagebox.showerror("AMOUNT UNAVAILABLE",
                                 "You do not have the necessary amount on your account to transfer this sum.\n Choose another sum")
            return
        if int(introduced_amount_transfer) > 5000:
            messagebox.showerror("AMOUNT TOO BIG",
                                 "The transfer amount is too big for ATM operations.\n Choose another sum or make the transfer at your bank")
            return
        # make necessary updates in balance
        dictionary_client[constants.CARD_INFO[2]] = str(
            available_amount - constants.TAXES[2] - int(introduced_amount_transfer))
        receipient_amount = int(recipient_dict[constants.CARD_INFO[2]])
        dictionary_full[constants.CARD_INFO[2]][index] = str(receipient_amount + int(introduced_amount_transfer))
        for key in dictionary_full:
            if key == constants.CARD_INFO[5]:
                for value in dictionary_full[key]:
                    if value == dictionary_client[constants.CARD_INFO[5]]:
                        index_client = dictionary_full[key].index(value)
                        dictionary_full[constants.CARD_INFO[2]][index_client] = dictionary_client[
                            constants.CARD_INFO[2]]
        messagebox.showinfo("TRANSFER", "Transferring......\nTransfer successfully!")
        self.helper_things.modify_bank_details(dictionary_full)
        args[0].delete(0, END)
        args[1].delete(0, END)
        args[0]["state"] = tkinter.DISABLED
        args[1]["state"] = tkinter.DISABLED
        return dictionary_client

    def pay_bills(self, dictionary_full, dictionary_client, *args):
        if args[2] == 1:
            self.helper_things.pay_eon_bill(args[2], dictionary_client, dictionary_full, args[0], args[3], args[1],
                                            args[4], args[5], args[6])
        elif args[2] == 2:
            self.helper_things.pay_eon_bill(args[2], dictionary_client, dictionary_full, args[0], args[3], args[1],
                                            args[4], args[5], args[6])
        elif args[2] == 3:
            self.helper_things.pay_other_things(args[2], dictionary_client, dictionary_full, args[0], args[1], args[4],
                                                args[5])
        elif args[2] == 4:
            self.helper_things.pay_other_things(args[2], dictionary_client, dictionary_full, args[0], args[1], args[4],
                                                args[5])
        return dictionary_client

    def transfer_money_abroad(self, dictionary_full, dictionary_client, input_iban_number, input_amount_transfer,
                              option_currency, *args):
        list_accounts = self.banker.get_account_numbers()
        input_iban_number_computed = self.helper_things.compute_account_number(input_iban_number)
        is_raifaissen = self.helper_things.card_bank(dictionary_client)
        if is_raifaissen:
            messagebox.showinfo("TAX", "Operation is 10 RON")
        else:
            messagebox.showinfo("TAX", "Operation is 13 RON")
        if len(input_iban_number) != 24:
            messagebox.showerror("ACCOUNT INVALID",
                                 "Account number should contain 24 characters\nPlease verify and type again")
            return
        elif input_iban_number_computed not in list_accounts:
            messagebox.showerror("ACCOUNT INVALID",
                                 "Account number is invalid or does not exist.\nPlease verify and type again")
            return
        available_amount = int(dictionary_client[constants.CARD_INFO[2]])
        if int(available_amount) - int(input_amount_transfer) < 0:
            messagebox.showerror("AMOUNT UNAVAILABLE",
                                 "You do not have the necessary amount on your account to transfer this sum.\nChoose another sum")
            return
        if int(input_amount_transfer) > 5000:
            messagebox.showerror("AMOUNT TOO BIG",
                                 "The transfer amount is too big for ATM operations.\nChoose another sum or make the transfer at your bank")
            return
        # make necessary updates in balance
        if not self.helper_things.card_bank(dictionary_client):
            for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                    dictionary_client[constants.CARD_INFO[2]] = str(
                        available_amount - (constants.TAXES[3] + 3) - int(input_amount_transfer))
                    dictionary_full[constants.CARD_INFO[2]][index] = str(
                        available_amount - (constants.TAXES[3] + 3) - int(input_amount_transfer))
                    self.helper_things.calculate_conversion_currency(option_currency, int(input_amount_transfer))
                    self.helper_things.modify_bank_details(dictionary_full)
                    messagebox.showinfo("TRANSFER", "Transferring......\nTransfer successfully!")
                    break
        else:
            for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                    dictionary_client[constants.CARD_INFO[2]] = str(
                        available_amount - constants.TAXES[3] - int(input_amount_transfer))
                    dictionary_full[constants.CARD_INFO[2]][index] = str(
                        available_amount - constants.TAXES[3] - int(input_amount_transfer))
                    self.helper_things.calculate_conversion_currency(option_currency, int(input_amount_transfer))
                    self.helper_things.modify_bank_details(dictionary_full)
                    messagebox.showinfo("TRANSFER", "Transferring......\nTransfer successfully!")
                    break
        args[0].delete(0, END)
        args[1].delete(0, END)
        args[0]["state"] = tkinter.DISABLED
        args[1]["state"] = tkinter.DISABLED
        return dictionary_client
