#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <stdbool.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    int key_length = 0;

    bool used[26] = {false};
    for (int i = 0; key[i] != '\o'; i++)
    {
        if (!isalpha(key[i]) || islower(key[i]) || used[toupper(key[i]) - 'A'])
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

    string text = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0; text[i] != '\0'; i++)
    {
        char c = text[i];
        if (isalpha(c))
        {
            char offset = isupper(c) ? 'A' : 'a';
            int index = toupper(c) - 'A';
            printf("%c", isupper(c) ? toupper(key[index]) : tolower(key[index]));
        }
        else
        {
            printf("%c", c);
        }
    }
    printf("\n");
    return 0;
}
