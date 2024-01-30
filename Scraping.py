import time
from bs4 import *
import requests
import threading
from Database_manipulation import *


class Scraping:
    """
    creating class 'Scraping' for necessary data scraping, data which will be uploaded into the SQL database on a
    later stage
    """

    def __init__(self, url):
        """
        :param url: base url which I will build the scraping around
        """
        self.__url = url
        self.__r = requests.get(self.__url)
        self.__soup = BeautifulSoup(self.__r.text, 'html.parser')
        self.__extensions = ['/coin/Qwsogvtv82FCd+bitcoin-btc',
                             '/coin/razxDUgYGNAdQ+ethereum-eth',
                             '/coin/HIVsRcGKkPFtW+tetherusd-usdt',
                             '/coin/WcwrkfNI4FUAe+bnb-bnb',
                             '/coin/aKzUVe4Hh_CON+usdc-usdc',
                             '/coin/-l8Mn2pVlRs-p+xrp-xrp',
                             '/coin/PDKcptVnzJTmN+okb-okb',
                             '/coin/qzawljRxB5bYu+cardano-ada',
                             '/coin/uW2tk-ILY0ii+polygon-matic',
                             '/coin/a91GCGd_u96cF+dogecoin-doge',
                             '/coin/vSo2fu9iE1s0Y+binanceusd-busd',
                             '/coin/25W7FG7om+polkadot-dot',
                             '/coin/zNZHO_Sjf+solana-sol',
                             '/coin/Mtfb0obXVh59u+wrappedether-weth',
                             '/coin/VLqpJwogdhHNb+chainlink-link',
                             '/coin/ymQub4fuB+filecoin-fil',
                             '/coin/qUhEFk1I61atv+tron-trx',
                             '/coin/MoTuySvg7+dai-dai',
                             '/coin/D7B1x_ks7WhV5+litecoin-ltc',
                             '/coin/_H5FVG9iW+uniswap-uni']
        """
        self.__extensions: list of the extensions, which will be added to the base url in a for loop, to scrape the 
        information about 20 different crypto-currencies that we are interested in...
        """

    def get_url(self):
        """
        :return: returns the value assigned to the variable '__url'.
        """
        return self.__url

    def get_extensions(self):
        """
        :return: returns a list of extension links, allows data manipulation inside the list
        """
        return self.__extensions

    def find(self, par1, par2):
        """
        :param par1: parameter 1 - has to be filled with a type of the paragraph
        :param par2: parameter 2 - name of the class_ within the source code, which is desired
        :return: returns text version of data that we are looking for
        """
        x = self.__soup.find_all(f'{par1}', class_=f'{par2}')
        for i in x:
            return i.getText()[13:-9:]

    def find_price(self, par1, par2):
        """
        :param par1: HTML tag of the element
        :param par2: Class name of the element
        :return: Text version of data that we are looking for
        """
        # Find the element using BeautifulSoup
        element = self.__soup.find(par1, class_=par2)

        if element:
            # Extract the text content
            text_content = element.get_text(strip=True)

            # Filter out non-numeric characters
            numeric_text = ''.join([char for char in text_content if char.isdigit() or char == '.'])

            return numeric_text
        else:
            return None

    def find_symbol(self, par1, par2):
        """
        :param par1: parameter 1 - has to be filled with a type of the paragraph
        :param par2: parameter 2 - name of the class_ within the source code, which is desired
        :return: returns text version of data that we are looking for
        """
        x = self.__soup.find(f'{par1}', class_=f'{par2}').text.strip()
        string = ''.join([i for i in x if i.isupper()])
        return string


########################################################################################################################


def scraping_main():
    """
    main function of that file
    """

    t = 10

    # 't' variable stands for 'time' - it is being used in the while loop in the 'sleep' function, to allow me refresh
    # the records every 't' seconds...

    webs = []

    web = Scraping('https://coinranking.com')
    ext = Scraping.get_extensions(web)
    for i in ext:
        """
        'For' loop creating urls by combining base url provided to the class, with the extensions available
         within that class. """
        i = web.get_url() + i
        webs.append(i)
    while True:
        """
        'While' loop which is calling 'scraping_names_and_prices' function every 'n' seconds (using 'time' module)
         to have the 'live' update on the data required.
         That data will be updated in SQL database on later stage of the code.
         """
        threading.Thread(target=scraping_names_and_prices(webs)).start()
        time.sleep(t)


def scraping_names_and_prices(websites):
    """
    :param websites: takes the list as a parameter
    function which scrapes the data for us
    """
    TRADER = DataBase()

    # Declaring a database object in variable 'TRADER'

    counter = 0

    # Starting value of the counter which will increment with each iteration of the 'for' loop,
    # to create unique PK for the records in table 'Crypto'
    for i in websites:
        x = Scraping(i)
        name = x.find('h1', 'hero-coin__name')
        price = x.find_price('div', "hero-coin__price")
        symbol = x.find_symbol('div', 'hero-coin__symbol')
        query = f"INSERT INTO Crypto (CryptoID, CName, Symbol, Price)" \
                f"VALUES (%s, %s, %s, %s)" \
                f"ON DUPLICATE KEY UPDATE CryptoID = VALUES(CryptoID)," \
                f" CName = VALUES(CName), Symbol = VALUES(Symbol), Price = VALUES(Price); "
        # Using 'ON DUPLICATE KEY UPDATE' syntax to avoid duplication of data and errors coming with it,
        # I want these records to be updated with every iteration of the 'While' loop.
        # Using that statement over the 'UPDATE' for the first time iteration - it would not have anything to update
        # without any existing records

        TRADER.set_query(query)
        if counter < 9:
            counter += 1
            c = '0' + str(counter)
            code = 'C' + c
            values = [(code, name, symbol, price)]
            TRADER.set_values(values)
            TRADER.insert_data()
        else:
            counter += 1
            c = str(counter)
            code = 'C' + c
            values = [(code, name, symbol, price)]
            TRADER.set_values(values)
            TRADER.insert_data()

