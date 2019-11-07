import pandas as pd
from sqlalchemy import create_engine
import urllib
import pymssql
import pyodbc
from cryptography.fernet import Fernet
import re
import uuid
import random
from datetime import date
# remove redundant libraries

key = Fernet.generate_key()
cipher_suite = Fernet(key)

# use online db?
params = urllib.parse.quote_plus(
    r'DRIVER={SQL Server};SERVER=JOSEPHKABAU\SQLEXPRESS;DATABASE=Shop')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine = create_engine(conn_str)


def check_is_none(*objs):  # function to check if an argument is of type None
    fact = True
    for val in objs:
        if val is None:
            fact = False
    return fact

def encrypt_pass(password):
    encoded_text = cipher_suite.encrypt(b'%password%')
    str_enc = encoded_text.decode("utf-8")
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


def create_account(user_id):
    balance = random.randint(500, 1000)
    new_account = pd.DataFrame({
        'account_id': uuid.uuid4(),
        'user_id': user_id,
        'balance': balance
    }, index=[1])
    new_account.to_sql('Account', engine, if_exists='append', index=False)

def create_user(email, password):
    user_id = uuid.uuid4()
    query = "SELECT * FROM Shop.dbo.User_table"  # refactor to use stored procs for security
    df_user = pd.read_sql(query, engine)
    ''''''
    if email == str(df_user['email']):
        pass
        '''
        df_email = df_user['email'][0]
        if email == df_email[0]:
            print('User already exists')
            # ...
        '''
    else:
        new_user = pd.DataFrame({
            'user_id': user_id,
            'email': email,
            'pass': encrypt_pass(password),
            'date_created': date.today()
        }, index=[1])
        new_user.to_sql('User_table', engine, if_exists='append', index=False)
        create_account(user_id)


def login(email, password):
    query = "SELECT * FROM Shop.dbo.User_table"  # refactor to use stored procs for security
    df_user = pd.read_sql(query, engine)
    i = 0
    for ind in range(len(df_user)):
        print(df_user['email'][ind])
        if email == df_user['email'][ind] and password == decrypt_pass(df_user['pass'][ind]):
            print('login successful')


def create_item(item_name, item_price, manufacturer, in_stock):
    if check_is_none(item_name, item_price, manufacturer, in_stock):
        new_item = pd.DataFrame({
            'product_name': item_name,
            'product_price': item_name,
            'manufacturer': manufacturer,
            'in_stock': in_stock
        }, index=[1])
        new_item.to_sql('Products', engine, if_exists='append', index=False)
    else:
        print("Cannot process null values")


def list_all_items():
    query = "SELECT * FROM Shop.dbo.Products"  # refactor to use stored procs for security
    df_products = pd.read_sql(query, engine)
    df_product = df_products['product_name'][0]
    print(df_product)


def add_to_cart(product_id, account_id):
    query = "SELECT * FROM Shop.dbo.Products WHERE PRODUCT_ID = {}".format(product_id)
    df_products = pd.read_sql(query, engine)
    df_product = df_products['product_name'][0]
    to_checkout = pd.DataFrame({
        'product_id': df_product
    }, index=[1])
    to_checkout.to_sql('Checkout', engine, if_exists='append', index=False)


def purchase(product_id, account_id):
    diff = 0
    a_query = "SELECT * FROM Shop.dbo.Account WHERE ACCOUNT_ID = {}".format(account_id)
    df_account = pd.read_sql(a_query, engine)
    df_balance = df_account['balance'][0]
    p_query = "SELECT * FROM Shop.dbo.Checkout WHERE PRODUCT_ID = {}".format(product_id)
    df_products = pd.read_sql(p_query, engine)
    df_product_price = df_products['product_price'][1]
    if df_balance < df_product_price:
        print("Not enough in the bank")
    else:
        diff = df_balance - df_product_price
        # update on account_id only
        to_deduct = pd.DataFrame({
            'balance': diff
        }, index=[1])
        to_deduct.to_sql('Account', engine, if_exists='append', index=False)
        print("successfully purchased")
        #  deduct function
        #  update (delete) value in checkout
        #  send email
        return diff
# Start program
# Use argparse for login or signup?
'''
parser = argparse.ArgumentParser(description='Login or Sign Up')
parser.add_argument("login", help="Enter 'login' or 'signup'")
parser.parse_args()
'''
#  if args.login == 'signup':


log_answer = input("Create a new account? Y/N")
if log_answer == 'Y' or log_answer == 'y':
    email = input("Enter your email address: ")
    password = input("Enter your password: ")
    validate_password(password)
    if validate_password(password):
        create_user(email, password)
else:
    sign_answer = input("Do you want to sign in? Y/N")
    if sign_answer == 'Y' or sign_answer == 'y':
        email = input("Enter email")
        password = input("Enter password")
        login(email, password)
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