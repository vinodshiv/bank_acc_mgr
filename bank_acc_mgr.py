"""
Vinod Shivarudrappa
Date: 18-Apr-2021
Term Project - Bank Account Manager (ATM Style)

This program is a Bank Account Manager app that works with the terminal

It works with a user to initially create a checking and a savings account,
then provide options to withdraw money, deposit money, check balances and
print out mini statement

Concurrency Note: This application is designed for single-user interactive use and is
not currently set up for concurrent users.
If this application were to be adapted for multi-user or concurrent access,
several aspects would need significant redesign, including but not limited to:
- Account Number Generation: The current method of generating account numbers in
  CheckingAccount and SavingsAccount classes (class-level attribute initialized
  once per script run) would not guarantee uniqueness across concurrent users.
- Database Transaction Management: SQLite can handle some level of concurrency,
  but the current implementation (each account class creating/deleting its own DB file
  like "CheckingAccount.db") is not suited for shared access. A robust multi-user
  system would require a centralized database, potentially with thread-safe connection
  pools, and careful transaction management (e.g., row-level locking, or serialized
  access for critical operations) to prevent race conditions and data corruption.
- State Management: Ensuring that the state of each user's session and account
  data is properly isolated and managed would be critical.
- File Handling: The `os.remove()` calls in account class `__init__` methods would
  cause issues if multiple users were simultaneously trying to initialize accounts.
"""
import re as regex
import time
import random
from tabulate import tabulate

# Import the Checking and Savings Account classes
from CheckingAccount import CheckingAccount
from SavingsAccount import SavingsAccount



def atm_func(acc_type):
    """ Functions of the ATM depending on account type passed"""

    # Define a dictionary for the ATM options and sort it as string
    opt_dict = {'1': 'Withdraw Money', '2': 'Deposit Money',
                '3': 'Check Balance',
                '4': 'Print Mini Statement', '5': 'Exit Session'}
    sorted_options_str = '\n'.join('{}: {}'.format(k, v) for
                                   k, v in sorted(opt_dict.items()))
    # Define other variables
    ops_bool = True
    dashes_str = "-" * 50
    orig_bal = round(acc_type.balance, 2)

    # Show ATM options
    while ops_bool:
        print(f'\n{dashes_str}')
        # Manual Test Cases for ATM Option Input:
        # 1. Non-numeric input (e.g., "a", "test"). Expected: "That's not a valid input! Try again."
        # 2. Numbers outside range (e.g., "0", "6", "-1"). Expected: "That's not a valid input! Try again."
        # 3. Empty input (just press Enter). Expected: "That's not a valid input! Try again."
        input_str = input(f'\nChoose from the following options: '
                          f'\n{sorted_options_str} \n')

        try:
            # Verify if choice is valid using opt_dict
            opt_str = opt_dict[input_str]
            sp_index = opt_dict[input_str].index(' ')
            print(f'{opt_str[:sp_index]}ing{opt_str[sp_index:]}...\n')
        except KeyError:
            print("That's not a valid input! Try again.")
            continue
        else:

            if input_str == '1':
                # Withdrawal
                # Manual Test Cases for Withdrawal Amount Input:
                # 1. Non-numeric input (e.g., "abc"). Expected: "Not a valid input! Please enter only numbers."
                # 2. Negative value (e.g., -50). Expected: Account class might handle this (e.g. Checking/SavingsAccount.withdraw(-50) currently treats it as a deposit).
                #    The ATM could ideally pre-validate to prevent negative withdrawals if that's desired behavior.
                # 3. Zero (e.g., 0). Expected: Account class handles this (withdraws $0.00).
                # 4. Amount greater than balance. Expected: Account class returns "Cannot overdraw!".
                # 5. Very large number (e.g., 999999999999999). Expected: Handled by float conversion, then by balance check.
                # 6. Empty input (just press Enter). Expected: "Not a valid input! Please enter only numbers." (due to float conversion failure).
                # 7. Input with spaces (e.g., "1 00"). Expected: "Not a valid input! Please enter only numbers."
                try:
                    w_amt = float(input(('Enter the amount to be withdrawn: ')))
                except ValueError:
                    print('Not a valid input! Please enter only numbers.')
                    continue
                else:
                    print(acc_type.withdraw(w_amt))
                    time.sleep(1)

            if input_str == '2':
                # Deposit
                # Manual Test Cases for Deposit Amount Input:
                # 1. Non-numeric input (e.g., "xyz"). Expected: "Not a valid input! Please enter only numbers."
                # 2. Negative value (e.g., -100). Expected: Account class returns "Cannot deposit negative amounts!".
                # 3. Zero (e.g., 0). Expected: Account class returns "Nothing to deposit.".
                # 4. Very large number (e.g., 999999999999999). Expected: Should deposit successfully if it's a valid float.
                # 5. Empty input (just press Enter). Expected: "Not a valid input! Please enter only numbers." (due to float conversion failure).
                # 6. Input with spaces (e.g., "1 00"). Expected: "Not a valid input! Please enter only numbers."
                try:
                    dep_amt = float(input(('Enter the amount to be deposited: ')))
                except ValueError:
                    print('Not a valid input! Please enter only numbers.')
                    continue
                else:
                    print(acc_type.deposit(dep_amt))
                    time.sleep(1)

            if input_str == '3':
                # Check balance
                print(acc_type)
                time.sleep(1)

            if input_str == '4':
                # Mini Statement
                stmt_list = acc_type.mini_statement()

                if len(stmt_list) > 0:
                    print(f'{acc_type}\nAccount Owner:'
                          f' {acc_type.owner}\nStatement Printed Time: '
                          f'{time.asctime()}\n\n{"-" * 77}')
                    print(tabulate(stmt_list, headers="firstrow",
                               numalign= "center", stralign="center",
                               tablefmt="presto"))
                    print(f'\nBalance at account creation was: '
                          f'${orig_bal:,.2f}')
                else:
                    print(f'{dashes_str} \nNo activity since account creation.')
                time.sleep(2)

            if input_str == '5':
                # Exit from current account session
                # Manual Test Flow Suggestion:
                # 1. After exiting an account (e.g., Checking), the loop for `acc_choice` (main menu) should appear.
                # 2. User should be able to choose the other account (e.g., Savings) and perform operations.
                #    Verify that the state of the first account (e.g., Checking) is preserved if accessed again later in the same overall ATM session.
                # 3. User should be able to choose to exit the ATM entirely (option 3 on `acc_choice` menu).
                #    Expected: Program terminates, "Thanks for using ATM..." message is displayed.
                #    The main script ensures `close_db_connection()` is called for both `chk_acc` and `sav_acc` upon full program exit.
                print(f'Exiting from {acc_type}')
                time.sleep(2)
                ops_bool = False


