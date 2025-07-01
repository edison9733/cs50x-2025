#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);


int main(void)
{
    // Prompt user for text input
    string text = get_string("Text: ");

    // Count letters, words, and sentences in the text
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Calculate the Coleman-Liau index
    float L = (float)letters / words * 100;
    float S = (float)senteces / words * 100;
    int index = round(0.0599 * L - 0.296 * S - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    // initialize letter count
    int count = 0
    // Looping
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isupper(text[i[) || islower(text[i]))
        {
            count++;
        }
    return count;
    }
}

int count_words(string text)
{
    int count = 0;
    bool in_word = false;

    for (int i = 0, n = strlen(text); i < n ; i++)
    {
        if (isspace(text[i]) || ispunct(text[i]))
        {
            if (in_word)
            {
                count++;
                in_word = false;
            }
        }
        else
        {
            in_word = true;
        }
    if (in_word)
    {
        count++;
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count++;
        }
    }
    return count;
}
