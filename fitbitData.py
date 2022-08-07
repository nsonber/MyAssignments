"""
31-Jul-2022
#Task 1 - Fitbit Dataset

1. Read this dataset in pandas , mysql and mongodb
2. while creating a table in mysql don't use manual approach to create it,
    always use automation to create a table in mysql
 ## hint - use csvkit library to automate this task and to load a data in bulk in you mysql
3. convert all the dates available in dataset to timestamp format in pandas and in sql you to convert it in date format
4 . Find out in this data that how many unique id's we have
5 . which id is one of the active id that you have in whole dataset
6 . how many of them have not logged there activity find out in terms of number of ids
7 . Find out who is the laziest person id that we have in dataset
8 . Explore over an internet that how much calories burn is required for a healthy person and find out
    how many healthy person we have in our dataset
9. how many person are not a regular person with respect to activity try to find out those
10 . who is the third most active person in this dataset find out those in pandas and in sql both .
11 . who is the 5th laziest person available in dataset find it out
12 . what is a total cumulative calories burn for a person find out
"""

import pandas as pd
import logging
import logging.handlers
import mysql.connector as conn
import pymongo


def init_logger():
    """
        Static method to initialize the logger.
    """
    # self.lg.basicConfig(filename=r'.\logs\Fitbit.log', level=self.lg.INFO,
    #                format='%(asctime)s - %(levelname)s - %(message)s')

    LOG_FILE = r'.\logs\Fitbit.log'
    # logger for console and file
    logging.getLogger().setLevel(logging.INFO)
    lg = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # console
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)
    # file
    filehandler = logging.FileHandler(LOG_FILE)
    filehandler.setFormatter(formatter)
    filehandler.setLevel(logging.INFO)

    lg.addHandler(console)
    lg.addHandler(filehandler)

    lg.info("----------------------------")
    return lg


