#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

// Points assigned to each alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4};

int compute_score(string word);

int main (void)
{
    // Promp the users for two words
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Calculate the scores

    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n" );
    }
}

 // make a new function
int compute_score(string word)
{
    // Init the score
    int score = 0;

    // Compute score for each letter
    for (int i = 0, len = strlen(word); i < len; i++)
    {
         // handle Uppercase letters
       if (isupper(word[i]))
         {
              score += POINTS[word[i] - 'A'];
         }
         // handle Lowercase letters
         else if (islower(word[i]))
         {
              score += POINTS[word[i] - 'a'];
         }

    }

return score;
}
