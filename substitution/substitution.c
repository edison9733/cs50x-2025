#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>

int main(int argc, string argv[])
{
    // Check if the number of command-line arguments is correct
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Check if the key is valid
    string key = argv[1];   // argv[1] is the key
    int key_length = 0;     // initialize key length
    bool used[26] = {false}; // to avoid duplicate letters

    for (int i = 0; key[i] != '\0'; i++)    // Looping until null terminator
    {
        // Requires #include <ctype.h>
        if (!isalpha(key[i]) || islower(key[i]) || used[toupper(key[i]) - 'A']) // to upper is to capitalized and -A is converted to number
        {
            printf("Invalid key\n");
            return 1;
        }
        used[toupper(key[i]) - 'A'] = true;
        key_length++;
    }

    if (key_length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");

    // Encrypt the plaintext
    printf("ciphertext: ");
    for (int i = 0; plaintext[i] != '\0'; i++)
    {
        char c = plaintext[i];
        if (isupper(c))
        {
            printf("%c", toupper(key[c - 'A'])); // 'A' is subtracted to convert to index 0-25
        }
        else if (islower(c))
        {
            printf("%c", tolower(key[c - 'a'])); // 'a' is subtracted to convert to index 0-25
        }
        else
        {
            printf("%c", c); // Non-alphabetic characters remain unchanged
        }
    }

    printf("\n");
    return 0;
}
