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


def dot_product(linkMatrix, scores):
    """Calculate the dot product of the vector of scores by the link matrix.

    Args:
        linkMatrix (list): the list (of lists) which represents the link
            matrix.
        scores (list): the list which represents the importance scores of the
            pages.

    Returns:
        list: the new importance scores of the pages after applying the link
        matrix.
    """
    newScores = []

    numPages = len(linkMatrix)
    pagesList = range(numPages)

    for page in pagesList:
        newScore = 0
        for otherPage in pagesList:
            newScore += linkMatrix[page][otherPage]*scores[otherPage]
        newScores.append(newScore)

    return newScores


def get_scores(linkMatrix):
    """Calculate the vector of scores of a network.

    Args:
        linkMatrix (list): the list (of lists) which represents the link
            matrix.

    Returns:
        list: the (final) importance scores of the pages.
    """
    epsilon = 1E-5
    m = 15E-2

    numPages = len(linkMatrix)
    initialScores = [1./numPages]*numPages

    # First iteration
    oldScores = initialScores
    newScores = dot_product(linkMatrix, oldScores)

    normInitialScores = multiply_list(initialScores, m)
    normNewScores = multiply_list(newScores, 1 - m)
    newScores = sum_list(normNewScores, normInitialScores)

    deltaScores = delta_list(newScores, oldScores)

    # Following iterations
    while norm(deltaScores) >= epsilon:
        oldScores = newScores
        newScores = dot_product(linkMatrix, oldScores)

        normNewScores = multiply_list(newScores, 1 - m)
        newScores = sum_list(normNewScores, normInitialScores)

        deltaScores = delta_list(newScores, oldScores)

    return newScores


def scores_rank(scores):
    """Return the list of pages in decreasing order of score."""
    return sorted(range(len(scores)), key=scores.__getitem__, reverse=True)


def page_rank(linkMatrix):
    """Rank the pages and print the ranking-score table."""
    scores = get_scores(linkMatrix)
    rankingList = scores_rank(scores)

    print('Rank\tPage\tImportance score')
    rank = 0
    for page in rankingList:
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
