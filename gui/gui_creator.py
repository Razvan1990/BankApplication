import sys
import tkinter
from tkinter import *
import os
from operations.bank_operations import BankOperations
from operations.bank_reader import BankReader
from helper.helper_things import Helper
from tkinter import messagebox
import helper.constants


class CreateWindowApp:

    def __init__(self):
        self.bank_ops = BankOperations()
        self.bank_reader = BankReader()
        self.helper = Helper()
        self.bank_dictionary = self.bank_reader.create_needed_dict()
        self.counter_pin_errors = 0
        self.working_dict = dict()

    def center(self, win):
        """
        Centers a Tkinter window.
        :param win: The main window or Toplevel window to center.
        """
        win.update_idletasks()  # Ensure accurate geometry values
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width

        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width

        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2

        win.geometry(f"{width}x{height}+{x}+{y}")
        win.deiconify()

    def exit_app(self):
        root_operations_menu.quit()

    '''
    MAIN MENU OPERATIONS
    '''

    def create_operations_gui(self):
        global root_operations_menu
        global sold_interogation_button
        global deposit_cash_button
        global retrieve_cash_button
        global change_pin_number_button
        global receipt_info_button
        global account_cash_transfer
        global pay_bills_button
        global western_union_button
        global exit_button
        root_operations_menu = Tk()
        root_operations_menu.title("OPERATIONS")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        root_operations_menu.iconbitmap(image_ico)
        root_operations_menu.geometry("800x500")
        root_operations_menu["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(root_operations_menu, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"), bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="OPERATIONS",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # just need to put buttons on frame
        sold_interogation_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                          cursor="target", width=25, height=2, justify="left",
                                          text="SOLD INTEROGATION", command=self.check_sold)
        deposit_cash_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                     cursor="target", width=25, height=2, justify="left",
                                     text="DEPOSIT MONEY", command=self.create_deposit_money_gui)
        retrieve_cash_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                      cursor="target", width=25, height=2, justify="left",
                                      text="RETRIEVE MONEY", command=self.create_retrieve_money_gui)
        change_pin_number_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                          cursor="target", width=25, height=2, justify="left",
                                          text="CHANGE PIN", command=self.change_pin)
        receipt_info_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                     cursor="target", width=25, height=2, justify="left",
                                     text="GET RECEIPT",
                                     command=lambda: self.bank_ops.get_receipt(self.bank_dictionary, self.working_dict))
        account_cash_transfer = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                       cursor="target", width=25, height=2, justify="left",
                                       text="ACCOUNT TRANSFER", command=self.create_account_transfer_gui)
        pay_bills_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                  cursor="target", width=25, height=2, justify="left",
                                  text="PAY BILLS", command=self.create_pay_bills_gui)
        western_union_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                      cursor="target", width=25, height=2, justify="left",
                                      text="WESTERN UNION", command=self.create_western_union_gui)
        exit_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                             cursor="target", width=25, height=2, justify="left",
                             text="EXIT BUTTON", command=self.exit_app)
        self.center(root_operations_menu)

        # put buttons on screen
        sold_interogation_button.place(x=25, y=15)
        deposit_cash_button.place(x=25, y=75)
        retrieve_cash_button.place(x=25, y=135)
        change_pin_number_button.place(x=25, y=195)
        receipt_info_button.place(x=25, y=255)
        account_cash_transfer.place(x=325, y=15)
        pay_bills_button.place(x=325, y=75)
        western_union_button.place(x=325, y=135)
        exit_button.place(x=325, y=195)

    def go_back(self, root_window):
        root_window.destroy()
        self.create_operations_gui()

    '''
      WESTERN UNION SECTION
    '''

    def create_western_union_details(self, option_currency_value):
        global western_details_root
        global western_account_input
        global western_sum_transfer_input
        western_union_root.destroy()
        western_details_root = Tk()
        western_details_root.title("ACCOUNT TRANSFER")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        western_details_root.iconbitmap(image_ico)
        western_details_root.geometry("800x500")
        western_details_root["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(western_details_root, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"),
                                 bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="WESTERN DETAILS",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create label for inserting account number
        label_account_number = Label(frame_title, text="ACCOUNT NUMBER", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     fg="#CBE336", bg="#1F6DB1", )
        label_account_number.place(x=50, y=75)
        # Create entry -
        western_account_input = Entry(frame_title, width=34, justify="center",
                                      font=("Helvetica", 11, "bold"), fg="#CBE336",
                                      bg="#1F6DB1")
        western_account_input.place(x=215, y=75)
        # create label for inserting amount
        label_money_transfer = Label(frame_title, text="TRANSFER SUM", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     fg="#CBE336", bg="#1F6DB1", )
        label_money_transfer.place(x=50, y=150)
        # Create entry
        western_sum_transfer_input = Entry(frame_title, width=16, justify="center",
                                           font=("Helvetica", 11, "bold"), fg="#CBE336",
                                           bg="#1F6DB1")
        western_sum_transfer_input.place(x=270, y=150)
        # button for enter
        check_button = Button(frame_title, text="TRANSFER", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                              font=("Helvetica", 9, "bold"),
                              command=lambda: self.bank_ops.transfer_money_abroad(self.bank_dictionary,
                                                                                  self.working_dict,
                                                                                  western_account_input.get(),
                                                                                  western_sum_transfer_input.get(),
                                                                                  option_currency_value,
                                                                                  western_account_input,
                                                                                  western_sum_transfer_input))
        back_button = Button(frame_title, text="BACK", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                             font=("Helvetica", 9, "bold"), command=lambda: self.go_back(western_details_root))
        check_button.place(x=100, y=225)
        back_button.place(x=330, y=225)
        self.center(western_details_root)

    def create_western_union_gui(self):
        global western_union_root
        root_operations_menu.destroy()
        western_union_root = Tk()
        western_union_root.title("ACCOUNT TRANSFER")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        western_union_root.iconbitmap(image_ico)
        western_union_root.geometry("800x500")
        western_union_root["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(western_union_root, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"),
                                 bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="WESTERN UNION",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create buttons for selecting the currency
        ron_to_euro_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                    cursor="target", width=25, height=2, justify="left",
                                    text="RON->EUR", command=lambda: self.create_western_union_details(1))
        ron_to_dollar_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                      cursor="target", width=25, height=2, justify="left",
                                      text="RON->USD", command=lambda: self.create_western_union_details(2))
        ron_to_pounds_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                      cursor="target", width=25, height=2, justify="left",
                                      text="RON->GBP", command=lambda: self.create_western_union_details(3))
        ron_to_swiss_francs_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"),
                                            bd=5,
                                            cursor="target", width=25, height=2, justify="left",
                                            text="RON->CHF", command=lambda: self.create_western_union_details(4))
        ron_to_yeni_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                    cursor="target", width=25, height=2, justify="left",
                                    text="RON->YEN", command=lambda: self.create_western_union_details(5))
        back_transfer_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                      cursor="target", width=25, height=2, justify="left",
                                      text="BACK", command=lambda: self.go_back(western_union_root))
        ron_to_euro_button.place(x=25, y=45)
        ron_to_dollar_button.place(x=25, y=135)
        ron_to_pounds_button.place(x=25, y=225)
        ron_to_swiss_francs_button.place(x=325, y=45)
        ron_to_yeni_button.place(x=325, y=135)
        back_transfer_button.place(x=325, y=225)
        self.center(western_union_root)

    '''
    BILL PAYMENT SECTION
    '''

    def create_pay_bills_gui(self):
        global bill_root
        root_operations_menu.destroy()
        bill_root = Tk()
        bill_root.title("BILL PAYMENT")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        bill_root.iconbitmap(image_ico)
        bill_root.geometry("800x500")
        bill_root["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(bill_root, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"),
                                 bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="PAY BILLS",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create buttons for options
        eon_electricity_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                        cursor="target", width=25, height=2, justify="left",
                                        text="EON ELECTRICITY", command=lambda: self.create_eon_payment_gui(1))
        eon_gas_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                cursor="target", width=25, height=2, justify="left",
                                text="EON GAS", command=lambda: self.create_eon_payment_gui(2))
        flat_utilities_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                       cursor="target", width=25, height=2, justify="left",
                                       text="FLAT UTILITIES",
                                       command=lambda: self.create_general_pay_bills_details_gui(3))
        house_mortgage_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"),
                                       bd=5,
                                       cursor="target", width=25, height=2, justify="left",
                                       text="HOUSE MORTGAGE",
                                       command=lambda: self.create_general_pay_bills_details_gui(4))
        back_payment_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                     cursor="target", width=25, height=2, justify="left",
                                     text="BACK", command=lambda: self.go_back(bill_root))
        eon_electricity_button.place(x=25, y=45)
        eon_gas_button.place(x=25, y=135)
        flat_utilities_button.place(x=25, y=225)
        house_mortgage_button.place(x=325, y=45)
        back_payment_button.place(x=325, y=135)
        self.center(bill_root)

    def create_general_pay_bills_details_gui(self, option):
        global pay_bills_details_root, name_service
        global pay_bill_account_input
        global pay_bill_money_input
        if option == 3:
            name_service = "FLAT ACCOUNT DETAILS"
        elif option == 4:
            name_service = "MORTGAGE ACCOUNT DETAILS"
        bill_root.destroy()
        pay_bills_details_root = Tk()
        pay_bills_details_root.title("UTILITIES DETAILS")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        pay_bills_details_root.iconbitmap(image_ico)
        pay_bills_details_root.geometry("800x500")
        pay_bills_details_root["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(pay_bills_details_root, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"),
                                 bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text=name_service,
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create label for inserting account number
        label_account_number = Label(frame_title, text="ACCOUNT NUMBER", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     fg="#CBE336", bg="#1F6DB1", )
        label_account_number.place(x=50, y=75)
        # Create entry -
        pay_bill_account_input = Entry(frame_title, width=34, justify="center",
                                       font=("Helvetica", 11, "bold"), fg="#CBE336",
                                       bg="#1F6DB1")
        pay_bill_account_input.place(x=215, y=75)
        # create label for inserting amount
        label_money_transfer = Label(frame_title, text="TRANSFER SUM", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     fg="#CBE336", bg="#1F6DB1", )
        label_money_transfer.place(x=50, y=150)
        # Create entry
        pay_bill_money_input = Entry(frame_title, width=16, justify="center",
                                     font=("Helvetica", 11, "bold"), fg="#CBE336",
                                     bg="#1F6DB1")
        pay_bill_money_input.place(x=270, y=150)
        # button for enter
        check_button = Button(frame_title, text="TRANSFER", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                              font=("Helvetica", 9, "bold"),
                              command=lambda: self.bank_ops.pay_bills(self.bank_dictionary, self.working_dict,
                                                                      pay_bill_account_input.get(),
                                                                      pay_bill_money_input.get(), option, 0,
                                                                      pay_bill_account_input,
                                                                      pay_bill_money_input,
                                                                      0))  # 0 represents the invoice which is not used here(args_3)
        back_button = Button(frame_title, text="BACK", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                             font=("Helvetica", 9, "bold"), command=lambda: self.go_back(pay_bills_details_root))
        check_button.place(x=100, y=225)
        back_button.place(x=330, y=225)
        self.center(pay_bills_details_root)

    def create_eon_payment_gui(self, option):
        global root_eon, name_section
        global input_account_bill
        global input_invoice_number
        global input_value_bill
        if option == 1:
            name_section = "EON ELECTRICITY"
        elif option == 2:
            name_section = "EON GAS"
        bill_root.destroy()
        root_eon = Tk()
        root_eon.title("EON DETAILS")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        root_eon.iconbitmap(image_ico)
        root_eon.geometry("800x500")
        root_eon["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(root_eon, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"),
                                 bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text=name_section,
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create label for inserting account bill number
        label_account_number = Label(frame_title, text="CLIENT NUMBER", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     fg="#CBE336", bg="#1F6DB1", )
        label_account_number.place(x=50, y=45)
        # Create entry -
        input_account_bill = Entry(frame_title, width=26, justify="center",
                                   font=("Helvetica", 11, "bold"), fg="#CBE336",
                                   bg="#1F6DB1")
        input_account_bill.place(x=235, y=45)
        # create label for inserting invoice number
        label_invoice_number = Label(frame_title, text="INVOICE NUMBER", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     fg="#CBE336", bg="#1F6DB1", )
        label_invoice_number.place(x=50, y=105)
        # Create entry -
        input_invoice_number = Entry(frame_title, width=26, justify="center",
                                     font=("Helvetica", 11, "bold"), fg="#CBE336",
                                     bg="#1F6DB1")
        input_invoice_number.place(x=235, y=105)
        # create label for inserting amount
        label_money_transfer = Label(frame_title, text="BILL SUM", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     fg="#CBE336", bg="#1F6DB1", )
        label_money_transfer.place(x=50, y=165)
        # Create entry
        input_value_bill = Entry(frame_title, width=16, justify="center",
                                 font=("Helvetica", 11, "bold"), fg="#CBE336",
                                 bg="#1F6DB1")
        input_value_bill.place(x=270, y=165)
        # button for enter
        check_button = Button(frame_title, text="PAY", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                              font=("Helvetica", 9, "bold"),
                              command=lambda: self.bank_ops.pay_bills(self.bank_dictionary, self.working_dict,
                                                                      input_account_bill.get(),
                                                                      input_value_bill.get(), option,
                                                                      input_invoice_number.get(), input_account_bill,
                                                                      input_value_bill, input_invoice_number))
        back_button = Button(frame_title, text="BACK", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                             font=("Helvetica", 9, "bold"), command=lambda: self.go_back(root_eon))
        check_button.place(x=100, y=225)
        back_button.place(x=330, y=225)
        self.center(root_eon)

    '''
    ACCOUNT TRANSFER SECTION
    * can only transfer to accounts present in banking details
    '''

    def create_account_transfer_gui(self):
        global account_transfer_root
        global input_account_number
        global input_money_transfer
        root_operations_menu.destroy()
        account_transfer_root = Tk()
        account_transfer_root.title("ACCOUNT TRANSFER")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        account_transfer_root.iconbitmap(image_ico)
        account_transfer_root.geometry("800x500")
        account_transfer_root["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(account_transfer_root, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"),
                                 bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="ACCOUNT TRANSFER",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create label for inserting account number
        label_account_number = Label(frame_title, text="ACCOUNT NUMBER", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     fg="#CBE336", bg="#1F6DB1", )
        label_account_number.place(x=50, y=75)
        # Create entry -
        input_account_number = Entry(frame_title, width=34, justify="center",
                                     font=("Helvetica", 11, "bold"), fg="#CBE336",
                                     bg="#1F6DB1")
        input_account_number.place(x=215, y=75)
        # create label for inserting amount
        label_money_transfer = Label(frame_title, text="TRANSFER SUM", justify="center",
                                     font=("Helvetica", 11, "bold"),
                                     fg="#CBE336", bg="#1F6DB1", )
        label_money_transfer.place(x=50, y=150)
        # Create entry
        input_money_transfer = Entry(frame_title, width=16, justify="center",
                                     font=("Helvetica", 11, "bold"), fg="#CBE336",
                                     bg="#1F6DB1")
        input_money_transfer.place(x=270, y=150)
        # button for enter
        check_button = Button(frame_title, text="TRANSFER", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                              font=("Helvetica", 9, "bold"),
                              command=lambda: self.bank_ops.transfer_money_accounts(self.bank_dictionary,
                                                                                    self.working_dict,
                                                                                    input_account_number.get(),
                                                                                    input_money_transfer.get(),
                                                                                    input_account_number,
                                                                                    input_money_transfer))
        back_button = Button(frame_title, text="BACK", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                             font=("Helvetica", 9, "bold"), command=lambda: self.go_back(account_transfer_root))
        check_button.place(x=100, y=225)
        back_button.place(x=330, y=225)
        self.center(account_transfer_root)

        '''
        DEPOSIT CASH FUNCTIONS
        '''

    def create_other_sum_gui_add(self):
        global other_sum_root_add
        global input_sum_add
        root_deposit_cash.destroy()
        other_sum_root_add = Tk()
        other_sum_root_add.title("DEPOSIT MONEY")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        other_sum_root_add.iconbitmap(image_ico)
        other_sum_root_add.geometry("800x500")
        other_sum_root_add["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(other_sum_root_add, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"), bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="OTHER SUM",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create label for inserting amount
        pin_label = Label(frame_title, text="INSERT AMOUNT", justify="center", font=("Helvetica", 15, "bold"),
                          fg="#CBE336", bg="#1F6DB1", )
        pin_label.place(x=175, y=75)
        # Create entry -> show * basically masks the pin value
        input_sum_add = Entry(frame_title, width=16, justify="center",
                              font=("Helvetica", 15, "bold"), fg="#CBE336",
                              bg="#1F6DB1")
        input_sum_add.place(x=175, y=150)
        # button for enter
        check_button = Button(frame_title, text="DEPOSIT", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                              font=("Helvetica", 9, "bold"),
                              command=lambda: self.bank_ops.add_cash(self.bank_dictionary, self.working_dict,
                                                                     7, input_sum_add.get(), input_sum_add))
        back_button = Button(frame_title, text="BACK", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                             font=("Helvetica", 9, "bold"),
                             command=lambda: self.go_back(other_sum_root_add))
        check_button.place(x=100, y=225)
        back_button.place(x=325, y=225)
        self.center(other_sum_root_add)

    def create_deposit_money_gui(self):
        global root_deposit_cash
        root_operations_menu.destroy()
        root_deposit_cash = Tk()
        root_deposit_cash.title("DEPOSIT MONEY")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        root_deposit_cash.iconbitmap(image_ico)
        root_deposit_cash.geometry("800x500")
        root_deposit_cash["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(root_deposit_cash, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"), bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="DEPOSIT",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # add buttons for every option sum
        ten_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                cursor="target", width=25, height=2, justify="left",
                                text="10 RON",
                                command=lambda: self.bank_ops.add_cash(self.bank_dictionary, self.working_dict,
                                                                       1))  # 1 is the key in helper.constants.BANK_DICTIONARY
        fifty_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                  cursor="target", width=25, height=2, justify="left",
                                  text="50 RON",
                                  command=lambda: self.bank_ops.add_cash(self.bank_dictionary, self.working_dict, 2))
        hundred_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                    cursor="target", width=25, height=2, justify="left",
                                    text="100 RON",
                                    command=lambda: self.bank_ops.add_cash(self.bank_dictionary, self.working_dict, 3))
        two_hundred_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                        cursor="target", width=25, height=2, justify="left",
                                        text="200 RON",
                                        command=lambda: self.bank_ops.add_cash(self.bank_dictionary, self.working_dict,
                                                                               4))
        five_hundred_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                         cursor="target", width=25, height=2, justify="left",
                                         text="500 RON",
                                         command=lambda: self.bank_ops.add_cash(self.bank_dictionary, self.working_dict,
                                                                                5))
        eight_hundred_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                          cursor="target", width=25, height=2, justify="left",
                                          text="800 RON",
                                          command=lambda: self.bank_ops.add_cash(self.bank_dictionary,
                                                                                 self.working_dict, 6))
        other_sum_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                      cursor="target", width=25, height=2, justify="left",
                                      text="OTHER SUM", command=self.create_other_sum_gui_add)
        back_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                 cursor="target", width=25, height=2, justify="left",
                                 text="BACK", command=lambda: self.go_back(root_deposit_cash))
        # put buttons on window
        ten_lei_button.place(x=25, y=15)
        fifty_lei_button.place(x=25, y=90)
        hundred_lei_button.place(x=25, y=165)
        two_hundred_lei_button.place(x=25, y=240)
        five_hundred_lei_button.place(x=325, y=15)
        eight_hundred_lei_button.place(x=325, y=90)
        other_sum_lei_button.place(x=325, y=165)
        back_lei_button.place(x=325, y=240)
        self.center(root_deposit_cash)

    '''
    RETRIEVE CASH FUNCTIONS
    '''

    def create_other_sum_gui_retrieve(self):
        global other_sum_root_retrieve
        global input_sum_retrieve
        root_retrieve_cash.destroy()
        other_sum_root_retrieve = Tk()
        other_sum_root_retrieve.title("RETRIEVE MONEY")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        other_sum_root_retrieve.iconbitmap(image_ico)
        other_sum_root_retrieve.geometry("800x500")
        other_sum_root_retrieve["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(other_sum_root_retrieve, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"),
                                 bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="OTHER SUM",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create label for inserting amount
        pin_label = Label(frame_title, text="RETRIEVE AMOUNT", justify="center", font=("Helvetica", 15, "bold"),
                          fg="#CBE336", bg="#1F6DB1", )
        pin_label.place(x=175, y=75)
        # Create entry -> show * basically masks the pin value
        input_sum_retrieve = Entry(frame_title, width=16, justify="center",
                                   font=("Helvetica", 15, "bold"), fg="#CBE336",
                                   bg="#1F6DB1")
        input_sum_retrieve.place(x=175, y=150)
        # button for enter
        check_button = Button(frame_title, text="RETRIEVE", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                              font=("Helvetica", 9, "bold"),
                              command=lambda: self.bank_ops.retreat_cash(self.bank_dictionary, self.working_dict,
                                                                         7, input_sum_retrieve.get(),
                                                                         input_sum_retrieve))
        back_button = Button(frame_title, text="BACK", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                             font=("Helvetica", 9, "bold"),
                             command=lambda: self.go_back(other_sum_root_retrieve))
        check_button.place(x=100, y=225)
        back_button.place(x=325, y=225)
        self.center(other_sum_root_retrieve)

    def create_retrieve_money_gui(self):
        global root_retrieve_cash
        root_operations_menu.destroy()
        root_retrieve_cash = Tk()
        root_retrieve_cash.title("RETRIEVE MONEY")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        root_retrieve_cash.iconbitmap(image_ico)
        root_retrieve_cash.geometry("800x500")
        root_retrieve_cash["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(root_retrieve_cash, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"), bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="RETRIEVE",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # add buttons for every option sum
        ten_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                cursor="target", width=25, height=2, justify="left",
                                text="10 RON",
                                command=lambda: self.bank_ops.retreat_cash(self.bank_dictionary, self.working_dict,
                                                                           1))  # 1 is the key in helper.constants.BANK_DICTIONARY
        fifty_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                  cursor="target", width=25, height=2, justify="left",
                                  text="50 RON",
                                  command=lambda: self.bank_ops.retreat_cash(self.bank_dictionary, self.working_dict,
                                                                             2))
        hundred_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                    cursor="target", width=25, height=2, justify="left",
                                    text="100 RON",
                                    command=lambda: self.bank_ops.retreat_cash(self.bank_dictionary, self.working_dict,
                                                                               3))
        two_hundred_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                        cursor="target", width=25, height=2, justify="left",
                                        text="200 RON",
                                        command=lambda: self.bank_ops.retreat_cash(self.bank_dictionary,
                                                                                   self.working_dict,
                                                                                   4))
        five_hundred_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                         cursor="target", width=25, height=2, justify="left",
                                         text="500 RON",
                                         command=lambda: self.bank_ops.retreat_cash(self.bank_dictionary,
                                                                                    self.working_dict,
                                                                                    5))
        eight_hundred_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                          cursor="target", width=25, height=2, justify="left",
                                          text="800 RON",
                                          command=lambda: self.bank_ops.retreat_cash(self.bank_dictionary,
                                                                                     self.working_dict, 6))
        other_sum_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                      cursor="target", width=25, height=2, justify="left",
                                      text="OTHER SUM", command=self.create_other_sum_gui_retrieve)
        back_lei_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                                 cursor="target", width=25, height=2, justify="left",
                                 text="BACK", command=lambda: self.go_back(root_retrieve_cash))
        # put buttons on window
        ten_lei_button.place(x=25, y=15)
        fifty_lei_button.place(x=25, y=90)
        hundred_lei_button.place(x=25, y=165)
        two_hundred_lei_button.place(x=25, y=240)
        five_hundred_lei_button.place(x=325, y=15)
        eight_hundred_lei_button.place(x=325, y=90)
        other_sum_lei_button.place(x=325, y=165)
        back_lei_button.place(x=325, y=240)
        self.center(root_retrieve_cash)

    '''
    CHECK SOLD
    '''

    def check_sold(self):
        global root_sold_value
        root_operations_menu.destroy()
        root_sold_value = Tk()
        root_sold_value.title("SOLD VALUE")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        root_sold_value.iconbitmap(image_ico)
        root_sold_value.geometry("800x500")
        root_sold_value["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(root_sold_value, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"), bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="SOLD",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # first we make the cash interrogation to update the dictionary
        self.center(root_sold_value)
        self.bank_ops.cash_interrogation(self.bank_dictionary, self.working_dict)
        # create label with value
        sold_label = Label(frame_title,
                           text="YOUR SOLD VALUE IS " + str(self.working_dict[helper.constants.CARD_INFO[2]]),
                           justify="center", font=("Helvetica", 15, "bold"),
                           fg="#CBE336", bg="#1F6DB1", )
        sold_label.place(x=130, y=125)
        # create button to go back
        back_button = Button(frame_title, fg="#CBE336", bg="#1F6DB1", font=("Helvetica", 9, "bold"), bd=5,
                             cursor="target", width=25, height=2, justify="left",
                             text="BACK", command=lambda: self.go_back(root_sold_value))
        back_button.place(x=170, y=200)
        self.center(root_sold_value)

    '''
    CHANGE PIN FUNCTION
    '''

    def change_pin(self):
        global root_new_pin
        global new_pin_input
        root_operations_menu.destroy()
        root_new_pin = Tk()
        root_new_pin.title("SOLD VALUE")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        root_new_pin.iconbitmap(image_ico)
        root_new_pin.geometry("800x500")
        root_new_pin["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(root_new_pin, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"), bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="PIN CHANGE",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)

        # create label for inserting pin
        pin_label = Label(frame_title, text="INSERT NEW PIN", justify="center", font=("Helvetica", 15, "bold"),
                          fg="#CBE336", bg="#1F6DB1", )
        pin_label.place(x=175, y=75)
        # Create entry -> show * basically masks the pin value
        new_pin_input = Entry(frame_title, width=16, justify="center",
                              font=("Helvetica", 15, "bold"), fg="#CBE336",
                              bg="#1F6DB1", show="*")
        new_pin_input.place(x=175, y=150)
        # button for enter
        check_button = Button(frame_title, text="ACCEPT", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                              font=("Helvetica", 9, "bold"),
                              command=lambda: self.bank_ops.change_pin_number(self.bank_dictionary, self.working_dict,
                                                                              new_pin_input.get(), new_pin_input))
        back_button = Button(frame_title, text="BACK", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                             font=("Helvetica", 9, "bold"),
                             command=lambda: self.go_back(root_new_pin))
        check_button.place(x=100, y=225)
        back_button.place(x=325, y=225)
        self.center(root_new_pin)

        '''
        PIN CHECK
        '''

    def check_pin(self):
        print(self.counter_pin_errors)
        '''
        Here with the help of the method in helper_things we will create our custom method
        :return: we will not return nothing because we already have the dictionary as it is from init
        '''
        """
        COMPUTE THE CLIENT DICTIONARY FIRST
        """
        # create a flag to check pin
        pin_ok = False
        index_list = -1
        print(input_pin.get())
        if self.counter_pin_errors > 1:
            messagebox.showerror("PIN INVALID", "Your card has been blocked! Contact your bank")
            sys.exit(0)
        for key in self.bank_dictionary:
            if key == helper.constants.CARD_INFO[0]:
                for pin_number in self.bank_dictionary[key]:
                    if input_pin.get() == pin_number and not pin_ok:
                        # get the index of the pin in the list to create dictionary for that person
                        index_list = self.bank_dictionary[key].index(pin_number)
                        pin_ok = True
        if not pin_ok:
            messagebox.showerror("PIN INVALID", "Re-type the PIN number")
            self.counter_pin_errors += 1
            return
        for key in self.bank_dictionary:
            self.working_dict.update({key: self.bank_dictionary[key][index_list]})
        if self.helper.card_bank(self.working_dict):
            message_welcome = "Hello " + self.working_dict[helper.constants.CARD_INFO[1]]
            messagebox.showinfo("WELCOME", message=message_welcome)
            # return self.working_dict
            print(self.working_dict)
        else:
            message_welcome = "Hello " + self.working_dict[helper.constants.CARD_INFO[1]]
            messagebox.showinfo("WELCOME", message=message_welcome)
            messagebox.showinfo("INFO", "Operations will be charged in regards with bank policies!")
            print(self.working_dict)
            # return self.working_dict
        '''
        PROCEED WITH CREATING THE NEW GUI WITH THE BUTTONS
        '''
        root_pin.destroy()
        self.create_operations_gui()

        '''
        START APP POINT
        '''

    def create_pin_gui(self):
        # create layout with a grey font
        global root_pin
        global input_pin
        # create start frame
        root_pin = Tk()
        root_pin.title("ADD")
        image_ico = os.path.join(r"G:\pycharm\pythonProject\BankingAppGui\gui\banking.ico")
        root_pin.iconbitmap(image_ico)
        root_pin.geometry("800x500")
        root_pin["bg"] = "#DEE1DB"
        # create first frame for title label
        frame_title = LabelFrame(root_pin, fg="#8A8E86", bg="#1F6DB1", font=("Helvetica", 12, "bold"), bd=5,
                                 cursor="target", width=550, height=350, labelanchor="n", text="PIN",
                                 relief=tkinter.RAISED)
        frame_title.place(x=125, y=75)  # put it in the middle
        frame_title.grid_rowconfigure(0, weight=1)
        frame_title.grid_columnconfigure(0, weight=1)
        # create label for inserting pin
        pin_label = Label(frame_title, text="INSERT PIN", justify="center", font=("Helvetica", 15, "bold"),
                          fg="#CBE336", bg="#1F6DB1", )
        pin_label.place(x=200, y=75)
        # Create entry -> show * basically masks the pin value
        input_pin = Entry(frame_title, width=16, justify="center",
                          font=("Helvetica", 15, "bold"), fg="#CBE336",
                          bg="#1F6DB1", show="*")
        input_pin.place(x=170, y=150)
        # button for enter
        check_button = Button(frame_title, text="ACCEPT", width=15, height=2, fg="#191A1A", bg="#1F6DB1",
                              font=("Helvetica", 9, "bold"), command=self.check_pin)
        check_button.place(x=200, y=225)
        self.center(root_pin)

        root_pin.mainloop()
