import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import plotly.express as px
import psycopg2
import seaborn as sns
import datetime



# Lets create a basic Stocks dashboard in streamlit: 

# give the title/name of your page: 

st.header("NYSE")
st.caption("Visualization fo Stocks Market Price")


####################    CONNECTION TO POSTGRES DATABASE AND DEFINITION OF CURSOR ###########################


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

# DEFINITION OF COLUMNS as those coming fromYour DataBase (dataset) before connecting to it

cols = [] 


# Connecting to the database
conn = init_connection() 


# declare a cursor object from the connection
cursor = conn.cursor() # corti 



##################    READING FILE TO PROCESS THE COMPLEX QUERY ################################

# Lets perform our query from a separate text file since it is quite long  !! 

# Reading the query from file 

# Inserire il percorso e il nome file

szSourcePath = os.path.join(".", "csv" , "query.txt" )
# ("D:","Temp", "Nomefile.txt")
# Il file viene aperto
f = open(szSourcePath, "r")
# Il contenuto del file viene letto (In questo caso la query)
szData = f.read()
# Il file viene chiuso
f.close()
# Sostituiamo tutti CrLf con degli spazi
szQry = szData.replace('\n', ' ')


# Execution della Query / Esegue la query, 
# rows = run_query(szQry) 

# Execute query
# sql = "SELECT * FROM tbl_market_data_202204"
cursor.execute(szQry)

# definisco i nomi delle colonne dei dati fetch 
# col_names = '"symbol", "datetimestamp", "open", "high", "low", "close", "exchange"'  
# # sostituisco la def colonne che va sopra dopo conn DB !!!!!!!!!  


# Fetching all the records
DataPack = cursor.fetchall()

# Insert the values/items  in its right columns
for elt in cursor.description:
    cols.append(elt[0])


##########################   UPLOADING DATA FETCH IN THE DATAFRAME PANDAS LIBRARY ###########################################

# BASIC SOLUTION USING CSV FILES IS NOT CONSIDERED: 
# def load_data():
   #  """ function for loading data """
    # df = pd.read_csv("./csv/MARKET_2015.csv", index_col="datatimestamp")

# Creating the DataFrame Pandas:
df = pd.DataFrame(data=DataPack, columns=cols)

# TESTED OPTIONS code lines to create the Pandas DataFrame after data fetch:    
# df = pd.DataFrame(data=rows, col_names = ["symbol", 'datetimestamp', 'open', "high", 'low', 'close', 'exchange']) # option 1
# df = pd.DataFrame("rows, index_col=datatimestamp") # option 2
# df = pd.DataFrame(data=DataPack, columns= [x[0] for x in cursor.description]) # option 3
# df = st.dataframe(rows) # per creare il dataframe in Streamlit individuato nella query eseguita e nominata 'rows' # option 4
# df = sqlio.read_sql_query("szQry", conn)  ## ERROR: Execution failed on sql 'szQry': syntax error at or near "szQry" LINE 1: szQry ^ # option 5
# df = pd.DataFrame({"symbol": list("symbol"), "datetimestamp": list("datetimestamp"), "open": list("open"), "high": list("high"), # option 6
#                   }, dtype="category") # prova con dtype category
# df.reset_index('datetimestamp', inplace=True) # option 7
# columns = tuple(df.columns)
# st.write(columns)

# let us visualize teh DataFrame in streamlit application with:
st.dataframe(df.head(3)) 

###################################################################################################################

# close the cursor object to avoid memory leaks
cursor.close()

# close the connection object
conn.close()

##################################################################################################################

numeric_df = df.select_dtypes(['float', 'int'])
numeric_cols = numeric_df.columns


text_df = df.select_dtypes(['string'])
text_cols = text_df.columns


stock_column = df(['symbol'])

unique_stocks = stock_column.unique()

# df, numeric_cols, text_cols, unique_stocks
# return df, numeric_cols, text_cols, unique_stocks = load_data()


# title of the dashboard
st.title("W3 Select Stock Market Data and show ")

# lets show the dataset of the dashboard
# st.write(df)


# add checkbox in sidebar

check_box3 = st.sidebar.checkbox(label="show data", key="check_box3")

if check_box3:
    # lets show the dataset
    st.write(df)


# give sidebar title
st.sidebar.title("Exchange")
st.sidebar.subheader("Timeseries settings")
feature_selection = st.sidebar.multiselect(label="Select Pricing",
options=numeric_cols, key="myid3")

stock_dropdown = st.sidebar.selectbox(label="Select Ticker",
options=unique_stocks)

# add plotly function / figure

print(feature_selection)

df = df[df['symbol']==stock_dropdown]
df_features = df[feature_selection]

plotly_figure = px.line(data_frame=df_features, x=df_features.index, y=feature_selection, title=(str(stock_dropdown) + ' ' + 'timeseries'))

st.plotly_chart(plotly_figure)


# ///////////////////// removing watermark

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)