#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool is_valid(string key);
string encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    // check whether there is one key
    if (argc != 2)
    {
        printf("Usage: ./substitution key");
        return 1;
    }
    // check whether key is valid
    if (is_valid(argv[1]))
    {
        // get plaintext from user, encrypt plaintext, output ciphertext
        string plaintext = get_string("Plaintext: ");
        string ciphertext = encrypt(plaintext, argv[1]);
        printf("ciphertext: %s\n", ciphertext);
        return 0;
    }
    else
    {
        printf("Key must contain 26 unique alphabetical characters.");
        return 1;
    }
}

bool is_valid(string key)
{
    // check whether key length is 26
    if (!(strlen(key) == 26))
    {
        return false;
    }
    // check whether every char is alphabetic
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }
    }
    // check whether key contains every char of the alphabet once
    string alphabet = "abcdefghijklmnopqrstuvwxyz";
    for (int i = 0; i < 26; i++)
    {
        bool match = false;
        for (int j = 0; j < 26; j++)
        {
            if (alphabet[i] == tolower(key[j]))
            {
                match = true;
            }
        }
        if (!match)
        {
            return false;
        }
    }
    return true;
}

string encrypt(string plaintext, string key)
{
    string ciphertext = plaintext;
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        // only encrypt alphabetical characters
        if (isalpha(plaintext[i]))
        {
            // find index in key with ascii
            int index = (isupper(plaintext[i])) ? plaintext[i] % 65 : plaintext[i] % 97;
            // replace char in text with char in key while making sure case is preserved
            ciphertext[i] = (islower(plaintext[i])) ? tolower(key[index]) : toupper(key[index]);
        }
    }
    return ciphertext;
}