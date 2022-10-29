from helper import constants
from helper.helper_things import Helper
from operations.bank_reader import BankReader
from computation.compute_elements import Computation
from operations.bank_operations import BankOperations


def run_app():

    # bank_reader = BankReader()
    # bank_ops = BankOperations()
    # helping = Helper()
    # database_dictionary = bank_reader.create_needed_dict()
    # client_dictionary = helping.check_PIN_card(database_dictionary)
    # #bank_ops.pay_bills(database_dictionary, client_dictionary)
    # #bank_reader.create_billing_dict(constants.EON_ELEC)
    # bank_ops.transfer_money_abroad(database_dictionary,client_dictionary)
    worker = Computation()
    worker.manage_operations()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_app()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
