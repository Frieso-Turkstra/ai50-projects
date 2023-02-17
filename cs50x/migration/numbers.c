#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    int numbers[] = {2, 4, 5, 8, 6, 1, 3, 9, 7};

    for (int i = 0; i < 10; i++)
    {
        if (numbers[i] == 0)
        {
            printf("Found 0 at position %i!", i);
            return 0;
        }
    }
    printf("Zero not found.");
    printf("%i", strcmp("a", "a"));
    return 1;
}