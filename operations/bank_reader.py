import os

from helper import constants


class BankReader:

    def __init__(self):
        self.list_accounts = []
        self.bank_dict = dict()
        self.list_split = list()

    def create_needed_dict(self):
        global bank_details
        try:
            helper_dict = {}
            file_path = constants.OUTPUT_PATH
            filename = constants.FILENAME
            os.chdir(file_path)
            bank_details = open(os.path.join(file_path, filename), mode="r", encoding="utf-8")
            list_lines = bank_details.readlines()
            for line in list_lines:
                temp_list = line.split(":")
                for temp_word in temp_list:
                    if temp_word.__contains__('\n'):
                        temp_word = temp_word[:-1]
                        self.list_split.append(temp_word)
                    else:
                        self.list_split.append(temp_word)
            # now we have a list of all words
            for i in range(0, len(self.list_split) - 1, 2):
                if self.list_split[i] in helper_dict:
                    combined_values = helper_dict[self.list_split[i]] + "_" + self.list_split[i + 1]
                    helper_dict.update({self.list_split[i]: combined_values})
                else:
                    helper_dict.update({self.list_split[i]: self.list_split[i + 1]})
            for key in helper_dict:
                temp_list = helper_dict[key].split("_")
                self.bank_dict.update({key: temp_list})
            return self.bank_dict
        except:
            raise FileNotFoundError
        finally:
            bank_details.close()

    def create_billing_dict(self, filename):
        global eon_details
        try:
            dict_client_bills_pair = {}
            list_numbers = []
            list_bills = []
            list_clients = []
            eon_details = open(filename, mode="r", encoding="utf-8")
            list_lines = eon_details.readlines()
            for line in list_lines:
                temp_list = line.split(":")
                for word in temp_list:
                    if word.__contains__('\n'):
                        word = word[:-1]
                        list_numbers.append(word)
                    else:
                        list_numbers.append(word)
            for i in range(0, len(list_numbers)):
                if i % 2 == 1:
                    list_individual_bill_number = list_numbers[i].split(" ")
                    list_bills.append(list_individual_bill_number)
            for i in range(0, len(list_numbers)):
                if i % 2 == 0:
                    list_clients.append(list_numbers[i])
            for i in range(0, len(list_clients)):
                dict_client_bills_pair.update({list_clients[i]: list_bills[i]})
            return dict_client_bills_pair
        except:
            raise FileNotFoundError
        finally:
            eon_details.close()

    def get_account_numbers(self):
        global file_accounts
        try:
            file_accounts = open(constants.ACC_NUMBERS, mode="r", encoding="utf-8")
            list_accounts_raw = file_accounts.readlines()
            for account in list_accounts_raw:
                if account.__contains__('\n'):
                    account = account[:-1]
                    self.list_accounts.append(account)
                else:
                    self.list_accounts.append(account)
            return self.list_accounts
        except:
            raise FileNotFoundError
        finally:
            file_accounts.close()
