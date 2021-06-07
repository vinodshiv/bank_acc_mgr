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
-
