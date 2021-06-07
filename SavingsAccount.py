"""
Vinod Shivarudrappa
Class: CS 521 - Spring 2
Date:18-Apr-2021
Term Project - Bank Account Manager (ATM Style)

This file contains the SavingsAccount class that will be used by BankMgr

Ensure to call SavingsAccount.close_db_connection if instantiated!
"""
import os
import time
import random
import string as st
import sqlite3


class SavingsAccount():
    """ Savings Account class - creates account, able to withdraw and
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
            if os.path.exists("SavingsAccount.db"):
                os.remove("SavingsAccount.db")

            db_conn = sqlite3.connect('SavingsAccount.db')
        except (OSError, PermissionError):
            print(
                '\nDatabase error on SavingsAccount. Close any programs '
                'that might be using the file "SavingsAccount.db" and try '
                'again. Exiting...')
            time.sleep(2)
            exit()
        else:
            # Create a Savings Account table on SavingsAccount db to
            # store transactions
            self.__dbconn = db_conn
            self.cur = db_conn.cursor()
            self.tb_name = 'SAV_' + SavingsAccount.acc_num

            create_tb_str = 'CREATE TABLE ' + self.tb_name + ' ('\
            '"Trans.ID" text, Timestamp text, "Remark" text,'\
            '"Trans. Amt" text, "Running Bal." text)'

            self.cur.execute(create_tb_str)

    def __str__(self):
        """ User friendly description of SavingsAccount"""
        return f'Savings Account #{SavingsAccount.acc_num}\n' \
               f'Available balance: ${self.balance:,.2f}'

    def __repr__(self):
        """ Representation of SavingsAccount"""
        return f'SavingsAccount({self.owner}, {self.balance})\n'

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
        SavingsAccount"""

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
    sav_acc = SavingsAccount(acc_owner, 20002)

    # Constructor tests
    assert int(sav_acc.acc_num) in range(100001, 999999), \
        "Account number invalid!"
    assert (sav_acc.owner, sav_acc.balance) == ('John Doe', 20002), \
        "Account owner and initial balance invalid!"
    assert os.path.exists("SavingsAccount.db"), "Database was not created!"
    assert sav_acc.tb_name == 'SAV_' + sav_acc.acc_num, \
        "Invalid SavingsAccount table name in database!"

    print(sav_acc)

    # Method tests
    # Check if mini statement gets generated without any transactions
    assert len(sav_acc.mini_statement()) == 0, \
        "Invalid mini statement functionality - Activities recorded although " \
        "no transactions have taken place!"

    # Check for deposits
    sav_acc.deposit(4000)
    assert sav_acc.balance == 24002, "Invalid balance after depositing money"

    # Check for withdrawals
    sav_acc.withdraw(sav_acc.balance)
    assert sav_acc.balance == 0, "Invalid balance after withdrawing money"

    # Check mini statement for exactly two transactions (including header)
    assert len(sav_acc.mini_statement()) == 3, \
        "Invalid # of activities recorded in the mini statement"

    # Close database connections after unit tests
    sav_acc.close_db_connection()
    db_status = False

    try:
        sav_acc.cur.execute("SELECT DATE()")
    except sqlite3.ProgrammingError:
        db_status = True

    assert db_status, "Database connection closure did not work!"

    # All tests passed!