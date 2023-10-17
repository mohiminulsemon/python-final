import random

class Account:
    accounts = []
    loan_feature = True
    bank_balance = 5000

    def __init__(self, name, email, address, type):
        self.name = name
        self.accountNo = random.randint(10000, 99999)
        self.email = email
        self.address = address
        self.balance = 0
        self.type = type
        self.transactions = []
        self.loan_count = 0
        self.loan_amount = 0
        Account.accounts.append(self)
        print(f"\nAccount created with Account No: {self.accountNo}")

    def deposit(self, amount):
        self.balance += amount
        self.bank_balance += amount
        print(f"\nDeposited ${amount}. New balance: ${self.balance}")

    def withdraw(self, amount):
        if self.bank_balance < amount:
            print('the bank is bankrupt')

        elif 0 <= amount <= self.balance:
            self.balance -= amount
            self.bank_balance -= amount
            print(f"\nWithdrew ${amount}. New balance: ${self.balance}")
        else:
            print("\nWithdrawal amount exceeded")

    def check_balance(self):
        print(f"\nCurrent Balance: ${self.balance}")

    def loan(self, amount):
        if self.loan_feature == True and self.loan_count < 2 and self.bank_balance > amount:
            self.loan_count += 1
            self.balance += amount
            self.loan_amount += amount
            print(f"\n--> Loaned ${amount}. New balance: ${self.balance}")
        else:
            print("\n--> Loan not available")

    def transfer(self, receiver, amount):
        if receiver not in Account.accounts:
            print("\n--> Account does not exist")
        else:
            if 0 <= amount <= self.balance:
                self.balance -= amount
                receiver.deposit(amount)
                print(f"\n--> Transferred ${amount} to {receiver.name}. New balance: ${self.balance}")
                self.transactions.append(f"--> transferred ${amount} to {receiver.name}")
            else:
                print("\n--> Invalid transfer amount")

    def transactions_history(self):
        print("\nTransaction history:")
        for transaction in self.transactions:
            print(transaction)

class Bank:
    def __init__(self):
        self.total_balance = 0
        self.total_loan_amount = 0

    def delete_account(self, account_no):
        for account in Account.accounts:
            if account.accountNo == account_no:
                Account.accounts.remove(account)
                print(f"\nAccount with Account No: {account_no} deleted.")
                return
        print(f"\nAccount with Account No: {account_no} not found.")

    def show_users(self):
        print("\nUser Accounts:")
        for account in Account.accounts:
            print(f"Account No: {account.accountNo}, Name: {account.name}")

    def get_total_balance(self):
        total_balance = sum(account.balance for account in Account.accounts)
        print(f"\nTotal Available Balance: ${total_balance}")

    def get_total_loan_amount(self):
        total_loan = sum(account.loan_amount for account in Account.accounts)
        print(f"\nTotal Loan Amount: ${total_loan}")

    def off_loan(self):
        Account.loan_feature = False
        print("\nLoan feature turned off.")

    def on_loan(self):
        Account.loan_feature = True
        print("\nLoan feature turned on.")

admin_pass = '123'
admin = False
current_user = None

while True:
    if current_user is None and not admin:
        print("No user logged in!")
        ch = input("Register/login (R/L), Admin login(A): ")
        if ch == "R":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            address = input("Enter your address: ")
            account_type = input("Enter account type: ")
            current_user = Account(name, email, address, account_type)
        elif ch == "L":
            account_number = int(input("Account number: "))
            for user in Account.accounts:
                if user.accountNo == account_number:
                    current_user = user
                    break
            if current_user is None:
                print("Account not found.")
        elif ch == "A":
            admin_pass_input = input("Enter admin password: ")
            if admin_pass_input == admin_pass:
                admin = True
        else:
            print("Invalid choice")

    else:
        if admin:
            print("\n Admin Options")
            print("1. Create Account")
            print("2. Delete Account")
            print("3. All Accounts")
            print("4. Total Balance")
            print("5. Total Loan")
            print("6. Toggle Loan Feature")
            print("7. Exit")
            admin_choice = input("Enter your choice: ")

            if admin_choice == "1":
                name = input("Enter user's name: ")
                email = input("Enter user's email: ")
                address = input("Enter user's address: ")
                account_type = input("Enter user's account type: ")
                Account(name, email, address, account_type)

            elif admin_choice == "2":
                account_no = int(input("Enter Account No to delete: "))
                Bank().delete_account(account_no)

            elif admin_choice == "3":
                Bank().show_users()

            elif admin_choice == "4":
                Bank().get_total_balance()

            elif admin_choice == "5":
                Bank().get_total_loan_amount()

            elif admin_choice == "6":
                toggle_choice = input("Enter 'on' to enable or 'off' to disable loan feature: ")
                if toggle_choice.lower() == "on":
                    Bank().on_loan()
                elif toggle_choice.lower() == "off":
                    Bank().off_loan()
                else:
                    print("Invalid choice")

            elif admin_choice == "7":
                admin = False

        else:
            print(f"\nWelcome {current_user.name} !\n")
            print("1. Deposit Money")
            print("2. Withdraw Money")
            print("3. Check Balance")
            print("4. Loan Request")
            print("5. Transfer Money")
            print("6. Transaction History")
            print("7. Exit")
            user_choice = input("Enter your choice: ")

            if user_choice == "1":
                amount = float(input("Enter the amount to deposit: "))
                current_user.deposit(amount)

            elif user_choice == "2":
                amount = float(input("Enter the amount to withdraw: "))
                current_user.withdraw(amount)

            elif user_choice == "3":
                current_user.check_balance()

            elif user_choice == "4":
                amount = float(input("Enter the amount to loan: "))
                current_user.loan(amount)

            elif user_choice == "5":
                amount = float(input("Enter the amount to transfer: "))
                receiver_account_no = int(input("Enter the receiver's Account No: "))
                for account in Account.accounts:
                    if account.accountNo == receiver_account_no:
                        current_user.transfer(account, amount)
                        break
                else:
                    print("Receiver not found.")

            elif user_choice == "6":
                current_user.transactions_history()

            elif user_choice == "7":
                current_user = None
