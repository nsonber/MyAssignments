import fitbitData as ft
import pandas as pd

o_fit = ft.FitbitData()

# 1. Read this dataset in pandas , mysql and mongodb
o_fit.read_data(r'.\rawfiles\FitBit data.csv')

# 3. convert all the dates available in dataset to timestamp format in pandas and in sql you to convert it in date format
o_fit.lg.info(f"Datatype of ActivityDate columns before conversion: {o_fit.df['ActivityDate'].dtypes}")

o_fit.df['ActivityDate'] = pd.to_datetime(o_fit.df['ActivityDate'])

o_fit.lg.info(f"Datatype of ActivityDate columns after conversion: {o_fit.df['ActivityDate'].dtypes}")

# 2. while creating a table in mysql don't use manual approach to create it,
#     always use automation to create a table in mysql
o_fit.create_table()

o_fit.insert_into_mysql()

# o_fit.insert_df_to_mongodb()

# o_fit.answers_using_pandas()

o_fit.answers_using_mysql()