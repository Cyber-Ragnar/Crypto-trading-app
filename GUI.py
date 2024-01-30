from Client import *
from tkinter import *
from tkinter.messagebox import showinfo
import random
from datetime import *
from PIL import ImageTk
import ctypes
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

LIGHT_GRAY = '#545454'
DARK_GRAY = '#242424'
GRAY = '#2e2e2e'
DARK_GRAY2 = '#1E1E1E'
DARK = '#001933'
# Color codes to make gui configuration less confusing

padding = {'pady': 10, 'padx': 10}
# Padding options used in multiple classes

ID = []
"""
Temporary storage container for the userid fetched from the database on the log-in stage, used mainly 
to identify correct data, that belongs to the current user. It is being emptied, once the application is being closed.
"""

check = []


class Processes:
    """
    class Processes allowing me to create threads.
    """

    def __init__(self, process, stat=False):
        """
        :param process: it is passing a function which I want to run on the thread.
        :param stat: allows me to change boolean value of the class attribute 'daemon' of the custom thread
        """
        self.__name = process
        self.t = threading.Thread(target=self.__name)
        self.t.daemon = stat

    def start(self):
        """
        Method starting a given thread
        """
        self.t.start()


class Root(Tk):
    """
    Class creating a first window in tkinter.
    """

    def __init__(self):
        super().__init__()
        self.center(600, 400)

        # Calling a method which will always display the window in the center of the screen

        self.configure(background=DARK_GRAY2)
        self.overrideredirect(True)
        self.resizable(False, False)

        # Setting boolean for width and height in method 'resizable' to 'False', so it will not be possible to change
        # the size of the starting window

        FirstWindow(self)
        # Creating the first frame, by calling its class

    def center(self, width, height):
        """
        Method which will place tkinter window in the center of the screen
        :param width: user defined width of the window
        :param height: user defined height of the window
        :return: sets 'geometry' of the window according to desired parameters and sets starting position of the window
        """
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


class FirstWindow(Frame):
    """
    Class for the first page which will ask user to either log in or register
    """

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.background = DARK_GRAY2

        self.title_frame = Frame(self.master, bg=DARK_GRAY, height=25)
        self.title_frame.pack(fill=X, side=TOP)
        self.title = Label(self.title_frame, font='Verdana 15', text='CRYPTO TRADER', bd=0, fg='white', bg=DARK_GRAY)
        self.title.pack(side=LEFT, padx=5)

        self.close_button = Button(self.title_frame, width=4, text='X', bg=DARK_GRAY, fg='white', font='Verdana 15',
                                   command=exit, relief=GROOVE, bd=0)
        self.close_button.pack(side=RIGHT)

        self.spacing_frame = Frame(self, background=DARK_GRAY2, height=50, bd=0)
        self.spacing_frame.pack(fill=BOTH)

        self.image = PhotoImage(file="./images/cryptos_logo2.png")
        self.logo_label = Label(self, image=self.image, background=DARK_GRAY2, bd=0, padx=0, pady=0)
        self.logo_label.pack(padx=0, pady=0)

        self.buttons_frame = Frame(self, background=DARK_GRAY2, width=300)
        self.buttons_frame.pack(fill=BOTH)

        self.login_button = Button(self.buttons_frame, text='Login', command=self.login_, width=15, background=GRAY,
                                   fg='light gray', bd=0, relief=RAISED, font='Verdana 15')
        self.login_button.pack(**padding, side=LEFT)

        self.register_button = Button(self.buttons_frame, text='Register', width=15, command=self.register_,
                                      background=GRAY, fg='light gray', bd=0, relief=RAISED, font='Verdana 15')

        self.register_button.pack(**padding, side=RIGHT)

        self.buttons = [self.register_button, self.login_button, self.close_button]
        for b in range(len(self.buttons)):
            self.buttons[b].bind('<Enter>', lambda event, i=b: self.buttons[i].configure(background='dark red'))
            self.buttons[b].bind('<Leave>', lambda event, i=b: self.buttons[i].configure(background=DARK_GRAY))

        # bind title bar to move window
        self.title_frame.bind('<Button-1>', self.get_position)
        self.title_frame.bind('<B1-Motion>', self.get_position)

        self.pack()

    def widget_destroy(self):
        """
        Method partially allowing for dynamic swapping screens in tkinter, by removing previous widgets from it
        """
        for widget in self.master.winfo_children():
            widget.destroy()

    def login_(self):
        """
        Method taking us to the next page, which is in that case login page
        """
        self.widget_destroy()
        self.destroy()
        Login(self.master)

    def register_(self):
        """
        Method taking us to the next page, which is in that case registration page
        """
        self.widget_destroy()
        self.destroy()
        Register(self.master)

    def get_position(self, event):
        """
        Method allowing for movement of the window, when dragged with mouse for the custom toolbar
        """
        x_window = self.master.winfo_x()
        y_window = self.master.winfo_y()
        start_x = event.x_root
        start_y = event.y_root

        y_window = y_window - start_y
        x_window = x_window - start_x

        def move(event):
            self.master.geometry('+{0}+{1}'.format(event.x_root + x_window, event.y_root + y_window))

        self.title_frame.bind('<B1-Motion>', move)


