from cs50 import get_string


def main():
    # get credit card number
    number = get_string("Number: ")

    if validate(number):
        # Check which card it is based on length and starting digits
        if (len(number) == 13 or len(number) == 16) and number.startswith("4"):
            print("VISA")
        elif len(number) == 16 and 51 <= int(number[:2]) <= 55:
            print("MASTERCARD")
        elif len(number) == 15 and (number.startswith("34") or number.startswith("37")):
            print("AMEX")
        else:
            print("INVALID")
    else:
        print("INVALID")


def validate(number):
    # Obscure one-liner, not good practice but a fun challenge
    return str(sum([int(number[-i]) for i in range(1, len(number) + 1, 2)] + [int(i) for i in "".join(list(map(lambda x: str(x * 2), [int(number[-i]) for i in range(2, len(number) + 1, 2)])))])).endswith("0")


if __name__ == "__main__":
    main()