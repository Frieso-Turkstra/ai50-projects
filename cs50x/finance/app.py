import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from string import punctuation, digits

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?;", session["user_id"])
    stocks = []
    row = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])
    cash = row[0]['cash']
    total = cash
    for symbol in symbols:
        shares = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = ? AND user_id = ?;",
                            symbol['symbol'], session["user_id"])
        price = lookup(symbol['symbol'])["price"]
        value = shares[0]['SUM(shares)'] * price
        total += value
        stocks.append((symbol['symbol'], shares[0]['SUM(shares)'], usd(price), usd(value)))

    return render_template("index.html", stocks=stocks, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # validate chosen stock
        symbol = request.form.get("symbol")
        if not symbol or not lookup(symbol):
            return apology("Invalid or missing symbol", 400)

        # validate number of shares
        shares = request.form.get("shares")
        try:
            shares = int(shares)
        except ValueError:
            return apology("Missing or invalid number", 400)
        if not shares or shares <= 0:
            return apology("Missing or invalid number", 400)

        # make sure user has sufficient cash
        price = lookup(symbol)["price"]
        row = db.execute("SELECT cash FROM users WHERE id == ?;", session["user_id"])
        if (shares * price) > row[0]["cash"]:
            return apology("You are too broke", 403)

        # perform the actual "purchase"
        new_cash = row[0]["cash"] - shares * price
        db.execute("UPDATE users SET cash = ? WHERE id == ?;", new_cash, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, time) VALUES (?, ?, ?, ?, ?);",
                   session["user_id"], symbol, shares, price, datetime.now())

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?;", session["user_id"])
    for transaction in transactions:
        transaction["price"] = usd(transaction["price"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol or not lookup(symbol):
            return apology("Invalid or missing symbol", 400)

        quote = lookup(symbol)
        return render_template("quoted.html", name=quote["name"], price=usd(quote["price"]), symbol=quote["symbol"])

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # check if username is not blank or already exists
        username = request.form.get("username")
        existing_usernames = [row['username'] for row in db.execute("SELECT username FROM users;")]
        if not username or username in existing_usernames:
            return apology("username is invalid or already exists", 400)

        # check if password or confirmations is not blank and match
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation or password != confirmation:
            return apology("password is invalid or does not match confirmation", 400)

        # make sure password is strong enough
        if len(password) < 8 or len(list(set(password) & set(punctuation))) < 1 or len(list(set(digits) & set(password))) < 1:
            return apology("password must contain 8 characters of which one symbol and one digit", 400)

        # hash password and add username and hash to database
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, hash)

        # return to login page
        return redirect("/login")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?;", session["user_id"])

    if request.method == "POST":
        # validate stock to be sold
        symbol = request.form.get("symbol")
        if not symbol or symbol not in [stock['symbol'] for stock in stocks]:
            return apology("stock not found", 400)

        # validate number of shares
        shares_owned = db.execute("SELECT SUM(shares) FROM transactions WHERE symbol = ? AND user_id = ?;",
                                  symbol, session["user_id"])
        shares = request.form.get("shares")
        if not shares or int(shares) < 1 or int(shares) > shares_owned[0]['SUM(shares)']:
            return apology("invalid number of shares", 400)

        # perform the actual "selling", i.e. update cash and transactions
        price = lookup(symbol)["price"]
        row = db.execute("SELECT cash FROM users WHERE id == ?;", session["user_id"])
        new_cash = row[0]["cash"] + int(shares) * price

        db.execute("UPDATE users SET cash = ? WHERE id == ?;", new_cash, session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, time) VALUES (?, ?, ?, ?, ?);",
                   session["user_id"], symbol, int(shares) * -1, price, datetime.now())

        return redirect("/")

    return render_template("sell.html", stocks=stocks)
