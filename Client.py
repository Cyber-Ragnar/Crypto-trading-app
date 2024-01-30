from socket import *
import threading
from pickle import *


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
        method starting a given thread
        """
        self.t.start()


class Client:
    """
    Class creating an object for the client
    """

    def __init__(self, host='localhost', port=5006, size=1024):
        """
        :param host: sets a host - default set to 'localhost'
        :param port: sets a port - default set to '5005'
        :param size: sets a size of a buffer - default set to '1024'
        """

        self.host = host
        self.port = port
        self.buffer = size
        self.address = (self.host, self.port)
        self.message = ''
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(self.address)

    def establishing_connection(self):
        """
        Method establishing connection with a server
        """
        message = self.socket.recv(self.buffer).decode()
        self.set_message(message)

    def close_the_socket(self):
        """
        Method closing the socket
        """
        self.socket.close()

    def sending_message(self, message):
        """
        Method sending the message
        """
        self.socket.send(message.encode())

    def set_message(self, string):
        """
        Method setting the message
        """
        self.message = string

    def get_message(self):
        """
        Method allowing to see the setted message
        """
        return self.message

    def email_exist(self, email):
        """
        Method that checks if an email already exists in the server's database
        :param email: The email address to check
        :return: True if the email exists, False otherwise
        """
        self.socket.send(('email_check,' + email).encode())
        response = self.socket.recv(self.buffer).decode()
        if response == 'pass':
            return True
        else:
            return False

    def login_details(self, email, password):
        """
        Method asking server to fetch login details
        """
        self.socket.send(f'login_details,{email},{password}'.encode())
        response = self.socket.recv(self.buffer).decode()
        if response == 'pass':
            return True
        else:
            return False

    def get_transactions(self, userid):
        """
        Method asking server to fetch transactions
        """
        self.socket.send(f'transactions,{userid}'.encode())
        response = self.socket.recv(self.buffer)
        data = (b'' + response)
        data = loads(data)
        return data

    def get_id(self, email):
        """
        Method asking server to fetch userid
        """
        self.socket.send(f'userID,{email}'.encode())
        response = self.socket.recv(self.buffer).decode()
        return response

    def get_wallet(self, userid):
        """
        Method asking server to fetch data from wallet table
        """
        self.socket.send(f'wallet,{userid}'.encode())
        response = self.socket.recv(self.buffer)
        data = (b'' + response)
        data = loads(data)
        return data

    def get_balance(self, userid):
        """
        Method asking server to fetch balance
        """
        self.socket.send(f'balance,{userid}'.encode())
        response = self.socket.recv(self.buffer).decode()
        return response

    def get_name(self, userid):
        """
        Method asking server to fetch users name
        """
        self.socket.send(f'welcome,{userid}'.encode())
        response = self.socket.recv(self.buffer).decode()
        return response

    def get_account_details(self, userid):
        """
        Method asking server to fetch account details
        """
        self.socket.send(f'acc_details,{userid}'.encode())
        response = self.socket.recv(self.buffer).decode()
        return response

    def get_crypto(self):
        """
        Method asking server to fetch all the data from the 'crypto' table
        """
        self.socket.send('crypto'.encode())
        response = self.socket.recv(self.buffer)
        data = (b''+response)
        data = loads(data)
        return data

    def get_price(self, coinid):
        """
        Method asking server to fetch prices of the currencies
        """
        self.socket.send(f'price,{coinid}'.encode())
        response = self.socket.recv(self.buffer).decode()
        return response

    def get_quantity(self, coinid):
        """
        Method asking server to fetch data on available quantity in the wallet
        """
        self.socket.send(f'quantity,{coinid}'.encode())
        response = self.socket.recv(self.buffer).decode()
        return response

    def transaction(self, walletid, userid, coinid, number, new_budget, time, transactionid, value):
        """
        Method asking server to buy coins and register transaction history
        """
        self.socket.send(f'bud_upd,{walletid},{userid},{coinid},{number},'
                         f'{new_budget},{time},{transactionid},{value}'.encode())

    def transaction_sell(self, walletid, userid, coinid, number, new_budget, time, transactionid, value):
        """
        Method asking server to sell coins and register transaction history
        """
        self.socket.send(f'sell,{walletid},{userid},{coinid},{number},'
                         f'{new_budget},{time},{transactionid},{value}'.encode())

    def withdrawal(self, amount, userid):
        """
        Method asking server for a withdrawal (update balance in the 'user' table).
        """
        self.socket.send(f'withdrawal,{amount},{userid}'.encode())

    def deposit(self, amount, userid):
        """
        Method asking server to deposit money (update balance in the 'user' table).
        """
        self.socket.send(f'deposit,{amount},{userid}'.encode())


client = Client()


def client_main():
    """
    Main function of this file, calling and connecting other files and their respective
    functionalities bringing 'Client' to life as a one organism.
    """

    p1 = client.establishing_connection()
    Processes(p1, True).start()
