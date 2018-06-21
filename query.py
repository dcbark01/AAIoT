import pyodbc
import pandas as pd


class QuerySqlPID(object):

    # Default settings for connecting to AA Houston Azure SQL database. Can be overridden when creating class.
    __SERVER = 'aaiot.database.windows.net'
    __DB = 'AAIoT'
    __DRIVER = '{ODBC Driver 13 for SQL Server}'

    def __init__(self, server=None, database=None, username=None, password=None, driver=None):
        if server is None:
            self.server = self.__SERVER
        else:
            self.server = server
        if database is None:
            self.database = self.__DB
        else:
            self.database = database
        if username is None:
            try:
                from credentials.credentials import aahouston
                self.username = aahouston.username
            except ImportError as e:
                self.username = input('Enter Azure SQL DB Username: ')
        if password is None:
            try:
                from credentials.credentials import aahouston
                self.password = aahouston.password
            except ImportError as e:
                self.password = input('Enter Azure SQL DB Password: ')
        if driver is None:
            self.driver = self.__DRIVER
        else:
            self.driver = driver

        self.connection = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1443;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)

    def query(self, query_sql):
        df = pd.read_sql(query_sql, self.connection)
        return df

    def query_all(self, query_sql=None):
        query_sql = query_sql if query_sql is not None else "SELECT deviceID, tstamp, temperature, humidity, pressure, pidVolts, pidPPM, pidCal, pidCalDate FROM AAIoT_Test"
        return self.query(query_sql=query_sql)


if __name__ == "__main__":

    db = QuerySqlPID()
    # sample_query = "SELECT deviceID, tstamp, temperature, humidity, pressure, pidVolts, pidPPM, pidCal, pidCalDate FROM AAIoT_Test"
    # df = db.query(sample_query)
    # print(df.head())
    # print(df.tail())
    # print(df.shape)
    # df.to_csv('example_data.csv')

    df = db.query_all()
    print(df.head())
    print(df.tail())
    print(df.shape)

    # location_query = "SELECT lat, lon FROM pidSensors"
    # df_loc = db.query(location_query)
    # print(df_loc.head())
    # print(df_loc.tail())
    # print(df_loc.shape)
