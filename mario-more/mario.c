#include <stdio.h>
#include <cs50.h>

int main(void)
 {
   // Get input of the Height
   int n;
   do
   {
    n = get_int("Height: ");
   }
   while ( n < 1 || n > 8);

   // Print desired pyramid height
   for (int i = 0; i < n; i++)
   {
    // Set perimeters for thee columns to print
    for (int j = 0; j < n+i+3; j++)
    {
        if ( j ==n || j == n+1 || j+i < n-1)
            printf(" ");
        else
            printf("#");
    }
    printf("\n");
   }
}
