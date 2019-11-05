import argparse
import pandas as pd
from sqlalchemy import create_engine
import urllib
import pymssql
import pyodbc
from cryptography.fernet import Fernet
import re

key = Fernet.generate_key()
cipher_suite = Fernet(key)

params = urllib.parse.quote_plus(
    r'DRIVER={SQL Server};SERVER=JOSEPHKABAU\SQLEXPRESS;DATABASE=Shop')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine = create_engine(conn_str)


def encrypt_pass(password):
    encoded_text = cipher_suite.encrypt(b'%password%')
    #  str_enc = encoded_text.decode("utf-8")
    return encoded_text


def decrypt_pass(encoded_text):
    decoded_text = cipher_suite.decrypt(encoded_text)
    return decoded_text


def validate_password(passwd):
    valid = False
    if len(passwd) <= 6:
        print('Please make sure your password is at least 8 characters long')
    else:
        valid = True
    return valid


def create_user(user_name, password):
    query = "SELECT * FROM Shop.dbo.User_Au"  # refactor to use stored procs for security
    df_user = pd.read_sql(query, engine)
    df_user_name = df_user['Name'][0]
    #print(df_user_name)

    if user_name == df_user_name[0]:
        print('User already exists')
        # ...
    else:
        new_user = pd.DataFrame({
            'Name': user_name,
            'Pass': encrypt_pass(password)
        }, index=[1])
        new_user.to_sql('User_Au', engine, if_exists='append', index=False)


# Start program
print("Do you want to Login or Sign Up?")
log_answer = input("Y or N: ")
if log_answer == 'Y' or log_answer == 'y':
    user_name = input("Enter your username: ")
    password = input("Enter your password: ")
    validate_password(password)
    if validate_password(password):
        create_user(user_name, password)
'''
#   welcome()
print("Do you want to sell an item?")
#   sell_item()
print("select  an item to add to your cart")
#   select_item()
print("do you want to checkout?")
#   checkout()
#   logout()
#   print_stats()
'''