class Login(Frame):
    """
    Class for the logging window, allows to either go back, or takes the user to the main application
    after entering correct credentials
    """

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.pass_details = {'admin': '1234', 'admin2': '4321'}
        self.configure(background=DARK_GRAY2)
        self.columnconfigure(0, weight=3)
        self.title_frame = Frame(self.master, bg=DARK_GRAY, height=20, bd=0, padx=0, pady=0)

        self.title_frame.pack(fill=X, side=TOP)
        self.title = Label(self.title_frame, font='Verdana 15', text='CRYPTO TRADER', bd=0, fg='white', bg=DARK_GRAY)
        self.title.pack(side=LEFT, padx=5)

        self.close_button = Button(self.title_frame, width=4, text='X', bg=DARK_GRAY, fg='white', font='Verdana 15',
                                   command=exit, relief=GROOVE, bd=0)
        self.close_button.pack(side=RIGHT)


        self.spacing_frame = Frame(self, background=DARK_GRAY2, height=50, bd=0)
        self.spacing_frame.grid(row=1, column=3, **padding)

        Label(self, text='Username: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=2, column=0)
        self.user_entry = Entry(self, justify=RIGHT, font='Verdana 15')
        self.user_entry.grid(row=2, column=1, columnspan=2, pady=5)

        Label(self, text='Password: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=3, column=0, **padding)
        self.pass_entry = Entry(self, show='*', justify=RIGHT, font='Verdana 15')
        self.pass_entry.grid(row=3, column=1, columnspan=2, pady=5)

        self.back_button = Button(self, text='Back', width=15, command=self.back_, background=DARK_GRAY2,
                                  fg='light gray', font='Verdana 15', relief=RAISED, bd=0)
        self.back_button.grid(row=4, column=0, sticky=W, **padding)

        self.submit_button = Button(self, text='Submit', width=15, relief=RAISED, bd=0,
                               command=lambda: self.login(), background=DARK_GRAY2, fg='light gray', font='Verdana 15')
        self.submit_button.grid(row=4, column=1, sticky=E, **padding)
        self.buttons = [self.back_button, self.submit_button, self.close_button]
        for b in range(len(self.buttons)):
            self.buttons[b].bind('<Enter>', lambda event, i=b: self.buttons[i].configure(background='dark red'))
            self.buttons[b].bind('<Leave>', lambda event, i=b: self.buttons[i].configure(background=DARK_GRAY))

        # bind title bar to move window
        self.title_frame.bind('<Button-1>', self.get_position)
        self.title_frame.bind('<B1-Motion>', self.get_position)

        self.pack()

    def back_(self):
        """
        method allowing to go back
        """
        for widget in self.master.winfo_children():
            widget.destroy()
        self.destroy()
        FirstWindow(self.master)

    def login(self):
        """
        Method opening the main app
        """
        if self.login_validation():
            ID.append(client.get_id(self.user_entry.get()))
            for widget in self.master.winfo_children():
                widget.destroy()
            self.master.destroy()
            MainApp()

    def login_validation(self):
        """
        Method validating user credentials
        """
        email = self.user_entry.get()
        password = self.pass_entry.get()
        if client.email_exist(email):
            showinfo('Error exist', 'Username not recognized')
            return False
        elif client.login_details(email, password):
            return True
        else:
            showinfo('Error', 'Wrong password')
            return False

    def get_position(self, event):
        """
        Mentioned before
        """
        x_window = self.master.winfo_x()
        y_window = self.master.winfo_y()
        start_x = event.x_root
        start_y = event.y_root

        y_window = y_window - start_y
        x_window = x_window - start_x

        def move(event):
            self.master.geometry('+{0}+{1}'.format(event.x_root + x_window, event.y_root + y_window))

        self.title_frame.bind('<B1-Motion>', move)


class Register(Frame):
    """
    Class for the registration window
    """

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.configure(background=DARK_GRAY2)

        self.title_frame = Frame(self.master, bg=DARK_GRAY, height=20)
        self.title_frame.pack(fill=X, side=TOP)
        self.title = Label(self.title_frame, font='Verdana 15', text='CRYPTO TRADER', bd=0, fg='white', bg=DARK_GRAY)
        self.title.pack(side=LEFT, padx=5)

        self.close_button = Button(self.title_frame, width=4, text='X', bg=DARK_GRAY, fg='white', font='Verdana 15',
                                   command=exit, relief=GROOVE, bd=0)
        self.close_button.pack(side=RIGHT)

        self.entries = {'padx': 0, 'pady': 5, 'columnspan': 1, 'column': 1, 'sticky': 'E'}
        self.entries_op = {'width': 15, 'justify': 'right', 'font': 'Verdana 15', 'bg': 'light gray'}

        Label(self, text='First Name: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=0, column=0, sticky=W, **padding)
        self.name_entry = Entry(self, **self.entries_op)
        self.name_entry.grid(row=0, **self.entries)

        Label(self, text='Last Name: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=1, column=0, sticky=W, **padding)
        self.last_entry = Entry(self, **self.entries_op)
        self.last_entry.grid(row=1, **self.entries)

        Label(self, text='D.O.B: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=2, column=0, sticky=W, **padding)
        self.dob_entry = Entry(self, **self.entries_op)
        self.dob_entry.grid(row=2, **self.entries)

        Label(self, text='Email: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=3, column=0, sticky=W, **padding)
        self.email_entry = Entry(self, **self.entries_op)
        self.email_entry.grid(row=3, **self.entries)

        Label(self, text='Password: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=4, column=0, sticky=W, **padding)
        self.pass_entry = Entry(self, **self.entries_op)
        self.pass_entry.grid(row=4, **self.entries)

        self.back_button = Button(self, text='Back', width=15, command=self.back_, background=DARK_GRAY2,
                                  fg='light gray', font='Verdana 15', relief=RAISED, bd=0)

        self.back_button.grid(row=5, column=0, sticky=W, **padding)

        self.submit_button = Button(self, text='Submit', width=15, relief=RAISED, bd=0,
                                    command=lambda: self.card_page(), background=DARK_GRAY2, fg='light gray',
                                    font='Verdana 15')
        self.submit_button.grid(row=5, column=1, sticky=E, **padding)

        self.buttons = [self.back_button, self.submit_button, self.close_button]
        for b in range(len(self.buttons)):
            self.buttons[b].bind('<Enter>', lambda event, i=b: self.buttons[i].configure(background='dark red'))
            self.buttons[b].bind('<Leave>', lambda event, i=b: self.buttons[i].configure(background=DARK_GRAY))

        # bind title bar to move window
        self.title_frame.bind('<Button-1>', self.get_position)
        self.title_frame.bind('<B1-Motion>', self.get_position)

        self.pack()

    def back_(self):
        """
        Method to go back
        """
        for widget in self.master.winfo_children():
            widget.destroy()
        FirstWindow(self.master)

    def card_page(self):
        """
        Method taking us to register the bank card
        """
        if self.validate_input():
            self.send_all_details()
            for widget in self.master.winfo_children():
                widget.destroy()
            BankAccountRegForm(self.master)

    def send_all_details(self):
        """
        Method entering all the details of the newly registered user into a database
        """
        name = self.name_entry.get()
        lname = self.last_entry.get()
        dob = self.dob_entry.get()
        email = self.email_entry.get()
        password = self.pass_entry.get()
        userID = name[0:3] + lname[0:3] + str(random.randint(0, 1000))
        message = f'user,{userID},{name},{lname},{dob},{email},{password}'
        client.sending_message(message)

    def validate_input(self):
        """
        Method validating user input
        """
        name = self.name_entry.get()
        lname = self.last_entry.get()
        email = self.email_entry.get()
        password = self.pass_entry.get()
        if not self.names_validation(name) or not self.names_validation(lname):
            showinfo('Error', 'Name or Surname is not valid')
            return False
        elif not self.date_validation():
            showinfo('Error', 'You need to be at least 18 years old '
                              'to register in Crypto trader app.')
            return False
        elif not client.email_exist(email):
            showinfo('Error', 'User with that email address already exists')
            return False
        elif '@' not in email and email[-4::] != '.com':
            showinfo('Error', 'Email address provided is not valid')
            return False
        elif not self.password_validation(password):
            showinfo('Error', 'Password has to contain minimum of 8 characters,'
                              'at least 1 letter, 1 number, 1 special character'
                              'and no white spaces')
            return False
        else:
            return True

    def date_validation(self):
        """
        Method validating date
        """
        data = self.dob_entry.get()
        try:
            if data != datetime.strptime(data, '%Y-%m-%d').strftime('%Y-%m-%d'):
                raise ValueError
            today_date = datetime.now().date()
            today_date = str(today_date)
            data_for_calculations = datetime.strptime(data, '%Y-%m-%d')
            today_date_for_calculation = datetime.strptime(today_date, '%Y-%m-%d')
            result = today_date_for_calculation - data_for_calculations
            difference = result.days // 365
            if difference < 18:
                return print('too young')
            return True
        except ValueError:
            showinfo('Error', 'Incorrect date format. '
                              'it suppose to be:'
                              'YYYY-MM-DD')
            return False

    @staticmethod
    def names_validation(name):
        """
        Method validating name and surname
        """
        if name.isalpha():
            return True
        else:
            return False

    @staticmethod
    def password_validation(password):
        """
        Method validating password
        """
        if len(password) < 8:
            return False
        elif not any(i.isdigit() or i.isalpha() for i in password):
            return False
        elif any(i.isspace() for i in password):
            return False
        elif all(i.isalnum() for i in password):
            return False
        else:
            return True

    def get_position(self, event):
        """
        Mentioned before
        """
        x_window = self.master.winfo_x()
        y_window = self.master.winfo_y()
        start_x = event.x_root
        start_y = event.y_root

        y_window = y_window - start_y
        x_window = x_window - start_x

        def move(event):
            self.master.geometry('+{0}+{1}'.format(event.x_root + x_window, event.y_root + y_window))

        self.title_frame.bind('<B1-Motion>', move)


class BankAccountRegForm(Frame):
    """
    Class to register bank card to make deposits, withdrawal and initial money in
    """

    def __init__(self, master):
        super().__init__()
        self.master = master

        self.title_frame = Frame(self.master, bg=DARK_GRAY, height=20)
        self.title_frame.pack(fill=X, side=TOP)
        self.title = Label(self.title_frame, font='Verdana 15', text='CRYPTO TRADER', bd=0, fg='white', bg=DARK_GRAY)
        self.title.pack(side=LEFT, padx=5)

        self.close_button = Button(self.title_frame, width=4, text='X', bg=DARK_GRAY, fg='white', font='Verdana 15',
                                   command=exit, relief=GROOVE, bd=0)
        self.close_button.pack(side=RIGHT)

        self.entries = {'padx': 0, 'pady': 10, 'columnspan': 2, 'column': 1, 'sticky': 'E'}
        self.entries_op = {'width': 15, 'justify': 'right', 'font': 'Verdana 15', 'bg': 'light gray'}

        self.widgets_frame = Frame(self, background=DARK_GRAY2)
        self.widgets_frame.pack(fill=BOTH, expand=True)

        Label(self.widgets_frame, text='Card Number: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=0, column=0, **padding)
        self.cn_entry = Entry(self.widgets_frame, **self.entries_op)
        self.cn_entry.grid(row=0, **self.entries)

        Label(self.widgets_frame, text='CVV: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=1, column=0, **padding)
        self.cvv_entry = Entry(self.widgets_frame, **self.entries_op)
        self.cvv_entry.grid(row=1, **self.entries)

        Label(self.widgets_frame, text='EXP Date: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=2, column=0, **padding)
        self.date_entry = Entry(self.widgets_frame, **self.entries_op)
        self.date_entry.grid(row=2, **self.entries)

        Label(self.widgets_frame, text='Money in: ', background=DARK_GRAY2, fg='light gray',
              font='Verdana 15').grid(row=3, column=0, **padding)
        self.money_entry = Entry(self.widgets_frame, **self.entries_op)
        self.money_entry.grid(row=3, **self.entries)

        self.back_button = Button(self.widgets_frame, text='Back', width=15, command=self.back_, background=DARK_GRAY2,
                                  fg='light gray', font='Verdana 15', relief=RAISED, bd=0)

        self.back_button.grid(row=5, column=0, sticky=W, **padding)

        self.submit_button = Button(self.widgets_frame, text='Submit', width=15, relief=RAISED, bd=0,
                                    command=lambda: self.login_page(), background=DARK_GRAY2, fg='light gray',
                                    font='Verdana 15')
        self.submit_button.grid(row=5, column=1, sticky=E, **padding)

        # bind title bar to move window
        self.title_frame.bind('<Button-1>', self.get_position)
        self.title_frame.bind('<B1-Motion>', self.get_position)
        self.buttons = [self.back_button, self.submit_button, self.close_button]
        for b in range(len(self.buttons)):
            self.buttons[b].bind('<Enter>', lambda event, i=b: self.buttons[i].configure(background='dark red'))
            self.buttons[b].bind('<Leave>', lambda event, i=b: self.buttons[i].configure(background=DARK_GRAY))

        self.pack()

    def back_(self):
        """
        Method to go back
        """
        for widget in self.master.winfo_children():
            widget.destroy()
        Register(self.master)

    def login_page(self):
        """
        Method prompting back to login page after successful registration
        """
        if self.input_validation():
            self.send_details()
            for widget in self.master.winfo_children():
                widget.destroy()
            Login(self.master)

    def send_details(self):
        """
        Sending all the details to database
        """
        cn = self.cn_entry.get().replace(' ', '')
        cvv = self.cvv_entry.get().replace(' ', '')
        exp = datetime.strptime(self.date_entry.get(), '%m/%y')
        money = self.money_entry.get()
        message = f'card,{cn},{cvv},{exp},{money}'
        client.sending_message(message)

    def input_validation(self):
        """
        Method for the input validation
        """
        if not self.card_number_validation():
            showinfo('Error', 'Card number invalid')
            return False
        elif not self.cvv_validation():
            showinfo('Error', 'CVV number invalid')
            return False
        elif not self.expiration_date_validation():
            showinfo('Error', 'Wrong expiry date')
            return False
        elif not self.money_validation():
            showinfo('Error', 'Wrong value for money-in.')
            return False
        else:
            return True

    def card_number_validation(self):
        """
        Method to validate card number
        """
        number = self.cn_entry.get().replace(' ', '')
        if not all(i.isdigit() for i in number):
            return False
        elif len(number) != 16:
            return False
        else:
            return True

    def cvv_validation(self):
        """
        Method to vaildate cvv
        """
        cvv = self.cvv_entry.get().replace(' ', '')
        if not all(i.isdigit() for i in cvv):
            return False
        elif len(cvv) != 3:
            return False
        else:
            return True

    def expiration_date_validation(self):
        """
        Method to validate card expiry date
        """
        exp_date = self.date_entry.get()
        try:
            expiry_date = datetime.strptime(exp_date, '%m/%y')
            # Parse expiry date string to datetime object

            now = datetime.now()
            # Get the current datetime

            if expiry_date < now:
                # Compare expiry date with current date

                showinfo('Error', 'Card out of date')
                return False
            else:
                return True
        except ValueError:
            showinfo('Error', 'Wrong date format - it should have been MM/YY')
            return False

    def money_validation(self):
        """
        Method validating money input
        """
        money_in = self.money_entry.get().replace(' ', '')
        if not all(i.isdigit() for i in money_in):
            return False
        else:
            return True

    def get_position(self, event):
        """
        Method allowing for movement of the window, when dragged by a toolbar
        """
        x_window = self.master.winfo_x()
        y_window = self.master.winfo_y()
        start_x = event.x_root
        start_y = event.y_root

        y_window = y_window - start_y
        x_window = x_window - start_x

        def move(event):
            self.master.geometry('+{0}+{1}'.format(event.x_root + x_window, event.y_root + y_window))

        self.title_frame.bind('<B1-Motion>', move)


class MainApp(Tk):
    """
    Class of the main application - biggest out of all of them since
    it has most of the graphic user interface in itself
    """

    def __init__(self):
        super().__init__()
        self.res_x = 1920
        self.res_y = 1080
        # Default resolution of x and y-axis of most of the monitors, used with self.scale for resizing

        self.scale = 1
        self.after_id = None
        # Basically a flag for 'after' allowing me to switch off the refreshing of the crypto frame, when I switch
        # to another frame, so the refreshed one won't replace the one I want to have in front of me at that moment.

        self.scaling()
        # Calling a method which will determine the scaling factor

        self.call('tk', 'scaling', self.scale)
        # Automatic scaling of the widgets

        self.attributes('-fullscreen', True)
        self.configure(background='black')
        self.title_frame = Frame(self, bg=DARK_GRAY, height=(self.res_y * self.scale) * 0.1)
        self.title_frame.pack(fill=X, side=TOP)
        self.budget = self.balance(ID[0])

        self.title = Label(self.title_frame, font='Verdana 20', text='CRYPTO TRADER', bd=0, fg='white', bg=DARK_GRAY)
        self.title.pack(side=LEFT, padx=5)

        self.close_button = Button(self.title_frame, width=4, text='X', bg=DARK_GRAY, fg='white', font='Verdana 20',
                                   command=exit, relief=GROOVE, bd=0)
        self.close_button.pack(side=RIGHT)
        self.close_button.bind('<Enter>', lambda event: self.close_button.configure(background='dark red'))
        self.close_button.bind('<Leave>', lambda event: self.close_button.configure(background=DARK_GRAY))

        self.main_frame = Frame(self, height=(self.res_y * self.scale), bg=GRAY)
        self.main_frame.pack(expand=True, fill=BOTH)

        self.left_frame = Frame(self.main_frame, width=(self.res_x * self.scale) * 0.2,
                                height=(self.res_y * self.scale) * 0.8, bg=DARK_GRAY2)
        self.left_frame.pack(side=LEFT, fill=BOTH, padx=2)

        self.right_frame = Frame(self.main_frame, width=(self.res_x * self.scale) * 0.8,
                                 height=(self.res_y * self.scale) * 0.8, bg=DARK_GRAY2)
        self.right_frame.pack(side=RIGHT, expand=True, fill=BOTH, padx=2)

        self.bottom_frame = Frame(self, width=self.res_x, height=(self.res_y * self.scale) * 0.2, bg=DARK_GRAY2)
        self.bottom_frame.pack(side=BOTTOM, fill=X, pady=5)

        self.image = ImageTk.PhotoImage(file='./images/cryptos_logo.png')
        self.logo_label = Label(self.left_frame, image=self.image, bd=0)
        self.logo_label.pack()

        self.welcome_label = Label(self.left_frame, text=f'Welcome {self.welcome(ID[0])}',
                                   font='Verdana 20', fg='light gray', bg=DARK_GRAY2)

        self.welcome_label.pack(fill=Y)

        self.button_options = {'master': self.left_frame, 'bg': GRAY, 'width': 15, 'bd': 0, 'relief': RAISED,
                               'fg': 'light gray', 'font': 'Verdana 20'}

        self.b1 = Button(**self.button_options, text='Account details', command=lambda: self.account_labels())
        self.b2 = Button(**self.button_options, text='Cryptos', command=lambda: self.start_update_crypto())
        self.b3 = Button(**self.button_options, text='Sell', command=lambda: self.selling_labels())
        self.b4 = Button(**self.button_options, text='Wallet', command=lambda: self.wallet_labels())
        self.b5 = Button(**self.button_options, text='Graph', command=lambda: self.graph())
        self.b6 = Button(**self.button_options, text='Withdraw/Deposit', command=lambda: self.withdraw_deposit())
        self.b7 = Button(**self.button_options, text='Transactions', command=lambda: self.transaction_labels())

        self.buttons = [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7]

        for b in self.buttons:
            b.pack(pady=10, padx=10)

        for b in range(len(self.buttons)):
            """
            Binding change of colors, when hovered over buttons
            """
            self.buttons[b].bind('<Enter>', lambda event, i=b: self.buttons[i].configure(background='dark red'))
            self.buttons[b].bind('<Leave>', lambda event, i=b: self.buttons[i].configure(background=DARK_GRAY))

        self.money_label = Label(self.left_frame, text=f'Available balance is: {self.budget} £',
                                 bg=DARK_GRAY2, fg='dark gray', font='Verdana 20')

        self.money_label.pack(side=BOTTOM)
        self.buy_image = PhotoImage(file="./images/buy_sell.png")
        self.image2 = PhotoImage(file="./images/withdraw_deposit.png")
        self.image3 = PhotoImage(file="./images/wallet.png")
        self.sell_small_image = PhotoImage(file="./images/selling_small.png")
        self.sell_big_image = PhotoImage(file="./images/selling_big.png")

    def graph(self):
        """
        Method creating matplotlib graph and embedding it in the tkinter GUI
        """
        self.fig, self.ax = plt.subplots()
        self.data = client.get_crypto()
        self.prices = {}
        for row, item in enumerate(self.data):
            # Using enumerate to iterate through list of tuples and add them to the dictionary

            coin = item[2]
            price = float(item[3])
            self.prices[coin] = price
        coin_price_pairs = list(self.prices.items())
        random.shuffle(coin_price_pairs)
        coins, prices = zip(*coin_price_pairs)
        self.stop_update_crypto()
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            # Loop which is removing previous widgests from the frame - allows for the dynamic change of widgets

        self.ax.plot(coins, prices)
        self.ax.set_ylim(min(prices), max(prices))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.toolbar_frame = Frame(self.right_frame)
        self.toolbar_frame.pack(side=BOTTOM, fill=X)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=BOTTOM, fill=X)

    def withdraw_deposit(self):
        """
        Method to create a frame for withdrawing and depositing money
        """

        self.stop_update_crypto()
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        client.get_balance(ID[0])
        spacing_frame = Frame(self.right_frame, background=DARK_GRAY2, height=(self.res_y * self.scale) * 0.2)
        spacing_frame.pack(fill=BOTH)

        logo_label = Label(self.right_frame, image=self.image2, bd=0)
        logo_label.pack()

        entry_window = Entry(self.right_frame, width=20, font='Verdana 20', justify=RIGHT, background=LIGHT_GRAY)
        entry_window.focus_set()
        entry_window.pack(pady=10)

        buttons_frame = Frame(self.right_frame, background=DARK_GRAY2, bd=0)
        buttons_frame.pack()

        self.button_options = {'master': buttons_frame, 'bg': GRAY, 'width': 15, 'bd': 0, 'relief': RAISED,
                               'fg': 'light gray', 'font': 'Verdana 20'}

        withdraw_button = Button(text='Withdraw', **self.button_options,
                                 command=lambda: self.withdraw(entry_window.get(), client.get_balance(ID[0])))
        withdraw_button.pack(side=LEFT, padx=5, pady=5)

        deposit_button = Button(text='Deposit', **self.button_options,
                                command=lambda: self.deposit(entry_window.get(), client.get_balance(ID[0])))
        deposit_button.pack(side=RIGHT, padx=5, pady=5)

        buttons = [withdraw_button, deposit_button]
        for b in range(len(buttons)):
            buttons[b].bind('<Enter>', lambda event, i=b: buttons[i].configure(background='dark red'))
            buttons[b].bind('<Leave>', lambda event, i=b: buttons[i].configure(background=DARK_GRAY))

    @staticmethod
    def withdraw(amount, balance):
        """
        Static method to withdraw money
        """
        x = eval(amount)
        y = eval(balance)
        if x > y:
            showinfo('Error', 'Not enough money in your balance')
        else:
            total = y - x
            client.withdrawal(str(total), ID[0])

    @staticmethod
    def deposit(amount, balance):
        """
        Static method to deposit money
        """
        x = eval(amount)
        y = eval(balance)
        total = y + x
        client.deposit(str(total), ID[0])

    def update_money_label(self):
        """
        Method which sets self.budget used in money label, which displays available balance
        in the left window under the buttons
        """
        self.budget = self.balance(ID[0])

    def stop_update_crypto(self):
        """
        Method checking for the flag stored in self.after_id, and letting me stop auto-update of the frame with
        cryptos
        """
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def start_update_crypto(self):
        """
        Method setting the flag for before-mentioned crypto auto-update functionality
        """
        self.crypto_labels()
        self.after_id = self.after(10000, self.start_update_crypto)

    def sell_click(self, coinid, quantity):
        """
        Method for selling cryptos
        """
        budget = eval(self.balance(ID[0]))
        price = eval(client.get_price(coinid))
        quantity = int(quantity)
        quantity_in_wallet = int(client.get_quantity(coinid))
        new_quantity = quantity_in_wallet - quantity
        total_cost = quantity * price
        new_budget = budget + total_cost
        total_cost = '+ ' + str(total_cost)
        time = datetime.now()
        time = str(time)
        transactionid = 'T' + str(random.randint(100, 10000))
        new_budget = str(new_budget)
        new_quantity = str(new_quantity)
        walletID = 'W' + ID[0] + coinid
        client.transaction_sell(walletID, ID[0], coinid, new_quantity, new_budget, time, transactionid, total_cost)
        self.update_money_label()

    def selling_labels(self):
        """
        Method creating labels in the right frame, after clicking 'sell' in the options buttons
        """
        self.stop_update_crypto()
        options = {'fg': 'light gray', 'font': 'Verdana 20'}
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        data = client.get_wallet(ID[0])
        image_label = Label(self.right_frame, image=self.sell_big_image, background=DARK_GRAY2, bd=0)
        image_label.pack()

        widget_frame = Frame(self.right_frame, background=DARK_GRAY2, bd=0)
        widget_frame.pack(fill=BOTH)

        for row, item in enumerate(data):
            # Using enumerate to iterate through list of tuples

            label1 = Label(widget_frame, text=item[0], width=25, bg=DARK_GRAY, **options)
            label1.grid(row=row, column=0, padx=5)

            label2 = Label(widget_frame, text=item[2].replace('\n', ''), bg=GRAY, width=25, **options)
            label2.grid(row=row, column=1, padx=5)

            label3 = Label(widget_frame, text=item[1], width=25, bg=DARK_GRAY, **options)
            label3.grid(row=row, column=2, padx=5)

            quantity_var = StringVar()
            quantity_spinbox = Spinbox(widget_frame, from_=0, to=int(item[4]), width=2, font='Verdana 20',
                                       textvariable=quantity_var)
            quantity_spinbox.grid(row=row, column=3)

            sell_button = Button(widget_frame, image=self.sell_small_image, width=50, height=30, bg='black',
                                 command=lambda i=item[0], q=quantity_var: self.sell_click(i, q.get()))
            sell_button.grid(row=row, column=4, columnspan=2, padx=2, pady=10)

    def wallet_labels(self):
        """
        Method creating a screen with contents of the e-wallet
        """
        self.stop_update_crypto()
        options = {'fg': 'light gray', 'font': 'Verdana 20'}
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        data = client.get_wallet(ID[0])

        logo = Label(self.right_frame, image=self.image3, background=DARK_GRAY2)
        logo.pack()
        label_frame = Frame(self.right_frame, background=DARK_GRAY2, bd=0, height=100)
        label_frame.pack(fill=BOTH)
        for row, item in enumerate(data):
            label1 = Label(label_frame, text=item[0], width=21, bg=DARK_GRAY, **options)
            label1.grid(row=row, column=0, padx=5)

            label2 = Label(label_frame, text=item[4], bg=GRAY, width=21, **options)
            label2.grid(row=row, column=1, padx=5)

            label3 = Label(label_frame, text=item[2].replace('\n', ''), width=21, bg=DARK_GRAY, **options)
            label3.grid(row=row, column=2, padx=5)

            label4 = Label(label_frame, text=item[3], width=21, bg=GRAY, **options)
            label4.grid(row=row, column=3, padx=5)

    def transaction_labels(self):
        """
        Method creating a screen with transactions
        """
        self.stop_update_crypto()
        options = {'fg': 'light gray', 'font': 'Verdana 20'}
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        data = client.get_transactions(ID[0])
        for row, item in enumerate(data):
            label1 = Label(self.right_frame, text=item[3], width=20, bg=DARK_GRAY, **options)
            label1.grid(row=row, column=0)

            label2 = Label(self.right_frame, text=item[4], width=25, bg=GRAY, **options)
            label2.grid(row=row, column=1)

            label3 = Label(self.right_frame, text=item[5], width=20, bg=DARK_GRAY, **options)
            label3.grid(row=row, column=2)

            label4 = Label(self.right_frame, text=item[6], width=25, bg=GRAY, **options)
            label4.grid(row=row, column=3)

    def crypto_labels(self):
        """
        Method displaying real life feed of the crypto
        """
        options = {'fg': 'light gray', 'font': 'Verdana 18'}
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        data = client.get_crypto()
        for row, item in enumerate(data):
            label1 = Label(self.right_frame, text=item[0], width=23, bg=DARK_GRAY, **options)
            label1.grid(row=row, column=0)

            label2 = Label(self.right_frame, text=item[1].replace('\n', ''), bg=GRAY, width=23, **options)
            label2.grid(row=row, column=1)

            label3 = Label(self.right_frame, text=item[2], width=23, bg=DARK_GRAY, **options)
            label3.grid(row=row, column=2)

            label4 = Label(self.right_frame, text=item[3], width=23, bg=GRAY, **options)
            label4.grid(row=row, column=3)

            quantity_var = StringVar()
            quantity_spinbox = Spinbox(self.right_frame, from_=0, to=100, width=2, font='Verdana 20',
                                       textvariable=quantity_var)
            quantity_spinbox.grid(row=row, column=4)

            buy_button = Button(self.right_frame, image=self.buy_image, width=50, height=30, bg='black',
                                command=lambda i=item[0], q=quantity_var: self.buy_clicked(i, q.get()))
            buy_button.grid(row=row, column=5, padx=2, pady=5)

    def account_labels(self):
        """
        Method creating account screen
        """
        self.stop_update_crypto()
        extras = ['User ID: ', '', 'First Name: ', 'Last Name', 'D.O.B: ', 'Email: ']
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
        data = list(self.account_details(ID[0]).split(','))
        for i in range(0, len(data) - 1):
            if i != 1:
                label_frame = Frame(self.right_frame, background=GRAY)
                label_frame.pack(fill=X)
                label = Label(label_frame, text=data[i], bg=GRAY, fg='light gray', font='Verdana 20')
                label.pack(fil=Y, side=RIGHT)
                lab = Label(label_frame, text=extras[i], bg=GRAY, fg='light gray', font='Verdana 20')
                lab.pack(fill=Y, side=LEFT)

    def buy_clicked(self, coinid, quantity):
        """
        Method byuying cryptos upon clicking the 'buy' button next to displayed cryptos
        """

        budget = eval(self.balance(ID[0]))
        price = eval(client.get_price(coinid))
        quantity = eval(quantity)
        total_cost = quantity * price
        new_budget = budget - total_cost
        total_cost = '- ' + str(total_cost)
        time = datetime.now()
        time = str(time)
        transactionid = 'T' + str(random.randint(100, 10000))
        if new_budget < 0:
            showinfo('Error', 'Not enough money in the account')
        else:
            new_budget = str(new_budget)
            quantity = str(quantity)
            walletID = 'W' + ID[0] + coinid
            client.transaction(walletID, ID[0], coinid, quantity, new_budget, time, transactionid, total_cost)
            self.update_money_label()

    @staticmethod
    def balance(userid):
        """
        Static method returning available balance from the database
        """
        data = client.get_balance(userid)
        return data

    @staticmethod
    def welcome(userid):
        """
        Stathic method getting a name of the user, which can be displayed in the welcome label
        """
        data = client.get_name(userid)
        return data

    @staticmethod
    def account_details(userid):
        """
        Static method getting for us user account details,
        which can be displayed after clicking 'Account details' button
        """
        data = client.get_account_details(userid)
        return data

    def scaling(self):
        """
        Method fetching information about the screen size and creating scale point, which is replaced in the
        class self parameters if it is not equal to 1
        """
        x = self.winfo_screenwidth()
        y = self.winfo_screenheight()
        result = (x + y) / (self.res_x + self.res_y)
        if result != 1:
            self.scale = result


def main():
    """
    Main function starting client and GUI on separate threads
    """
    t2 = client_main
    t1 = starting_gui
    Processes(t1).start()
    Processes(t2, True).start()



def starting_gui():
    """
    Function creating an object of application
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # Function which makes the widgets appear 'sharper'

    app = Root()
    app.mainloop()
    FirstWindow(app)


if __name__ == '__main__':
    main()
