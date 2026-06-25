class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance


class Transaction:
    def __init__(self, account):
        self.account = account

    def process(self, amount, target_account=None):
        pass


class Deposit(Transaction):
    def process(self, amount, target_account=None):
        self.account.balance += amount
        print(f"{self.account.owner} deposited {amount}")


class Withdrawal(Transaction):
    def process(self, amount, target_account=None):
        self.account.balance -= amount
        print(f"{self.account.owner} withdrew {amount}")


class Transfer(Transaction):
    def process(self, amount, target_account=None):
        if target_account:
            self.account.balance -= amount
            target_account.balance += amount
            print(f"{self.account.owner} transferred {amount} to {target_account.owner}")


employer = Account("Employer", 5000)
employee = Account("Employee", 1000)

Deposit(employer).process(2000)
Withdrawal(employer).process(1500)
Transfer(employer).process(1000, employee)

print("Employer balance:", employer.balance)
print("Employee balance:", employee.balance)
