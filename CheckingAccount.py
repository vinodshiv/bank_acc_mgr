"""
Vinod Shivarudrappa
Class: CS 521 - Spring 2
Date:18-Apr-2021
Term Project - Bank Account Manager (ATM Style)

This file contains the CheckingAccount class that will be used by BankMgr

Ensure to call CheckingAccount.close_db_connection if instantiated!
"""
import os
import time
import random
import string as st
import sqlite3


class CheckingAccount():
    """ Checking Account class - creates account, able to withdraw and
    deposit money, also print out a mini statement of the last 10 transactions
    """

    # class attribute - account number
    acc_num = str(random.randrange(100001, 999999))

    def __init__(self, owner, balance=0):
        """Constructor creates
      - An account for the owner supplied with the default balance is 0
      - A sqlite database that would store transaction information"""

        self.owner = owner
        self.balance = balance

        # Create connection to sqlite and create a database
        try:
            if os.path.exists("CheckingAccount.db"):
                os.remove("CheckingAccount.db")

            db_conn = sqlite3.connect('CheckingAccount.db')
        except (OSError, PermissionError):
            print(
                '\nDatabase error on CheckingAccount. Close any programs '
                'that might be using the file "CheckingAccount.db" and try '
                'again. Exiting...')
            time.sleep(2)
            exit()
        else:
            # Create a Checking Account table on CheckingAccount db to
            # store transactions
            self.__dbconn = db_conn
            self.cur = db_conn.cursor()
            self.tb_name = 'CHK_' + CheckingAccount.acc_num

            create_tb_str = 'CREATE TABLE ' + self.tb_name + ' ('\
            '"Trans.ID" text, Timestamp text, "Remark" text,'\
            '"Trans. Amt" text, "Running Bal." text)'

            self.cur.execute(create_tb_str)

    def __str__(self):
        """ User friendly description of CheckingAccount"""
        return f'Checking Account #{CheckingAccount.acc_num}\n' \
               f'Available balance: ${self.balance:,.2f}'

    def __repr__(self):
        """ Representation of CheckingAccount"""
        return f'CheckingAccount({self.owner}, {self.balance})\n'

    def deposit(self, dep_amt):
        """ Function that verifies the input amount and deposits into Account"""

        # Verify if amount being deposited is positive
        if dep_amt < 0:
            return f'Cannot deposit negative amounts! Current balance is ' \
                   f'${self.balance:,.2f}'
        elif dep_amt == 0:
            return f'Nothing to deposit. Current balance is ${self.balance:,.2f}'
        else:
            # If yes, add to balance and insert a transaction record
            self.balance += dep_amt

            trans_id = ''.join(random.choices(st.ascii_uppercase + st.digits, k=8))
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            trans_remark = 'Credit'
            trans_amt = "{:,.2f}". format(dep_amt)
            curr_bal = "{:,.2f}". format(self.balance)

            insert_str = "INSERT INTO " + self.tb_name + " VALUES ('" \
                         + trans_id + "','" + timestamp + "','" + \
                         trans_remark + "','$" + trans_amt +\
                         "','$" + curr_bal + "')"

            self.cur.execute(insert_str)
            self.__dbconn.commit()

            # Return the deposited amount and the new balance
            return f'Deposit of ${dep_amt} accepted! \nThe new balance is ' \
                   f'${curr_bal}'

    def withdraw(self, w_amt):
        """ Function that verifies the input amount and withdraws from
        CheckingAccount"""

        # Verify if withdrawal amount is under the balance
        if w_amt > self.balance:
            return f'Cannot overdraw! Available balance is ${self.balance:,.2f}'
        else:
            # If yes, deduct from balance and insert a transaction record
            self.balance -= w_amt

            trans_id = ''.join(random.choices(st.ascii_uppercase + st.digits, k=8))
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            trans_remark = 'Debit'
            trans_amt = "{:,.2f}". format(w_amt)
            curr_bal = "{:,.2f}". format(self.balance)

            insert_str = "INSERT INTO " + self.tb_name + " VALUES ('" \
                         + trans_id + "','" + timestamp + "','" + \
                         trans_remark + "','$" + trans_amt +\
                         "','$" + curr_bal + "')"

            self.cur.execute(insert_str)
            self.__dbconn.commit()

            # Return the withdrawn amount and the new balance
            return f'Withdrawn ${w_amt}. The new balance is ${curr_bal}'

    def mini_statement(self):
        """ Function that produces a list of list of transactions for Account
        """

        # Start with an empty list
        stmt_list = []

        # Iterate through the and append to list, as list
        for i in self.cur.execute('SELECT * FROM ' + self.tb_name +
                                  ' ORDER BY "Timestamp" DESC LIMIT 10'):
            stmt_list.append(list(i))

        # If transactions exist, add the header to index 0
        if len(stmt_list) > 0:
            headers = [i[0] for i in self.cur.description]
            stmt_list.insert(0, headers)

        # Finally return the list containing transactions
        return stmt_list

    def close_db_connection(self):
        """ Closes the database connection when called"""
        self.__dbconn.close()


# Unit Tests
if __name__ == '__main__':

    # Instantiate Class
    acc_owner = 'John Doe'
    chk_acc = CheckingAccount(acc_owner, 2000.458)

    # Constructor tests
    assert int(chk_acc.acc_num) in range(100001, 999999), \
        "Account number invalid!"
    assert (chk_acc.owner, chk_acc.balance) == ('John Doe', 2000.458), \
        "Account owner and initial balance invalid!"
    assert os.path.exists("CheckingAccount.db"), "Database was not created!"
    assert chk_acc.tb_name == 'CHK_' + chk_acc.acc_num, \
        "Invalid CheckingAccount table name in database!"

    print(chk_acc)

    # Method tests
    # Check if mini statement gets generated without any transactions
    assert len(chk_acc.mini_statement()) == 0, \
        "Invalid mini statement functionality - Activities recorded although " \
        "no transactions have taken place!"

    # Check for deposits
    chk_acc.deposit(200)
    assert chk_acc.balance == 2200.458, "Invalid balance after depositing money"

    # Check for withdrawals
    chk_acc.withdraw(chk_acc.balance)
    assert chk_acc.balance == 0, "Invalid balance after withdrawing money"

    # Check mini statement for exactly two transactions (including header)
    assert len(chk_acc.mini_statement()) == 3, \
        "Invalid # of activities recorded in the mini statement"

    # Close database connections after unit tests
    chk_acc.close_db_connection()
    db_status = False

    try:
        chk_acc.cur.execute("SELECT DATE()")
    except sqlite3.ProgrammingError:
        db_status = True

    assert db_status, "Database connection closure did not work!"

    # All tests passed!

