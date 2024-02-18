import os
from datetime import datetime
import tkinter
from tkinter import messagebox

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
        if dictionary_client[constants.CARD_INFO[0]] == "0065" and dictionary_client[
            constants.CARD_INFO[1]] == "UNGUREANU IOAN RAZVAN":
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
        if option == args[6]:
            return args[6]

    def count_spaces(self, account_number):
        counter = 0
        for letter in account_number:
            if letter == " ":
                counter += 1
        return counter

    def compute_account_number(self, account_number):
        account_number_computed = ""
        counter = 0
        for i in range(0, len(account_number)):
            if counter % 4 == 0 and counter != 0:
                account_number_computed += " " + account_number[i]
                counter += 1
            else:
                account_number_computed += account_number[i]
                counter += 1
        return account_number_computed

    def check_account_number(self, account_number, dictionary_full):
        index = -1
        if len(str(account_number)) != 24:
            return 1, index
        account_number_spaces = self.compute_account_number(account_number)
        for key in dictionary_full:
            if key == constants.CARD_INFO[5]:
                for number in dictionary_full[constants.CARD_INFO[5]]:
                    if number == account_number_spaces:
                        index = dictionary_full[key].index(number)
        if index == -1:
            return 2, index
        return 0, index

    # from account number, but simpler to use in pay_bills method
    def check_IBAN_number(self, account_number, correct_number1, *args):
        if len(account_number) != 29:
            return 1
        elif args[1] == 3:
            if account_number != correct_number1:
                return 2
        elif args[1] == 4:
            if account_number != args[0]:
                return 2
        else:
            return 0

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
        messagebox.showinfo("RECEIPT", "Please take the receipt")
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

    def check_allowed_pin(self, dictionary_full, dictionary_client, introduced_pin_number):
        helper_dict = {}
        name_client = dictionary_client[constants.CARD_INFO[1]]
        bank_account_client = dictionary_client[constants.CARD_INFO[5]]
        for key in dictionary_full:
            if key == constants.CARD_INFO[1]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                    if name_client == value and bank_account_client != dictionary_full[constants.CARD_INFO[5]][index]:
                        helper_dict.update({constants.CARD_INFO[0]: dictionary_full[constants.CARD_INFO[0]][index]})
                        helper_dict.update({constants.CARD_INFO[1]: dictionary_full[constants.CARD_INFO[1]][index]})
                        helper_dict.update({constants.CARD_INFO[2]: dictionary_full[constants.CARD_INFO[2]][index]})
                        helper_dict.update({constants.CARD_INFO[3]: dictionary_full[constants.CARD_INFO[3]][index]})
                        helper_dict.update({constants.CARD_INFO[4]: dictionary_full[constants.CARD_INFO[4]][index]})
                        helper_dict.update({constants.CARD_INFO[5]: dictionary_full[constants.CARD_INFO[5]][index]})
                        if helper_dict[constants.CARD_INFO[0]] == introduced_pin_number:
                            return True
        return False

    def pay_eon_bill(self, option_client, dictionary_client, dictionary_full, client_number_inp, invoice_number_inp,
                     sum_inp, arg1, arg2, arg3):
        global dict_eon
        is_raifaissen = self.card_bank(dictionary_client)
        if is_raifaissen:
            messagebox.showinfo("TAX", "Operation is 2 RON")
        else:
            messagebox.showinfo("TAX", "Operation is 4 RON")
        if option_client == 1:
            dict_eon = self.bank_reader.create_billing_dict(constants.EON_ELEC)
        elif option_client == 2:
            dict_eon = self.bank_reader.create_billing_dict(constants.EON_GAZ)
        # make checks
        if len(client_number_inp) != 10 or not client_number_inp.isnumeric():
            message_error_client = "Client number must have 10 characters and must be just numeric"
            messagebox.showerror("INVALID CLIENT NUMBER", message=message_error_client)
            return
        if len(invoice_number_inp) != 10 or not invoice_number_inp.isnumeric():
            message_error_invoice = "Invoice number must have 10 characters and must be just numeric"
            messagebox.showerror("INVALID INVOICE NUMBER", message=message_error_invoice)
            return
        if not (client_number_inp in dict_eon and invoice_number_inp in dict_eon[client_number_inp]):
            message_error = "Client number or invoice number not in database.\nPlease recheck and type again"
            messagebox.showerror("INVALID DETAILS", message=message_error)
            return
        amount_available = dictionary_client[constants.CARD_INFO[2]]
        amount_available_int = int(amount_available)
        if amount_available_int - int(sum_inp) < 0:
            messagebox.showerror("AMOUNT UNAVAILABLE", "You do not have the necessary amount on your account for the payment.\nChoose another sum")
            return
        for key in dictionary_client:
            if key == constants.CARD_INFO[2]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                    if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][
                        index]:
                        if not is_raifaissen:
                            dictionary_client[constants.CARD_INFO[2]] = str(
                                amount_available_int - int(sum_inp) - constants.TAXES[1])
                            dictionary_full[constants.CARD_INFO[2]][index] = str(
                                amount_available_int - int(sum_inp) - 2 * constants.TAXES[1])
                            self.modify_bank_details(dictionary_full)
                            messagebox.showinfo("PAYMENT SUCCESSFULLY",
                                                "Transferring....Payment successfully!\nPlease take the receipt! ")
                            self.create_payment_bill_receipt(option_client, dictionary_client, int(sum_inp))
                            arg1.delete(0, tkinter.END)
                            arg2.delete(0, tkinter.END)
                            arg3.delete(0, tkinter.END)
                            arg1["state"] = tkinter.DISABLED
                            arg2["state"] = tkinter.DISABLED
                            arg3["state"] = tkinter.DISABLED
                            break
                        dictionary_client[constants.CARD_INFO[2]] = str(
                            amount_available_int - int(sum_inp) - constants.TAXES[1])
                        dictionary_full[constants.CARD_INFO[2]][index] = str(
                            amount_available_int - int(sum_inp) - constants.TAXES[1])
                        self.modify_bank_details(dictionary_full)
                        messagebox.showinfo("PAYMENT SUCCESSFULLY",
                                            "Transferring....Payment successfully!\nPlease take the receipt! ")
                        self.create_payment_bill_receipt(option_client, dictionary_client, int(sum_inp))
                        arg1.delete(0, tkinter.END)
                        arg2.delete(0, tkinter.END)
                        arg3.delete(0, tkinter.END)
                        arg1["state"] = tkinter.DISABLED
                        arg2["state"] = tkinter.DISABLED
                        arg3["state"] = tkinter.DISABLED
                        break
        return dictionary_client

    def pay_other_things(self, client_option, dictionary_client, dictionary_full, client_number_inp, inp_sum, arg1, arg2):
        global is_iban_ok
        counter_tries = 0
        is_raifaissen = self.card_bank(dictionary_client)
        if is_raifaissen:
            messagebox.showinfo("TAX", "Operation is 2 RON")
        else:
            messagebox.showinfo("TAX", "Operation is 4 RON")
        client_number_inp_computed = self.compute_account_number(client_number_inp)
        is_iban_ok = self.check_IBAN_number(client_number_inp_computed, constants.FLAT_BILLS, constants.BANK_ACCOUNT, client_option)
        if is_iban_ok == 1:
            message_error ="IBAN number should contain 24 digits.\nPlease verify again and reintroduce"
            messagebox.showerror("IBAN INVALID", message=message_error)
            return
        elif is_iban_ok == 2:
            message_error = "IBAN number is not the correct one for this transfer.\nPlease recheck"
            messagebox.showerror("IBAN INVALID", message=message_error)
            return
        amount_available = dictionary_client[constants.CARD_INFO[2]]
        amount_available_int = int(amount_available)
        if amount_available_int - int(inp_sum) < 0:
            messagebox.showerror("AMOUNT UNAVAILABLE",
                                 "You do not have the necessary amount on your account for the payment.\nChoose another sum")
            return
        for key in dictionary_client:
            if key == constants.CARD_INFO[2]:
                for index, value in enumerate(dictionary_full[constants.CARD_INFO[5]]):
                    if dictionary_client[constants.CARD_INFO[5]] == dictionary_full[constants.CARD_INFO[5]][index]:
                        if not is_raifaissen:
                            dictionary_client[constants.CARD_INFO[2]] = str(
                                amount_available_int - int(inp_sum) - constants.TAXES[1])
                            dictionary_full[constants.CARD_INFO[2]][index] = str(
                                amount_available_int - int(inp_sum) - 2 * constants.TAXES[1])
                            self.modify_bank_details(dictionary_full)
                            messagebox.showinfo("PAYMENT SUCCESSFULLY",
                                                "Transferring....Payment successfully!\nPlease take the receipt! ")
                            self.create_payment_bill_receipt(client_option, dictionary_client, int(inp_sum))
                            arg1.delete(0, tkinter.END)
                            arg2.delete(0, tkinter.END)
                            arg1["state"] = tkinter.DISABLED
                            arg2["state"] = tkinter.DISABLED
                            break
                        dictionary_client[constants.CARD_INFO[2]] = str(
                            amount_available_int - int(inp_sum) - constants.TAXES[1])
                        dictionary_full[constants.CARD_INFO[2]][index] = str(
                            amount_available_int - int(inp_sum) - constants.TAXES[1])
                        self.modify_bank_details(dictionary_full)
                        messagebox.showinfo("PAYMENT SUCCESSFULLY",
                                            "Transferring....Payment successfully!\nPlease take the receipt! ")
                        self.create_payment_bill_receipt(client_option, dictionary_client, int(inp_sum))
                        arg1.delete(0, tkinter.END)
                        arg2.delete(0, tkinter.END)
                        arg1["state"] = tkinter.DISABLED
                        arg2["state"] = tkinter.DISABLED
                        break

        return dictionary_client

    def create_payment_bill_receipt(self, client_option, dictionary_client, amount_paid):
        name_operation = ""
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
            name_operation = constants.BILLING_NAMES[0]
        elif client_option == 2:
            name_operation = constants.BILLING_NAMES[1]
        elif client_option == 3:
            name_operation = constants.BILLING_NAMES[2]
        elif client_option == 4:
            name_operation = constants.BILLING_NAMES[3]
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
        final_string = date_formated + '\n' + constants.NAME_BANK + '\n\n' + "CARD NUMBER:  " + masked_result_card_number + '\n' + "PLATA FACTURA" + '\n' + name_operation + '\n\n' + "SUMA\t\t" + str(
            amount_paid) + " RON" + "\n\n" + "####################" + "THANK YOU!" + "####################"
        file_path = constants.OUTPUT_PATH
        filename_trimed = constants.OUTPUT_FILENAME[:-4]
        filename_now = os.path.join(file_path, filename_trimed)
        filename_final = filename_now + "_" + name_operation + ".txt"
        with open(file=filename_final, mode="w", encoding="utf-8") as receipt_file:
            receipt_file.write(final_string)
        os.system(filename_final)

    def calculate_conversion_currency(self, user_option, amount_transferred):
        if user_option == 1:
            result = amount_transferred / constants.DICTIONARY_CURRENCY[constants.NAMES_CURRENCY[0]]
            message = "You are transferring {} {}".format(round(result, 2), constants.NAMES_CURRENCY_ABREVIATED[0])
            messagebox.showinfo("AMOUNT TO TRANSFER", message=message)
        if user_option == 2:
            result = amount_transferred / constants.DICTIONARY_CURRENCY[constants.NAMES_CURRENCY[1]]
            message = "You are transferring {} {}".format(round(result, 2), constants.NAMES_CURRENCY_ABREVIATED[1])
            messagebox.showinfo("AMOUNT TO TRANSFER", message=message)
        if user_option == 3:
            result = amount_transferred / constants.DICTIONARY_CURRENCY[constants.NAMES_CURRENCY[2]]
            message = "You are transferring {} {}".format(round(result, 2), constants.NAMES_CURRENCY_ABREVIATED[2])
            messagebox.showinfo("AMOUNT TO TRANSFER", message=message)
        if user_option == 4:
            result = amount_transferred / constants.DICTIONARY_CURRENCY[constants.NAMES_CURRENCY[3]]
            message = "You are transferring {} {}".format(round(result, 2), constants.NAMES_CURRENCY_ABREVIATED[3])
            messagebox.showinfo("AMOUNT TO TRANSFER", message=message)
        if user_option == 5:
            result = 100 * amount_transferred / constants.DICTIONARY_CURRENCY[constants.NAMES_CURRENCY[4]]
            message = "You are transferring {} {} (value is multiplied with *100)".format(round(result, 2),
                                                                                          constants.NAMES_CURRENCY_ABREVIATED[
                                                                                              4])
            messagebox.showinfo("AMOUNT TO TRANSFER", message=message)