class FitbitData:
    """
    A class to analyze FitBit data.
    """
    __dbname = ''

    def __init__(self):
        """
        Init method of the FitbitData class, which will invoke the logger and set the class attributes.
        """
        self.cursor = None
        self.db = None
        self.df = pd.DataFrame()
        self.lg = init_logger()

    def get_sqldb_conn(self, username, password, dbname):
        """
        Function creates a connection to mysql database.
        It also creates and sets the database if not set already for the class object.

        :param username: Username of the mysql db to connect
        :param password: Password of mysql db
        :param dbname: Database name
        :return: True --> if successfully connected to database
                 False --> if database connection is not acquired
        """

        try:
            self.lg.info("Getting SQL DB connection")
            self.db = conn.connect(host='localhost',
                                   user=username,
                                   passwd=password
                                   )

            self.cursor = self.db.cursor(buffered=True)

            self.lg.debug(f"Database is set to {self.__dbname}")
            # print(f"Database is set to {self.__dbname}")

            if len(self.__dbname) == 0:
                self.lg.info("Creating DB for the first time")
                self.cursor.execute(f"create database if not exists {dbname}")
                self.__dbname = dbname

            self.cursor.execute(f"use {dbname}")

        except Exception as e:
            self.lg.error("Error encountered while acquiring SQL DB connection")
            self.lg.error(e)
            return False

        self.lg.info("SQL DB connection acquired")

        return True

    def close_db(self):
        self.db.close()

    def get_nosql_db(self, username, password, dbname, collection):
        """
        Method creates a collection in MongoDb and returns
        :return:
        """
        self.lg.info("Getting Mongo DB connection")
        hostname = 'cluster0.iertm.mongodb.net/?retryWrites=true&w=majority'
        conn_str = "mongodb+srv://" + username + ":" + password + "@" + hostname
        client = pymongo.MongoClient(conn_str)
        db = client[dbname]
        coll = db[collection]
        self.lg.info("Mongo DB connection acquired")
        return coll

    def read_data(self, filename: str):
        try:
            self.lg.info("Reading the file")
            self.df = pd.read_csv(filename)
        except Exception as e:
            self.lg.error("Error occurred while reading the file")
            self.lg.error(str(e))

    def create_table(self):
        """
        Function creates table of FITBIT_DATA in mysql database.
        :return:
        """

        # get db connection and cursor
        self.get_sqldb_conn(username='root', password="Mysql@Jul22", dbname='FitBit')

        statement = 'CREATE TABLE IF NOT EXISTS `FitBit_data` (' \
                    '`Id` DECIMAL(38, 0) NOT NULL,' \
                    '`ActivityDate` DATE NOT NULL,' \
                    '`TotalSteps` DECIMAL(38, 0) NOT NULL,' \
                    '`TotalDistance` DECIMAL(38, 17) NOT NULL,' \
                    '`TrackerDistance` DECIMAL(38, 17) NOT NULL,' \
                    '`LoggedActivitiesDistance` DECIMAL(38, 15) NOT NULL,' \
                    '`VeryActiveDistance` DECIMAL(38, 17) NOT NULL,' \
                    '`ModeratelyActiveDistance` DECIMAL(38, 16) NOT NULL,' \
                    '`LightActiveDistance` DECIMAL(38, 17) NOT NULL,' \
                    '`SedentaryActiveDistance` DECIMAL(38, 17) NOT NULL,' \
                    '`VeryActiveMinutes` DECIMAL(38, 0) NOT NULL,' \
                    '`FairlyActiveMinutes` DECIMAL(38, 0) NOT NULL,' \
                    '`LightlyActiveMinutes` DECIMAL(38, 0) NOT NULL,' \
                    '`SedentaryMinutes` DECIMAL(38, 0) NOT NULL,' \
                    '`Calories` DECIMAL(38, 0) NOT NULL)'

        try:
            self.cursor.execute(statement)
        except Exception as e:
            self.lg.error("Error encountered while creating table")
            self.lg.error(str(e))

        self.close_db()

        return

    def insert_into_mysql(self):
        """
        Function performs a check if data already exist in the Fitbit table,
        If no data present, then it inserts the data into table, else it skips.
        :return:
        """

        self.get_sqldb_conn(username='root', password="Mysql@Jul22", dbname='FitBit')

        try:
            # check if data already exists in the table
            self.cursor.execute("SELECT COUNT(*) FROM FitBit_data")

            record = self.cursor.fetchall()

            if record[0][0] == 0:

                self.lg.info("Inserting data to FitBit_data")
                i = 0
                for index, row in self.df.fillna('').iterrows():
                    self.cursor.execute(
                        'INSERT INTO FITBIT_DATA (ID, ACTIVITYDATE, TOTALSTEPS, TOTALDISTANCE'
                        ', TRACKERDISTANCE, LOGGEDACTIVITIESDISTANCE, VERYACTIVEDISTANCE, MODERATELYACTIVEDISTANCE'
                        ', LIGHTACTIVEDISTANCE, SEDENTARYACTIVEDISTANCE, VERYACTIVEMINUTES, FAIRLYACTIVEMINUTES'
                        ', LIGHTLYACTIVEMINUTES, SEDENTARYMINUTES, CALORIES)'
                        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (row['Id'], row['ActivityDate'], row['TotalSteps'], row['TotalDistance'],
                         row['TrackerDistance'], row['LoggedActivitiesDistance'], row['VeryActiveDistance'],
                         row['ModeratelyActiveDistance'], row['LightActiveDistance'], row['SedentaryActiveDistance'],
                         row['VeryActiveMinutes'], row['FairlyActiveMinutes'], row['LightlyActiveMinutes'],
                         row['SedentaryMinutes'], row['Calories']
                         )
                    )
                    i = index

                self.cursor.execute('commit')

                self.lg.info(f"Inserted {i} records to FitBit_data")
            self.close_db()

        except Exception as e:
            self.lg.error("Error encountered while inserting data")
            self.lg.error(str(e))
            self.close_db()
            return False
        return True

    def insert_df_to_mongodb(self):
        """
        Function inserts data to MongoDB
        :return:
        """
        coll = self.get_nosql_db('ineuronmongo', 'ineuron1', 'FitBit', 'FitBitData')
        coll.delete_many({})
        try:
            coll.insert_many(self.df.to_dict('records'))

            self.lg.info(f"Inserted {len(self.df)} records to MongoDB")
        except Exception as e:
            self.lg.error("Error encountered while inserting data to MongoDB")
            self.lg.exception(e)
            return False
        return True

    def answers_using_pandas(self):
        """
        Function returns answers to following questions using pandas only.

        4 . Find out in this data that how many unique id's we have
        5 . which id is one of the active id that you have in whole dataset
        6 . how many of them have not logged there activity find out in terms of number of ids
        7 . Find out who is the laziest person id that we have in dataset
        8 . Explore over an internet that how much calories burn is required for a healthy person and find out
            how many healthy person we have in our dataset
        9. how many person are not a regular person with respect to activity try to find out those
        10 . who is the third most active person in this dataset find out those in pandas and in sql both .
        11 . who is the 5th laziest person available in dataset find it out
        12 . what is a total cumulative calories burn for a person find out
        :return:
        """

        self.lg.info("4 . Find out in this data that how many unique id's we have?")
        self.lg.info(f"Total unique IDs in data : {len(self.df['Id'].unique())}")
        self.lg.info("5 . which id is one of the active id that you have in whole dataset?")
        mostactiveid = \
            self.df.groupby(['Id'])['VeryActiveMinutes'].sum().reset_index().sort_values(by=['VeryActiveMinutes'],
                                                                                         ascending=False).head(1)['Id']
        self.lg.info(f"Most active ID : {mostactiveid.values[0]}")
        self.lg.info("6 . how many of them have not logged there activity find out in terms of number of ids")

        temp_df = self.df.groupby(['Id'])['LoggedActivitiesDistance'].sum().reset_index().sort_values(
            by=['LoggedActivitiesDistance'], ascending=True)
        temp_df2 = temp_df[temp_df['LoggedActivitiesDistance'] == 0]

        self.lg.info(f"IDs with No LoggedActivitiesDistance ")
        self.lg.info(temp_df2)

        self.lg.info("7 . Find out who is the laziest person id that we have in dataset")
        temp_df = self.df.groupby(['Id'])['SedentaryMinutes'].sum().reset_index().sort_values(
            by=['SedentaryMinutes'], ascending=False).head(1)['Id']
        self.lg.info(f"Laziest ID based on most SedentaryMinutes : {temp_df.values[0]}")

        self.lg.info("8 . Explore over an internet that how much calories burn is required for a healthy" +
                     "person and find out how many healthy person we have in our dataset")
        temp_df = self.df.groupby(['Id'])['Calories'].sum().reset_index()
        temp_df = temp_df[temp_df['Calories'] >= 2200]['Id'].unique()

        self.lg.info(f"Healthy IDs who have lost more than 2200 calories per week: {temp_df}")

        self.lg.info("9. how many persons are not regular with respect to activity")
        temp_df = self.df.groupby(['Id'])['Calories'].var().reset_index().sort_values(by=['Calories'], ascending=False)
        temp_df = temp_df['Id'].head(5)
        self.lg.info(f"Top 5 irregular persons based on Variance in Calories lost : {temp_df}")

        self.lg.info("10 . who is the third most active person in this dataset find out those in pandas")
        mostactiveid = \
            self.df.groupby(['Id'])['VeryActiveMinutes'].sum().reset_index().sort_values(by=['VeryActiveMinutes'],
                                                                                         ascending=False).head(3).tail(
                1)['Id']
        self.lg.info(f"Third most active person based on VeryActiveMinutes : {mostactiveid.values[0]}")

        self.lg.info("11 . who is the 5th laziest person available in dataset find it out")

        temp_df = self.df.groupby(['Id'])['SedentaryMinutes'].sum().reset_index().sort_values(
            by=['SedentaryMinutes'], ascending=False).head(5).tail(1)['Id']

        self.lg.info(f"5th laziest person based on most SedentaryMinutes : {temp_df.values[0]}")

        self.lg.info("12 . what is a total cumulative calories burn for a person find out")
        temp_df = self.df.groupby(['Id'])['Calories'].sum().reset_index().sort_values(
            by=['Calories'], ascending=False)

        self.lg.info(f"Cumulative calories burned by each person : {temp_df}")

        return True

    def answers_using_mysql(self):
        """
        Function analyzes Fitbit data stored in MongoDb collection and provides answers to questions asked on 31-Jul-2022
        :param self:
        :return:
        """
        self.get_sqldb_conn(username='root', password="Mysql@Jul22", dbname='FitBit')

        self.lg.info("4 . Find out in this data that how many unique id's we have?")

        statement = "SELECT COUNT(distinct ID) FROM fitbit_data"
        self.cursor.execute(statement)
        records = self.cursor.fetchall()

        self.lg.info(f"Total unique IDs in data : {records[0][0]}")
        self.lg.info("5 . which id is one of the active id that you have in whole dataset?")

        statement = "SELECT ID FROM fitbit_data"


        self.lg.info(f"Most active ID : {mostactiveid.values[0]}")

        self.close_db()
