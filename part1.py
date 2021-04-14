# -*- coding: utf-8 -*-
"""
Programming Exercise - Part 1.

File name: part1.py
Author: Gabriel Farias Caccaos
E-mail: gabriel.caccaos@gmail.com
Date created: 02/12/2018
Python version: 3.6.7
"""


def norm(vector):
    """Calculate the 1-norm of a vector.

    Args:
        vector (list): the list which represents the vector.

    Returns:
        int: the sum of the vector's absolute values.
    """
    return sum(abs(element) for element in vector)


def delta_list(list1, list2):
    """Calculate the element-wise subtraction of two lists.

    Args:
        list1 (list): the frist list.
        list2 (list): the second list.

    Returns:
        list: the element-wise subtraction of the two lists.
    """
    return [a - b for a, b in zip(list1, list2)]


def sum_list(list1, list2):
    """Calculate the element-wise sum of two lists.

    Args:
        list1 (list): the frist list.
        list2 (list): the second list.

    Returns:
        list: the element-wise sum of the two lists.
    """
    return [a + b for a, b in zip(list1, list2)]


def multiply_list(vector, scalar):
    """Calculate the element-wise product of a vector by a scalar.

    Args:
        vector (list): the list which represents the vector.
        scalar (float): the value of the scalar.

    Returns:
        list: the element-wise product of the vector by the scalar.
    """
    return [scalar*element for element in vector]


def dot_product(link_matrix, scores):
    """Calculate the dot product of the vector of scores by the link matrix.

    Args:
        link_matrix (list): the list (of lists) which represents the link
            matrix.
        scores (list): the list which represents the importance scores of the
            pages.

    Returns:
        list: the new importance scores of the pages after applying the link
        matrix.
    """
    new_scores = []

    num_pages = len(link_matrix)
    pages_list = range(num_pages)

    for page in pages_list:
        new_score = 0
        for other_page in pages_list:
            new_score += link_matrix[page][other_page]*scores[other_page]
        new_scores.append(new_score)

    return new_scores


def get_scores(link_matrix):
    """Calculate the vector of scores of a network.

    Args:
        link_matrix (list): the list (of lists) which represents the link
            matrix.

    Returns:
        list: the (final) importance scores of the pages.
    """
    epsilon = 1E-5
    m = 15E-2

    num_pages = len(link_matrix)
    initial_scores = [1./num_pages]*num_pages

    # First iteration
    old_scores = initial_scores
    new_scores = dot_product(link_matrix, old_scores)

    norm_initial_scores = multiply_list(initial_scores, m)
    norm_new_scores = multiply_list(new_scores, 1 - m)
    new_scores = sum_list(norm_new_scores, norm_initial_scores)

    delta_scores = delta_list(new_scores, old_scores)

    # Following iterations
    while norm(delta_scores) >= epsilon:
        old_scores = new_scores
        new_scores = dot_product(link_matrix, old_scores)

        norm_new_scores = multiply_list(new_scores, 1 - m)
        new_scores = sum_list(norm_new_scores, norm_initial_scores)

        delta_scores = delta_list(new_scores, old_scores)

    return new_scores


def scores_rank(scores):
    """Return the list of pages in decreasing order of score."""
    return sorted(range(len(scores)), key=scores.__getitem__, reverse=True)


def page_rank(link_matrix):
    """Rank the pages and print the ranking-score table."""
    scores = get_scores(link_matrix)
    ranking_list = scores_rank(scores)

    print('Rank\tPage\tImportance score')
    rank = 0
    for page in ranking_list:
        score = scores[page]
        print(f'{rank + 1}\t{page + 1}\t{score:.5f}')
        rank += 1


# Main program
if __name__ == "__main__":
    A = [[0, 0, 0, 0, 0, 0, 0, 1/2],
         [1/2, 0, 0, 0, 0, 0, 0, 0],
         [1/2, 1/2, 0, 0, 0, 0, 0, 1/2],
         [0, 1/2, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1/2, 0, 0, 0, 0],
         [0, 0, 1/2, 1/2, 1, 0, 0, 0],
         [0, 0, 1/2, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 0]]

    page_rank(A)
