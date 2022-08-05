import pandas as pd
import logging as lg
import mysql.connector as conn
import pymongo


def init_logger():
    lg.basicConfig(filename=r'.\logs\DressDataLog.log', level=lg.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')


def close_logger():
    lg.shutdown()


class Dress:

    def __init__(self):
        self.cursor = None
        self.db = None
        init_logger()

    def get_sqldb_conn(self):

        try:
            lg.info("Getting SQL DB connection")
            self.db = conn.connect(host='localhost',
                                   user='root',
                                   passwd="Mysql@Jul22"
                                   )

            self.cursor = self.db.cursor(buffered=True)
            self.cursor.execute("use dress_sales")
        except Exception as e:
            lg.error("Error encountered while acquiring SQL DB connection")
            lg.error(e)

        lg.info("SQL DB connection acquired")

        return

    def close_db(self):
        self.db.close()

    def get_nosql_db(self):
        client = pymongo.MongoClient(
            "mongodb+srv://ineuronmongo:ineuron1@cluster0.iertm.mongodb.net/?retryWrites=true&w=majority")
        db = client['Dress_DB']
        return db

    def read_data(self, filename: str):
        """

        :param filename:
        """
        try:
            lg.info("Reading the file")
            raw_df = pd.read_excel(filename)
        except Exception as e:
            lg.error("Error occurred while reading the file")
            lg.error(str(e))
            return pd.DataFrame()

        return raw_df

    def insert_dress_attribute_data(self, in_df):
        """Insert data into the database"""
        # get db connection and cursor
        self.get_sqldb_conn()

        try:
            self.cursor.execute("truncate table DRESS_MASTER")
            lg.info("Inserting data to DRESS_MASTER")
            for index, row in in_df.fillna('').iterrows():
                self.cursor.execute(
                    'INSERT INTO DRESS_MASTER (Dress_ID, Style, Price, Rating, Size, Season, NeckLine, SleeveLength, '
                    'waiseline, Material, FabricType, Decoration, PatternType, Recommendation) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (row['Dress_ID'], row['Style'], row['Price'], row['Rating'], row['Size'], row['Season']
                     , row['NeckLine'], row['SleeveLength'], row['waiseline'], row['Material'], row['FabricType']
                     , row['Decoration'], row['Pattern Type'], row['Recommendation'])
                )
                i = index

            self.cursor.execute('commit')

            lg.info(f"Inserted {i} records to DRESS_MASTER")
            self.close_db()

        except Exception as e:
            lg.error("Error encountered while inserting data")
            lg.error(str(e))
            self.close_db()
            return False
        return True

    def sanitize_date(self, v_date):
        return pd.to_datetime(v_date)

    def sanitize_quntity(self, qty):
        try:
            qty = int(qty)
        except ValueError:
            qty = 0
        return qty

    def form_list_of_tuples(self, row):
        dress_id = row.values[0]
        ls = []
        for key, value in row.items():
            if key != 'Dress_ID':
                t = (dress_id, self.sanitize_date(key), self.sanitize_quntity(value))
                ls.append(t)
        return ls

    def insert_dress_sales_data(self, in_df):
        """Insert data into the database"""
        # get db connection and cursor
        self.get_sqldb_conn()

        i = 0
        sales = []

        try:
            self.cursor.execute("truncate table DRESS_SALES")
            lg.info("Inserting data to DRESS_SALES")
            for index, row in in_df.fillna(0).iterrows():
                sales = self.form_list_of_tuples(row)

                dress_id = row['Dress_ID']
                self.cursor.executemany(
                    'INSERT INTO DRESS_SALES (Dress_ID, SALE_DATE, QUANTITY) '
                    'VALUES (%s, %s, %s)',
                    sales
                )

                i = i + len(sales)

            self.cursor.execute('commit')

            lg.info(f"Inserted {i} records to DRESS_MASTER")
            self.close_db()

        except Exception as e:
            lg.error("Error encountered while inserting data")
            lg.error(str(e))
            self.close_db()
            return False
        return True

    def insert_df_to_mongodb(self, df):
        nosqldb = self.get_nosql_db()
        coll = nosqldb['DressAttribute']
        df['Dress_ID'] = df['Dress_ID'].astype('str')
        # data = df1.fillna('').to_dict('split')
        coll.delete_many({})
        try:
            coll.insert_many(df.to_dict('records'))

            lg.info(f"Inserted {len(df)} records to MongoDB")
        except Exception as e:
            lg.error("Error encountered while inserting data to MongoDB")
            lg.error(str(e))
            return False
        return True


