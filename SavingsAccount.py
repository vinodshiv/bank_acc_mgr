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

    Concurrency Note: This class is not designed to be thread-safe.
    - The `acc_num` class attribute is generated once when the class is defined.
      If multiple instances were created across different sessions or processes without
      re-initializing the script (which re-runs `random.randrange`), it could lead
      to non-unique account numbers. In the current `bank_acc_mgr.py` usage,
      each run generates new account numbers as the script/class is reloaded.
    - Database operations: While each instance creates its own "SavingsAccount.db"
      (deleting any existing one), if the design were changed to allow shared database
      files or connections across multiple concurrent instances/threads,
      concurrent database writes could lead to data corruption or race conditions
      without proper locking mechanisms. SQLite's default concurrency support
      depends heavily on connection management and threading model.
    """

    # class attribute - account number
    acc_num = str(random.randrange(100001, 999999))
    # Concurrency Note on acc_num: This is a class-level attribute. If this script were part of a
    # larger system where multiple SavingsAccount instances could be created by different
    # threads/processes without restarting the Python interpreter (and thus re-running this
    # class definition), all instances would share the acc_num generated by the first
    # execution of this line. This would make acc_num non-unique. The current bank_acc_mgr.py
    # re-runs the script for each user session, mitigating this for that specific use case.

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

    # Test depositing zero amount
    initial_balance = sav_acc.balance
    deposit_zero_msg = sav_acc.deposit(0)
    assert sav_acc.balance == initial_balance, "Balance changed after depositing zero"
    assert "Nothing to deposit" in deposit_zero_msg, "Incorrect message for zero deposit"

    # Test depositing negative amount
    initial_balance = sav_acc.balance
    deposit_neg_msg = sav_acc.deposit(-50)
    assert sav_acc.balance == initial_balance, "Balance changed after depositing negative amount"
    assert "Cannot deposit negative amounts" in deposit_neg_msg, "Incorrect message for negative deposit"

    # Check for withdrawals
    # Test withdrawing zero amount
    initial_balance = sav_acc.balance
    withdraw_zero_msg = sav_acc.withdraw(0)
    assert sav_acc.balance == initial_balance, "Balance changed after withdrawing zero"
    assert "Withdrawn $0" in withdraw_zero_msg, "Incorrect message for zero withdrawal" # Based on current code, 0 is a valid withdrawal

    # Test withdrawing negative amount (current behavior allows this, effectively a deposit)
    initial_balance = sav_acc.balance
    # Current balance is 24002 (after previous tests)
    sav_acc.withdraw(-100) # This will act like a deposit of 100
    assert sav_acc.balance == initial_balance + 100, "Balance did not increase after withdrawing negative amount"

    # Test withdrawing amount greater than balance
    initial_balance = sav_acc.balance
    overdraft_msg = sav_acc.withdraw(initial_balance + 100)
    assert sav_acc.balance == initial_balance, "Balance changed after attempting to overdraw"
    assert "Cannot overdraw!" in overdraft_msg, "Incorrect message for overdraft attempt"

    # Original withdrawal test to empty the account
    sav_acc.withdraw(sav_acc.balance) # Withdraw remaining balance
    assert sav_acc.balance == 0, "Invalid balance after withdrawing all money"

    # Mini-Statement Tests
    # Create more than 10 transactions
    # Re-initialize account for a clean transaction history for this specific test
    sav_acc.close_db_connection() # Close previous connection for sav_acc
    sav_acc_stmt_test = SavingsAccount("Stmt Test User SAV", 10000) # New instance, new DB
    for i in range(12):
        sav_acc_stmt_test.deposit(100) # 12 deposits

    mini_stmt = sav_acc_stmt_test.mini_statement()
    # Expected: 1 header + 10 transactions = 11 items
    assert len(mini_stmt) == 11, \
        f"Mini statement should show 10 transactions plus header, got {len(mini_stmt)} items"
    # Verify header is present
    assert mini_stmt[0] == ["Trans.ID", "Timestamp", "Remark", "Trans. Amt", "Running Bal."], \
        "Mini statement header is incorrect or missing for SavingsAccount"
    sav_acc_stmt_test.close_db_connection()


    # Comment on Account Number Generation:
    # acc_num is a class attribute. If multiple SavingsAccount objects are created
    # in the same script run without re-importing or re-defining the class,
    # they might share the same account number because random.randrange() is called
    # only once when the class is defined. For true uniqueness per instance,
    # acc_num should be generated within the __init__ method.

    # Comment on Database Interaction Testing:
    # Testing for database corruption, non-writable scenarios (e.g., due to file permissions),
    # or other I/O errors with the database file itself is complex in standard unit tests.
    # Such tests would typically require mocking (e.g., `unittest.mock.patch` for `sqlite3.connect`
    # or os level functions) or more involved integration testing setups that can manipulate
    # file system states and permissions.

    # Close database connections after unit tests
    # The original sav_acc's db was removed when sav_acc_stmt_test was created.
    # We need a valid sav_acc object to test its close_db_connection.
    # The original sav_acc's db was removed when sav_acc_stmt_test was created.
    # So, we create a new one for this specific test.
    final_test_acc = SavingsAccount("Final Test SAV", 100) # This creates a new SavingsAccount.db
    final_test_acc.close_db_connection() # Now close it
    db_status = False

    try:
        # Try to use the cursor of the now-closed connection
        final_test_acc.cur.execute("SELECT DATE()")
    except sqlite3.ProgrammingError:
        # This exception is expected if the connection is properly closed
        db_status = True

    assert db_status, "Database connection closure did not work for final_test_acc (Savings)!"

    # All tests passed!
    print("\nAll augmented unit tests for SavingsAccount passed!")