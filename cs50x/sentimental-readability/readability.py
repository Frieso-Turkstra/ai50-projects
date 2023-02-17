from cs50 import get_string


def main():
    # Get input from user and calculate index
    text = get_string("Text: ")
    index = compute_index(text)
    # Output grade according to index
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def compute_index(text):
    # Calculate number of letters, words and sentences
    letter_count = 0
    word_count = 1 if len(text) > 0 else 0
    sentence_count = 0

    for char in text:
        if char.isalpha():
            letter_count += 1
        elif char == " ":
            word_count += 1
        elif char in ('.', '?', '!'):
            sentence_count += 1

    # Average number of letters per 100 words
    L = letter_count / word_count * 100
    # Average number of sentences per 100 words
    S = sentence_count / word_count * 100
    # Return Coleman-Liau index
    return round(0.0588 * L - 0.296 * S - 15.8)


if __name__ == "__main__":
    main()