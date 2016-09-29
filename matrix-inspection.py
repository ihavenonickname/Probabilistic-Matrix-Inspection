from random import randint
import sys

def random_entry(n, m):
    '''Given dimensions n and m, generates two random matrices A and P(A) with Bernoulli random numbers. 
    '''

    # a random number for each column, and it for each line.
    pa = [[randint(1, 99) for i in range(m)] for j in range(n)]

    a = []

    # a random {1, 0} for each column in pa, and it for each line in pa.
    for line in pa:
        newline = [(1 if randint(1, 99) < cell else 0) for cell in line]
        a.append(newline)
    
    return a, pa

def inspection_column_order(pa):
    '''Given a matrix of probability, returns the optimal order of columns to be inspected.
    '''

    n, m = len(pa), len(pa[0])

    columns_order = []

    # a tuple of (column index, probability of success) for each column in pa.
    for column in range(m):
        # sum all probabilities in column.
        success = sum(pa[line][column] for line in range(n))
        # appends the index and the probability of the column.
        columns_order.append((column, success))
    
    # sorts by probability of success.
    columns_order = sorted(columns_order, key=(lambda x: x[1]), reverse=True)

    # returns only the column indexes.
    return [line for line, success in columns_order]

def inspection_values_order(column):
    '''Given a column of probability, returns the optimal order of values to be inspected.
    '''

    # creates a sorted list with the value index and its probability.
    column_sorted = sorted(enumerate(column), key=(lambda x: x[1]))

    # returns only the indexes (which are already sorted).
    return [line for line, value in column_sorted]

def column_values(column_index, pa):
    '''Given a column index and a matrix, returns the values of respective column.
    '''
    n = len(pa)
    return [pa[line_index][column_index] for line_index in range(n)]

def compute(a, pa):
    '''Given two matrix of Bernoulli random numbers, returns an indication of its feasibility and the values inspected.
    '''

    n, m = len(a), len(a[0])

    positions_inspected = []

    # for all columns (in the optimal order).
    for column_index in inspection_column_order(pa):
        values_in_column = column_values(column_index, pa)

        # if some value has 0% of probability to be feasible, no need to inspect the column.
        if 0 in values_in_column:
            continue

        feasible_ones = 0

        # for each value in column (in optimal order).
        for line_index in inspection_values_order(values_in_column):
            # if the value has 100% of probability to be feasible, no need to inspect it.
            if pa[line_index][column_index] == 100:
                feasible_ones += 1
                continue

            # remembers what values were inspected.
            positions_inspected.append((line_index, column_index))

            # if it's 0, no need to inspect other values in same column.
            if a[line_index][column_index] == 1:
                feasible_ones += 1
            else:
                break
        
        # if the number of feasible agents is the number of lines, then matrix is feasible.
        if feasible_ones == n:
            return True, positions_inspected
    
    # if all columns were inspected and no one was feasible, the matrix is not feasible.
    return False, positions_inspected

def show_results(a, pa, is_feasible, values_inspected):
    print("Matrix A:")

    for line in a:
        for value in line:
            print("%2d" % value, end=" ")
        print("\n")

    print()

    print("Matrix P(A):")

    for line in pa:
        for value in line:
            print("%3d" % value, end=" ")
        print("\n")

    print()

    print("Feasibility:")

    print("Feasible" if is_feasible else "Infeasible")

    print()

    print("Inspected %s values" % len(values_inspected))

    for line, column in values_inspected:
        print("(%d, %d)" % (line, column))
    

if __name__ == "__main__":
    n, m = sys.argv[1:]

    a, pa = random_entry(int(n), int(m))
    is_feasible, values_inspected = compute(a, pa)

    show_results(a, pa, is_feasible, values_inspected)

    