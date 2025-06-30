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
    float L = (float)
}

int count_letters(string text)
{

}

int count_words(string text)
{

}

int count_sentences(string text)
{

}
