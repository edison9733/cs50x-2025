#include <stdio.h>
#include <cs50.h>

int main(void)
 {
    int number = get_int("Height: ");
    if (number <= 0)
    {
        printf("Please enter a positive height.\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < number; i++)
        {
            // Print spaces
            for (int a = 0; a < number - i; a++)
            {
                printf(" ");
            }
            // Print left side of the pyramid
            for (int j = 0; j <= i ; j++)
            {
                printf("#");
            }
            // Print gap between the two sides
            printf("  ");
            // Print right side of the pyramid
            for (int o = 0 ; o < i + 1; o++)
            {
                printf("#");
            }
            printf("\n");
        }
    }
}
