from computation.compute_elements import Computation
from gui.gui_creator import CreateWindowApp


def run_app():
    worker = Computation()
    gui = CreateWindowApp()
    #worker.manage_operations()
    gui.create_pin_gui()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_app()
