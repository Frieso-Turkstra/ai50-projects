import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    database_file = open(sys.argv[1], "r")
    reader = csv.reader(database_file)

    # TODO: Read DNA sequence file into a variable
    sequence_file = open(sys.argv[2], "r")
    sequence = sequence_file.readline().rstrip()

    # TODO: Find longest match of each STR in DNA sequence
    profile = [str(longest_match(sequence, STR)) for STR in next(reader)[1:]]

    # TODO: Check database for matching profiles
    for row in reader:
        if row[1:] == profile:
            print(row[0])
            break
    else:
        print("No match")

    database_file.close()
    sequence_file.close()
    sys.exit(0)


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()