if __name__ == '__main__':

    print('\n\t\t \U0001F4B5\U0001F4B5\U0001F4B5 Welcome to ATM at 521 '
          'Commonwealth Ave \U0001F4B5\U0001F4B5\U0001F4B5 ')

    # Define variables
    sent_bool = True
    acc_sess_bool = True
    ops_bool = True
    dashes_str = "-" * 50


    # Begin account creation and ATM functionality
    while sent_bool:
        # Ask for user's name and generate accounts
        # Manual Test Cases for Name Input:
        # 1. Empty input (just press Enter). Expected: "Please enter a valid name..."
        # 2. Name with numbers (e.g., "John Doe123"). Current regex r"(\w+)$" only checks the end of the string.
        #    If it ends with a word character, it might pass. Expected: Ideally, "Please enter a valid name...".
        # 3. Name with special characters (e.g., "John Doe!@#"). Similar to above, depends on the last character.
        #    Expected: Ideally, "Please enter a valid name...".
        # 4. Very long name (e.g., 100+ characters). Expected: Should handle gracefully.
        # 5. Name consisting only of spaces. Expected: "Please enter a valid name..." (after strip, it would be empty, but current regex might fail before strip if only spaces).
        # 6. Name with leading/trailing spaces (e.g., "  John Doe  "). Expected: Should be stripped, "John Doe" used. (The code does use .strip() later).
        name_str = input('\nTo start, enter your first and last name to '
                         'create Checking and Savings accounts: \n')
        match = regex.search(r"(\w+)$", name_str) # Note: This regex only checks if the string *ends* with a word character.
                                                 # It doesn't strictly validate "first and last name" format or disallow internal numbers/symbols.

        if match:
            print('Thanks! Please wait.. Creating and loading accounts...')
            time.sleep(3)

            # Derive first name from full name and make it account owner
            name_str = name_str.strip().title()
            name_list = name_str.split()

            # Generate accounts and balances
            chk_acc = CheckingAccount(name_str,
                                      random.randrange(1000,5000) / 1.11)
            sav_acc = SavingsAccount(name_str,
                                     random.randrange(5000, 100000) / 1.11)

            # Print out info about generated accounts
            print(f'\nCongratulations {name_list[0]}! Your accounts '
                  f'have been created!\n')
            print(f'Account owner: {name_str} \n+{dashes_str}+')
            print(f'{chk_acc}\n\n{sav_acc}\n+{dashes_str}+')

            # Ask which account before providing ATM options
            while acc_sess_bool:
                # Manual Test Cases for Account Choice Input:
                # 1. Non-numeric input (e.g., "a", "test"). Expected: "Not a valid input! Try again.."
                # 2. Numbers outside range (e.g., "0", "4", "-1"). Expected: "Not a valid input! Try again.."
                # 3. Empty input (just press Enter). Expected: "Not a valid input! Try again.."
                acc_choice = input(('\nWhich account do you want to use for '
                                  'this session?\n1: Checking\n2: Savings '
                                    '\n3: Exit ATM\n'))

                if acc_choice == '1':
                    # Call atm_func to provide working options for Checking
                    # Manual Test Flow Suggestion:
                    # 1. After choosing Checking, perform a sequence: Deposit -> Withdraw -> Check Balance -> Print Statement.
                    # 2. Try to exit this account session (option 5 in atm_func) and then select Checking again to ensure state is preserved or reset as expected.
                    print(f'\n{dashes_str} \n{chk_acc}')
                    atm_func(chk_acc)

                elif acc_choice == '2':
                    # Call atm_func to provide working options for Savings
                    # Manual Test Flow Suggestion:
                    # 1. After choosing Savings, perform a sequence: Withdraw (try to overdraw) -> Deposit -> Print Statement -> Check Balance.
                    # 2. Try to exit this account session (option 5 in atm_func) and then select Savings again.
                    print(f'\n{dashes_str} \n{sav_acc}')
                    atm_func(sav_acc)

                elif acc_choice == '3':
                    # Exit full program
                    print('\n\t\U0001F4B5\U0001F4B5 Thanks for using ATM '
                          'at 521 Commonwealth Ave! \U0001F4B5\U0001F4B5\n')
                    acc_sess_bool = False
                    sent_bool = False
                    # Close database connections
                    chk_acc.close_db_connection()
                    sav_acc.close_db_connection()

                else:
                    # Loop back if choice is not one of options
                    print("Not a valid input! Try again..")
                    continue

        else:
            # Loop back if entered name is not per rules
            print('Please enter a valid name as prompted! Try again..')
            continue
