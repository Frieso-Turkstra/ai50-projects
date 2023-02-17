#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

float compute_index(string text);

int main(void)
{
    // get text from user
    string text = get_string("Text: ");
    // compute and output Coleman-Liau index
    int index = compute_index(text);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

float compute_index(string text)
{
    int letter_count = 0;
    int word_count = (strlen(text) > 0) ? 1 : 0;
    int sentence_count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // increase letter count if char is in the alphabet
        if (isalpha(text[i]))
        {
            letter_count++;
        }
        // increase word count if char is a space
        else if (isspace(text[i]))
        {
            word_count++;
        }
        // increase sentence count if char is a . or ! or ?
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentence_count++;
        }
    }

    // L = average number of letters per 100 words, S = average number of sentences per 100 words)
    float L = letter_count / (float) word_count * 100;
    float S = sentence_count / (float) word_count * 100;
    // formula to compute the Coleman-Liau index
    float index = 0.0588 * L - 0.296 * S - 15.8;
    return round(index);
}