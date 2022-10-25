from computation.compute_elements import Computation
from operations.bank_reader import BankReader
from helper.helper_things import Helper
from operations.bank_operations import BankOperations


def run_app():
    worker = Computation()
    worker.manage_operations()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_app()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
