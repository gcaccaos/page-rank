# -*- coding: utf-8 -*-
"""
Programming Exercise - Part 2.

File name: part2.py
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


def scores_rank(scores):
    """Return the list of pages in decreasing order of score."""
    return sorted(range(len(scores)), key=scores.__getitem__, reverse=True)


def compressed_sparse_row(matrix):
    """Perform the CSR compression (in "row-major" order) on a matrix.

    Args:
        matrix (list): a list of lists.

    Returns:
        values (list): the values of the non-zero entries in the matrix
        rows (list): the rows of the non-zero entries in the matrix
        columns (list): the columns of the non-zero entries in the matrix
    """
    nRows = len(matrix)
    nCols = len(matrix[0])

    # Data structure for the non-zero entries
    values, rows, columns = [], [], []

    # Row-wise loop through the matrix
    for row in range(nRows):
        for column in range(nCols):
            value = matrix[row][column]
            if value != 0:
                values.append(value)
                rows.append(row)
                columns.append(column)

    return values, rows, columns


def get_num_pages(numGroups):
    """Return the number of pages of a network."""
    numChiefs = numGroups
    numIndians = sum(page for page in range(1, numGroups + 1))

    return numChiefs + numIndians


def create_adjacency_matrix(numGroups):
    """Return the adjacency matrix of a network."""
    numPages = get_num_pages(numGroups)
    chiefsList = []

    # Create adjency matrix (full of zeros)
    adjacencyMatrix = [
        [0 for column in range(numPages)] for row in range(numPages)
    ]

    # Handle links to pages (including chiefs) that belong to the same group
    for group in range(numGroups):
        chiefPage = int(group*(group + 3)/2)
        chiefsList.append(chiefPage)

        groupPages = list(range(chiefPage, chiefPage + group + 2))

        for thisPage in groupPages:
            targetPages = [page for page in groupPages if page != thisPage]
            for targetPage in targetPages:
                adjacencyMatrix[thisPage][targetPage] = 1

    # Handle links between chief pages
    for chiefPage in chiefsList:
        targetPages = [page for page in chiefsList if page != chiefPage]
        for targetPage in targetPages:
            adjacencyMatrix[chiefPage][targetPage] = 1

    return adjacencyMatrix


def create_link_matrix(numGroups):
    """Return the link matrix of a network given its adjacency matrix.

    To do this, the columns of the adjacency matrix must be normalized (this
    fixes the weights of the links that comes to the same page).
    """
    numPages = get_num_pages(numGroups)

    adjacencyMatrix = create_adjacency_matrix(numGroups)
    linkMatrix = [row for row in adjacencyMatrix]

    for page in range(numPages):
        numIncomingLinks = sum(
            pointedBy[page] for pointedBy in adjacencyMatrix
        )
        for otherPage in linkMatrix:
            otherPage[page] /= numIncomingLinks

    return linkMatrix


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

    # Apply sparse row compression on the link matrix:
    # get the non-zero entries values and positions
    values, rows, columns = compressed_sparse_row(linkMatrix)

    numPages = len(linkMatrix)
    initialScores = [1./numPages]*numPages

    # First iteration
    oldScores = initialScores
    y = [0]*numPages
    for (link, page, otherPage) in zip(values, rows, columns):
        y[page] += link*oldScores[otherPage]
    y = multiply_list(y, 1./norm(y))

    normInitialScores = multiply_list(initialScores, m)
    normNewScores = multiply_list(y, 1 - m)
    newScores = sum_list(normNewScores, normInitialScores)

    deltaScores = delta_list(newScores, oldScores)

    # Following iterations
    while norm(deltaScores) >= epsilon:
        oldScores = newScores
        for (link, page, otherPage) in zip(values, rows, columns):
            y[page] += link*oldScores[otherPage]
        y = multiply_list(y, 1./norm(y))

        normInitialScores = multiply_list(initialScores, m)
        normNewScores = multiply_list(y, 1 - m)
        newScores = sum_list(normNewScores, normInitialScores)

        deltaScores = delta_list(newScores, oldScores)

    return newScores


def page_rank(linkMatrix):
    """Rank the pages and print the ranking-score table."""
    numPages = len(linkMatrix)
    numGroups = int(((8*numPages + 9)**0.5 - 3)/2)

    chiefsList = [int(group*(group + 3)/2) for group in range(numGroups)]

    scores = get_scores(linkMatrix)
    rankingList = scores_rank(scores)

    printedGroups = []
    print('Rank\tPage(s)\t\tGroup\tImportance score')

    rank = 0
    for page in rankingList:
        # Find chief and group of this page
        chief = [
            chiefPage for chiefPage in chiefsList if chiefPage <= page
        ].pop()
        group = int(((8*chief + 9)**0.5 - 3)/2)

        # Handle chief pages
        if page in chiefsList:
            score = scores[page]
            print(f'{rank + 1: >2}\t{page + 1: >3}\t\t{group + 1: >2}\t{score:.5f}')
            rank += 1

        # Handle indian pages
        elif group not in printedGroups:
            score = scores[page]
            lastGroupPage = chief + group + 1
            if lastGroupPage != page:
                print(f'{rank + 1: >2}\t{page + 1: >3} to {lastGroupPage + 1: >3}\t{group + 1: >2}\t{score:.5f}')
            else:
                print(f'{rank + 1: >2}\t{page + 1: >3}\t\t{group + 1: >2}\t{score:.5f}')
            printedGroups.append(group)
            rank += 1


# Main program
if __name__ == "__main__":
    numGroups = 20					# this value can be changed (default = 20)

    linkMatrix = create_link_matrix(numGroups)
    page_rank(linkMatrix)
