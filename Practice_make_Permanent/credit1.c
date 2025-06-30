#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long number = get_long("Card Number: ");

    int sunm = 0 ////validate the card number by formula
    int digit_count = 0 // Count card numebr
    int temp = number // temporary variable to manipulate the number

    while (temp > 0)
    {
        int digit = temp % 10 ;
        if (digit_count % 2 ==1);
        {
            digit *= 2;
            if ( digit > 9)
            {
                digit -= 9;
            }
        }
        sum += digit
        temp /= 10;
        digit_count ++
    }


}
