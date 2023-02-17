# SENTENTIAL LOGIC VALIDATOR
#### Video Demo:  https://youtu.be/n_lEAMCPzHQ
#### Description:

This sentential logic validator checks the validity of an argument. It takes as input an argument, consisting of a set of premises and a non-empty conclusion. The program checks if the argument is well formed and if so, whether the argument is valid or not. An argument is *invalid* if it is possible for all its premises to be true whilst the conclusion is false. In all other cases, the argument is *valid*.

#### Templates

- layout.html
A simple layout on top of which the other two templates are built.
- help.html
A page that is rendered when the "help" button is pressed. The page displays information about the program and how to use it.
- index.html
This template is the main page. It contains two input fields, one for premises and one for the conclusion, and three buttons, validate, clear and help. The help button, as aforementioned, renders "help.html". The clear button clears the output from previous calls to validate and any error messages. The validate button starts the main function - the inner workings of which are discussed next.

#### Implementation

The first step is to get the user input from the input fields and pass these formulas into the function ```format_input()``` which prevents common errors by:
- removing any whitespace
- ignoring empty and duplicate formulas
- adding outer parentheses if missing
- turning all variables into uppercase
- checking the grammaticality

The last prerequisite is checked by the function ```check_grammaticality()```. This function checks for errors such as:
- using a symbol other than the connectives, parentheses or Roman letters
- unbalanced parentheses
- closing before opening parentheses
- invalid number of arguments per operator

I used a recursive function that checks the subformula in the inner parentheses with a pretty cool regular expression and if that checks out, the subformula is replaced by the atomic formula "A" until there are no more subformulas and if the initial formula is well formed, the remainder should be the atomic formula "A".

Now that the inputted formulas are well formed, it is time to perform the actual validity check. First, the function ```create_truth_table()``` is called which 1) identifies all the unique variables from the premises and the conclusion and 2) calculates all the permutations of the truth values these variables can take. Each permutation can be seen as a possible truth assignment or as a row in a truth table.

The premises are then assigned these truth assignments and evaluated with a similar recursive function as the one described previously to yield a single truth value which is subsequently stored in a truth table.

The last step consists of the validity check proper and is done by the function ```validate()``` which checks if there is a row in the truth table where all the premises are true but the conclusion is false. If there is one, it returns the invalidating assignment (i.e. the index of that row).

The result, "valid" or "invalid" alongside the truth table are outputted on the screen and the invalidating assignment is marked red.

#### Justification
I decided to split up the validation process of the user input into two parts because the first part, handled by ```format_input()``` concerns errors that the program can resolve and then returns a newly formatted formula. The second type of errors are handled by ```check_grammaticality()``` through flashing an error message and returning false.

The program only marks the first invalidating assignment as that suffices to proof the invalidity of the argument. Moreover, marking all invalidating assignments may become unwieldy when more variables get involved and the truth table grows exponentially with 2^(len(variables)).

#### Future development directions
Here is a list of further development directions that were not feasible within the timeframe of this project.
- Add precedence so the user has to input less parentheses
- Support first-order and/or modal logic
- Add a dark mode
- Add a proof checker
- Enable to make an account and save proofs/truth tables