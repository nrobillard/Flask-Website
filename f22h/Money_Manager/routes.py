import time

from flask import Blueprint  # Blueprint defines the one .py file that indicated where all of our urls will nav to
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from threading import Timer
from flask import url_for
from Money_Manager.Entities.UserEntity import User
from Money_Manager.Entities.Loan import Loan
from Money_Manager.Entities.Goal_Setting import GoalSetting
from Money_Manager.Entities.Recurring_Payments import RecurringPayment

routes = Blueprint('routes', __name__)

currentUser = User(None, None, None, None, None)
currentGoal = GoalSetting(None,None,None)


@routes.route('/login-400')
def login_400():
    return render_template('login_400.html', currentUser=currentUser)


@routes.route('/login-500')
def login_500():
    return render_template('login_500.html', currentUser=currentUser)


@routes.route('/logout')
def logout():
    flash("Successful logout", category="success'")
    currentUser = None  # Delete current user so the next sign-up does not have a populated object
    time.sleep(1)
    return redirect('/')


# return render_template('logout.html', currentUser=currentUser, currentLoan = currentLoan)


@routes.route('/logout-400')
def logout_400():
    return render_template('logout_400.html', currentUser=currentUser)


@routes.route('/logout-500')
def logout_500():
    return render_template('logout_500.html', currentUser=currentUser)


@routes.route('/account')
def view_account():
    return render_template('view_account.html', currentUser=currentUser)


@routes.route('/', methods=('GET', 'POST'))
def create_account():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don/t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            flash('Account created!', category='success')
            currentUser.set_username(email)
            currentUser.set_email(email)
            currentUser.set_first_name(first_name)
            currentUser.set_last_name(last_name)
            currentUser.set_password(password1)
            return redirect('/login')

    return render_template('create_account.html', currentUser=currentUser)


@routes.route('/login', methods=['GET', 'POST'])  # No name indicated default page
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        valid_login = authenticate(email, password)
        if not valid_login:
            flash("Invalid login credentials", category='error')
        else:
            flash("Successful login", category="success")
            return redirect('/home')

    return render_template('login.html', currentUser=currentUser)


@routes.route('/home',  methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_selection = request.form.get("transaction_type")
        transaction_amount = request.form.get("transaction_amount")
        transaction_amount = float(transaction_amount)

        if (transaction_amount) < 0: flash("Transaction amount can not be negative", category='error')

        if user_selection == "deposit" and transaction_amount >= 0:
            currentUser.add_balance(transaction_amount)
            flash("Successful Transaction", category='success')

        elif user_selection == "charge" and transaction_amount >= 0:
            currentUser.subtract_balance(transaction_amount)
            flash("Successful Transaction", category='success')



    return render_template('home.html', currentUser=currentUser)


@routes.route('/goal-setting')
def goal_setting():
    currentGoal = GoalSetting(currentUser.get_current_balance(), None, None)
    return render_template('goal_setting.html', currentUser=currentUser, currentGoal = currentGoal)


@routes.route('/history')
def balance_history():
    return render_template('balance_history.html', currentUser=currentUser)


@routes.route('/new-loan')
def add_loan():
    return render_template('add_loan.html', currentUser=currentUser)


@routes.route('/loans', methods=['GET', 'POST'])
def view_loans():
    currentLoan = Loan(None, None, None, None, None, None)
    if request.method == 'POST':
        currentLoan = Loan(None, None, None, None, None, None)
        loan_name = request.form.get('loan_name')
        if len(loan_name) == 0:
            flash("Please enter a name for your loan", category='error')

        loan_amount = float(request.form.get('loan_amount'))
        if loan_amount < 0:
            flash("Loan Amount can not be less than zero", category='error')

        interest_rate = float(request.form.get('interest_rate'))
        if interest_rate < 0:
            flash("Interest Rate can not be less than zero", category='error')

        loan_term = float(request.form.get('loan_term'))
        if loan_term < 0:
            flash("Loan Term can not be less than zero", category='error')

        currentLoan.set_loan_name(loan_name)
        currentLoan.set_balance(loan_amount)
        currentLoan.set_apr(interest_rate)
        currentLoan.set_loan_term(loan_term)
        status_code = currentLoan.basic_loan_calc(loan_amount, loan_term, interest_rate, loan_name)

        if status_code == 200: # 200 status codes means all set
            currentUser.append_loans_list(currentLoan)
            flash("Loan Created")
        else:
            flash("Unable to process request", category='error')

    print(currentUser.get_loan_list())

    return render_template('view_loans.html', currentUser=currentUser, currentLoan = currentLoan)


@routes.route('recurring_payment', methods=['GET', 'POST'])
def view_recurring_payment():
    current_recurring_payment = RecurringPayment(None, None, None)
    if request.method == 'POST':
        current_recurring_payment = RecurringPayment(None, None, None)
        title: str = request.form.get('recurring_payment_name')
        amount: float = request.form.get('recurring_payment_amount')
        new_type: bool = get_type(request.form.get('payment_type'))

        if len(title) == 0:
            flash("Please enter Title", category='error')
        if float(amount) <= 0:
            flash("Please enter valid Amount", category='error')

        temp = request.form.get('payment_type')
        print(f'Type: {temp}')
        current_recurring_payment.update(title, amount, new_type)

        if not len(title) == 0 and not float(amount) <= 0:
            currentUser.append_recurring_payment_list(current_recurring_payment)
            flash("New Recurring Payment Added", category='Success')
        else:
            flash("Could not create recurring transaction", category='error')

    print(currentUser.get_recurring_payment_list())

    return render_template('view_recurring_payment.html', currentUser=currentUser,
                           current_recurring_payment=current_recurring_payment)


def get_type(new_type: str) -> bool:
    return True if new_type == "Deposit" else False
def authenticate(login_email, login_password):
    return currentUser.get_email() == login_email and currentUser.get_password() == login_password

# @routes.route('/Recurring_Payment')
# def view_recurring_payments():
