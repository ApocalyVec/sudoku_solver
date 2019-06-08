"""
Formulation of the CSP

variables: cells, there are 9*9 of them
domain: 1-9
constraints:
    all the numbers on the same row can not be the same
    all the numbers on the same column can not be the same
    all the nunmbers in the 3*3 cells can not be the same

"""
import csv
import numpy as np
import time

sudoku_domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def read_csv_as_sudoku(fn):
    sudoku = np.zeros([9, 9], dtype=int)  # make a 9*9 matrix with all zeros, the data type is integer

    with open(fn) as csv_file:  # open the csv file with the name 'fn'
        csv_reader = csv.reader(csv_file, delimiter=';')  # read in the csv file, using ';' as delimiter
        i = 0  # the row index for the csv file, we need this to index the numpy matrix

        for row in csv_reader:  # iterate through the rows
            j = 0  # the column index for the csv file, we need this to index the numpy matrix
            for item in row:  # iterate through the columns in a row
                if item != '':  # if there is a number at [i][j] in the csv file
                    sudoku[i][j] = int(item)
                j += 1  # increment the column count
            i += 1  # increment the row count

    return sudoku  # return the numpy matrix


def recursive_backtraing(csp, domain):
    """
    :param csp: the 9*9 numpy matrix that represents the sudoku problem
    :param domain: the list containing the all the values which the variable may take
    """
    if isAssignmentComplete(csp):
        return csp

    unassigned_var = select_unassigned_var(csp)  # get the coordinates of the first zero-filled cell

    for value in domain:  # try out all the values for this cell
        if check_assignment_consistency(unassigned_var, value, csp):
            csp[unassigned_var[0]][unassigned_var[1]] = value
            result = recursive_backtraing(csp, domain)
            if result is not None:
                print(result)
                return result
            print('Backtracking')
            csp[unassigned_var[0]][unassigned_var[1]] = 0
    return None


def isAssignmentComplete(csp):
    return csp.all()  # returns True if there is no zeros in the matrix (csp)


def select_unassigned_var(csp):
    """
    :param csp:
    :return: the coordinates of the first zero-filled cell that we encounter
            i is the row index, j is the column index
    """
    for i in range(len(csp)):
        for j in range(len(csp[i])):  # iterate through the ith row
            if not csp[i][j]:
                return i, j


def cap_to_three(num):
    if num < 3:
        return 3
    else:
        return num


def check_assignment_consistency(var, value, csp):
    """
    constraints to check:
    all the numbers on the same row can not be the same
    all the numbers on the same column can not be the same
    all the nunmbers in the 3*3 cells can not be the same

    :param var: the coordinates of the first zero-filled cell, var[0] is row index, var[1] is column
    :param value: a number between 1-9
    :param csp: the 9*9 matrix representing the sudoku problem
    """

    row_to_check = csp[var[0]]  # grab the row where the unassigned var is at
    column_to_check = csp[:, var[1]]  # grab the column where the unassigned var is at

    first = int(var[0] / 3) * 3
    second = (int(var[0] / 3) + 1) * 3
    third = int(var[1] / 3) * 3
    forth = (int((var[1]) / 3) + 1) * 3
    matrix_to_check = csp[first:second, third:forth]  # 3*3 matrix where the unassigned var is at

    if value in row_to_check or value in column_to_check or value in matrix_to_check:
        return False
    else:
        return True


csp = read_csv_as_sudoku('sudoku1.csv')
print('Sudoku read in:')
print(csp)
input('Press Enter to Continue...')

start = time.time()
result = recursive_backtraing(csp, sudoku_domain)
end = time.time()
if result is not None:
    print('Solution found, took ' + str(end-start) + ' sec')
    print(result)
else:
    print('Solution does not exist!')