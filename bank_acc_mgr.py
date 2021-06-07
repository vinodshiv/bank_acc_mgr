"""
Vinod Shivarudrappa
Class: CS 521 - Spring 2
Date: 18-Apr-2021
Term Project - Bank Account Manager (ATM Style)

This program is a Bank Account Manager app that works with the terminal

It works with a user to initially create a checking and a savings account,
then provide options to withdraw money, deposit money, check balances and
print out mini statement
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
                # Exit
                print(f'Exiting from {acc_type}')
                time.sleep(2)
                ops_bool = False


if __name__ == '__main__':

    print('\n\t\t \U0001F4B5\U0001F4B5\U0001F4B5 Welcome to METCS ATM at 521 '
          'Commonwealth Ave \U0001F4B5\U0001F4B5\U0001F4B5 ')

    # Define variables
    sent_bool = True
    acc_sess_bool = True
    ops_bool = True
    dashes_str = "-" * 50


    # Begin account creation and ATM functionality
    while sent_bool:
        # Ask for user's name and generate accounts
        name_str = input('\nTo start, enter your first and last name to '
                         'create Checking and Savings accounts: \n')
        match = regex.search(r"(\w+)$", name_str)

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
                acc_choice = input(('\nWhich account do you want to use for '
                                  'this session?\n1: Checking\n2: Savings '
                                    '\n3: Exit ATM\n'))

                if acc_choice == '1':
                    # Call atm_func to provide working options for Checking
                    print(f'\n{dashes_str} \n{chk_acc}')
                    atm_func(chk_acc)

                elif acc_choice == '2':
                    # Call atm_func to provide working options for Savings
                    print(f'\n{dashes_str} \n{sav_acc}')
                    atm_func(sav_acc)

                elif acc_choice == '3':
                    # Exit full program
                    print('\n\t\U0001F4B5\U0001F4B5 Thanks for using METCS ATM '
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
