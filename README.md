# ai50-projects
All the projects I did for the Computer Science for AI course at Harvard University.

## Crossword
This program models the generation of a crossword as a constraint satisfaction problem. Each word in the crossword needs to be of the right length (the unary constraint) and must have the correct overlap with its neighbours (the binary constraints).

## Degrees
This program implements breadth-first search to find the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

## Heredity
This program implements a model to make inferences about a population; given information about people, who their parents are, and whether they have a particular observable trait (e.g. hearing loss) caused by a given gene, this AI will infer the probability distribution for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question.

## Knights
This program represents Knights and Knaves puzzles in propositional logic, such that an AI running a model-checking algorithm can solve these problems. In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth and a knave will always lie. The objective of the puzzle is, given a set of sentences spoken by each of the characters, determine, for each character, whether that character is a knight or a knave. For example, consider a simple puzzle with just a single character named A. A says “I am both a knight and a knave.” Logically, we might reason that if A were a knight, then that sentence would have to be true. But we know that the sentence cannot possibly be true, because A cannot be both a knight and a knave – we know that each character is either a knight or a knave, but not both. So, we could conclude, A must be a knave.

## Minesweeper 
This program implements an AI that can play Minesweeper. It is a knowledge-based agent who makes decisions by considering its knowledge base, and making inferences based on that knowledge.

## Nim
This program implements an AI that can perfectly play Nim (https://en.wikipedia.org/wiki/Nim). It learns the game by playing against itself repeatedly and learning from experience. More specifically, it uses the reinforcement learning algorithm called Q-learning.

## PageRank
This program implements PageRank’s algorithm, according to which a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. Both the iterative version of the algorithm and the Random Surfer Model have been implemented.

## Parser
This program implements a simple context-free grammar formalism to parse English sentences to determine their structure.

## Questions
This program implements a very simple question answering system based on inverse document frequency. It performs two tasks: document retrieval and passage retrieval. When presented with a query (a question in English asked by the user), document retrieval will first identify which document(s) are most relevant to the query. Once the top documents are found, the top document(s) will be subdivided into sentences so that the most relevant passage to the question can be determined.

## Shopping
This program implements a nearest-neighbor classifier that is trained on data from a shopping website from about 12,000 user sessions. Given information about a user — how many pages they’ve visited, whether they’re shopping on a weekend, what web browser they’re using, etc. — the classifier will predict whether or not the user will make a purchase.

## Traffic
This program uses TensorFlow to build a neural network that can classify road signs based on an image of those signs. To train the network, the German Traffic Sign Recognition Benchmark (GTSRB) dataset was used, which contains thousands of images of 43 different kinds of road signs.
