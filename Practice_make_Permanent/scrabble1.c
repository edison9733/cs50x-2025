#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int POINTS[26] = {
    1, 3, 3, 2, 1, 4, 2, 4, 1, 8,
    5, 1, 3, 1, 1, 3, 10, 1, 1, 1,
    1, 4, 4, 8, 4, 10
};
int compute_score(string word);
int main(void)
{
    string words[2];

    words[0] = get_string("Player 1: ");
    words[1] = get_string("Player 2: ");

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
  int score = 0;

  for (int i = 0, n = strlen(word); i < n; i++)
  {
    if (isupper(word[i]))
    {
        score += POINTS[word[i] - 'A'];
    }
    else if (islower(word[i]))
    {
        score += POINTS[word[i] - 'a'];
    }

   }
  return score;
}
