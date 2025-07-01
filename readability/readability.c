#include <stdio.h>
#include <cs50.h>
#include <math.h>  // rount the result to the nearest integer
#include <string.h> // for string functions
#include <ctype.h> // for character classification functions

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get input text from the user
    string text = get_string("Text: ");

    // Count letters, words, and sentences in the text
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Calculate the Coleman-Liau index
    float L = (float)letters / words * 100; // average number of letters per 100 words
    float S = (float)sentences / words * 100; // average number of sentences per 100 words
    int index = round(0.0588 * L - 0.296 * S - 15.8); // Coleman-Liau formula

    // Determine the grade level based on the index
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
        printf("Grade %d\n", index);
    }
}

int count_letters(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]) || islower(text[i])) // Check if the character is a letter
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 0;
    bool in_word = false; // Track if we are currently in a word

    for (int j = 0, A = strlen(text); j < A; j++)
    {
        if (isspace(text[j]) || ispunct(text[j])) // Check for spaces or punctuation
        {
            if (in_word) // If we were in a word, we just ended it
            {
                count++;
                in_word = false; // Reset the in_word flag
            }
        }
        else
        {
            in_word = true; // We are in a word
        }
    }

    // If the last character was part of a word, count it
    if (in_word)
    {
        count++;
    }

    return count;
}       

int count_sentences(string text)
{
    int count = 0;
    for (int k = 0, B = strlen(text); k < B; k++)
    {
        if (text[k] == '.' || text[k] == '!' || text[k] == '?') // Check for sentence-ending punctuation
        {
            count++;
        }
    }
    return count;
}


