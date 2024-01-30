from Scraping import *
from socket import *
from pickle import *


db = DataBase()


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


class Server:
    """
    Class creating an object pof the server
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

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.address)
        self.clients = []

    def listening(self, num_of_client):
        """
        Method allowing server a connection with the specified number of clients
        :param num_of_client: parameter passed into '.listen()' setting a number of clients, that server
        is listening to simultaneously
        """
        self.socket.listen(num_of_client)

    def handle_client(self, client, address):
        """
        Method to handle incoming client connections using the first input in the list,
        from the command send through 'socket'. it checks for prompts and according, to the
        commands allows server to execute commands necessary to manipulate database.
        :param client: client socket object
        :param address: client address tuple
        """
        userID = []
        print(f'Connection from: {address}')
        client.send('Connected to a server...'.encode())
        while True:
            message = client.recv(self.buffer).decode()
            if message == 'end':
                # Conditional statement to use secure port closing, it will be used to close application
                print('Closing connection and port...')
                client.send('Connection securely closed...'.encode())
                self.clients.remove(client)
                client.close()
                # Secure closing of the port, so it can be used again within short period of time
                break
                # Exit loop and close connection with the client
            else:
                message_list = list(message.split(','))
                if message_list[0] == 'email_check':
                    checker = self.email_check(message_list[1])
                    if not checker:
                        client.send('pass'.encode())
                    else:
                        client.send('error'.encode())

                elif message_list[0] == 'login_details':
                    checker = self.login_details(message_list[1], message_list[2])
                    if checker:
                        client.send('pass'.encode())
                    else:
                        client.send('error'.encode())

                elif message_list[0] == 'user':
                    userID.append(message_list[1])
                    query = "INSERT INTO user (userID, Password, Fname, Lname, DOB, Email, Budget) " \
                            "VALUES (%s, %s, %s, %s, %s, %s, %s);"
                    db.set_query(query)
                    values = [(message_list[1], message_list[6], message_list[2],
                               message_list[3], message_list[4], message_list[5], '0')]
                    db.set_values(values)
                    # db.insert_data()

                elif message_list[0] == 'card':
                    db.insert_data()
                    query = "INSERT INTO card (Card_num, UserID, CVV, EXP_DATE) " \
                            "VALUES (%s, %s, %s, %s);"
                    db.set_query(query)
                    values = [(message_list[1], userID[0], message_list[2], message_list[3])]
                    db.set_values(values)
                    db.insert_data()
                    query2 = "UPDATE user SET Budget = %s WHERE userID = %s;"
                    db.set_query(query2)
                    values = [(message_list[4], userID[0])]
                    db.set_values(values)
                    db.insert_data()
                    userID.pop()

                elif message_list[0] == 'userID':
                    data = self.userid(message_list[1])
                    client.send(data.encode())

                elif message_list[0] == 'balance':
                    data = self.record('Budget', 'user', 'userID', message_list[1])
                    client.send(data.encode())

                elif message_list[0] == 'welcome':
                    data = self.record('Fname', 'user', 'userID', message_list[1])
                    client.send(data.encode())

                elif message_list[0] == 'acc_details':
                    data = db.fetch_row('user', message_list[1])
                    client.send(data.encode())

                elif message_list[0] == 'crypto':
                    data = db.fetch_all('crypto')
                    data = dumps(data)
                    client.send(data)

                elif message_list[0] == 'price':
                    data = db.fetch_price(message_list[1])
                    client.send(data.encode())

                elif message_list[0] == 'bud_upd':

                    if db.check_wallet(message_list[3]):
                        amount_have = int(db.fetch_ammount(message_list[3]))
                        amount_bought = int(message_list[4])
                        new_ammount = str(amount_have + amount_bought)
                        query = "INSERT INTO wallet (WalletID, UserID, CryptoID, Ammount) VALUES (%s, %s, %s, %s)" \
                                "ON DUPLICATE KEY UPDATE WalletID = VALUES(WalletID), UserID = VALUES(UserID)," \
                                " CryptoID = VALUES(CryptoID), Ammount = VALUES(Ammount);"
                        db.set_query(query)
                        values = [(message_list[1], message_list[2], message_list[3], new_ammount)]
                        db.set_values(values)
                        db.insert_data()
                    else:
                        query2 = "INSERT INTO wallet (WalletID, UserID, CryptoID, Ammount) VALUES (%s, %s, %s, %s)"
                        db.set_query(query2)
                        values2 = [(message_list[1], message_list[2], message_list[3], message_list[4])]
                        db.set_values(values2)
                        db.insert_data()


                    query2 = "UPDATE user SET Budget = %s WHERE userID = %s;"
                    db.set_query(query2)
                    values2 = [(message_list[5], message_list[2])]
                    db.set_values(values2)
                    db.insert_data()
                    query3 = "INSERT INTO transactions (TransactionID, UserID, WalletID, CryptoID, DOT, Amount, Value) " \
                             "VALUES (%s, %s, %s, %s, %s, %s, %s);"
                    db.set_query(query3)
                    values3 = [(message_list[7], message_list[2], message_list[1], message_list[3],
                                message_list[6], message_list[4], message_list[8])]
                    db.set_values(values3)
                    db.insert_data()

                elif message_list[0] == 'sell':
                    if db.check_wallet(message_list[3]):
                        query = "INSERT INTO wallet (WalletID, UserID, CryptoID, Ammount) VALUES (%s, %s, %s, %s)" \
                                "ON DUPLICATE KEY UPDATE WalletID = VALUES(WalletID), UserID = VALUES(UserID)," \
                                " CryptoID = VALUES(CryptoID), Ammount = VALUES(Ammount);"
                        db.set_query(query)
                        values = [(message_list[1], message_list[2], message_list[3], message_list[4])]
                        db.set_values(values)
                        db.insert_data()
                    else:
                        query2 = "INSERT INTO wallet (WalletID, UserID, CryptoID, Ammount) VALUES (%s, %s, %s, %s)"
                        db.set_query(query2)
                        values2 = [(message_list[1], message_list[2], message_list[3], message_list[4])]
                        db.set_values(values2)
                        db.insert_data()

                    query2 = "UPDATE user SET Budget = %s WHERE userID = %s;"
                    db.set_query(query2)
                    values2 = [(message_list[5], message_list[2])]
                    db.set_values(values2)
                    db.insert_data()
                    query3 = "INSERT INTO transactions (TransactionID, UserID, WalletID, CryptoID, DOT, Amount, Value) " \
                             "VALUES (%s, %s, %s, %s, %s, %s, %s);"
                    db.set_query(query3)
                    values3 = [(message_list[7], message_list[2], message_list[1], message_list[3],
                                message_list[6], message_list[4], message_list[8])]
                    db.set_values(values3)
                    db.insert_data()


                elif message_list[0] == 'transactions':

                    data = db.fetch_all_specified('transactions', message_list[1])
                    data = dumps(data)
                    client.send(data)

                elif message_list[0] == 'wallet':
                    data = db.fetch_wallet(message_list[1])
                    data = dumps(data)
                    client.send(data)

                elif message_list[0] == 'quantity':
                    data = db.fetch_one_record('Ammount', 'wallet', 'CryptoID', message_list[1])
                    client.send(data.encode())

                elif message_list[0] == 'withdrawal':
                    query = "UPDATE user SET Budget = %s WHERE userID = %s;"
                    db.set_query(query)
                    values = [(message_list[1], message_list[2])]
                    db.set_values(values)
                    db.insert_data()

                elif message_list[0] == 'deposit':
                    query = "UPDATE user SET Budget = %s WHERE userID = %s;"
                    db.set_query(query)
                    values = [(message_list[1], message_list[2])]
                    db.set_values(values)
                    db.insert_data()

    def establishing_connection(self):
        """
        Method to establish connections with multiple clients using threads
        """
        while True:
            print('Waiting for connection...')
            (client, address) = self.socket.accept()
            self.clients.append(client)
            client_thread = threading.Thread(target=self.handle_client, args=(client, address), daemon=True)
            client_thread.start()


    @staticmethod
    def email_check(data):
        """
        Method returning 'True' if the email exists in the database
        :param data:
        :return:
        """
        check = db.fetch_one('user', f'{data}')
        return check

    @staticmethod
    def login_details(email, password):
        """
        Method returning true if login details are correct
        :param email:
        :param password:
        :return:
        """
        check = db.fetch_password(email, password)
        if check:
            # print(True)
            return True
        else:
            # print(False)
            return False

    @staticmethod
    def userid(email):
        """
        Method retrieving user id from the SQL
        :param email:
        :return:
        """
        print(email)
        data = db.fetch_id(email)
        return data

    @staticmethod
    def record(what, table, column, attribute):
        """
        Universal method shich can be used for various syntaxes manipulating database
        :param what:
        :param table:
        :param column:
        :param attribute:
        :return:
        """
        data = db.fetch_one_record(what, table, column, attribute)
        return data

    @staticmethod
    def acc_details(userid):
        pass


def main():
    """
    Main function of this file, calling and connecting other files and their respective
    functionalities bringing 'Server' to life as a one organism.
    """
    t1 = scraping_main
    t2 = starting_server
    Processes(t1, True).start()
    Processes(t2).start()


def starting_server():
    """
    Function bringing server to life
    :return:
    """
    server = Server()
    server.listening(5)
    server.establishing_connection()


if __name__ == '__main__':
    main()
