// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <math.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 1000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hashed = hash(word);
    // bucket is empty
    if (table[hashed] == NULL)
    {
        return false;
    }
    // check the linked list
    node *n = table[hashed];
    // as long as the node has a word, compare it to word and go to next node
    while (true)
    {
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }
        if (n->next == NULL)
        {
            break;
        }
        n = n->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int hash = 6133;
    for (int i = 0; i < strlen(word); i++)
    {
        hash = (hash + toupper(word[i])) * toupper(i);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open dictionary.\n");
        return false;
    }

    int index = 0;
    char word[LENGTH + 1];
    char c;
    while (fread(&c, sizeof(char), 1, file))
    {
        // word is complete
        if (c == '\n')
        {
            // terminate current word
            word[index] = '\0';

            // hash word
            unsigned int hashed = hash(word);

            // add word to new node
            node *new = malloc(sizeof(node));
            strcpy(new->word, word);

            // add next to new node
            if (table[hashed] == NULL)
            {
                // first element
                new->next = NULL;
            }
            else
            {
                // add second+ element to linked list
                new->next = table[hashed];
            }

            // add node to table
            table[hashed] = new;

            // get ready for next word
            index = 0;
            continue;
        }

        // keep adding char to word
        word[index] = c;
        index++;
    }

    // Check whether there was an error
    if (ferror(file))
    {
        fclose(file);
        printf("Error reading dictionary.\n");
        unload();
        return false;
    }

    // Close text
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    int number = 0;
    // check every 'bucket' in the hash table
    for (int i = 0; i < N; i++)
    {
        // bucket is empty
        if (table[i] == NULL)
        {
            continue;
        }
        number++;
        // check all other linked nodes
        node *n = table[i];
        while (n->next != NULL)
        {
            number++;
            n = n->next;
        }
    }
    return number;
}

void free_the_people(node *n)
{
    if (n->next != NULL)
    {
        free_the_people(n->next);
    }
    free(n);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        if (table[i] == NULL)
        {
            continue;
        }
        free_the_people(table[i]);
    }
    return true;
}
