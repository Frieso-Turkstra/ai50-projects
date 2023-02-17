#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count = 0;
int candidate_count;

// Array of visited nodes
int visited[MAX];
int len_visited = 0;


// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
bool has_indegree(int arr_len, bool arr[MAX][MAX], int node);
int find_source_node(int arr_len, bool arr[MAX][MAX]);
bool is_visited(int node);
bool find_cycle(bool arr[MAX][MAX]);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // loop through candidates
    for (int i = 0; i < candidate_count; i++)
    {
        // if name matches a candidate's name, add candidate's index to ranks[candidate's rank according to voter]
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = 1; i + j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[i + j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
    return;
}


// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // Bubble sort
    int current, next;
    pair temp;
    int swap_count = 0;

    while (true)
    {
        swap_count = 0;
        for (int j = 0; j < pair_count - 1; j++)
        {
            // look at current and the next value
            current = preferences[pairs[j].winner][pairs[j].loser];
            next = preferences[pairs[j + 1].winner][pairs[j + 1].loser];
            if (current < next)
            {
                // swap places
                temp = pairs[j];
                pairs[j] = pairs[j + 1];
                pairs[j + 1] = temp;
                swap_count++;
            }
        }
        // sorting is complete
        if (swap_count == 0)
        {
            return;
        }
    }
}

bool has_indegree(int arr_len, bool arr[MAX][MAX], int node)
{   
    // looks for a node i pointing into node, i.e. node has an indegree
    for (int i = 0; i < arr_len; i++)
    {
        if (arr[i][node])
        {
            return true;
        }
    }
    return false;
}

int find_source_node(int arr_len, bool arr[MAX][MAX])
{   
    // if a node has no indegrees, it is a source node
    for (int i = 0; i < arr_len; i++)
    {
        if (has_indegree(arr_len, arr, i))
        {
            continue;
        }
        return i;
    }
    return -1;
}

bool is_visited(int node)
{   
    // checks if node has already been visited
    for (int i = 0; i < len_visited; i++)
    {
        if (visited[i] == node)
        {
            return true;
        }
    }
    return false;
}

bool dfs(arr[MAX][MAX])
{
    
}

bool find_cycle(arr[MAX][MAX])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (arr[i][j])
            {
                dfs(arr[MAX][MAX]);
            }
        }
    }
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{   
    // for every pair
    for (int i = 0; i < pair_count; i++)
    {   
        locked[pairs[i].winner][pairs[i].loser] = true;
        if (find_cycle(locked))
        {
            locked[pairs[i].winner][pairs[i].loser] = false;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    /*
    int source_node = find_source(locked_len, locked);
    int candidate_index = pairs[source_node].winner;
    printf("%s\n", candidates[candidate_index]);
    */
    return;
}
