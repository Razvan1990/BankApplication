import os

from helper import constants


class BankReader:

    def __init__(self):
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
