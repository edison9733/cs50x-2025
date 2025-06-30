#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int number = get_int("Height: ");

    if ( number <= 0)
    {
        printf("INVALID");
    }
    else
    {
        for ( int i = 0; i < number; i++)
        {
            for (int j = 0; j < number - i ; j++)
            {
                printf(" ");
            }
            for (int k = 0; k < i + 1; k++)
            {
                printf("#");
            }
            printf("  ");
            for (int l = 0; l < i + 1; l++)
            {
                printf("#");
            }
            printf("\n");
        }
    }
}
