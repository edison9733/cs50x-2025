#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {
    1, // A
    3, // B
    3, // C
    2, // D
    1, // E
    4, // F
    2, // G
    4, // H
    1, // I
    8, // J
    5, // K
    1, // L
    3, // M
    1, // N
    1, // O
    3, // P
    10,// Q
    1, // R
    1, // S
    1, // T
    1, // U
    4, // V
    4, // W
    8, // X
    4, // Y
    10,// Z
};

int compute_score(string word);
int main(void)
{
    // Prompt for two words
    string words[2];

    words[0] = get_string("Player 1: ");
    words[1] = get_string("Player 2: ");

    // Compute the score of each word

    int scores[2];

    scores[0] = compute_score(words[0]);
    scores[1] = compute_score(words[1]);

    if (scores[0] > scores[1])
    {
        printf("Player 1 wins with a score of %d!\n", scores[0]);
    }
    else if (scores[1] > scores[0])
    {
        printf("Player 2 wins with a score of %d!\n", scores[1]);
    }
    else
    {
        printf("It's a tie! Both players scored %d.\n", scores[0]);
    }
}

int compute_score(string word)
{
    // Initialize score variable
    int score = 0;

    // Compute score for each character
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        if (isupper(word[i]))
        {
            score += POINTS[word[i] - 'A']; // Convert uppercase letter to index
        }
        else if (islower(word[i]))
        {
            score += POINTS[word[i] - 'a']; // Convert lowercase letter to index
        }
    }
    return score;
}
