import gradio as gr

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited {amount}. New balance: {self.balance}"
        return "Deposit amount must be positive."

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Available balance: {self.balance}")
        elif amount > 0:
            self.balance -= amount
            return f"Withdrew {amount}. New balance: {self.balance}"
        return "Withdrawal amount must be positive."

    def get_balance(self):
        return f"Balance: {self.balance}"

    def display_account_info(self):
        return f"Account Number: {self.account_number}, Account Holder: {self.account_holder}, Balance: {self.balance}"

class SavingsAccount(Account):
    def __init__(self, account_number, account_holder, initial_balance=0, interest_rate=0.01):
        super().__init__(account_number, account_holder, initial_balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return f"Interest: {interest}. New balance: {self.balance}"

class CheckingAccount(Account):
    def __init__(self, account_number, account_holder, initial_balance=0):
        super().__init__(account_number, account_holder, initial_balance)

accounts = {}

def create_account(account_number, account_holder, account_type, initial_balance, interest_rate=0.01):
    if account_number in accounts:
        return "Account already exists!"
    
    if account_type.lower() == "savings":
        accounts[account_number] = SavingsAccount(account_number, account_holder, initial_balance, interest_rate)
    elif account_type.lower() == "checking":
        accounts[account_number] = CheckingAccount(account_number, account_holder, initial_balance)
    else:
        return "Invalid account type!"
    
    return f"Account {account_number} created successfully."

def deposit_money(account_number, amount):
    if account_number in accounts:
        return accounts[account_number].deposit(amount)
    return "Account not found!"

def withdraw_money(account_number, amount):
    if account_number in accounts:
        try:
            return accounts[account_number].withdraw(amount)
        except InsufficientFundsError as e:
            return str(e)
    return "Account not found!"

def check_balance(account_number):
    if account_number in accounts:
        return accounts[account_number].get_balance()
    return "Account not found!"

def display_account_info(account_number):
    if account_number in accounts:
        return accounts[account_number].display_account_info()
    return "Account not found!"

def calculate_interest(account_number):
    if account_number in accounts and isinstance(accounts[account_number], SavingsAccount):
        return accounts[account_number].calculate_interest()
    return "Interest calculation only applies to savings accounts!"

with gr.Blocks() as app:
    gr.Markdown("# 🏦 Simple Banking System with Gradio")
    
    with gr.Tab("Create Account"):
        account_number = gr.Textbox(label="Account Number")
        account_holder = gr.Textbox(label="Account Holder")
        account_type = gr.Dropdown(["savings", "checking"], label="Account Type")
        initial_balance = gr.Number(label="Initial Balance")
        interest_rate = gr.Number(label="Interest Rate (for savings)", value=0.01)
        create_button = gr.Button("Create Account")
        create_output = gr.Textbox(label="Result")
        create_button.click(create_account, inputs=[account_number, account_holder, account_type, initial_balance, interest_rate], outputs=create_output)

    with gr.Tab("Deposit Money"):
        dep_acc_number = gr.Textbox(label="Account Number")
        dep_amount = gr.Number(label="Amount")
        dep_button = gr.Button("Deposit")
        dep_output = gr.Textbox(label="Result")
        dep_button.click(deposit_money, inputs=[dep_acc_number, dep_amount], outputs=dep_output)

    with gr.Tab("Withdraw Money"):
        with_acc_number = gr.Textbox(label="Account Number")
        with_amount = gr.Number(label="Amount")
        with_button = gr.Button("Withdraw")
        with_output = gr.Textbox(label="Result")
        with_button.click(withdraw_money, inputs=[with_acc_number, with_amount], outputs=with_output)

    with gr.Tab("Check Balance"):
        bal_acc_number = gr.Textbox(label="Account Number")
        bal_button = gr.Button("Check Balance")
        bal_output = gr.Textbox(label="Balance")
        bal_button.click(check_balance, inputs=[bal_acc_number], outputs=bal_output)

    with gr.Tab("Account Info"):
        info_acc_number = gr.Textbox(label="Account Number")
        info_button = gr.Button("Get Info")
        info_output = gr.Textbox(label="Account Info")
        info_button.click(display_account_info, inputs=[info_acc_number], outputs=info_output)

    with gr.Tab("Calculate Interest"):
        int_acc_number = gr.Textbox(label="Account Number")
        int_button = gr.Button("Calculate Interest")
        int_output = gr.Textbox(label="Interest Calculation Result")
        int_button.click(calculate_interest, inputs=[int_acc_number], outputs=int_output)

app.launch()