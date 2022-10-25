import datetime
from helper import constants
from helper.helper_things import Helper

class BankOperations:

    def __init__(self):
        self.helperThings = Helper()

    def change_PIN_number(self, dictionary_full, dictionary_client):
        global key
        global new_pin_conversed
        self.helperThings.ask_certainty_operation("change pin number")
        user_input = input("")
        if user_input=="":
            print("Enter new pin number")
            print("____")
            new_pin = input("")
            while len(new_pin)!=4:
                print("PIN must have 4 numbers. Try again")
                new_pin = input("")
            while not self.helperThings.check_if_pin_has_just_digits(new_pin):
                print("PIN must contain just digits. Make sure to add digits")
                new_pin = input()
                self.helperThings.check_if_pin_has_just_digits(new_pin)
            for key in dictionary_client:
                if key ==constants.CARD_INFO[0]:
                    for index,value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                        if dictionary_client[constants.CARD_INFO[1]]==dictionary_full[constants.CARD_INFO[1]][index]:
                            dictionary_full[key][index]=new_pin
                            dictionary_client[key]= new_pin
                            break
                #create new file
            self.helperThings.modify_bank_details(dictionary_full)
        elif user_input=="back":
            return dictionary_client
        return dictionary_client


    def cash_interogation(self, dictionary_client):
        for key in dictionary_client:
            if key == constants.CARD_INFO[2]:
                print("Your current amount is {}". format(dictionary_client[key]))
                break

    def add_cash(self, dictionary_full, dictionary_client):
        self.helperThings.ask_certainty_operation("add cash")
        user_input = input("")
        if user_input == "":
            print("Enter the amount you want to add")
            x = int(input())
            available_amount_string = dictionary_client[constants.CARD_INFO[2]]
            available_amount = int(available_amount_string)
            not_ok_amount_cause = self.helperThings.check_amount_value(x, available_amount)
            while not_ok_amount_cause==1 or  not_ok_amount_cause==2 or  not_ok_amount_cause==3:
                if not_ok_amount_cause==1:
                    print("Please introduce a value greater than 10 RON")
                    x = int(input())
                    not_ok_amount_cause = self.helperThings.check_amount_value(x, available_amount)
                elif not_ok_amount_cause==2:
                    print("Sum is too big. Introduce a smaller amount")
                    x = int(input())
                    not_ok_amount_cause = self.helperThings.check_amount_value(x, available_amount)
                elif not_ok_amount_cause==3:
                    print("Please introduce a multiple of 10")
                    x = int(input())
                    not_ok_amount_cause = self.helperThings.check_amount_value(x, available_amount)
            for key in dictionary_client:
                if key ==constants.CARD_INFO[2]:
                    for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                        if dictionary_client[constants.CARD_INFO[1]]==dictionary_full[constants.CARD_INFO[1]][index]:
                            availableAmount = int(dictionary_client[key])
                            new_amount = availableAmount +x
                            dictionary_full[key][index]=new_amount
                            dictionary_client[key]=new_amount
                            break
            self.helperThings.modify_bank_details(dictionary_full)
        elif user_input=="back":
            return dictionary_client
        return dictionary_client

    def retreat_cash(self, dictionary_full, dictionary_client):
        self.helperThings.ask_certainty_operation("retreat cash")
        user_input = input("")
        if user_input == "":
            print("Enter the amount you want to retrieve")
            x = int(input())
            available_amount_string = dictionary_client[constants.CARD_INFO[2]]
            available_amount = int(available_amount_string)
            not_ok_amount_cause = self.helperThings.check_amount_value(x, available_amount)
            while not_ok_amount_cause==1 or  not_ok_amount_cause==2 or  not_ok_amount_cause==3 or not_ok_amount_cause==4:
                if not_ok_amount_cause==1:
                    print("Please introduce a value greater than 10 RON")
                    x = int(input())
                    not_ok_amount_cause = self.helperThings.check_amount_value(x, available_amount)
                elif not_ok_amount_cause==2:
                    print("Sum is too big. Introduce a smaller amount")
                    x = int(input())
                    not_ok_amount_cause = self.helperThings.check_amount_value(x, available_amount)
                elif not_ok_amount_cause==3:
                    print("Please introduce a multiple of 10")
                    x = int(input())
                    not_ok_amount_cause = self.helperThings.check_amount_value(x, available_amount)
                elif not_ok_amount_cause==4:
                    print("Not enough cash on card. Maximum to retreat is {}".format(available_amount))
                    x = int(input())
                    not_ok_amount_cause = self.helperThings.check_amount_value(x, available_amount)
            for key in dictionary_client:
                if key ==constants.CARD_INFO[2]:
                    for index, value in enumerate(dictionary_full[constants.CARD_INFO[1]]):
                        if dictionary_client[constants.CARD_INFO[1]]==dictionary_full[constants.CARD_INFO[1]][index]:
                            availableAmount = int(dictionary_client[key])
                            new_amount = availableAmount -x
                            dictionary_full[key][index]=new_amount
                            dictionary_client[key] = new_amount
                            break
            self.helperThings.modify_bank_details(dictionary_full)
        elif user_input=="back":
            return dictionary_client
        return dictionary_client

    def get_receipt(self, client_dictionary):
        result_dict =""; masked_result_pin=""; masked_result_card_number=""
        for key in client_dictionary:
            if key == constants.CARD_INFO[0]:
               first_value = client_dictionary[constants.CARD_INFO[0]][0]
               masked_result_pin+=first_value
               for i in range (1, len(client_dictionary[constants.CARD_INFO[0]])):
                   masked_result_pin +='X'
        for key in client_dictionary:
            if key == constants.CARD_INFO[4]:
                visible_number = client_dictionary[constants.CARD_INFO[4]][-5:-1]
                for i in range(0, len(client_dictionary[constants.CARD_INFO[4]])):
                    masked_result_card_number+="X"
                masked_result_card_number+=visible_number
        for key in client_dictionary:
            if key!=constants.CARD_INFO[0] and key!= constants.CARD_INFO[4]:
                result_dict+=key+":"+str(client_dictionary[key])+'\n'

        now = datetime.datetime.now()
        year = '{:02d}'.format(now.year)
        month = '{:02d}'.format(now.month)
        day = '{:02d}'.format(now.day)
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        seconds = '{:02d}'.format(now.second)
        date_formated = day+"-"+month+"-"+year+"   "+hour+":"+minute+":"+seconds
        receipt_file  = date_formated+'\n'+constants.NAME_BANK+'\n'+constants.CARD_INFO[0]+":"+masked_result_pin+'\n'+result_dict+constants.CARD_INFO[4]+":"+masked_result_card_number
        self.helperThings.create_receipt_file(receipt_file)















