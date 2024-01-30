import mysql.connector as mysql


class DataBase:
    """
    creating class DataBase, which I am going to use to manipulate data within my SQL database
    """
    def __init__(self, host='localhost', name='root', password='t7x5RmyQFFdDPA4p2433fyKGjmclYq2C', database='trader'):
        self.db = mysql.connect(
            host=host,
            user=name,
            password=password,
            database=database)
        self.cursor = self.db.cursor()
        self.query = ''
        self.values = None

    def set_query(self, query):
        """
        method setting a query for SQL syntax
        :param query: query which we will pass from a variable to set
        :return:
        """
        self.query = query

    def get_query(self):
        """
        method allowing me to see what query is currently set for specified object
        :return: returns value of 'self.query'
        """
        return self.query

    def set_values(self, values):
        """
        method setting values for the SQL syntax to be used alongside querry to manipulate SQL database
        :param values: values being passed on while calling the method
        :return:
        """
        self.values = values

    def get_values(self):
        """
        method allowing me to see current value of 'values' in specified object
        :return: returns 'self.values'
        """
        return self.values

    def insert_data(self):
        """
        method allowing me to execute querries in SQL by combining them with values and using function 'commit'
        :return:
        """
        self.cursor.executemany(self.query, self.values)
        self.db.commit()
        return self.cursor.rowcount

    def fetch_wallet(self, userid):
        """
        Method with SQL syntax to get the contents of the 'wallet' table
        :param userid: passes userid of currently logged-in user, to use it as an identifier in an SQL syntax
        :return:
        """
        self.cursor.execute(f"SELECT crypto.CryptoID, crypto.Price, CName, Symbol, Ammount FROM crypto "
                            f"INNER JOIN wallet ON crypto.CryptoID = wallet.CryptoID  AND wallet.userID = '{userid}';")
        data = self.cursor.fetchall()
        print(data)
        return data

    def fetch_one_record(self, what, table, column, attribute):
        """
        Method allowing for custom SQL syntaxes,
        what should help with reusing the same function for more than one operation
        """
        self.cursor.execute(f"SELECT {what} from {table} WHERE {column}='{attribute}';")
        data = self.cursor.fetchone()[0]
        data = str(data)
        return data

    def fetch_id(self, email):
        """
        Method which gets for us the userid based on the email, that user have used to log-in,
        it is being passed into a temporary container on the client side, where it is being used
        to create multiple SQL querries based on userid as an identifier.
        """
        self.cursor.execute(f"SELECT userID FROM user WHERE Email='{email}';")
        data = self.cursor.fetchone()[0]
        print(data)
        return data

    def fetch_one(self, table, userid):
        """
        Method which confirms if the email exists in the database to determine if the user exists already on
        the log-in stage of the application
        """
        self.cursor.execute(f"SELECT * FROM {table} WHERE Email='{userid}';")
        row = self.cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def fetch_password(self, email, password):
        """
        Method which gets password from a database and compares it with an input on the log-in page.
        """
        self.cursor.execute(f"SELECT Password FROM user WHERE Email = '{email}';")
        data = self.cursor.fetchone()[0]
        if password == data:
            return True
        else:
            return False

    def check_wallet(self, coinid):
        """
        Method which determines which SQL syntax to use for either
        inputting or updating existing data in the wallet table.
        """
        self.cursor.execute(f"SELECT * FROM wallet WHERE CryptoID = '{coinid}';")
        data = self.cursor.fetchone()
        if data is None:
            return False
        else:
            return True

    def fetch_ammount(self, coinid):
        """
        Method which checks how much of the specified currency user owes in the wallet,
        so he/she cannot sell more than he/she actually owes.
        :param coinid:
        :return:
        """
        print(coinid)
        self.cursor.execute(f"SELECT Ammount FROM wallet WHERE CryptoID = '{coinid}'")

        data = self.cursor.fetchone()[0]
        return data

    def fetch_all_specified(self, table, identifier):
        """
        Multiple use method for SQL syntax.
        """
        self.cursor.execute(f"SELECT * from {table} WHERE userID = '{identifier}';")
        records = self.cursor.fetchall()
        return records

    def fetch_all(self, table):
        """
        method designed to fetch all data from a table in database, which name has been passed in the parameter
        :param table: name of the table desired
        :return: returns all the records in new lines each using a 'for' loop
        """
        self.cursor.execute(f'SELECT * from {table} ;')
        records = self.cursor.fetchall()
        return records

    def fetch_price(self, coinid):
        """
        Method getting a current prices from the crypto table, for accurate sale prices. (When user is selling)
        """
        self.cursor.execute(f"SELECT Price FROM crypto WHERE CryptoID = '{coinid}'")
        data = self.cursor.fetchone()[0]
        return data

    def fetch_row(self, table, userid):
        """
        Method of multiple use, which gets the whole row of data from the database.

        """
        self.cursor.execute(f"SELECT * FROM {table} WHERE userID = '{userid}';")
        data = self.cursor.fetchall()[0]
        variable = ''
        for i in range(len(data)):
            variable = variable + ',' + str(data[i])
        variable = variable[1::]
        return variable

    def execute(self, num=0):
        """
        Method to execute single query
        :return: prints out number of rows of data affected
        """
        if num == 1:
            query = self.query
            self.cursor.execute(query)
            return self.cursor.rowcount
        if num == 0:
            return print(self.cursor.rowcount, 'rows affected')

########################################################################################################################
