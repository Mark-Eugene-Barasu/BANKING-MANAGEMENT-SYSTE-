# BANK MANAGEMENT SYSTEM

import re
import sys
import secrets
import string

def generate_account_number():
    return ''.join(secrets.choice(string.digits) for _ in range(10))

def generate_pin_number():
    return ''.join(secrets.choice(string.digits) for _ in range(5))

system_database = {}

def safe_input(prompt):
    while True:
        data_guard = input(prompt).strip()
        if data_guard.lower() == 'quit' or data_guard.lower() == 'q':
            print('Exiting the program...')
            sys.exit()

        if data_guard == '':
            print('Error: You need to enter something valid!')
            continue

        return data_guard
    
def create_accounts():
    account_number = generate_account_number()
    pin_number = generate_pin_number()

    user_name = safe_input('Enter your name: ').title()
    while not re.fullmatch(r"[A-Za-z '-]+", user_name):
        print("Name can't contain numbers or special characters!")
        user_name = safe_input('Enter your name: ').title()

    user_surname = safe_input('Enter your surname: ').title()
    while not re.fullmatch(r"[A-Za-z '-]+", user_surname):
        print("Surname can't contain numbers or special characters!")
        user_surname = safe_input('Enter your surname: ').title()

    identity_document = safe_input('Enter your official identity document number: ')
    while not identity_document.isdigit():
        print('ID must contain only numbers.')
        identity_document = safe_input('Enter your official identity document number: ')
        
    user_id = safe_input('Your system user ID: ')

    account = {
        "account_id": account_number,
        "pin": pin_number,
        "name": user_name,
        "surname": user_surname,
        "id_doc": identity_document,
        "id": user_id,
        "balance": 0.0,  # Changed to float for standard currency representation
        "active": True
    }

    system_database[account_number] = account

    print('\n' + '='*35)
    print('ACCOUNT CREATED SUCCESSFULLY!')
    print(f"Account Number : {account_number}")
    print(f"Generated PIN   : {pin_number}")
    print(f"Account Holder  : {user_name} {user_surname}")
    print('='*35)

def get_balance():
    if not system_database:
        print("\nNo accounts registered in the database yet.")
        return
        
    for acc_num in system_database:
        user_data = system_database[acc_num]
        print(f"\nACCOUNT NUMBER: {acc_num}")
        print(f"USER NAME: {user_data['name']}")
        print(f"USER SURNAME: {user_data['surname']}")
        print(f"USER ID-DOCUMENT: {user_data['id_doc']}")
        print(f"BALANCE: R{user_data['balance']:.2f}")
        print("-" * 20)

def deposit():
    while True:
        account_number = safe_input("Enter the account number ('q' to cancel): ")
        if account_number in system_database:
            user_data = system_database[account_number]
            print(f"\nACCOUNT FOUND: {user_data['name']} {user_data['surname']}")
            print(f"CURRENT BALANCE: R{user_data['balance']:.2f}")

            while True:
                amount_input = safe_input("Enter the amount in RANDS: ")
                try:
                    amount = float(amount_input)
                    if amount <= 0:
                        print("Amount must be greater than zero.")
                        continue
                    break
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")

            user_data['balance'] += amount
            
            print(f"\nSuccessfully deposited R{amount:.2f} into account {account_number}")
            print(f"NEW BALANCE: R{user_data['balance']:.2f}")
            break
        else:
            print("Account number not found. Please try again.")

def withdraw():
    while True:
        account_number = safe_input("Enter the account number to withdraw from ('q' to cancel): ")
        if account_number in system_database:
            user_data = system_database[account_number]
            attempts = 3
            
            while attempts > 0:
                pin_number = safe_input(f"Enter the pin code ({attempts} attempts left): ")  
                if pin_number == user_data['pin']:
                    print(f"CURRENT BALANCE: R{user_data['balance']:.2f}")
                    
                    while True:
                        try:
                            withdrawal_amount = float(safe_input("Enter the withdrawal amount: "))
                            if withdrawal_amount <= 0:
                                print("Amount must be greater than zero.")
                                continue
                            break
                        except ValueError:
                            print("Invalid amount. Please enter a number.")
                    
                    if withdrawal_amount > user_data['balance']:
                        print('INSUFFICIENT FUNDS!')
                    else:
                        user_data['balance'] -= withdrawal_amount
                        print(f"\nSUCCESSFULLY WITHDRAWN: R{withdrawal_amount:.2f}")
                        print(f"NEW BALANCE: R{user_data['balance']:.2f}")
                    return # Exit function completely on completion
                else:
                    print('Wrong PIN!')
                    attempts -= 1

            if attempts == 0:
                print('\nYou have exceeded the maximum number of attempts!')
                print('Account locked temporarily. Visit your nearest branch.')
                return
        else:
            print("Account number not found. Please try again.")

def transfer():
    while True:
        sender_account = safe_input("Enter the account to transfer from ('q' to cancel): ")
        if sender_account in system_database:
            user_data = system_database[sender_account]
            attempts = 3
            
            while attempts > 0:
                user_pin = safe_input(f"Enter your PIN ({attempts} attempts left): ")
                if user_pin == user_data['pin']:
                    
                    while True:
                        receiver_account = safe_input('Enter the destination account: ')
                        if receiver_account == sender_account:
                            print("You cannot transfer money to the same account.")
                            continue
                        if receiver_account in system_database:
                            receiver_data = system_database[receiver_account]
                            break
                        print("Destination account not found. Try again.")

                    print(f"\nRECIPIENT: {receiver_data['name']} {receiver_data['surname']}")
                    
                    while True:
                        try:
                            amount = float(safe_input('Enter the amount to transfer: '))
                            if amount <= 0:
                                print("Amount must be greater than zero.")
                                continue
                            break
                        except ValueError:
                            print('Invalid input. Please enter a valid numeric value.')

                    if amount > user_data['balance']:
                        print('INSUFFICIENT FUNDS!')
                    else:
                        user_data['balance'] -= amount
                        receiver_data['balance'] += amount
                        
                        print(f"\nSUCCESSFULLY TRANSFERRED: R{amount:.2f} to {receiver_data['name']} {receiver_data['surname']}")
                        print(f"YOUR NEW BALANCE: R{user_data['balance']:.2f}")
                    return
                else:
                    print("Wrong PIN.")
                    attempts -= 1
            
            if attempts == 0:
                print('Too many incorrect PIN attempts. Security lock engaged.')
                return
        else:
            print("Sender account not found.")

def print_menu():
    print("\n" + "="*15 + " MENU " + "="*15)
    print("1. CREATE ACCOUNT")
    print("2. VIEW BALANCES")
    print("3. DEPOSIT MONEY")
    print("4. WITHDRAW CASH")
    print("5. TRANSFER MONEY")
    print("6. EXIT")
    print("=" * 36)

# --- MAIN EXECUTION LOOP ---
print('WELCOME TO THE BANKING SYSTEM')

while True:
    print_menu()
    choice = safe_input("Select an option from the menu: ")
    
    if choice not in ['1', '2', '3', '4', '5', '6']:
        print('Wrong selection, please choose a valid menu-option.')
        continue

    if choice == '1':
        create_accounts()
    elif choice == '2':
        get_balance()
    elif choice == '3':
        deposit()
    elif choice == '4':
        withdraw()
    elif choice == '5':
        transfer()
    elif choice == '6':
        print('\nTHANKS FOR USING OUR SERVICES, GOODBYE!')
        break
