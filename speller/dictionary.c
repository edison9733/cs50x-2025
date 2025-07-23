// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Declare variables
unsigned int word_count;
unsigned int hash_value;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    hash_value = hash(word);
    node *cursor = table[hash_value];

    // Fo through linked list at that bucket
    while (cursor != NULL)
    {
        // Compare word to cursor's word
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true; // If they match, return true
        }
        cursor = cursor->next; // Move to next node in linked list
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned long total = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        total += tolower(word[i]);
    }
    return total % N; // Simple hash function that sums ASCII values and takes modulo N to find its bucket
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open the dictionary file
    FILE *file = fopen(dictionary, "r");

    // Return NULL if file could not be opened
    if (file == NULL)
    {
        printf("Could not open %s\n", dictionary);
        return false;
    }
    // Declare variable called word
    char word[LENGTH+1];

    // Scan dictionary for strings up until EOF
    while ( fscanf(file, "%s", word) != EOF )
    {
        // Create a new node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {

            return false;
        }

        // Copy the word into the node
        strcpy(n->word, word);
        hash_value = hash(word);
        n->next = table[hash_value];
        table[hash_value] = n;
        word_count++;
    }
    fclose(file);
    return true;

}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (word_count > 0)
    {
        return word_count;
    }
    else
    {
        return 0;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        if (cursor == NULL)
            {
                return true;
            }

    }
    return false;
}
