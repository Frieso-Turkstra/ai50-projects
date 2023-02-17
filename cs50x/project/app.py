from flask import Flask, flash, request, render_template, session
from flask_session import Session
import re
import itertools

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "validate" in request.form:
            print("validate")
            # get premises and conclusion
            premises = format_input(request.form.get("premises").split(";"))
            conclusion = format_input([request.form.get("conclusion")])

            if premises != "Error" and conclusion != "Error":
                if len(conclusion) == 1:
                    variables, permutations, truth_table = create_truth_table(premises, conclusion)
                    thead = ["#"] + variables + premises + conclusion
                    tbody = [list(permutations[index]) + truth_table[index] for index in range(2**len(variables))]
                    invalidating_assignment = validate(truth_table)
                    validity = "INVALID" if invalidating_assignment else "VALID"
                    # output truth table
                    return render_template("index.html", validity=validity, thead=thead, tbody=tbody, invalid_row=invalidating_assignment)
                else:
                    flash("Error - Conclusion not found")
        elif "help" in request.form:
            return render_template("help.html")

    return render_template("index.html")


@app.route("/help", methods=["GET", "POST"])
def help():
    if request.method == "POST":
        return render_template("index.html")
    return render_template("help.html")


def format_input(formulas):
    new_formulas = []
    for index, formula in enumerate(formulas):
        # remove all whitespace
        formula = "".join(formula.split())

        # remove empty formulas
        if not formula:
            continue

        # ensure formula has outer parentheses
        if not formula.startswith("(") or not formula.endswith(")"):
            formula = f"({formula})"

        # ensure all variables are uppercase
        for index, char in enumerate(formula):
            if char.isalpha():
                formula = formula[:index] + char.upper() + formula[index+1:]

        # check grammaticality
        if check_grammaticality(formula):
            # ensure there are no duplicates
            if formula not in new_formulas:
                new_formulas.append(formula)
        else:
            return "Error"

    return new_formulas


def check_grammaticality(formula):
    # ensure only parentheses, connectives and variables are used
    for index, char in enumerate(formula):
        if not char.isalpha() and char not in ("~", "&", "|", ">", "=", "(", ")"):
            flash(f"Error - Invalid symbol found: {char}")
            return False

    # ensure parentheses are balanced
    if formula.count("(") != formula.count(")"):
        flash("Error - Make sure you have an equal number of opening and closing parentheses")
        return False

   # ensure parentheses are placed correctly and operators have right number of arguments
    while "(" in formula:
        # find inner parentheses
        left_parenthesis = formula.rfind("(")
        right_parenthesis = left_parenthesis + formula[left_parenthesis:].find(")")
        # check if there is something between the parentheses
        subformula = formula[left_parenthesis+1:right_parenthesis]
        if not subformula:
            flash("Error - Check your parentheses")
            return False
        # subformula must be 1) atomic, possibly negated or 2) complex with a binary operator and two arguments, possibly negated
        if not re.search(r"(^~*[A-Z]{1}$)|(^~*[A-Z]{1}(&{1}|\|{1}|>{1}|={1})~*[A-Z]{1}$)", subformula):
            flash("Error - Check the number of arguments per operator")
            return False
        # replace parentheses and its content with a placeholder, viz. the atomic formula "A"
        formula = formula[:left_parenthesis] + "A" + formula[right_parenthesis+1:]

    if not formula == "A":
        flash("Error - Formula is not well formed")
        return False

    return True


def evaluate(formula):
    while formula not in ("T", "F"):
        # find inner parenthesis
        left_parenthesis = formula.rfind("(")
        right_parenthesis = left_parenthesis + formula[left_parenthesis:].find(")")
        # evaluate what is between the parentheses
        subformula = formula[left_parenthesis+1:right_parenthesis]
        # replace all negations
        while "~" in subformula:
            subformula = subformula.replace("~T", "F")
            subformula = subformula.replace("~F", "T")
        # replace all binary operators
        mini_truth_tables = {
            "&": ("T", "F", "F", "F"),
            "|": ("T", "T", "T", "F"),
            ">": ("T", "F", "T", "T"),
            "=": ("T", "F", "F", "T")
            }
        for connective in ("&", "|", ">", "="):
            if connective in subformula:
                subformula = subformula.replace(f"T{connective}T", mini_truth_tables[connective][0])
                subformula = subformula.replace(f"T{connective}F", mini_truth_tables[connective][1])
                subformula = subformula.replace(f"F{connective}T", mini_truth_tables[connective][2])
                subformula = subformula.replace(f"F{connective}F", mini_truth_tables[connective][3])
                break
        formula = subformula

    # return a single truth value, "T" or "F"
    return formula


def create_truth_table(premises, conclusion):
    # find all unique variables from premises and conclusion
    variables = sorted(set([char for char in "".join(premises) + conclusion[0] if char.isalpha()]))
    # list all possible truth value combinations of variables
    permutations = list(itertools.product(['T', 'F'], repeat=len(variables)))

    # complete truth table
    truth_table = [[] for _ in range(2**(len(variables)))]
    for formula in premises + conclusion:
        #truth_values = []
        for index, permutation in enumerate(permutations):
            # replace variables with the truth values from each permutation
            assigned_formula = formula
            for i in range(len(variables)):
                assigned_formula = assigned_formula.replace(variables[i], permutation[i])
            # evaluate the truth value of the expression and add to truth table
            truth_table[index].append(evaluate(assigned_formula))

    return variables, permutations, truth_table


def validate(truth_table):
    for index, row in enumerate(truth_table):
        if all([val == "T" for val in row[:-1]]) and row[-1] == "F":
            return index + 1


