# Bank Account Manager – ATM Style

## What is it?
  A python program that offers the user an ATM style banking application on a terminal
 
## How does it work?

- The program prompts the user to enter their name as a starting point – the Account Owner

- It creates two accounts for the user – Checking and Savings, gives them a random 6-digit account number, and loads them with a random $ amount
  - Checking Account – between $1,000 and $5,000
  - Savings Account – between $5,000 and $100,000

- The user is then prompted to choose one of the accounts to work with. The below options are prompted for user interaction, *for the selected account*:
  1.	**Withdraw Money**: 
        Prompts the user to enter the amount to be withdrawn.
        Verifies that the amount entered is under the available balance, deduces it from the available balance and prints out the new balance in the account
  2. **Deposit Money**:
      Prompts the user to enter the amount to be deposited.
      Verifies that the amount entered is not zero or negative, adds it to the balance in the account. It then prints out the new balance in the account

  3.	**Check Balance**: 
      Prints out the account number and the available balance

  4.	**Print Mini Statement**
        All the transactions that have taken place are recorded in a sqlite3 database behind the scenes. This option tabulates the latest ten transactions on the terminal showing the fields: Trans.ID, Timestamp, Remark, Transaction Amount, and Running Balance

- The program ensures that possible errors are handled, loops back as required, and exits gracefully. For example, if the user enters anything other than a number to withdraw or deposit money, the program prints an appropriate message and prompts the choices again.


## Files and Modules
- The program runs only on Python 3+ environments. Please ensure installation

- The following modules from the standard library are used:
regex, time, random, string, sqlite3, os

- The module tabulate is used to pretty print the mini statement – this is not a part of the standard library and will have to be installed using pip: ```pip install tabulate```
- The program consists of 3 files:
  - bank_acc_mgr.py  - containing the main functionality
  - CheckingAccount.py – containing the class for Checking Account
  - SavingsAccount.py – containing the class for Savings Account

- When executed, it produces two more files – CheckingAccount.db and SavingsAccount.db – sqlite3 databases for the respective accounts. The files are left on the file system after the program exits – this is to retain statement information if needed to access from outside the program.

## Instructions to run
Clone this repo or download as zip, within the downloaded folder, execute the file bank_acc_mgr.py – either on an IDE, directly from the file system, or from the command line
python <path>/bank_acc_mgr.py 

## Manual Testing Considerations
The `bank_acc_mgr.py` script includes detailed comments pointing to specific areas and inputs that are good candidates for manual testing. Here's a summary of areas to focus on:

**1. Input Validation:**
   - **User Name Input (Initial Setup):**
     - Empty names.
     - Names containing numbers or special characters (note the current regex `r"(\w+)$"` only validates the end of the string).
     - Very long names.
     - Names consisting only of spaces.
   - **Numeric Menu Choices (Account Selection, ATM Options):**
     - Non-numeric inputs (e.g., letters, symbols).
     - Numbers outside the valid range for the menu.
     - Empty input (just pressing Enter).
   - **Withdrawal/Deposit Amounts:**
     - Non-numeric inputs.
     - Negative amounts (observe how `CheckingAccount` and `SavingsAccount` classes handle these – e.g., negative withdrawal might act as deposit, negative deposit is rejected).
     - Zero amounts.
     - Withdrawing an amount greater than the available balance.
     - Very large valid numbers.

**2. Application Flow:**
   - **Sequence of Operations:**
     - Perform transactions in various orders within an account session (e.g., Deposit -> Withdraw -> Check Balance -> Print Statement -> Deposit again).
     - Check mini-statement after no transactions, after one, and after more than ten transactions.
   - **Session Management:**
     - Select an account (e.g., Checking), perform some operations, then exit that account's session (using option '5').
     - Immediately re-enter the same account (Checking) to ensure its state (balance, transactions) is preserved.
     - Select the other account (e.g., Savings) and perform operations.
     - Exit one account session, then select the other, and then exit the ATM completely.
   - **Exiting the Application:**
     - Ensure graceful exit using option '3' from the main account selection menu.
     - Verify the "Thanks for using ATM..." message appears.
     - (Behind the scenes, database connections should be closed automatically by the script).

**3. Data Persistence (Mini-Statement):**
   - After performing several transactions and exiting the ATM, if you restart the application and create accounts for the *same owner name*, the `CheckingAccount.db` and `SavingsAccount.db` files will be overwritten due to the `os.remove()` call in the `__init__` method of the account classes. This means transaction history is effectively reset for each run of `bank_acc_mgr.py` *for the same database filenames*. True persistence across application runs would require a different database handling strategy.

The comments within `bank_acc_mgr.py` provide more context for these test points directly in the code.

