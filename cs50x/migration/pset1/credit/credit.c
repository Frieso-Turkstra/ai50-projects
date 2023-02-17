#include <math.h>
#include <cs50.h>
#include <stdio.h>

int len(long cnn);
int get_digit(int n, long cnn);
bool checksum(long cnn);
string type_of(long cnn);

int main(void)
{
    // prompt the user for a credit card number
    long cnn = get_long("Number: ");
    
    // print the type of card if number is valid
    string output = (checksum(cnn)) ? type_of(cnn) : "INVALID";
    printf("%s\n", output);

}

int len(long num)
{
    // determine length of num with some modulus magic
    int length = 1;
    for (long i = 10; num % i != num; i *= 10)
    {
        length++;
    }
    return length;
}

int get_digit(int n, long cnn)
{   
    // returns the nth digit of cnn with some more modulus magic
    long divisor = pow(10, n + 1);
    return (cnn % divisor - cnn % (divisor / 10)) / (divisor / 10);
}

bool checksum(long cnn)
{
    int res = 0;
    for (int i = 0; i < len(cnn); i++)
    {   
        // add even numbers to res
        if (i % 2 == 0)
        {
            res += get_digit(i, cnn);
        }
        else
        {   
            // multiply oneven numbers by 2 before adding to res
            if (len((long) get_digit(i, cnn) * 2) == 2)
            {   
                // double digit products are added as their individual constituents
                long x = get_digit(i, cnn) * 2;
                res += get_digit(0, x);
                res += get_digit(1, x);
            }
            else
            {
                res += get_digit(i, cnn) * 2;
            }
        }
    }
    // check whether last number is 0
    return res % 10 == 0;
}

string type_of(long cnn)
{
    int length = len(cnn);
    // length = 13/16, first digits = 4
    if (length == 13 | length == 16 && get_digit(length - 1, cnn) == 4)
    {
        return "VISA";
    }
    // length = 15, first digits = 34/37
    else if (length == 15 && get_digit(length - 1, cnn) == 3 && (get_digit(length - 2, cnn) == 4 | get_digit(length - 2, cnn) == 7))
    {
        return "AMEX";
    }
    // length = 16, first digits = 51-55
    else if (length == 16 && get_digit(length - 1, cnn) == 5 && (get_digit(length - 2, cnn) >= 1 && get_digit(length - 2, cnn) <= 5))
    {
        return "MASTERCARD";
    }
    else
    {
        return "INVALID";
    }
}
