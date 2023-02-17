#include <stdio.h>
#include <cs50.h>

int fibonacci(int n);

int main(void)
{
    int n = get_int("Length: ");
    // print out the first n elements of fibonacci sequence
    for (int i = 0; i < n; i++)
    {
        printf("%i\n", fibonacci(i));
    }
}

int fibonacci(int n)
{
    // returns nth element in fibonacci sequence
    if (n == 0 || n == 1)
        return 1;
    else
        return fibonacci(n-1) + fibonacci(n-2);
}