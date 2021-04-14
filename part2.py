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
    n_rows = len(matrix)
    n_cols = len(matrix[0])

    # Data structure for the non-zero entries
    values, rows, columns = [], [], []

    # Row-wise loop through the matrix
    for row in range(n_rows):
        for column in range(n_cols):
            value = matrix[row][column]
            if value != 0:
                values.append(value)
                rows.append(row)
                columns.append(column)

    return values, rows, columns


def get_num_pages(num_groups):
    """Return the number of pages of a network."""
    num_chiefs = num_groups
    num_indians = sum(page for page in range(1, num_groups + 1))

    return num_chiefs + num_indians


def create_adjacency_matrix(num_groups):
    """Return the adjacency matrix of a network."""
    num_pages = get_num_pages(num_groups)
    chiefs_list = []

    # Create adjency matrix (full of zeros)
    adjacency_matrix = [
        [0 for column in range(num_pages)] for row in range(num_pages)
    ]

    # Handle links to pages (including chiefs) that belong to the same group
    for group in range(num_groups):
        chief_page = int(group*(group + 3)/2)
        chiefs_list.append(chief_page)

        group_pages = list(range(chief_page, chief_page + group + 2))

        for this_page in group_pages:
            target_pages = [page for page in group_pages if page != this_page]
            for target_page in target_pages:
                adjacency_matrix[this_page][target_page] = 1

    # Handle links between chief pages
    for chief_page in chiefs_list:
        target_pages = [page for page in chiefs_list if page != chief_page]
        for target_page in target_pages:
            adjacency_matrix[chief_page][target_page] = 1

    return adjacency_matrix


def create_link_matrix(num_groups):
    """Return the link matrix of a network given its adjacency matrix.

    To do this, the columns of the adjacency matrix must be normalized (this
    fixes the weights of the links that comes to the same page).
    """
    num_pages = get_num_pages(num_groups)

    adjacency_matrix = create_adjacency_matrix(num_groups)
    link_matrix = [row for row in adjacency_matrix]

    for page in range(num_pages):
        num_incoming_links = sum(
            pointed_by[page] for pointed_by in adjacency_matrix
        )
        for other_page in link_matrix:
            other_page[page] /= num_incoming_links

    return link_matrix


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

    # Apply sparse row compression on the link matrix:
    # get the non-zero entries values and positions
    values, rows, columns = compressed_sparse_row(link_matrix)

    num_pages = len(link_matrix)
    initial_scores = [1./num_pages]*num_pages

    # First iteration
    old_scores = initial_scores
    y = [0]*num_pages
    for (link, page, other_page) in zip(values, rows, columns):
        y[page] += link*old_scores[other_page]
    y = multiply_list(y, 1./norm(y))

    norm_initial_scores = multiply_list(initial_scores, m)
    norm_new_scores = multiply_list(y, 1 - m)
    new_scores = sum_list(norm_new_scores, norm_initial_scores)

    delta_scores = delta_list(new_scores, old_scores)

    # Following iterations
    while norm(delta_scores) >= epsilon:
        old_scores = new_scores
        for (link, page, other_page) in zip(values, rows, columns):
            y[page] += link*old_scores[other_page]
        y = multiply_list(y, 1./norm(y))

        norm_initial_scores = multiply_list(initial_scores, m)
        norm_new_scores = multiply_list(y, 1 - m)
        new_scores = sum_list(norm_new_scores, norm_initial_scores)

        delta_scores = delta_list(new_scores, old_scores)

    return new_scores


def page_rank(link_matrix):
    """Rank the pages and print the ranking-score table."""
    num_pages = len(link_matrix)
    num_groups = int(((8*num_pages + 9)**0.5 - 3)/2)

    chiefs_list = [int(group*(group + 3)/2) for group in range(num_groups)]

    scores = get_scores(link_matrix)
    ranking_list = scores_rank(scores)

    printed_groups = []
    print('Rank\tPage(s)\t\tGroup\tImportance score')

    rank = 0
    for page in ranking_list:
        # Find chief and group of this page
        chief = [
            chief_page for chief_page in chiefs_list if chief_page <= page
        ].pop()
        group = int(((8*chief + 9)**0.5 - 3)/2)

        # Handle chief pages
        if page in chiefs_list:
            score = scores[page]
            print(f'{rank + 1: >2}\t{page + 1: >3}\t\t{group + 1: >2}\t{score:.5f}')
            rank += 1

        # Handle indian pages
        elif group not in printed_groups:
            score = scores[page]
            last_group_page = chief + group + 1
            if last_group_page != page:
                print(f'{rank + 1: >2}\t{page + 1: >3} to {last_group_page + 1: >3}\t{group + 1: >2}\t{score:.5f}')
            else:
                print(f'{rank + 1: >2}\t{page + 1: >3}\t\t{group + 1: >2}\t{score:.5f}')
            printed_groups.append(group)
            rank += 1


# Main program
if __name__ == "__main__":
    num_groups = 20					# this value can be changed (default = 20)

    link_matrix = create_link_matrix(num_groups)
    page_rank(link_matrix)
