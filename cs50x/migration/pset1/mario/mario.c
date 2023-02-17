#include <cs50.h>
#include <stdio.h>

void print_times(char c, int n);

int main(void)
{
    // Get the height of the pyramid from user
    int height;
    do
    {
        height = get_int("Enter height of pyramid: ");
    }
    while (height < 1 || height > 8);

    // print the pyramid
    for (int layer = 1; layer <= height; layer++)
    {
        print_times(' ', height - layer);
        print_times('#', layer);
        printf("  ");
        print_times('#', layer);
        printf("\n");
    }
}

void print_times(char c, int n)
{
    // print character c, n times
    for (int i = 0; i < n; i++)
    {
        printf("%c", c);
    }
}
