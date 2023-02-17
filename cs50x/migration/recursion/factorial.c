#include <stdio.h>
#include <cs50.h>

int fact(int n);

int main(void)
{
    int n = get_int("Number: ");
    printf("%i\n", fact(n));
}

int fact(int n)
{
    if (n == 1)
        return 1;
    else
        return n * fact(n-1);
}