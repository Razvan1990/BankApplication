import os
from helper import constants


class Helper:

    def print_bank_operation(self):
        x = int(input("Please introduce your option "))
        while x<0 or x >5:
            print("Option does not exist. Please repeat action")
            x = int(input(""))
        return x

    def ask_certainty_operation(self, name_operation):
        print('''Press "enter" if you would like to continue operation ''' + name_operation)
        print('''Type "back" if you would like to cancel operation '''+name_operation )

    def modify_bank_details(self, dictionary_full):
        counter_values = 0
        file_new =""
        os.chdir(constants.OUTPUT_PATH)
        dict_values = list(dictionary_full.values())
        for value in dict_values:
            for value_list in value:
                counter_values+=1
            break
        for x in range(0, counter_values):
            for key in dictionary_full:
                file_new+=key+":"+str(dictionary_full[key][x])+'\n'
        f = open(os.path.join(constants.OUTPUT_PATH, constants.FILENAME), mode ='w', encoding="utf-8")
        f.write(file_new)

    def create_receipt_file(self,word):
        os.chdir(constants.OUTPUT_PATH)
        new_file = os.path.join(constants.OUTPUT_PATH, constants.OUTPUT_FILENAME)
        with open (new_file, mode="w", encoding="utf-8") as f:
            f.write(word)
        print("Receipt is available here {}".format(new_file))
        os.system(new_file)

    def check_amount_value(self, amount_introduced, amount_available):
        cause =0
        is_10_multiple = amount_introduced%10
        if amount_introduced<10:
           cause =1
        elif amount_introduced>5000:
            cause=2
        elif is_10_multiple!=0:
            cause =3
        elif self.check_retreat_amount(amount_introduced, amount_available):
            cause = 4
        return cause

    def check_retreat_amount(self, value1, value2):
        return value1>value2

    def check_if_pin_has_just_digits(self, pin_introduced_new):
        return pin_introduced_new.isnumeric()


    #define here a function which creates a dictionary with the details for which we have the pin
    def check_PIN_card(self, dictionary_bank):
        working_dict ={}
        index_list =-1
        is_correct_pin = True
        counter_errors =0

        while(is_correct_pin):
            if (counter_errors > 2):
               raise SystemError("Too many attempts to access the card. Please contact the bank!")
            print("Please enter your pin number")
            print("____")
            x =(input(""))
            for key in dictionary_bank:
                if key=="PIN":
                    for pin_number in dictionary_bank[key]:
                        if x == pin_number:
                            #get the index of the pin in the list to create dictionary for that person
                            index_list = dictionary_bank[key].index(pin_number)
                            is_correct_pin = False
            if(index_list ==-1):
                counter_errors+=1
                if counter_errors<3:
                    print("PIN number incorrect. Please re-type the pin number")
            else:
                for key in dictionary_bank:
                    working_dict.update({key:dictionary_bank[key][index_list]})
        print("Hello ", working_dict["NUME"])
        return working_dict

