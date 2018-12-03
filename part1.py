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
    """Calculates the 1-norm of a vector.
    
    Args:
        vector (list): The list which represents the vector.
        
    Returns:
        int: Sum of the absolute values of the vector.
    """
    
    return sum(abs(element) for element in vector)

def deltaList(list1, list2):
    """Calculates the element-wise subtraction of two lists.
    
    Args:
        list1 (list): The frist list.
        list2 (list): The second list.
        
    Returns:
        list: Element-wise subtraction of the two lists.
    """
    
    return [a - b for a, b in zip(list1, list2)]

def sumList(list1, list2):
    """Calculates the element-wise sum of two lists.
    
    Args:
        list1 (list): The frist list.
        list2 (list): The second list.
        
    Returns:
        list: Element-wise sum of the two lists.
    """
    
    return [a + b for a, b in zip(list1, list2)]

def multiplyList(vector, scalar):
    """Calculates the element-wise product of a vector by a scalar.
    
    Args:
        vector (list): The list which represents the vector.
        scalar (float): The value of the scalar.
        
    Returns:
        list: Element-wise product of the vector by the scalar.
    """
    
    return [scalar*element for element in vector]

def dotProduct(linkMatrix, scores):
    """Calculates the dot product of the vector of scores by the link matrix.
    
    Args:
        linkMatrix (list): The list (of lists) which represents the link matrix.
        scores (list): The list which represents the importance scores of the
		pages.
        
    Returns:
        list: The new importance scores of the pages after applying the link
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

def getScores(linkMatrix):
    """Calculates the vector of scores of a network described by the given
	link matrix.
    
    Args:
        linkMatrix (list): The list (of lists) which represents the link matrix.

    Returns:
        list: The (final) importance scores of the pages.
    """
    
    epsilon = 1E-5
    m = 15E-2
    
    numPages = len(linkMatrix)
    initialScores = [1./numPages]*numPages

    # First iteration
    oldScores = initialScores
    newScores = dotProduct(linkMatrix, oldScores)
    
    normInitialScores = multiplyList(initialScores, m)
    normNewScores = multiplyList(newScores, 1 - m)
    newScores = sumList(normNewScores, normInitialScores)

    deltaScores = deltaList(newScores, oldScores)
    
    # Following iterations
    while norm(deltaScores) >= epsilon:
        oldScores = newScores
        newScores = dotProduct(linkMatrix, oldScores)

        normNewScores = multiplyList(newScores, 1 - m)
        newScores = sumList(normNewScores, normInitialScores)
        
        deltaScores = deltaList(newScores, oldScores)

    return newScores

def scoresRank(scores):
    """Returns the list of pages in decreasing order of score."""
	
    return sorted(range(len(scores)), key = scores.__getitem__, reverse = True)

def pageRank(linkMatrix):
    """Performs the ranking of the pages and prints the ranking-score table for
	a network described by the link matrix.
    """
    
    scores = getScores(linkMatrix)
    rankingList = scoresRank(scores)
    
    print('Rank\tPage\tImportance score')
    rank = 0
    for page in rankingList:
        score = scores[page]
        print('{0}\t{1}\t{2:.5f}'.format(rank + 1, page + 1, score))
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

    pageRank(A)