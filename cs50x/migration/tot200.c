#include <stdio.h>

int main(void)
{
    int n = 200;
    for (int i = 0; i < 200; i++)
    {
        n += n - 1;
    }
}
