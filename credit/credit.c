#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long card_number = get_long("Card Number: ");
    

    //initialize variables
    int sum = 0; //validate the card number by formula
    int digit_count = 0;
    long temp = card_number; //temporary variable to manipulate the number

    // Count the number of digits and calculate the sum
    while (temp > 0)
    {
        int digit = temp % 10;
        if (digit_count % 2 == 1)
        {
            digit *=2;
            if (digit > 9)
            {
                digit -= 9;

            }
        }
        sum += digit;
        temp /= 10;
        digit_count++;
    }

    // Check if the card number is valid
    if (sum % 10 != 0 || digit_count < 13 || digit_count > 16)
    {
        printf("INVALID\n");
        return 0;
    }
    // Print Amex
    if ((card_number >= 34e13 && card_number < 35e13) || (card_number >= 37e13 && card_number < 38e13))
    {
        printf("AMEX\n");
    }
    else if (card_number >= 51e14 && card_number < 56e14)
    {
        printf("MASTERCARD\n");
    }
    else if ((card_number >= 4e12 && card_number < 5e12) || (card_number >= 4e15 && card_number < 5e15))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

}
