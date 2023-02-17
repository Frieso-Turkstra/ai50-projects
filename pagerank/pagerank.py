import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = dict()

    for page_name in corpus.keys():
        # the 0.15 probability a surfer randomly ends up on a certain page
        probability = (1 - damping_factor) / len(corpus)

        # page links to no other pages
        if not corpus[page]:
            probability += damping_factor / len(corpus)

        # the 0.85 probability a surfer clicks on a link in page
        elif page_name in corpus[page]:
            probability += damping_factor / len(corpus[page])

        # add to probability distribution
        probability_distribution[page_name] = probability

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # set counter for all pages to 0
    counter = {page: 0 for page in corpus.keys()}

    # random starting sample
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        # update current page's counter
        counter[current_page] += 1

        # choose next page based on probability distribution (PD) of current page
        pd = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(pd.keys()), list(pd.values()))[0]

    # convert counter (integers) to ranks (probabilities)
    ranks = {page: count / n for (page, count) in counter.items()}

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # set all pages to equal probability
    ranks = {page: 1 / len(corpus) for page in corpus.keys()}

    while True:
        old_ranks = ranks.copy()

        # calculate probability of landing on page for each page in corpus
        for page in corpus.keys():
            # 0.15 probability of randomly landing there
            random_probability = (1 - damping_factor) / len(corpus)

            # 0.85 probability of getting there through links
            link_probability = 0
            for page_name, links in corpus.items():
                # consider as if all pages were linked if page has no links
                if not links:
                    link_probability += ranks[page_name] / len(corpus)
                # probability of clicking that link to this page
                elif page in links:
                    link_probability += ranks[page_name] / len(links)

            # update PageRank for page
            ranks[page] = random_probability + damping_factor * link_probability

        # base condition: break if no change in values was bigger than 0.001
        for page in corpus.keys():
            if abs(old_ranks[page] - ranks[page]) > 0.001:
                break
        else:
            break

    return ranks


if __name__ == "__main__":
    main()