o_dress = Dress()
# 3. read these dataset in pandas as a dataframe
print("# 3. read these dataset in pandas as a dataframe")
print(f"_______________________________________")
df1 = o_dress.read_data(r'.\rawfiles\Attribute DataSet.xlsx')
df2 = o_dress.read_data(r'.\rawfiles\Dress Sales.xlsx')

# 2. Do a bulk load for these two table for respective dataset
print("# 2. Do a bulk load for these two table for respective dataset")
print(f"_______________________________________")
insert_flag = o_dress.insert_dress_attribute_data(df1)
if insert_flag:
    print("Inserted data to Mysql - Dress Attribute")
else:
    print("Error: Check the Log file for error description")

insert_flag = o_dress.insert_dress_sales_data(df2)
if insert_flag:
    print("Inserted data to Mysql - Dress Sales")
else:
    print("Error: Check the Log file for error description")

# 4. Convert attribute dataset in json format
print("# 4. Convert attribute dataset in json format")
print(f"_______________________________________")
df1.to_json(r'.\AttributeDataset.json', orient='index')
print("#  4. Convert attribute dataset in json format")
print(f"_______________________________________")

# 5. Store this dataset into mongodb
print("# 5. Store this dataset into mongodb")
print(f"_______________________________________")
insert_flag = o_dress.insert_df_to_mongodb(df1)
if insert_flag:
    print("Inserted data to MongoDB - Dress Attribute")
else:
    print("Error: Check the Log file for error description")
print(f"_______________________________________")

# 6. in sql task try to perform left join operation with attribute dataset and dress dataset on column Dress_ID
# get db connection and cursor
o_dress.get_sqldb_conn()
statement = "select * from dress_master " \
            "left join dress_sales " \
            "on dress_master.Dress_id = dress_sales.Dress_ID"
o_dress.cursor.execute(statement)
records = o_dress.cursor.fetchmany(10)

print("# 6. in sql task try to perform left join operation with attribute dataset and dress dataset on column Dress_ID")
print(f"_______________________________________")
for rec in records:
    print(rec)
print(f"_______________________________________")

# 7. Write a sql query to find out how many unique dress that we have based on dress id
statement = "select count(distinct dress_id) from dress_master"

o_dress.cursor.execute(statement)
print("# 7. Write a sql query to find out how many unique dress that we have based on dress id")
print(f"_______________________________________")
print(f"Number of unique dresses in Dress Attribute data are : {o_dress.cursor.fetchall()[0][0]}")
print(f"_______________________________________")

# 8. Try to find out how mnay dress is having recommendation 0
statement = "select count(distinct dress_id) from dress_master where Recommendation = 0"

o_dress.cursor.execute(statement)
print("# 8. Try to find out how mnay dress is having recommendation 0")
print(f"_______________________________________")
print(f"Number of unique dresses in Dress Attribute with Recommendation as 0 are : {o_dress.cursor.fetchall()[0][0]}")
print(f"_______________________________________")

# 9. Try to find out total dress sell for individual dress id
statement = "select dress_id, sum(Quantity) from dress_sales group by dress_id"

o_dress.cursor.execute(statement)
records = o_dress.cursor.fetchmany(10)
print(f"9. Try to find out total dress sell for individual dress id")
print(f"_______________________________________")
print("Dress_ID \t - \t Quantity Sold")
for rec in records:
    print(f"{rec[0]} \t - \t {rec[1]}")

# 10. Try to find out a third highest most selling dress id
statement = "select dress_id, sum(Quantity) from dress_sales group by dress_id order by 2 desc LIMIT 1 OFFSET 2"

o_dress.cursor.execute(statement)
print("# 10. Try to find out a third highest most selling dress id")
print(f"_______________________________________")
print(f"Third Highest most selling Dress : {o_dress.cursor.fetchall()[0][0]}")